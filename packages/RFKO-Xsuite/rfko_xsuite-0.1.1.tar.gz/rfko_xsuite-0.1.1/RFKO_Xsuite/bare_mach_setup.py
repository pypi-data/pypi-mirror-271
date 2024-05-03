

import numpy as np
import scipy
import matplotlib.pyplot as plt
import inspect

import xtrack as xt
import xpart as xp
import xobjects as xo

from . import xsuite_helper as xh
from . import slowex_helper as slwex
from . import phy_helper as ph






def build_particles2(line, n_part=1000, DPP_FACTOR=2.35e-3, debunched_co=True,ramping_sex=False,exn=2.64378704e-06, eyn= 4.7590473e-07, twiss=None, out_params=False):
    ''' TODO
        - add bunched generation options

    :param line:
    :param n_part:
    :param DPP_FACTOR:
    :param debunched_co:
    :param exn:
    :param eyn:
    :param twiss:
    :param out_params:
    :return:
    '''
    if out_params: # can be useful if not used with the wrapper
        params = locals()

    if ramping_sex:
        ##  account for the real setup of the first turns
        xse_names = ['pr.xse01.a', 'pr.xse01.b', 'pr.xse07']
        setter = xt.MultiSetter(line, xse_names, field='k2')  # multisetter obj
        xse0 = setter.get_values()  # initial/nominal values
        setter.set_values([0., 0., 0.])  # changes of value

    if twiss is None:
        twiss = line.twiss(method='4d')

    twiss_df = twiss.to_pandas()
    sigmas, sigmas_p = xp.generate_2D_gaussian(int(n_part))

    z_array = scipy.stats.uniform.rvs(loc=0,
                                      scale=twiss['circumference'],
                                      size=int(n_part))

    # momentum off set will be gauss distributed along zero and DPP_FACTOR will be the standard deviation
    delta_array = scipy.stats.norm.rvs(loc=0, scale=DPP_FACTOR , size=int(n_part))
    if debunched_co:
        # Transport the particles along the line adding the orbit distortion to each point
        sigmas,sigmas_p = xh.nearest_betx(twiss_df,sigmas,sigmas_p,z_array)


    particles = line.build_particles(
        method='4d',
        zeta = z_array,
        delta=delta_array,
        nemitt_x=exn,
        nemitt_y=eyn,
        x_norm=sigmas,
        px_norm=sigmas_p,
        y_norm=sigmas,
        py_norm=sigmas_p,
    )
    # particles.zeta = z_array
    # particles.delta = delta_array

    # RESET THE LINE TO THE NOMINAL VALUES
    if ramping_sex:
        setter.set_values(xse0)
    if out_params:
        return particles, params
    else:
        return particles


def insert_septa_monitor(line, SEPTA_X_MM=-75, n_turns=1000, n_part=1000, out_monitor=True,out_params=False):
    ''' It is not general in where we could place the monitor, mostly beacause for my purposes I don't need this generalization
        and the same is true for every PS sequences. Eventually this will be generalized to different sequences
    '''
    line.unfreeze()
    if out_params:
        params = locals()
    ################################## SEPTUM
    septum = xt.LimitRect(
        min_x=SEPTA_X_MM * 0.001
    )

    line.insert_element(
        element=septum,
        name="SEPTUM",
        index='pe.smh57'
    )
    ##### end SEPTUM

    #######################  MONITOR AT THE SEPTUM
    monitor = xt.ParticlesMonitor(
        num_particles=n_part,
        start_at_turn=0,
        stop_at_turn=n_turns,
        auto_to_numpy=True
    )

    line.insert_element(index='pe.smh57', element=monitor, name='septa_monitor')

    ####### end MONITOR
    if out_monitor&out_params:
        return monitor,params
    elif out_monitor:
        return monitor


def plot_stable(out_dict, s=2, figsize=(12, 7), interpolate=False, wrongf=False, center=True):
    twiss_df = out_dict['twiss'].to_pandas()
    monitor = out_dict['monitor']
    S_strength, S_mu = slwex.Virtual_sextupole_complete(out_dict)  # compute sextupole strength and mu
    dmu = twiss_df[twiss_df.name == 'pe.smh57'].mux.iloc[0] * 2 * np.pi - S_mu
    # dmu from the virtual sextupole to know the rotation

    Monitor = xh.Normalize_monitor(out_dict, normalize_particles=False, center=center)
    color = np.arange(out_dict['params']['n_turns'])
    colors = np.tile(color, (out_dict['params']['n_part'], 1))

    extracted_mask = Monitor.x != 0
    argmin = np.argmin(np.abs(twiss_df.mux * 2 * np.pi - S_mu))
    # INTERPOLATEE BETX AND X
    if (interpolate) & (wrongf is False):
        xi, idxi = np.unique(twiss_df.mux, return_index=True)
        yi = twiss_df.iloc[idxi].betx
        yix = twiss_df.iloc[idxi].x
        betxinterp = np.interp(S_mu / (2 * np.pi), xi, yi)
        xinterp = np.interp(S_mu / (2 * np.pi), xi, yix)

        print(f'X: nearest={twiss_df.iloc[argmin]["x"]}, interpolated={xinterp}')
        print(f'BETX: nearest= {twiss_df.iloc[argmin]["betx"]}, interpolated= {betxinterp}')
        # INTERPOLATED
        Xo = xinterp / np.sqrt(betxinterp)

    elif wrongf is False:
        ### NEAREST method
        Xo = twiss_df.iloc[argmin]['x'] / np.sqrt(twiss_df.iloc[argmin]['betx'])
    else:
        # WRONG version THAT WORKs BETTER
        Xo = twiss_df.iloc[argmin]['x'] / twiss_df.iloc[argmin]['betx']

        ## CLOSED ORBIT CAUSES A CHANGE IN TUNE SHIFT
    dq0 = (out_dict['twiss'].qx - 6 - 1 / 3)  # normal as without distorsions and dispersion
    dq = dq0 - S_strength * Xo / (2 * np.pi)  # distortion correction

    ####check if DPP_FACTOR NON ZERO ADD CHROMATICITY CORRECTION
    # print(f'The tune is {out_dict["twiss"].qx}')
    # print(f'The tune distance is {dq} and the Sextupole strength {S_strength}')
    # print(f'their ratio (proportional to the area) {dq/S_strength}')

    plt.figure(figsize=figsize)
    plt.scatter(Monitor.x[extracted_mask], Monitor.px[extracted_mask], s=s, c=colors[extracted_mask])
    plt.colorbar(label='Turns')
    if center is False:
        # TRANLATION OF THE TRIANGLE AT THE MONITOR CLOSED ORBIT
        xt = twiss_df[twiss_df.name == 'pe.smh57'].x.iloc[0]
        pxt = twiss_df[twiss_df.name == 'pe.smh57'].px.iloc[0]
        betx = twiss_df[twiss_df.name == 'pe.smh57'].betx.iloc[0]
        alfx = twiss_df[twiss_df.name == 'pe.smh57'].alfx.iloc[0]
        twiss_df[twiss_df.name == 'pe.smh57'].alfx.iloc[0]
        Xt = xt / np.sqrt(betx)
        Pxt = Xt * alfx + pxt * np.sqrt(betx)
        t_vector = np.array([Xt, Pxt])
        slwex.stable_tri_plot(dq, - S_strength, dmu=dmu, linewidth=1, translation_vector=t_vector)

    else:
        slwex.stable_tri_plot(dq, - S_strength, dmu=dmu, linewidth=1)
    plt.title(
        f'Tune =  {round(out_dict["twiss"].qx, 5)}, ratio tune distance to sextupole = {round(dq / S_strength, 5)}')


def insert_rfko(line,Brho=None,pc=None,beta=None,charge=None,volt=0,third_frev=True,twiss=None,chirp_type='linear',
                frev=None,freq_start_ratio=90/100,freq_end_ratio=110/100,sampling_freq=1e9,
                duration=1/2000,time=0.04,ctx = xo.ContextCpu(),out_params=False,kick_function=1):
    if out_params: # useful if used without the wrapper
        params = locals()

    if (Brho is None)|(pc is None)|(beta is None):
        print('no dynamical parameters given, used standard lead ions at 650 Mev per nucleon')
        rel_params = ph.energy()
        pc = rel_params['pc']
        beta = rel_params['beta']
        Brho = rel_params['Brho']
        charge = rel_params['charge']

    if kick_function==1:
        rfko_kick = slwex.kick_angle(float(volt),Brho,pc,beta,charge)
    else:
        rfko_kick = slwex.kick_angle_(float(volt),Brho,pc,beta,charge)

    if twiss is None:
        twiss = line.twiss(method='4d')
    
    # revolution freq
    if frev is None:
        trev = twiss['T_rev0']
        frev = 1 / trev
        print(f'revolution frquency = {frev}')
    # frequancies scanned
    if third_frev:
        start_freq = frev/3 * freq_start_ratio
        end_freq = frev/3 * freq_end_ratio
    else:
        start_freq = frev * freq_start_ratio
        end_freq = frev * freq_end_ratio

    
    if chirp_type =='linear':
        t,chirp_signal = ph.generate_chirp(start_freq, end_freq, duration, sampling_freq)
    else:
        t, chirp_signal = ph.generate_chirp_non_linear(start_freq, end_freq, duration, sampling_freq)
    
    line.unfreeze()
    
    # Exciter config; the duration parameter tells it to repeat the chirp_signal
    rfko_exciter = xt.Exciter(
        _context=ctx,
        samples=chirp_signal,
        sampling_frequency=sampling_freq,
        frev=frev,
        duration=float(time),
        start_turn=0,
        knl=[rfko_kick]
    )
    
    line.insert_element(
        element=rfko_exciter,
        name='EXCITER',
        index='pr.kfb97'
    )
    if out_params:
        params['frev'] = frev
        return params

    
def builder_wrapper(line_dict,twiss=None,third_frev=True,extraction = True,targetx = None,debunched_co=True,n_part=1000,
                    n_turns=None,DPP_FACTOR=2.35e-3, exn=2.64378704e-06, eyn= 4.7590473e-07,
                    SEPTA_X_MM=-75,freq_start_ratio=90/100,freq_end_ratio=110/100,volt=0,sampling_freq=1e9,
                    duration=1/2000,time=None,chirp_type='linear',emittance_norm=True,kick_function=1):
    ''' TODO
    - Better adapt the mechanism to pass the parameters to the functions without passing through the maual creation of the params dict


    :return:
    '''

    line = line_dict['line']
    if twiss is None:
        twiss = line.twiss(method='4d')

    outdict1 = dict(line=line, twiss=twiss)

    ############################################################# MATCHING XTUNE
    matching(outdict1,targetx=targetx,extraction=extraction)
    twiss = outdict1['twiss']

    gamma = line_dict['params']['gamma']
    beta = line_dict['params']['beta']
    pc = line_dict['params']['pc']
    Brho = line_dict['params']['Brho']
    charge = line_dict['params']['charge']

    if emittance_norm: 
        ex = exn/(gamma*beta)
        ey = eyn/(gamma*beta)
    else:
        ex = exn.copy()
        ey = eyn.copy()
        exn = ex*gamma*beta
        eyn = ey*gamma*beta
        
        
    ### SIMULATIONS TIME AND NUMBER OF TURNS
    trev = twiss['T_rev0']
    frev = 1 / trev
    print(f'revolution frequency is {frev}')
    if (time is None) & (n_turns is not None):
        time = trev*n_turns
    if (time is not None) & (n_turns is None):
        n_turns = time/trev
    if (time is None)&(n_turns is None):
        # Turns are the default if None is given
        n_turns=1000
        time =  trev*n_turns

   # PARAMS TO PASS TO THE FUNCTIONS
    params = dict(n_part=n_part,n_turns=n_turns,third_frev=third_frev,pc=pc,Brho=Brho,beta=beta,charge=charge,debunched_co=debunched_co,DPP_FACTOR=DPP_FACTOR, exn=exn, eyn=eyn,
                  SEPTA_X_MM=SEPTA_X_MM,freq_start_ratio=freq_start_ratio,volt=volt,freq_end_ratio=freq_end_ratio,
                  sampling_freq=sampling_freq,duration=duration,gamma=gamma,time=time,ex=ex,ey=ey,
                  chirp_type=chirp_type,emittance_norm=emittance_norm,frev=frev,kick_function=kick_function)
    
    ########
    #This is a check to see if I put al the parameters i wanted in the params dictionary
    # The expected exceptions are : [trev,line,twiss,params]
    #######################################
    # for i in locals().keys():
    #     if i not in params.keys():
    #        print(i)
    # ############
    
    



    ######## AUTOMATIC CHOOSING THE PARAMS FROM PARAMS DICT, THAT ARE USED BY THE FUNCTIONS
    # inspect.getfullargspec
    bpart_args = inspect.getfullargspec(build_particles2).args[1:] # the first is the line non keyword arg
    monito_args = inspect.getfullargspec(insert_septa_monitor).args[1:]
    rfkoel_args = inspect.getfullargspec(insert_rfko).args[1:]
    subpart = dict()
    submon = dict()
    subrko = dict()
    for key,val in params.items():
        if key in bpart_args:
            subpart[key]=val
        if key in monito_args:
            submon[key]=val
        if key in rfkoel_args:
            subrko[key]=val

    #### 1.MONITOR AND SEPTA
    monitor = insert_septa_monitor(line,**submon)
    # 2.RFKO EXCITER
    insert_rfko(line,twiss=twiss,**subrko)
    ### Having unfreezed the line to insert the element, we lose the tracker
    line.build_tracker(_context=xo.ContextCpu())
    # 3.BUILD PARTICLES
    particles = build_particles2(line, twiss=twiss, **subpart)

    ## OUTPUT
    outdict = dict(line=line,twiss=twiss,monitor=monitor,particles=particles,params=params)
    
    return outdict


def matching(outdict, targetx=None,extraction=True):
    ''' TODO
    - More flexible and change the default case for the setting of kf kd
    - add the possibility to match the chromaticity
    '''
    line = outdict['line']
    knobs = ['k1prbhf', 'k1prbhd', 'k2prmp', 'k2prmpj']

    # Value matched to the measurements TUNES OF BARE MACHINE
    vals = [0.05714293659989464, -0.05719922125376693, 0.010731455338789136, -0.019018243990104253]
    for i in range(len(knobs)):
        line.vars[knobs[i]] = vals[i]

    if extraction:
        ####### EXTRACTION UNITS
        line.vars['kpebsw23'] = 0  # from LSA not --> -0.001570859932
        line.vars['kpebsw57'] = 5.544860897340004E-4  # from LSA
        line.vars['kprqse'] = 0.09088224  # Value from LSA try length
        line.vars['kprxse'] = 1.4193310000000103  # value at the steady from LSA


        if targetx is None:  ### STANDARD QXTARGET {6.32 }

            line.vars['kf'] =  0.002252965399686161
            line.vars['kd'] = -0.009766502523392236
            twiss = line.twiss(method='4d')
            outdict['twiss'] = twiss
            print(f'standard value Qx = {twiss.qx}')
        else:
            print(f'the target qx is {targetx}')
            line.match(method='4d', n_steps_max=30, vary=[xt.Vary('kf', step=1e-9), xt.Vary('kd', step=1e-9)],
                       targets=[xt.Target('qx', targetx, tol=0.000005), xt.Target('qy', outdict['twiss'].qy, tol=0.005)])
            twiss = line.twiss(method='4d')
            print(f'after match {twiss.qx}')
            outdict['twiss'] = twiss
    else:
        twiss = line.twiss(method='4d')
        outdict['twiss'] = twiss




