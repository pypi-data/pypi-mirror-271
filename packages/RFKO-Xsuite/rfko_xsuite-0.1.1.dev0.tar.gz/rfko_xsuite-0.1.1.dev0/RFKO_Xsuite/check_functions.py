



import numpy as np
import matplotlib.pyplot as plt



from . import xsuite_helper as xh
from . import slowex_helper as slwex
from . import xsuite_actions as xa
from . import line_setup
from . import plotting2 as plt2

from . import utility

from . import bare_mach_setup as bms


def plot_stable(out_dict, s=2, figsize=(12, 7), interpolate=False, wrongf=False, center=True):
    twiss_df = out_dict['twiss'].to_pandas()
    monitor = out_dict['monitor']
    S_strength, S_mu = utility.Virtual_sextupole_complete(out_dict)  # compute sextupole strength and mu
    dmu = twiss_df[twiss_df.name == 'pe.smh57'].mux.iloc[0] * 2 * np.pi - S_mu
    # dmu from the virtual sextupole to know the rotation

    Monitor = utility.Normalize_monitor(out_dict, normalize_particles=False, center=center)
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
        plt2.stable_tri_plot(dq, - S_strength, dmu=dmu, linewidth=1, translation_vector=t_vector)

    else:
        plt2.stable_tri_plot(dq, - S_strength, dmu=dmu, linewidth=1)
    plt.title(
        f'Tune =  {round(out_dict["twiss"].qx, 5)}, ratio tune distance to sextupole = {round(dq / S_strength, 5)}')




def amplitude_growth(outdict, n_parts=3, figsize=(10, 8), plot=True, return_amp=False, exclude_extr=False,label_by='mean'):
    ''' I suppose to take just few particles, if not one
    TO DO :
    - ADD STATISTICS :
        - moving average,
        - std on the moving average?
    '''

    # Normalizing function
    # There was not centering, this shouldn't change many things
    monitor = utility.Normalize_monitor(outdict, keep_zeroes=True, normalize_particles=False,center=True)

    twiss = outdict['twiss']
    if exclude_extr:
        # Takes out the particles that become axtracted at some point
        idnz = []
        for n in range(monitor.x.shape[0]):
            if 0 not in monitor.x[n, :]:
                idnz.append(n)
        ids = np.random.choice(idnz, size=n_parts,replace=False)
    else:
        ids = np.random.choice([n for n in range(outdict['params']['n_part'])],size=n_parts,replace=False)
    amps = np.sqrt(monitor.x[ids, :] ** 2 + monitor.px[ids, :] ** 2)

    freq = 1 / twiss.T_rev0 - twiss.slip_factor * monitor.delta[
        ids, 0] * 1 / twiss.T_rev0  # it doesn't change on a turn basis
    tune = twiss.qx + twiss.dqx * monitor.delta[ids, 0]
    if plot:
        plt.figure(figsize=figsize)
        for i in range(n_parts):
            mean_amp = np.mean(amps[i, :])
            if label_by=='mean':
                plt.plot(amps[i, :], label=f'mean amplitude = {round(mean_amp, 6)}', alpha=0.5)
            elif label_by=='tune':
                plt.plot(amps[i,:],label=f'tune = {round(tune[i],6)}')
            else :
                init_amp = amps[i,0] # This should be the initial amplitude
                plt.plot(amps[i, :], label=f'initial ampl = {round(init_amp, 6)}')
        plt.title(f"Amplitudes per turn with Gain = {outdict['params']['volt']}")
        plt.xlabel('Turns')
        plt.legend()
    if return_amp:
        return amps





####################### PROTYPE AND CKETCH SPACE
def amps_stats(amps,plot=False,figsize=(10,8),xvar='means'):
    ''' PROBLEM IT CONSIDERS ALL THE AMPLITUDE BUT AT SOME POINT IF A PARTICLE IS EXCTRACTED THOSE GOES TO ZERO AND THE
    STATISTICS DOESN'T MAKE SENSE ANYMORE!!

    :param amps:
    :param plot:
    :param figsize:
    :param xvar:
    :return:
    '''
    stds = np.std(amps,axis=1)
    means = np.mean(amps,axis=1)
    rel_std = stds/means
    print('--> statistics of the amplitudes')
    print(f'--> The average std is {np.mean(stds)}, The average mean is {np.mean(means)}')
    if xvar != 'means':
        init_amps = amps[:,0]
    if plot:
        fig, ax = plt.subplots(2, 1, sharex=True, height_ratios=[2, 2], figsize=figsize)
        if xvar=='means':
            ax[0].scatter(means, stds)
            ax[0].set_xlabel('Mean amplitude')
            ax[1].scatter(means, rel_std)
            ax[1].set_xlabel('Mean amplitude')
        else:
            ax[0].scatter(init_amps, stds)
            ax[0].set_xlabel('Init amplitude')
            ax[1].scatter(init_amps, rel_std)
            ax[1].set_xlabel('Init amplitude')

            #labels by init amps
        ax[0].set_ylabel('Standard deviation vs mean')
        ax[1].set_ylabel('Relative standard deviation vs mean')
    return stds,means,rel_std


##############

def quick_routine( n_turns = 1000,n_part = 1,monofreq=True,volt=0,tune_factor=None,targetx=6.32,max_amp= 4e-3,return_all=False):
   if tune_factor is None:
       tune_factor = targetx-6
   if targetx==6.32:
        # To give the standard value already calculated for this value, avoiding to match again
        targetx = None

   lined = line_setup.build_line_baremachine()
   outdict = dict(line=lined['line'], twiss=lined['line'].twiss(method='4d'))
   bms.matching(outdict,targetx=targetx)

   # Monitor
   monitor = xa.insert_monitor(lined['line'], 'pe.smh57', n_turns=n_turns, n_part=n_part)
   slwex.insert_rfko_custom(lined['line'], tune_factor=tune_factor, volt=volt, n_turns=n_turns, monofreq=monofreq)
   outdict['params'] = dict(n_turns=n_turns, n_part=n_part)
   # Generate particles in a range of amplitudes
   A0 = np.linspace(0,max_amp, n_part)
   particles = xa.build_part(lined['line'], A0)
   # particles = bms.build_particles2(lined['line'],n_part=n_part,DPP_FACTOR=0)
   outdict['particles'] = particles
   outdict['monitor'] = monitor
   outdict['params']['volt'] = volt  # for the amplitude growth funcition
   # Just for using fu2.plot_flex
   outdict['params']['SEPTA_X_MM'] = -75 # JUST FOR PLOTTING, THERE's NO SEPTA
   xh.tracking(outdict)
   ### Calculate the amplitudes
   amp = amplitude_growth(outdict, n_parts=n_part, return_amp=True, plot=False)
   ## statistics for the amplitudes
   print('--> basic statistics for the amplitude')
   stds,means,rel_std= amps_stats(amp, plot=True)

   if return_all:
       return dict(outdict=outdict,stats=dict(stds=stds,means=means,rel_std=rel_std))






def amplitude_growth_(outdict, n_parts=3, figsize=(10, 8), return_amp=False, exclude_extr=False):
    '''
    '''

    # I try the normalizing funciton
    monitor = utility.Normalize_monitor(outdict, keep_zeroes=True, normalize_particles=False)
    ids = np.random.randint(len(monitor.x[:, 0]), size=n_parts)
    twiss = outdict['twiss']
    amps = []
    if exclude_extr:
        idnz = []
        for n in range(monitor.x.shape[0]):
            if 0 in monitor.x[n, :]:
                dx_ = np.where(monitor[n,:]==0)[0][0]
            else:
                dx_= None
            amps.append(np.sqrt(monitor.x[n,:dx_]**2+monitor.px[n,:dx_]**2))
        #ids = np.random.choice(np.arange(len(idnz)), size=n_parts)

    #amps = np.sqrt(monitor.x[ids, :idnz] ** 2 + monitor.px[ids, :] ** 2)

    freq = 1 / twiss.T_rev0 - twiss.slip_factor * monitor.delta[
        :, 0] * 1 / twiss.T_rev0  # it doesn't change on a turn basis
    tune = twiss.qx + twiss.dqx * monitor.delta[ids, 0]

    plt.figure(figsize=figsize)
    for i in range(n_parts):
        mean_amp = np.mean(amps[i, :])
        plt.plot(amps[i, :], label=f'mean amplitude = {round(mean_amp, 6)}', alpha=0.5)
        # plt.plot(amps[i,:],label=f'tune = {round(tune[i],4)}')
    plt.title(f"Amplitudes per turn with Gain = {outdict['params']['volt']}")
    plt.xlabel('Turns')
    plt.legend()
    if return_amp:
        return amps
