import numpy as np
import matplotlib.pyplot as plt
import xobjects as xo
import xtrack as xt
from matplotlib.colors import LinearSegmentedColormap

from . import xsuite_helper as xh
from . import slowex_helper as slwex

from . import phy_helper as ph






#
#
# def insert_rfko_custom(line, signal=None, Brho=None, pc=None, beta=None, tune_factor=1 / 3, volt=0,twiss=None, chirp_type='linear', monofreq=False,
#                        frev=None, freq_start_ratio=90 / 100, freq_end_ratio=110 / 100, sampling_freq=1e9,
#                        duration=1 / 2000, time=None, n_turns=None, ctx=xo.ContextCpu(), out_params=False):
#     ''' it can accept a signal already made up to be repeated
#     '''
#     if out_params:  # useful if used without the wrapper
#         params = locals()
#
#     if (Brho is None) | (pc is None) | (beta is None):
#         print('--> no dynamical parameters given, used standard lead ions at 650 Mev per nucleon')
#         rel_params = ph.energy()
#         pc = rel_params['pc']
#         beta = rel_params['beta']
#         Brho = rel_params['Brho']
#
#     rfko_kick = slwex.kick_angle(float(volt), Brho, pc, beta)
#     if twiss is None:
#         twiss = line.twiss(method='4d')
#
#     # revolution freq
#     if frev is None:
#         trev = twiss['T_rev0']
#         frev = 1 / trev
#         print(f'--> revolution frquency = {frev}')
#
#     # frequancies scanned
#
#     start_freq = frev * tune_factor * freq_start_ratio
#     end_freq = frev * tune_factor * freq_end_ratio
#
#
#     line.unfreeze()
#
#     if signal is not None:
#         plt.title('custom signal fed to exciter')
#         plt.plot(np.arange(len(signal)) / sampling_freq, signal)
#
#     if signal is None:
#         if monofreq:
#             if time is None: # I could delete this simply
#                 time = (n_turns + 3) * twiss.T_rev0
#             t = np.linspace(0,time,int(sampling_freq*time))
#             chirp_signal = np.cos(2*np.pi*frev*tune_factor*t)
#         else:
#             t, chirp_signal = ph.generate_chirp(start_freq, end_freq, duration, sampling_freq)
#         if (time is None) & (n_turns is None):
#             print(
#                 '----- There is no way to infer the total simulation time and for the chirp signal repetion is needed ----')
#
#         elif (time is None) & (n_turns is not None):
#             time = (n_turns + 3) * twiss.T_rev0
#
#         # Exciter config; the duration parameter tells it to repeat the chirp_signal
#         rfko_exciter = xt.Exciter(
#             _context=ctx,
#             samples=chirp_signal,
#             sampling_frequency=sampling_freq,
#             frev=frev,
#             duration=float(time),
#             start_turn=0,
#             knl=[rfko_kick]
#         )
#
#     elif time is None:
#         # Signal already provided with a length matching the total simulation
#         rfko_exciter = xt.Exciter(
#             _context=ctx,
#             samples=signal,
#             sampling_frequency=sampling_freq,
#             frev=frev,
#             start_turn=0,
#             knl=[rfko_kick]
#         )
#     else:
#         rfko_exciter = xt.Exciter(
#             _context=ctx,
#             samples=signal,
#             sampling_frequency=sampling_freq,
#             frev=frev,
#             duration=float(time),
#             start_turn=0,
#             knl=[rfko_kick]
#         )
#
#     line.insert_element(
#         element=rfko_exciter,
#         name='EXCITER1',
#         index='pr.kfb97'
#     )
#     if out_params:
#         params['frev'] = frev
#         return params
#



def insert_rfko_custom_(rfko, tune_factor=1 / 3, signal=None, gain=None, total_signal=True, monofreq=False,
                       freq_start_ratio=None, freq_end_ratio=None, sampling_freq=None,signal_check=True,
                       duration=None,init_phase_random=False,return_signal=False, ctx=None):
    """
    :param rfko: RFKO object.
    :param signal: RF signal to be fed to the exciter. Default is None.
    :param tune_factor: Factor to tune the RF frequency. Default is 1/3.
    :param gain: Gain parameter for the exciter. If None, the default gain from rfko.sim_params will be used.
    :param total_signal: Flag to indicate if the signal provided has a length matching the total simulation time. Default is True.
    :param monofreq: Flag to indicate if a monofrequency signal should be generated. Default is False.
    :param freq_start_ratio: Ratio of the starting frequency to the revolution frequency. Default is None.
    :param freq_end_ratio: Ratio of the ending frequency to the revolution frequency. Default is None.
    :param sampling_freq: Sampling frequency of the signal. If None, the default sampling frequency from rfko.sim_params will be used.
    :param signal_check: Flag to indicate if a check should be performed on the generated signal. Default is True.
    :param duration: Duration of the signal in seconds. If None, the default duration from rfko.sim_params will be used.
    :param init_phase_random: Flag to indicate if the initial phase of the signal should be random. Default is False.
    :param return_signal: Flag to indicate if the generated signal should be returned. Default is False.
    :param ctx: Context object required for the Exciter. If None, the default value from rfko.sim_params will be used.
    :return: If return_signal and monofreq flags are True, the generated signal is returned. Otherwise, None is returned.
    """
    ##################################### Setting the params
    if gain is None:
        gain = rfko.sim_params['gain']
    if freq_end_ratio is None:
        freq_end_ratio= rfko.sim_params['freq_end_ratio']
    if freq_start_ratio is None:
        freq_start_ratio= rfko.sim_params['freq_start_ratio']
    if duration is None:
        duration = rfko.sim_params['duration']
    if sampling_freq is None:
        sampling_freq = rfko.sim_params['sampling_freq']
    if ctx is None:
        ctx = rfko.sim_params['ctx']

    line = rfko.line

    pc = rfko.line_params['pc']
    beta = rfko.line_params['beta']
    Brho = rfko.line_params['Brho']
    charge = rfko.line_params['charge']
    rfko_kick = slwex.kick_angle(float(gain), Brho, pc, beta,charge)
    rfko.sim_params['kick_angle'] = rfko_kick
    try:
        twiss = rfko.twiss
    except:
        twiss = rfko.line.twiss(method='4d')

    #### Tune_factor si the same parameter as third_frev so when i use this I can directly change third_frev
    if tune_factor is None:
        tune_factor = rfko.sim_params['third_frev']
    rfko.sim_params['third_frev'] = tune_factor
    ############################################
    # revolution freq
    frev = 1/twiss.T_rev0
    time = rfko.sim_params['time']
    # frequency span of the chirp in terms of frev
    start_freq = frev * tune_factor * freq_start_ratio
    end_freq = frev * tune_factor * freq_end_ratio
    if init_phase_random:
        phase_random = 2*np.pi*np.random.random()
    else:
        phase_random =  0
    line.unfreeze()

    if signal is not None:
        plt.title('custom signal fed to exciter')
        plt.plot(np.arange(len(signal)) / sampling_freq, signal)

        if total_signal:
            # Signal already provided with a length matching the total simulation
            rfko_exciter = xt.Exciter(
                _context=ctx,
                samples=signal,
                sampling_frequency=sampling_freq,
                frev=frev,
                start_turn=0,
                knl=[rfko_kick]
            )
        else: # Signal extended to the total simulation duration
            rfko_exciter = xt.Exciter(
                _context=ctx,
                samples=signal,
                sampling_frequency=sampling_freq,
                frev=frev,
                duration=float(time),
                start_turn=0,
                knl=[rfko_kick]
            )

    if signal is None:
        if monofreq:
            # To check
            t = np.linspace(0,time,int(sampling_freq*time))
            signal = np.cos(2*np.pi*frev*tune_factor*t+phase_random)
            if signal_check:
                _,_,f = ph.Ft(signal,t[1],peaks=1,ret_freqs=True,plot=False,window='hann')
                rfko.logger.warning(f'This is a check of the frequency on the rf signal,'
                                    f'desired f = {frev*tune_factor} \n FFT of the signal {f}')
        else:
            t, signal = ph.generate_chirp(start_freq, end_freq, duration, sampling_freq)

        # Exciter config; the duration parameter tells it to repeat the chirp_signal
        rfko_exciter = xt.Exciter(
            _context=ctx,
            samples=signal,
            sampling_frequency=sampling_freq,
            frev=frev,
            duration=float(time),
            start_turn=0,
            knl=[rfko_kick]
        )



    line.insert_element(
        element=rfko_exciter,
        name='EXCITER1',
        index='pr.kfb97'
    )
    if (return_signal)&(monofreq):
        return signal
    else:
        return None




















def plot_kobayashi(dq, S, traj_num=10, npointsXtraj=1000, plot_lims=False, H_max=2, plot_size_ratio=1
                    ):
    ''' Plot kobayashi's Hamiltonia contours
    H max defines the maximum of the Action we want to plot in UNITS of the Stable amplitude'''

    def implicit_function(x, px, dq=dq, S=S):
        # x and px must be normalized
        return 3 * np.pi * dq * (x ** 2 + px ** 2) + 1 / 4 * S * (3 * x * px ** 2 - x ** 3)

    epsilon = 6 * np.pi * dq
    Hsep = ((4 * np.pi * dq) ** 3) / (S ** 2)
    # H_stable = np.array([0,Hsep])
    Hs_in = np.linspace(0, Hsep, traj_num // 2 + 1)
    Hs_out = np.linspace(Hsep, H_max * Hsep, traj_num // 2 + 1)

    X_lim = np.sort([-2 * epsilon / (3 * S), (4 * epsilon / (3 * S))])
    PX_lim = np.sort([-2 * epsilon / (np.sqrt(3) * S), 2 * epsilon / (np.sqrt(3) * S)])

    ## For the plot
    # Define the gradual color palette
    colors1 = [(0, 'green'), (0.5, 'cyan'), (1, 'blue')]  # Example color transitions
    cmap1 = LinearSegmentedColormap.from_list('gradual_palette', colors1)
    colors2 = [(0, 'orange'), (1, 'red')]  # Example color transitions
    cmap2 = LinearSegmentedColormap.from_list('gradual_palette', colors2)

    X_ = np.linspace(-X_lim[1] * 2 * (1 + plot_size_ratio), X_lim[1] * 2 * (1 + plot_size_ratio), npointsXtraj + 1)
    PX_ = np.linspace(-(1 + plot_size_ratio) * PX_lim[1], PX_lim[1] * (1 + plot_size_ratio), npointsXtraj + 1)
    X, Y = np.meshgrid(X_, PX_)
    # Evaluate the implicit function
    Z = implicit_function(X, Y)
    plt.contour(X, Y, Z, levels=np.sort(Hs_in), cmap=cmap1, linewidths=0.5)  # Contour at Z = 0
    ######## external

    X_ = np.linspace(-X_lim[1] * 2 * (1 + plot_size_ratio), X_lim[1] * 2 * (1 + plot_size_ratio), npointsXtraj + 1)
    PX_ = np.linspace(-(1 + plot_size_ratio) * PX_lim[1], PX_lim[1] * (1 + plot_size_ratio), npointsXtraj + 1)
    X, Y = np.meshgrid(X_, PX_)
    # Evaluate the implicit function
    Z = implicit_function(X, Y)
    plt.contour(X, Y, Z, levels=np.sort(Hs_out), cmap=cmap2, linewidths=0.5)  # Contour at Z = 0

    if plot_lims:
        plt.axvline(X_lim[0])
        plt.axvline(X_lim[1])
        plt.axhline(PX_lim[0])
        plt.axhline(PX_lim[1])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Contour Plot of Implicit Function')
    plt.grid(True)
    plt.axis('equal')  # Equal aspect ratio
    plt.show()


def plot_kobayashi_simple(dq, S, traj_num=10, npointsXtraj=1000, plot_lims=False, H_max=2, plot_size_ratio=1,
                   outside_stable=True):
    ''' H max defines the maximum of the Action we want to plot in UNITS of the Stable amplitude'''

    def implicit_function(x, px, dq=dq, S=S, H=-33e-8):
        # x and px must be normalized
        return 3 * np.pi * dq * (x ** 2 + px ** 2) + 1 / 4 * S * (3 * x * px ** 2 - x ** 3) - H

    epsilon = 6 * np.pi * dq
    Hsep = ((4 * np.pi * dq) ** 3) / (S ** 2)
    # H_stable = np.array([0,Hsep])
    Hs_in = np.linspace(0, Hsep, traj_num // 2 + 1)
    Hs_out = np.linspace(Hsep, H_max * Hsep, traj_num // 2 + 1)
    Xs = []
    PXs = []
    X_lim = np.sort([-2 * epsilon / (3 * S), (4 * epsilon / (3 * S))])
    PX_lim = np.sort([-2 * epsilon / (np.sqrt(3) * S), 2 * epsilon / (np.sqrt(3) * S)])

    ## For the plot
    # Define the gradual color palette
    colors = [(0, 'blue'), (0.5, 'green'), (1, 'red')]  # Example color transitions
    cmap = LinearSegmentedColormap.from_list('gradual_palette', colors)

    for i, H in enumerate(Hs_in):
        # For the version of stable amplitudes inside the stable triangle
        if outside_stable:
            X_ = np.linspace(-X_lim[1] * 2 * (1 + plot_size_ratio), X_lim[1] * 2 * (1 + plot_size_ratio),
                             npointsXtraj + 1)
            PX_ = np.linspace(-(1 + plot_size_ratio) * PX_lim[1], PX_lim[1] * (1 + plot_size_ratio), npointsXtraj + 1)
        else:
            X_ = np.linspace(X_lim[0], X_lim[1], npointsXtraj + 1)
            PX_ = np.linspace(PX_lim[0], PX_lim[1], npointsXtraj + 1)
        X, Y = np.meshgrid(X_, PX_)
        # Evaluate the implicit function
        Z = implicit_function(X, Y, H=H)
        plt.contour(X, Y, Z, levels=[0], colors='r', linewidths=0.5)  # Contour at Z = 0

    for i, H in enumerate(Hs_out):
        X_ = np.linspace(-X_lim[1] * 2 * (1 + plot_size_ratio), X_lim[1] * 2 * (1 + plot_size_ratio), npointsXtraj + 1)
        PX_ = np.linspace(-(1 + plot_size_ratio) * PX_lim[1], PX_lim[1] * (1 + plot_size_ratio), npointsXtraj + 1)
        X, Y = np.meshgrid(X_, PX_)
        # Evaluate the implicit function
        Z = implicit_function(X, Y, H=H)
        plt.contour(X, Y, Z, levels=[0], colors='b', linewidths=0.5)  # Contour at Z = 0
    if plot_lims:
        plt.axvline(X_lim[0])
        plt.axvline(X_lim[1])
        plt.axhline(PX_lim[0])
        plt.axhline(PX_lim[1])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Contour Plot of Implicit Function')
    plt.grid(True)
    plt.axis('equal')  # Equal aspect ratio
    plt.show()


def kobay_vs_tracking_1(rfko, tune_corr=False, pdigit=3):
    ''' to start simple it will consider a particle. Package formalism

   '''
    assert hasattr(rfko, 'monitor'), 'No tracked particle'

    if not hasattr(rfko, 'twiss'):
        rfko.twiss = rfko.line.twiss()

    ## Temporary for 1 particle
    assert rfko.sim_params['n_part'] == 1, 'This procedure is reserved for 1 particle at the moment'

    element = rfko.monitor.placed_at_element
    outdict = rfko.to_dict()
    Monitor = xh.Normalize_monitor(outdict)

    #### I ROTATE THE TRACKED PARTICLES to bring them back at the correct orientation of the Hamiltonian
    tri_g = slwex.tri_geom(outdict, negate_s=True, sqrt=tune_corr, interpolate=True)
    tune_dist = tri_g['tune_distance']
    nominal_dq = rfko.twiss.qx - 6 - 1 / 3
    S = tri_g['S']
    dmu = rfko.twiss.mux[rfko.twiss.name == element] * 2 * np.pi - tri_g['S_mu']

    # Plot pos 1
    plt.figure(figsize=(10, 8))
    plt.scatter(Monitor.x, Monitor.px)
    plt.title('Normalized')

    # Rotate coordinate of the tracked particle
    X, PX = ph.rotate(Monitor.x[0], Monitor.px[0], -dmu[0],
                   center_mean=True)  # the mean_center shouldn't change the situation
    ### Plot pos2 VS
    plt.figure(figsize=(10, 8))
    plt.scatter(X, PX)
    plt.title(f"Debug ph.rotated of {dmu} (pi)")
    ######### calculate Hs
    Hs = np.mean(slwex.kobay(X, PX, dq=tune_dist, S=S))
    print(Hs)
    order_Hs = np.log10(np.abs(Hs))
    Hs_cut = round(float(Hs), int(np.abs(order_Hs)) + pdigit)

    #### PLot H
    plt.figure()
    plt.plot(slwex.kobay(X, PX) / Hs)
    plt.title('H-values')

    ### PLOT THE CORRESPONDING CONTOURPLOT AND THEN ON TOP, THE TRACKED PARTICLES
    margin_ = 1.2  # margin of the contour plot
    X_ = np.linspace(np.min(X) * margin_, np.max(X) * margin_, 2000)
    PX_ = np.linspace(margin_ * np.min(PX), margin_ * np.max(PX), 2000)
    meshx, meshpx = np.meshgrid(X_, PX_)
    # print(Hs)

    Hmesh = slwex.kobay(meshx, meshpx, dq=tune_dist, S=S)

    # BAKUP POINT
    plt.figure()
    plt.contour(meshx, meshpx, Hmesh, levels=[Hs])
    plt.scatter(X, PX, s=2)
    print(f'The nominal tune distance is {nominal_dq} \n The one with the correction to the orbit is {tune_dist}')
    plt.show()


def kobay_vs_tracking_n(rfko, tune_sqrt=False):
    ''' to start simple it will consider a particle. Package formalism

   '''
    assert hasattr(rfko, 'monitor'), 'No tracked particle'
    assert rfko.sim_params['DPP_FACTOR'] == 0, 'The corrections for the off momentum particles is wrong still'
    if (not hasattr(rfko, 'twiss'))&(rfko.line_type!='henon_map'):
        rfko.twiss = rfko.line.twiss()

    element = rfko.monitor.placed_at_element
    outdict = rfko.to_dict()
    Monitor = xh.Normalize_monitor(outdict)

    #### I ROTATE THE TRACKED PARTICLES to bring them back at the correct orientation of the Hamiltonian
    if rfko.line_type != 'henon_map':
        tri_g = slwex.tri_geom(outdict, negate_s=True, sqrt=tune_sqrt, interpolate=True)
        tune_dist = tri_g['tune_distance']
        nominal_dq = rfko.twiss.qx - 6 - 1 / 3
        S = tri_g['S']
        dmu = rfko.twiss.mux[rfko.twiss.name == element] * 2 * np.pi - tri_g['S_mu']
    else:
        dmu = 0 # monitor is at the virtual sextupole
        tune_dist = rfko.henon_params['qx']-6-1/3
        nominal_dq = tune_dist
        # Without the dispersion the nomila tune distance is the same as the tune distance
        S = rfko.henon_params['S']

    # Rotate coordinate of the tracked particle
    X, PX = ph.rotate(Monitor.x, Monitor.px, -dmu[0],
                   center_mean=True)
    # Rotation sign is for diplacement from the sextupole so to go back sign need to be inverted
    # the mean_center shouldn't change the situation since the traj are already centered

    # Mean value of the hamiltonian (whole trajectorie) for every particle
    Hs = np.mean(slwex.kobay(X, PX, dq=tune_dist, S=S), axis=1)

    ### PLOT THE CORRESPONDING CONTOURPLOT AND THEN ON TOP, THE TRACKED PARTICLES
    margin_ = 1.2  # margin of the contour plot
    X_ = np.linspace(np.min(X) * margin_, np.max(X) * margin_, 2000)
    PX_ = np.linspace(margin_ * np.min(PX), margin_ * np.max(PX), 2000)
    meshx, meshpx = np.meshgrid(X_, PX_)

    Hmesh = slwex.kobay(meshx, meshpx, dq=tune_dist, S=S)
    colors = [(0, 'blue'), (0.5, 'green'), (1, 'red')]  # Example color transitions
    cmap = LinearSegmentedColormap.from_list('gradual_palette', colors)
    H_color = (Hs - np.min(Hs)) / np.abs(np.max(Hs - np.min(Hs)))
    print(Hs)
    print(H_color)
    # BAKUP POINT
    plt.figure(figsize=(10, 8))
    plt.contour(meshx, meshpx, Hmesh, levels=np.sort(Hs), cmap=cmap)
    colors = cmap(H_color)
    for i in range(X.shape[0]):
        plt.scatter(X[i], PX[i], s=2, color=colors[i])
    print(f'The nominal tune distance is {nominal_dq} \n The one with the correction to the orbit is {tune_dist}')
    plt.show()