import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
# from matplotlib.cm import ScalarMappable
from tqdm import tqdm
import time as timing
from scipy.fftpack import rfft, rfftfreq

import xtrack as xt

from . import xsuite_helper as xh
from . import slowex_helper as slwex
from . import plotting2 as plt2
from . import utility
from .Rfko import Rfko

def binning(outdict, turn_binning=5, current=True, plot_stairs=False, duty_factor=True,time_binning=None,
                 duty_binning=None):
    ''' Binning and spill manipulation from the rfko object (or dictionary for now)'''
    particles = outdict['particles']
    revt = outdict['twiss'].T_rev0

    if duty_binning is None:
        duty_binning=turn_binning
    data = {
        'at_turn': particles.at_turn,
        'x': particles.x,
        'px': particles.px,
        'delta': particles.delta,
    }
    df = pd.DataFrame(data)
    # count extracted particles for every turn
    # considering extracted at_turns 0 == index 0
    bincount = np.bincount(df['at_turn'])[:-1]

    binning = []

    time_step = []
    for x in range(len(bincount) // turn_binning + 1):
        binning.append(np.sum(bincount[x * turn_binning : x * turn_binning + turn_binning]))
        time_step.append(x * turn_binning*revt)
            # time_step[n] : is the istant at the start of the time-at-binning
            # from 0----> (nturns-1)*revolution_period

    #### NO Duty factor is One single value for every binning
    if duty_factor:
        mean = np.mean(binning)
        mean_sq = mean ** 2
        sq_mean = np.mean( binning ** 2)
        duty = (mean_sq / sq_mean)

    if current:
        # Divide the counts for the time interval of the binning
        binning = np.array(binning) / time_step[1]
        ### for the DUTY FACTOR THIS SHOULD NOT CHANGE

    else:
        binning = np.array(binning)
    if plot_stairs:
        plt.stairs(binning, time_step)
    if duty_factor:
        return np.array(time_step), binning, duty
    else:
        return np.array(time_step), binning


def binning_data(folder_name,turn_binning=5,duty_factor=True,
                 normalize_counts=True):
    ''' Binning and manipulation of the spill FROM DATA
    RETURN: timestep : istant of time at the beginning of the bin 
            binning is the count of extracted particles in the time (timestep[binning]--timestetep[binning+1
        '''
    part_at_turn = np.load(f'{folder_name}/part_at_turn.npy')

    bincount = np.bincount(part_at_turn)[:-1]
    ## Getting revolution period, not explicitly saved
    # real time simulated
    time = utility.read_from_txt(f'{folder_name}/params.txt','time ')
    n_turns = utility.read_from_txt(f'{folder_name}/params.txt','n_turns ',type_='int')
    revt = time/n_turns

    binning = []
    time_step = []

    ## The last turn will in general consider a different number of turns
    # another idea : I could jus elimintae it
    decimal = len(bincount) / turn_binning- len(bincount) // turn_binning
    if decimal>0.5:
        n_binnings = int(len(bincount) // turn_binning) + 1
    else:
        n_binnings = int(len(bincount) // turn_binning) - 1

    for x in range(n_binnings ): # plus or minus one should depend on the remainder
        binning.append(np.sum(bincount[x * turn_binning : x * turn_binning + turn_binning]))
        time_step.append(x * turn_binning*revt)
    binning = np.array(binning)
    if normalize_counts:
        binning = binning/np.sum(binning)

    if duty_factor:
        mean_sq = np.mean(binning)**2
        sq_mean = np.mean( np.array(binning)**2)
        duty = mean_sq / sq_mean

        return time_step, binning, duty
    else:
        return time_step, binning






def _clean_dependencies(dependencies):
    clean_dep = []
    for x in dependencies:
        clean_dep.append(str(x)[6:].strip("']"))
    return clean_dep


def dependencies_quad(outdict, names_dict,which='all'):
    ''' Find the variables which the quadropoles are based on'''
    #line_df = outdict['line'].to_pandas()
    line = outdict['line']
    full_dep_list = []
    allowed_which = ['all','main_units','low_energy_quads']
    assert which in allowed_which, f'which can only be one of these : {allowed_which}'
    ## possible keys from the find_multipole_component functions 'multipoles', 'combf_knl', 'quad_mult', 'direct_ele', 'combf_sing'
    if which == 'all':
        which_keys = names_dict.keys()
    elif which == 'main_units':
        which_keys = ['combf_sing']
    elif which == 'low_energy_quads':
        which_keys = ['direct_ele']
    for key in which_keys:
        if len(names_dict[key]) != 0:
            names = names_dict[key]
            # select_field = dict(multipoles='knl[1]',combf_knl='knl[1]',quad_mult='knl[1]',direct_ele='k1',combf_sing='k1')
            dep_list = []
            for name in names:
                if key in ['multipole', 'combf_knl', 'quad_mult']:
                    dep_list.append(list(line.element_refs[name].knl[1]._expr._get_dependencies()))
                elif key in ['direct_ele', 'combf_sing']:

                    dep_list.append(list(line.element_refs[name].k1._expr._get_dependencies()))
                else:
                    print('something is strange')

            flat_dep = [x for sub in dep_list for x in sub]

            full_dep_list.append(list(set(flat_dep)))
    return _clean_dependencies(full_dep_list[0])


def tracking(outdict, f=100, A=0.001,sextupole_turns = None,twiss=False,return_time=False,which_quads = 'all'):
    ''' Performs tracking simulating quadrupole's sinusoidal ripples.

    The ripples are introduced through the variable that control the quadrupole strength and NOT the
    Multisetter object it may be slower because it does a for loop every turn
    '''
    # A is a relative amplitude, relative to the actual value of the variable
    if isinstance(outdict,Rfko):
        rfko = outdict
        outdict = rfko.to_dict()
    line = outdict['line']
    particles = outdict['particles']
    line_df = line.to_pandas()
    line_dict = dict()
    twiss_dict = dict()

    #######

    turns = outdict['params']['n_turns']
    # time passed after every turn, its relative because a shift in time is a phase shift
    t_turn = outdict['twiss'].T_rev0 * np.arange(turns)
    if sextupole_turns is not None:
        assert sextupole_turns>0
        #outdict['params']['dynamic_sextupole']=True # This is added to know if the virtual sextupole has to be computed every turn
        outdict['params']['dynamic_sextupole'] = sextupole_turns
        #take the values of sextupoles and set them
        xse_names = ['pr.xse01.a', 'pr.xse01.b', 'pr.xse07']
        try:
            setter = xt.MultiSetter(line, xse_names, field='k2')  # multisetter obj
        except:
            # in some version these elements are multipole!
            setter = xt.MultiSetter(line, xse_names, field='knl',index=2)  # multisetter obj
        xse0 = setter.get_values()  # initial/nominal values
        ramp = np.linspace(0, 1, sextupole_turns)

    # FIND THE QUADRUPOLE element names
    quad_names = xh.find_multipole_component(line_df, 'quadrupole') # find quad elems
    # find the vARIABLES underlying the elements
    dep_vars = dependencies_quad(outdict, quad_names,which=which_quads)
    amp_val = dict()
    for x in dep_vars:
        # initial values
        amp_val[x] = line.vars[x]._get_value()
    time_before = timing.perf_counter()
    it = 0
    # TRACKING
    if line.tracker is None:
        line.build_tracker()
    for _ in tqdm(np.arange(turns)):
        # each turn changes the value of the variable, ad the twiss and new line and track the turn
        ### (A * amp_val[x]) is considered the amplitude of the sinusoid
        if sextupole_turns is not None:
            if it < sextupole_turns:
                k2_it = xse0 * ramp[it]
                setter.set_values(k2_it)  # changes of sextupoles value

        for x in amp_val.keys():
            # changes of quadrupole-vars values
            line.vars[x] = amp_val[x] + (A * amp_val[x]) * np.sin(2 * np.pi * f * t_turn[it])


        line_dict[f'line_{it}'] = line
        if twiss: # Save a twiss for every turn
            twiss_dict[f'twiss_{it}'] = line.twiss(method='4d')
        line.track(particles, num_turns=1)
        it += 1
    time_taken = timing.perf_counter() - time_before
    print(f'Seconds elapsed = {time_taken}')
    #print('temporal_twiss and line saved to twiss_dynamics')
    if twiss:
        outdict['twiss_dynamics'] = twiss_dict
    outdict['line_dynamics'] = line_dict
    # RESETTING TO the INITIAL VALUES
    for key in amp_val.keys():
        line.vars[key] = amp_val[key]
    print(f'Total extracted particles = {np.sum(particles.at_turn<turns)}')

    ##à ADD THE PARAMETERS USED TO THE OUTDITCT and RFKO OBJ (if)
    outdict['params']['qr_amp'] = A
    outdict['params']['qr_f'] = f
    if 'rfko' in locals():
        rfko.sim_params['qr_amp']=A
        rfko.sim_params['qr_f'] = f
    if return_time:
        return time_taken

# alternativa senza usare le variabili per vedere se questo funziona senza errori
#### With multisetter
# def quad_ripples_multisetter(outdict, A=0.1, f=100, out=True):
#     line = outdict['line']
#     particles = outdict['particles']
#     line_df = line.to_pandas()
#     twiss_dict = dict()
#     line_dict = dict()
#     t_turn = np.arange(outdict['params']['n_turns']) * outdict['twiss'].T_rev0
#     quad_names = utility.find_multipole_component(line_df, 'quadrupole')
#     comp = [x for x in quad_names.keys() if len(quad_names[x]) != 0]
#     names_knl = [quad_names[x] for x in comp if x in ['multipole', 'combf_knl', 'quad_mult']]  ### Not used for now
#     names_k1 = [quad_names[x] for x in comp if x in ['direct_ele', 'combf_sing']]
#     name_k1_flat = [x for sub in names_k1 for x in sub]
#     setter1 = xt.MultiSetter(line, name_k1_flat, field='k1')
#     initk1 = setter1.get_values()
#
#     it = 0
#     time_before = timing.time()
#     for _ in tqdm(np.arange(outdict['params']['n_turns'])):
#         k1_it = initk1 + initk1 * A * np.sin(np.pi * 2 * f * t_turn[it])
#         setter1.set_values(k1_it)
#         # if out:
#         # twiss_dict[f'twiss_{it + 1}'] = line.twiss(method='4d')
#         # line_dict[f'line_{it + 1}'] = line
#         line.track(particles, num_turns=1)
#         it += 1
#
#     time_taken = timing.time() - time_before
#     print(f"> finished tracking, {time_taken} seconds elapsed")
#     # if out:
#     # outdict['dynamic_twiss'] = twiss_dict
#     # outdict['dynamic_line'] = line_dict


def norm_ripples(outdict, element='pe.smh57'):
    ''' Center on the distortion and the dispersion (particle-wise) orbit and Normalize
    '''
    monitor = outdict['monitor']
    particles = outdict['particles']
    particles_norm = outdict['particles'].copy()
    X = []
    PX = []
    for n in range(outdict['params']['n_turns']):
        twiss = outdict['twiss_dynamics'][f'twiss_{n}']
        twiss_df = twiss.to_pandas()

        betx = twiss_df[twiss_df.name == element].betx.iloc[0]
        alfx = twiss_df[twiss_df.name == element].alfx.iloc[0]
        xc = twiss_df[twiss_df.name == element].x.iloc[0]
        pxc = twiss_df[twiss_df.name == element].px.iloc[0]

        mask_null = monitor.x[:, n] != 0

        # NORMALIZE the turn with the selection given by mask_null
        # np.array(mask) could be unnecessary
        Xturn = (monitor.x[:, n] - np.array(mask_null) * xc) / np.sqrt(betx)
        PXturn = Xturn * alfx + monitor.px[:, n] * np.array(mask_null) * np.sqrt(betx)

        X.append(Xturn)
        PX.append(PXturn)
        particles_norm.x[particles.at_turn == n] = particles_norm.x[particles.at_turn == n] / np.sqrt(betx)
        particles_norm.px[particles.at_turn == n] = particles_norm.x[particles.at_turn == n] * alfx + particles_norm.px[
            particles.at_turn == n] * np.sqrt(betx)
    return (np.array(X).T, np.array(PX).T, particles_norm)


def anim_ph_qd_ripples(out_dict, filename=None, message='', step=5):
    ''' Phase space plot with the 'central' stable trangle
    ---------TODO
    - Tune correction not completed or not correct
    - Sextupole ramping ?
    -
    '''
    particles = out_dict['particles']
    monitor = out_dict['monitor']
    twiss_df = out_dict['line'].twiss(method='4d').to_pandas()
    SEPTA_X_MM = out_dict['params']['SEPTA_X_MM']  ## also this needs to be adjusted actually

    n_turns = out_dict['params']['n_turns']
    fig, ax = plt.subplots(figsize=(12, 8))
    scat = ax.scatter([], [], s=2)

    X, PX, Particles = norm_ripples(out_dict)
    if 'dynamic_sextupole' not in out_dict['params'].keys():
        S_strength, S_mu = slwex.Virtual_sextupole_complete(out_dict)

    def update(frame):
        # a frame is a turn
        if 'dynamic_sextupole' in out_dict['params'].keys():
            S_strength, S_mu = slwex.Virtual_sextupole_complete(dict(line=out_dict['line'],params=out_dict['params'],twiss=out_dict['twiss_dynamics'][f'twiss_{frame}']))
        at_turn = frame
        if frame % 50 == 0:
            print(f'frame {frame}')
        ax.clear()

        twiss = out_dict['twiss_dynamics'][f'twiss_{frame}']
        twiss_df = twiss.to_pandas()
        xc = twiss_df[twiss_df.name == 'pe.smh57'].x.iloc[0]
        pxc = twiss_df[twiss_df.name == 'pe.smh57'].px.iloc[0]
        betx = twiss_df[twiss_df.name == 'pe.smh57'].betx.iloc[0]

        X_extr = Particles.x[particles.at_turn <= at_turn]
        PX_extr = Particles.px[particles.at_turn <= at_turn]

        mask = monitor.x[:, at_turn] != 0  # mask on the monitor array, for the extracted particles (at_turn)
        dmu = twiss_df[twiss_df.name == 'pe.smh57'].mux.iloc[0] - S_mu

        dq0 = (twiss.qx - 6 - 1 / 3)  # normal as without distorsions and dispersion
        # the tune is different for every particle and so the stable triangle, but not including the dispersion,
        # means we consider just the stable for the zero dispersion particles
        dq = dq0 - S_strength * xc / (2 * np.pi * np.sqrt(betx))  # + twiss.dqx*monitor.delta[mask,at_turn]/(2*np.pi)
        ax.text(0.1, 0.9, f'{len(X_extr)} extracted', transform=ax.transAxes)
        ax.set_title(f'Phase space turn :{frame}/{n_turns}')
        ax.set_xlabel('x')
        ax.set_ylabel('px')
        # ax.axvline(SEPTA_scaled, c="r", linestyle="--")

        # XAXES LIMITS
        axes_margin = 0.1

        # xmin = np.min(np.concatenate((X.flatten(), SEPTA_scaled)))
        xmin = np.min(X)

        xmax = np.max(X)
        ax.set_xlim(xmin - np.abs((xmin - xmax) * axes_margin), xmax + np.abs((xmax - xmin) * axes_margin))

        # Yaxes LIMITS
        ymin = np.min(PX)
        ymax = np.max(PX)
        ax.set_ylim(ymin - np.abs((ymin - ymax) * axes_margin), ymax + np.abs((ymax - ymin) * axes_margin))

        ax.scatter(X[mask, at_turn], PX[mask, at_turn], c='b', s=2)
        ax.scatter(X_extr, PX_extr, c='r', s=2)
        plt2.stable_tri_plot(dq, S_strength, dmu=dmu)

        return scat,

    ani = FuncAnimation(fig, update, frames=range(0, n_turns, step), blit=True)
    if filename is None:
        filename = f'n_part{out_dict["params"]["n_part"]}_QX{out_dict["twiss"].qx}_Volt{out_dict["params"]["volt"]}_duration{out_dict["params"]["duration"]}'
    if os.path.isdir('./gif_wes'):
        ani.save(f'./gif_wes/ph_space_stable_quad_ripples_{message}_{filename}.gif', dpi=200)
    else:
        ani.save(f'./gif_wes/ph_space_stable_quad_ripples_{message}_{filename}.gif', dpi=200)

    return None


