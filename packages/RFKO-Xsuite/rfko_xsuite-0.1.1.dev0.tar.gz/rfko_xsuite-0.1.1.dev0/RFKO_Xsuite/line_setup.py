# Import standard packages
import os
import sys
import numpy as np
import scipy
import logging

# Import simulation packages
import xtrack as xt
import xpart as xp
import xobjects as xo
from cpymad.madx import Madx
# CUSTOM functions there were previously on this notebook

try:
    import requests
except:
    print('the module request is not imported for a compatibility problem with OpeSSL.')
    print('this means that you cannot use the function rfko_setup with the corr_seq parameter set to False (True is the default)')




from . import phy_helper as ph
from . import slowex_helper as slwex

np.set_printoptions(threshold=sys.maxsize)  # To print tthe full length of np array

#logging.disable(logging.INFO)
#
#logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__) # I could use a diffrent name?


def set_logging(level):
    ''' St the level of logging for the logging in stance of the whole module'''
    if level in ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']:
        logger.setLevel(level=level)
    else:
        logger.error("Non recognized error")
        logger.debug(f"Use one of the following : {['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']}")
        return None


def tune_match(mad, Qx, Qxp, Qy, Qyp,verbose=True):
    mad.input('''
    ptc_twiss_macro(order, dp, slice_flag): macro = {
    ptc_create_universe;
    ptc_create_layout, time=false, model=2, exact=true, method=6, nst=3;
    IF (slice_flag == 1){
        select, flag=ptc_twiss, clear;
        select, flag=ptc_twiss, column=name,keyword,s,l,x,px,beta11,beta22,disp1,k1l;
        ptc_twiss, closed_orbit, icase=56, no=order, deltap=dp, table=ptc_twiss, summary_table=ptc_twiss_summary, slice_magnets=true;
    }
    ELSE{
        select, flag=ptc_twiss, clear;
        select, flag=ptc_twiss, column=name,keyword,s,x,px,beta11,alfa11,beta22,alfa22,disp1,disp2,mu1,mu2,energy,l,angle,K1L,K2L,K3L,HKICK,SLOT_ID;    
        ptc_twiss, closed_orbit, icase=56, no=order, deltap=dp, table=ptc_twiss, summary_table=ptc_twiss_summary, normal;
    }
    ptc_end;
    };

    ''')

    # /**********************************************************************************
    # *                        Matching using the PFW
    # ***********************************************************************************/
    mad.input("Qx   := " + str(Qx) + "; !Horizontal Tune")
    mad.input("Qxp  := " + str(Qxp) + "; !Horizontal Chromaticity")

    mad.input("Qy   := " + str(Qy) + "; !Vertical Tune")
    mad.input("Qyp  := " + str(Qyp) + "; !Vertical Chromaticity")

    mad.input('''
    use, sequence=PS;
    match, use_macro;
            vary, name = k1prpfwf;
            vary, name = k1prpfwd;
            vary, name = k2prpfwf;
            vary, name = k2prpfwd;
            use_macro, name = ptc_twiss_macro(2,0,0);
            constraint, expr = table(ptc_twiss_summary,Q1)  = Qx;
            constraint, expr = table(ptc_twiss_summary,Q2)  = Qy;
            constraint, expr = table(ptc_twiss_summary,DQ1) = Qxp;
            constraint, expr = table(ptc_twiss_summary,DQ2) = Qyp;
    jacobian,calls=50000,bisec=3;
    ENDMATCH;
    ''')

    mad.use(sequence="PS")
    twiss_tune_matching = mad.twiss().dframe()  # Needed to refresh the tune values
    mad.input('qx = table(SUMM, Q1);')
    mad.input('qy = table(SUMM, Q2);')
    mad.input('qxp = table(SUMM, DQ1);')
    mad.input('qyp = table(SUMM, DQ2);')


    tune_info_dict = {"Qx": mad.globals["qx"], "Qy": mad.globals["qy"], "Qxp": mad.globals["qxp"],
                      "Qyp": mad.globals["qyp"]}
    pfw_dict = {"k1prpfwf": mad.globals["k1prpfwf"], "k1prpfwd": mad.globals["k1prpfwd"],
                "k2prpfwf": mad.globals["k2prpfwf"], "k2prpfwd": mad.globals["k2prpfwd"]}
    if verbose:
        print(
        f"H-tune: {round(tune_info_dict['Qx'], 3)}, H-Chroma: {round(tune_info_dict['Qxp'], 3)}\nV-Tune: {round(tune_info_dict['Qy'], 3)}, V-Chroma: {round(tune_info_dict['Qyp'], 3)}")
        print(f"")
        print(
        f"PFW settings: \n  k1prpfwf: {round(pfw_dict['k1prpfwf'], 6)}\n  k1prpfwd: {round(pfw_dict['k1prpfwd'], 6)}\n  k2prpfwf: {round(pfw_dict['k2prpfwf'], 6)}\n  k2prpfwd: {round(pfw_dict['k2prpfwd'], 6)}")

    return pfw_dict, tune_info_dict


def rfko_setup(REL_GAMMA=None, E_0 =193.766308,E_n =None,exn=2e-6, eyn=2e-6, duration=1 / 1000, volt=0, time=0.004, n_part=1000,
               n_turns=1000, freq_start_ratio=90 / 100, freq_end_ratio=110 / 100, sampling_freq=1e9,
               QY_TARGET=0.256, QPY_TARGET=-0.242, QX_TARGET=0.325, QPX_TARGET=-0.5, rf10MHz_enable='0',
               DPP_FACTOR=0, SEPTA_X_MM=-60, ctx=xo.ContextCpu(), chirp_type='linear', verbose=True, norm_gain=False,
               corr_seq=True, return_form='dict'):
    # Beam parameters

    every = ['freq_start_ratio', 'freq_end_ratio', 'duration', 'sampling_freq', 'REL_BETA', 'REL_GAMMA', 'exn',
             'eyn', 'p', 'Brho', 'QX_TARGET', 'QPX_TARGET', 'QY_TARGET', 'QPY_TARGET', 'volt', 'rf10MHz_enable', 'time',
             'n_part', 'n_turns', 'SEPTA_X_MM']
    if (E_n is None) & (REL_GAMMA is None):
        E_n = 0.650 # 650 Mev per nucleon


    E_tot = E_n*208+E_0
    REL_GAMMA = E_tot/E_0
    REL_BETA = np.sqrt(1 - REL_GAMMA ** (-2))
    pc = E_tot*REL_BETA
    momentum = pc
    ex = exn / (REL_BETA * REL_GAMMA)
    ey = eyn / (REL_BETA * REL_GAMMA)

    Brho = pc * 3.3356/54 # conversions to have Tm
    PARENT_DIR = "."



    mad = Madx(stdout=False)
    ###
    ######
    ##########   LINES TO IMPORT FROM PS official (?) sequence WES
    if corr_seq == False:
        mad.input(requests.get("https://gitlab.cern.ch/acc-models/acc-models-ps/-/raw/2022/ps_mu.seq").text)
        mad.input(requests.get("https://gitlab.cern.ch/acc-models/acc-models-ps/-/raw/2022/ps_ss.seq").text)
        mad.input(requests.get(
            "https://gitlab.cern.ch/acc-models/acc-models-ps/-/raw/2022/scenarios/east/4_slow_extraction/ps_se_east.str").text)
    else:
        mad.call('./clean_seq/corr_gitlab.cern.ch_acc-models_acc-models-ps_-_raw_2022_ps_mu.seq.txt')
        mad.call('./clean_seq/corr_gitlab.cern.ch_acc-models_acc-models-ps_-_raw_2022_ps_ss.seq.txt')
        mad.call('./clean_seq/corr_gitlab.cern.ch_acc-models_acc-models-ps_-_raw_2022_scenarios_east_4_slow_extraction_ps_se_east.str.txt')

    mad.input(f' BEAM, PARTICLE=Pb54, MASS=193.737692, CHARGE=54., ENERGY=193.737692 + {E_n}*208;')
    mad.input(f"BRHO      = BEAM->PC * 3.3356/54;")
    mad.use(sequence="PS")
    #### To test ion parameters
    # mad.input('PC = BEAM->PC;')
    # mad.input('ETOT = BEAM->ENERGY;')
    # mad.input('MASS0 = BEAM->MASS;')
    # print('ion parameters checking')
    # print(f'E_tot = {mad.globals.etot}, PC = {mad.globals.pc}, mass = {mad.globals.mass0} ')
    ############################### turn off 23 for ions BUMPER ELECTROSTATIC
    mad.input("kPEBSW23 = 0;")
    mad.input(
        'SELECT, FLAG=TWISS, COLUMN=NAME,KEYWORD,S,L,K1L,KEYWORD,BETX,ALFX,X,DX,PX,DPX,MUX,BETY,ALFY,Y,DY,PY,DPY,MUY,APERTYPE,APER_1,APER_2,APER_3,APER_4,KMIN,RE11,RE12,RE21,RE22,RE33,RE34,RE43,RE44,RE16,RE26;')
    mad.input('savebeta, label=bumped23, place = PR.BPM23;')


    # Makethin with 4 slices
    QUAD_SLICE = 4
    mad.use(sequence='ps')
    mad.select(flag='makethin', class_='rbend', slice_=QUAD_SLICE)
    mad.select(flag='makethin', class_='quadrupole', slice_=QUAD_SLICE)
    mad.select(flag='makethin', class_='sbend', slice_=QUAD_SLICE)
    mad.select(flag='makethin', class_='hkicker', slice_=QUAD_SLICE, thick=False)
    mad.select(flag='makethin', class_='sextupole', slice_=2)
    mad.makethin(sequence='ps')

    # Match tune using PFWs
    pfw_dict_on_resonance, tune_info_on_resonance = tune_match(mad, Qx=QX_TARGET, Qxp=QPX_TARGET, Qy=QY_TARGET,
                                                               Qyp=QPY_TARGET, verbose=verbose)
    # pfw_dict_on_resonance, tune_info_on_resonance = Tmatch(mad,Qx=QX_TARGET,Qxp=QPX_TARGET,Qy=QY_TARGET,Qyp=QPY_TARGET, p=p, ex=ex, ey=ey)

    mad.input("k1prpfwf = " + str(pfw_dict_on_resonance["k1prpfwf"]) + ";")
    mad.input("k1prpfwd = " + str(pfw_dict_on_resonance["k1prpfwd"]) + ";")
    mad.input("k2prpfwf = " + str(pfw_dict_on_resonance["k2prpfwf"]) + ";")
    mad.input("k2prpfwd = " + str(pfw_dict_on_resonance["k2prpfwd"]) + ";")
    twiss_after_makethin = mad.twiss().dframe()

    print("> Import Complete, MAD-X is ready to go!")

    Qx = tune_info_on_resonance['Qx']
    Qxp = tune_info_on_resonance['Qxp']
    if verbose:
        print(f"\n Qx = {Qx}, Qxp = {Qxp}")

    ############################## Convert Line to Xsuite   #####################
    mad.use(sequence="PS")


    if corr_seq == False:
        line = xt.Line.from_madx_sequence(
            mad.sequence(), allow_thick=True)
    else:
        line = xt.Line.from_madx_sequence(
            mad.sequence(), allow_thick=True, deferred_expressions=True)

    ## WHY SHOULD I CALL THE PARTICLE REF ALSO HERE??

    line.particle_ref = xp.Particles(
        mass0=E_0*1e9,                 # I could change with the output from the energy function!! without accepting it as a value in the funciton
        q0=54,
        beta0=REL_BETA)

    ######################### Calculate Frev ------> REVOLUTION FREQUENCY | WES   ######################
    line.build_tracker(_context=ctx)
    twiss_parameters = line.twiss(method='4d')
    if verbose:
        print(f'CHROMATICITY IN XSUITE :{twiss_parameters.dqx}')  ######
    trev = twiss_parameters['T_rev0']
    frev = 1 / trev
    line.unfreeze()
    if verbose:
        print(f"frev = {frev}")


    # N_turn override
    if n_turns is None or n_turns == 0 or n_turns == '0':
        if verbose:
            print("> n_turns not specified, calculating from time")
            print(f">This sim will run for {n_turns} turns")
        n_turns = int(float(time) * frev)
    else:
        n_turns = int(n_turns)
        if verbose:
            print("> n_turns overridden")

    rf10MHz_enable = True if (rf10MHz_enable == '1') | (rf10MHz_enable == 1) | (rf10MHz_enable == 'True') else False

    ####################  ADDING THE SEPTUM        ############################

    septum = xt.LimitRect(
        min_x=SEPTA_X_MM * 0.001,  # in meters
    )

    line.insert_element(
        element=septum,
        name="SEPTUM",
        index='pe.smh57'
    )

    # TFB Config
    rfko_kick = slwex.kick_angle(float(volt), Brho)
    if norm_gain:
        rfko_kick = rfko_kick / Brho
    ############################# Define your parameters for a single chirp ######################

    start_freq = frev/3 * freq_start_ratio
    end_freq = frev/3 * freq_end_ratio

    # Generate the repeated chirp

    if chirp_type == 'linear':
        t, chirp_signal = ph.generate_chirp(start_freq, end_freq, duration, sampling_freq)
    else:  # non ci sono altre opzioni
        t, chirp_signal = ph.generate_chirp_non_linear(start_freq, end_freq, duration, sampling_freq)

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
        name=f'EXCITER',
        index='pr.kfb97'
    )
    if verbose:
        print('exciter Done')

    ########################## RF Cavity Config; voltage 0 if disabled   ########################
    if rf10MHz_enable:
        RF_VOLTAGE = 130e3  # V
    else:
        RF_VOLTAGE = 0

    RF_HARMONIC = 8
    RF_FREQUENCY = frev * RF_HARMONIC

    PHASE = 0  # rising-edge

    rf_cavity = xt.Cavity(
        _context=ctx,
        voltage=RF_VOLTAGE,
        frequency=RF_FREQUENCY,
        lag=PHASE
    )

    line.insert_element(
        element=rf_cavity,
        name="rf_cavity",
        at_s=0
    )
    ######################

    ####################### Insert a monitor to record the particles MONITOR AT THE SEPTUM  #############
    monitor = xt.ParticlesMonitor(
        num_particles=n_part,
        start_at_turn=0,
        stop_at_turn=n_turns,
        auto_to_numpy=True
    )

    line.insert_element(index='pe.smh57', element=monitor, name='septa_monitor')

    line.build_tracker(_context=ctx)
    line.particle_ref = xp.Particles(
        mass0=E_0*1e9,
        q0=54,
        beta0=REL_BETA
    )

    ###############################     PARTICLE GENERARION--- from bunch if RF #####################

    if rf10MHz_enable:
        if verbose:
            print("RF present; generating from generate_matched_gaussian_bunch()")
        particles = xp.generate_matched_gaussian_bunch(
            line=line,
            num_particles=int(n_part),
            nemitt_x=exn,
            nemitt_y=eyn,
            sigma_z=4.3,
            total_intensity_particles=30e10
        )
    else:
        if verbose:
            print("RF not present")
        sigmas, sigmas_p = xp.generate_2D_gaussian(int(n_part))

        try:
            z_array = scipy.stats.uniform.rvs(loc=0,
                                              scale=twiss_parameters['circumference'],
                                              size=int(n_part))
            delta_array = scipy.stats.norm.rvs(loc=0, scale=DPP_FACTOR / 2, size=int(n_part))
            particles = line.build_particles(
                method='4d',
                delta=delta_array,
                zeta=z_array,
                nemitt_x=exn,
                nemitt_y=eyn,
                x_norm=sigmas,
                px_norm=sigmas_p,
                y_norm=sigmas,
                py_norm=sigmas_p,
            )

            # particles.zeta = z_array
            # particles.delta = delta_array
        except AssertionError:
            print("Failed line.build, trying xp.build_particles()")
            z_array = scipy.stats.uniform.rvs(loc=0,
                                              scale=twiss_parameters['circumference'],
                                              size=int(n_part))
            delta_array = scipy.stats.norm.rvs(loc=0, scale=DPP_FACTOR / 2, size=int(n_part))
            particles = xp.build_particles(
                particle_ref=line.particle_ref,
                method='4d',
                delta=delta_array,
                zeta = z_array,
                nemitt_x=exn,
                nemitt_y=eyn,
                x_norm=sigmas,
                px_norm=sigmas_p,
                y_norm=sigmas,
                py_norm=sigmas_p,
            )

            # particles.zeta = z_array
            # particles.delta = delta_array
        else:
            if verbose:
                print("Generating from line.build_particles()")

    # RECOMPUTE THE FINAL TWISS because twiss_parameters is calculated before adding SEPTA-TRANSVERSE_EXCITER
    final_twiss = line.twiss(method='4d')

    if verbose:
        print(
            f'Summary of the used parameters: \n  \n Gain = {volt} \n \n RF_generation = {rf10MHz_enable} \n \n exn,exy = {exn}, {eyn} \n \n DPP = {DPP_FACTOR} \n \n' +
            f' Chirp frequencies = ({start_freq},{end_freq}) \n \n revolution freq = {frev} \n \n X Tune = {Qx} \n \n X Chromaticity = {Qxp} \n \n Septa x lim [mm] = {SEPTA_X_MM}')
    params_out = dict(REL_GAMMA=REL_GAMMA, exn=exn, pc=pc, eyn=eyn, duration=duration, volt=volt, time=time,
                      n_part=n_part,
                      n_turns=n_turns, freq_start_ratio=freq_start_ratio, freq_end_ratio=freq_end_ratio,
                      sampling_freq=sampling_freq,
                      QY_TARGET=QY_TARGET, QPY_TARGET=QPY_TARGET, QX_TARGET=QX_TARGET, QPX_TARGET=QPX_TARGET,
                      rf10MHz_enable=rf10MHz_enable,
                      DPP_FACTOR=DPP_FACTOR, SEPTA_X_MM=SEPTA_X_MM, ctx=ctx, return_form=return_form, REL_BETA=REL_BETA,
                      momentum=momentum, Brho=Brho)

    if return_form == 'dict':
        output = dict(line=line, particles=particles, monitor=monitor, twiss=final_twiss, params=params_out, mad=mad)
        return output










def build_line_baremachine(ions = True,E_nucleons=0.650,dir='mad_file',madout=False,print_info=False,makethin=True):
    '''
    :param ions: True for Ions
    :param print_info: True for printing info of the line and the beam parameters
    :param E_0: rest energy in Gev
    :param E_tot: Total energy in Gev (E_0+T)
    :param out_params: bool, if you want to output a dictionary of parameter
    :param madout: bool, if you want to output the mad object
    :return: Line, depending on option (mad OR params)
    '''
    #,E_0=193.766308,E_tot =328.966308
    rel_params = ph.energy(ions,E_nucleons)
    E_0 = rel_params['E_0']
    if ions:
        particle = 'Pb54'
        charge = 54
    else:
        charge = 1
        particle = 'PROTON'


    mad = Madx(stdout=False)




    ## MAIN UNITS
    mad.call(f'./{dir}/final_corr_STANDARD_PR_YETS 2022-2023_20-MAR-2023.seq')

    mad.input(f'BEAM, PARTICLE={particle}, MASS={rel_params["E_0"]}, CHARGE={charge}., ENERGY={rel_params["E_tot"]};')
    mad.input(f'BRHO = BEAM->PC * 3.3356 /{charge}.;') # Beam rigidity
    mad.input('PC=BEAM->PC;') # more for debugging than else
    mad.call(f'./{dir}/ps_ion_bare_machine.str')


    ########## MAKETHIN
    if makethin:
        QUAD_SLICE = 4
        mad.use(sequence='ps')
        mad.select(flag='makethin', class_='rbend', slice_=QUAD_SLICE)
        mad.select(flag='makethin', class_='quadrupole', slice_=QUAD_SLICE)
        mad.select(flag='makethin', class_='sbend', slice_=QUAD_SLICE)
        mad.select(flag='makethin', class_='hkicker', slice_=QUAD_SLICE, thick=False)
        mad.select(flag='makethin', class_='sextupole', slice_=2)
        mad.makethin(sequence='ps')


    ### Twiss to GET SOME PARAMETER CALCULATED IN MADX
    mad.input('SELECT, FLAG=TWISS, CLEAR;')
    mad.input('SELECT, FLAG=TWISS, FULL;')
    mad.twiss()
    ## Found in Xsuite --> momentum_compaction_factor
    mad.input('DQX = TABLE(SUMM,DQ1);')
    mad.input('DQY = TABLE(SUMM,DQ2);')
    mad.input('QX = TABLE(SUMM,Q1);')
    mad.input('QY = TABLE(SUMM,Q2);')
    mad.input('GAMMATR = TABLE(SUMM,GAMMATR);')

    if print_info:
         print(f'the value for PC in madx is {mad.globals.pc} Gev')
         print(f'the chromaticities in madx are : dqx = {mad.globals.dqx},   dqy = {mad.globals.dqy}')
         print(f'gamma transition is : {mad.globals.gammatr}')
         #print(mad.globals.gammatr)
         print(f'Brho of mad is {mad.globals.brho}')
         #print(mad.globals.brho)


    # Relativistic params calcualted by energy
    gamma = rel_params['gamma']
    beta = rel_params['beta']
    pc = rel_params['pc']

    print('--------------------------ENERGY -------------')
    print(f'gamma = {gamma}   beta = {beta}     pc = {pc}')
    print('----------------------------------------------------------')
    ## LINE TO XSUITE
    ctx = xo.ContextCpu()
    line = xt.Line.from_madx_sequence(mad.sequence(),allow_thick=True,deferred_expressions=True)
    line.particle_ref = xp.Particles(
        mass0=E_0*1e9,
        q0=charge,
        beta0=beta)

    line.build_tracker(_context=ctx)

    if print_info:
        twiss = line.twiss(method="4d")
        print(f'chromaticities in Xsuite are : dqx = {twiss.dqx}, dqy = {twiss.dqy}')

    ########## OUTPUT
    if madout :
        print('returning a dictionary with the mad object and the line and the params')
        out = dict(params=rel_params,mad=mad,line=line)
        return out
    else:
        return dict(line=line,params=rel_params)




def henon_map_line(ions=True,E_nucleons=200,alfx=None,betx=None,alfy=None,bety=None,qx=6.32000,
                   qy=6.2445267,dqx=4.068617,dqy=-10.248037,dx=2.985807,k2nl=-2.867035,S=None):
    '''TODO 1) check the correct environment, 2) add other custom parameters to input for henon map'''
    rel_params = ph.energy(ions, E_nucleons)
    E_0 = rel_params['E_0']
    if ions:
        particle = 'Pb54'
        charge = 54
    else:
        charge = 1
        particle = 'PROTON'
    # this is the order accepted for the henon map
    twiss_params = [alfx, betx, alfy, bety]
    # Default value from the PS line
    std_twiss = [0.838476296628905,13.784753228063757,
     -0.7032505108349398,21.134855356093915]
    for i,x in enumerate(twiss_params):
        if x is None:
            twiss_params[i] = std_twiss[i]

    if S is not None:
        # Overrides the values of k2nl
        k2nl = 2*S/(twiss_params[1]**(3/2))
    else:
        S = k2nl*twiss_params[1]**(3/2)/2

    gamma = rel_params['gamma']
    beta = rel_params['beta']
    pc = rel_params['pc']

    omega_x = 2*np.pi*qx
    omega_y = 2*np.pi*qy
    Henon_ele = xt.Henonmap(omega_x=omega_x,omega_y=omega_y,dqx=dqx,dqy=dqy,dx=dx,
                            twiss_params=twiss_params,norm=False,multipole_coeffs=[k2nl])
    line = xt.Line(elements=[Henon_ele],element_names=['Henon_sextupole'])

    line.particle_ref = xp.Particles(
        mass0=E_0*1e9,
        q0=charge,
        beta0=beta)
    henon_params = dict(qx=qx,qy=qy,dqx=dqx,dqy=dqy,dx=dx,
                            twiss_params=twiss_params,norm=False,multipole_coeffs=[k2nl],S=S)

    return dict(line=line,params = rel_params,henon_params=henon_params)


def rfko_setup_old(REL_GAMMA=25.598474067, exn=2e-6, p=5.392, eyn=2e-6, duration=1 / 1000, volt=0, time=0.004,
                   n_part=1000,
                   n_turns=1000, freq_start_ratio=90 / 100, freq_end_ratio=110 / 100, sampling_freq=1e9,
                   QY_TARGET=0.256, QPY_TARGET=-0.242, QX_TARGET=0.325, QPX_TARGET=-0.5, rf10MHz_enable='0',
                   DPP_FACTOR=0, SEPTA_X_MM=-60, ctx=xo.ContextCpu(), chirp_type='linear', verbose=True,
                   norm_gain=False,dir=None, corr_seq=True, return_form='dict'):
    # Beam parameters

    every = ['freq_start_ratio', 'freq_end_ratio', 'duration', 'sampling_freq', 'REL_BETA', 'REL_GAMMA', 'exn',
             'eyn', 'p', 'Brho', 'QX_TARGET', 'QPX_TARGET', 'QY_TARGET', 'QPY_TARGET', 'volt', 'rf10MHz_enable', 'time',
             'n_part', 'n_turns', 'SEPTA_X_MM']

    REL_BETA = np.sqrt(1 - REL_GAMMA ** (-2))
    momentum = p
    ex = exn / (REL_BETA * REL_GAMMA)
    ey = eyn / (REL_BETA * REL_GAMMA)
    Brho = p * 3.3356
    PARENT_DIR = "."
    os.makedirs(PARENT_DIR, exist_ok=True)
    if verbose:
        print(f"Parent Directory: {PARENT_DIR}")
    mad = Madx(stdout=False)

    ##########
    ##########   LINES TO IMPORT FROM PS official (?) sequence WES
    if dir is None:
        dir = 'clean_seq'
    if corr_seq == False:
        mad.input(requests.get("https://gitlab.cern.ch/acc-models/acc-models-ps/-/raw/2022/ps_mu.seq").text)
        mad.input(requests.get("https://gitlab.cern.ch/acc-models/acc-models-ps/-/raw/2022/ps_ss.seq").text)
        mad.input(requests.get(
            "https://gitlab.cern.ch/acc-models/acc-models-ps/-/raw/2022/scenarios/east/4_slow_extraction/ps_se_east.str").text)
    else:
        mad.call(f'./{dir}/corr_gitlab.cern.ch_acc-models_acc-models-ps_-_raw_2022_ps_mu.seq.txt')
        mad.call(f'./{dir}/corr_gitlab.cern.ch_acc-models_acc-models-ps_-_raw_2022_ps_ss.seq.txt')
        mad.call(
            f'./{dir}/corr_gitlab.cern.ch_acc-models_acc-models-ps_-_raw_2022_scenarios_east_4_slow_extraction_ps_se_east.str.txt')

    mad.command.beam(
        particle="PROTON",
        pc=p,
        ex=ex,
        ey=ey,
        charge=1
    )
    mad.input(f"BRHO      = BEAM->PC * 3.3356;")
    mad.use(sequence="PS")

    ############################### turn off 23 for ions BUMPER ELECTROSTATIC
    mad.input("kPEBSW23 = 0;")
    mad.input(
        'SELECT, FLAG=TWISS, COLUMN=NAME,KEYWORD,S,L,K1L,KEYWORD,BETX,ALFX,X,DX,PX,DPX,MUX,BETY,ALFY,Y,DY,PY,DPY,MUY,APERTYPE,APER_1,APER_2,APER_3,APER_4,KMIN,RE11,RE12,RE21,RE22,RE33,RE34,RE43,RE44,RE16,RE26;')
    mad.input('savebeta, label=bumped23, place = PR.BPM23;')

    # Makethin with 4 slices
    QUAD_SLICE = 4
    mad.use(sequence='ps')
    mad.select(flag='makethin', class_='rbend', slice_=QUAD_SLICE)
    mad.select(flag='makethin', class_='quadrupole', slice_=QUAD_SLICE)
    mad.select(flag='makethin', class_='sbend', slice_=QUAD_SLICE)
    mad.select(flag='makethin', class_='hkicker', slice_=QUAD_SLICE, thick=False)
    mad.select(flag='makethin', class_='sextupole', slice_=2)
    mad.makethin(sequence='ps')

    # Match tune using PFWs
    pfw_dict_on_resonance, tune_info_on_resonance = tune_match(mad, Qx=QX_TARGET, Qxp=QPX_TARGET, Qy=QY_TARGET,
                                                               Qyp=QPY_TARGET, verbose=verbose)
    # pfw_dict_on_resonance, tune_info_on_resonance = Tmatch(mad,Qx=QX_TARGET,Qxp=QPX_TARGET,Qy=QY_TARGET,Qyp=QPY_TARGET, p=p, ex=ex, ey=ey)

    mad.input("k1prpfwf = " + str(pfw_dict_on_resonance["k1prpfwf"]) + ";")
    mad.input("k1prpfwd = " + str(pfw_dict_on_resonance["k1prpfwd"]) + ";")
    mad.input("k2prpfwf = " + str(pfw_dict_on_resonance["k2prpfwf"]) + ";")
    mad.input("k2prpfwd = " + str(pfw_dict_on_resonance["k2prpfwd"]) + ";")
    twiss_after_makethin = mad.twiss().dframe()

    print("> Import Complete, MAD-X is ready to go!")

    Qx = tune_info_on_resonance['Qx']
    Qxp = tune_info_on_resonance['Qxp']  # Questa dovrebbe esssere la cromaticità
    if verbose:
        print(f"\n Qx = {Qx}, Qxp = {Qxp}")

    ############################## Convert Line to Xsuite   #####################
    mad.use(sequence="PS")

    if corr_seq == False:
        line = xt.Line.from_madx_sequence(
            mad.sequence(), allow_thick=True)

    else:
        line = xt.Line.from_madx_sequence(
            mad.sequence(), allow_thick=True, deferred_expressions=True)

    line.particle_ref = xp.Particles(
        mass0=xp.PROTON_MASS_EV,
        q0=1,
        p0c=p * scipy.constants.c)

    ######################### Calculate Frev ------> REVOLUTION FREQUENCY | WES   ######################
    line.build_tracker(_context=ctx)
    twiss_parameters = line.twiss(method='4d')
    if verbose:
        print(f'CHROMATICITY IN XSUITE :{twiss_parameters.dqx}')  ######
    trev = twiss_parameters['T_rev0']
    frev = 1 / trev
    line.unfreeze()
    if verbose:
        print(f"frev = {frev}")
    # frev = 412657.22413208015

    # N_turn override
    if n_turns is None or n_turns == 0 or n_turns == '0':
        if verbose:
            print("> n_turns not specified, calculating from time")
            print(f">This sim will run for {n_turns} turns")
        n_turns = int(float(time) * frev)
    else:
        n_turns = int(n_turns)
        if verbose:
            print("> n_turns overridden")

    rf10MHz_enable = True if (rf10MHz_enable == '1') | (rf10MHz_enable == 1) | (rf10MHz_enable == 'True') else False

    ####################  ADDING THE SEPTUM        ############################

    septum = xt.LimitRect(
        min_x=SEPTA_X_MM * 0.001,  # in meters
    )

    line.insert_element(
        element=septum,
        name="SEPTUM",
        index='pe.smh57'
    )

    # TFB Config
    rfko_kick = slwex.kick_angle(float(volt), Brho)
    if norm_gain:
        rfko_kick = rfko_kick / Brho
    ############################# Define your parameters for a single chirp ######################

    start_freq = frev * freq_start_ratio
    end_freq = frev * freq_end_ratio

    # Generate the repeated chirp

    if chirp_type == 'linear':
        t, chirp_signal = ph.generate_chirp(start_freq, end_freq, duration, sampling_freq)
    else:  # non ci sono altre opzioni
        t, chirp_signal = ph.generate_chirp_non_linear(start_freq, end_freq, duration, sampling_freq)

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
        name=f'EXCITER',
        index='pr.kfb97'
    )
    if verbose:
        print('exciter Done')

    ########################## RF Cavity Config; voltage 0 if disabled   ########################
    if rf10MHz_enable:
        RF_VOLTAGE = 130e3  # V
    else:
        RF_VOLTAGE = 0

    RF_HARMONIC = 8
    RF_FREQUENCY = frev * RF_HARMONIC

    PHASE = 0  # rising-edge

    rf_cavity = xt.Cavity(
        _context=ctx,
        voltage=RF_VOLTAGE,
        frequency=RF_FREQUENCY,
        lag=PHASE
    )

    line.insert_element(
        element=rf_cavity,
        name="rf_cavity",
        at_s=0
    )
    ######################

    ####################### Insert a monitor to record the particles MONITOR AT THE SEPTUM  #############
    monitor = xt.ParticlesMonitor(
        num_particles=n_part,
        start_at_turn=0,
        stop_at_turn=n_turns,
        auto_to_numpy=True
    )

    line.insert_element(index='pe.smh57', element=monitor, name='septa_monitor')

    line.build_tracker(_context=ctx)
    line.particle_ref = xp.Particles(
        mass0=xp.PROTON_MASS_EV,
        q0=1,
        p0c=p * scipy.constants.c
    )

    ###############################     PARTICLE GENERARION--- from bunch if RF #####################

    if rf10MHz_enable:
        if verbose:
            print("RF present; generating from generate_matched_gaussian_bunch()")
        particles = xp.generate_matched_gaussian_bunch(
            line=line,
            num_particles=int(n_part),
            nemitt_x=exn,
            nemitt_y=eyn,
            sigma_z=4.3,
            total_intensity_particles=30e10
        )
    else:
        if verbose:
            print("RF not present")
        sigmas, sigmas_p = xp.generate_2D_gaussian(int(n_part))

        try:
            particles = line.build_particles(
                method='4d',
                delta=DPP_FACTOR,
                nemitt_x=exn,
                nemitt_y=eyn,
                x_norm=sigmas,
                px_norm=sigmas_p,
                y_norm=sigmas,
                py_norm=sigmas_p,
            )
            z_array = scipy.stats.uniform.rvs(loc=0 - twiss_parameters['circumference'] / 2,
                                              scale=twiss_parameters['circumference'],
                                              size=int(n_part))
            delta_array = scipy.stats.norm.rvs(loc=0, scale=DPP_FACTOR / 2, size=int(n_part))
            particles.zeta = z_array
            particles.delta = delta_array
        except AssertionError:
            print("Failed line.build, trying xp.build_particles()")
            particles = xp.build_particles(
                particle_ref=line.particle_ref,
                method='4d',
                delta=DPP_FACTOR,
                nemitt_x=exn,
                nemitt_y=eyn,
                x_norm=sigmas,
                px_norm=sigmas_p,
                y_norm=sigmas,
                py_norm=sigmas_p,
            )
            z_array = scipy.stats.uniform.rvs(loc=0 - twiss_parameters['circumference'] / 2,
                                              scale=twiss_parameters['circumference'],
                                              size=int(n_part))
            delta_array = scipy.stats.norm.rvs(loc=0, scale=DPP_FACTOR / 2, size=int(n_part))
            particles.zeta = z_array
            particles.delta = delta_array
        else:
            if verbose:
                print("Generating from line.build_particles()")

    # RECOMPUTE THE FINAL TWISS because twiss_parameters is calculated before adding SEPTA-TRANSVERSE_EXCITER
    final_twiss = line.twiss(method='4d')

    if verbose:
        print(
            f'Summary of the used parameters: \n  \n Gain = {volt} \n \n RF_generation = {rf10MHz_enable} \n \n exn,exy = {exn}, {eyn} \n \n DPP = {DPP_FACTOR} \n \n' +
            f' Chirp frequencies = ({start_freq},{end_freq}) \n \n revolution freq = {frev} \n \n X Tune = {Qx} \n \n X Chromaticity = {Qxp} \n \n Septa x lim [mm] = {SEPTA_X_MM}')
    params_out = dict(REL_GAMMA=REL_GAMMA, exn=exn, p=p, eyn=eyn, duration=duration, volt=volt, time=time,
                      n_part=n_part,
                      n_turns=n_turns, freq_start_ratio=freq_start_ratio, freq_end_ratio=freq_end_ratio,
                      sampling_freq=sampling_freq,
                      QY_TARGET=QY_TARGET, QPY_TARGET=QPY_TARGET, QX_TARGET=QX_TARGET, QPX_TARGET=QPX_TARGET,
                      rf10MHz_enable=rf10MHz_enable,
                      DPP_FACTOR=DPP_FACTOR, SEPTA_X_MM=SEPTA_X_MM, ctx=ctx, return_form=return_form, REL_BETA=REL_BETA,
                      momentum=momentum, Brho=Brho)

    if return_form == 'dict':
        output = dict(line=line, particles=particles, monitor=monitor, twiss=final_twiss, params=params_out, mad=mad)
        return output


