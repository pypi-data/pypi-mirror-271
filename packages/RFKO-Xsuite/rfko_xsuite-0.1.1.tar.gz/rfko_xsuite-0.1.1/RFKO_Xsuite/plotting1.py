
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import os


from .utility import replace_extracted_val
from . import slowex_helper as slwex
from . import xsuite_helper as xh
from .Rfko import Rfko

#######################
##########         STATIC PLOT FUNCTIONS
def plot_extracted(out_dict, figsize=(10, 8), rf_plot=True,beam_loss=False,all_particles_ref=False):

    if isinstance(out_dict, Rfko):
        out_dict = out_dict.to_dict()

    particles = out_dict['particles']
    particles_lost = np.bincount(particles.at_turn)
    if rf_plot:
        #adding the option for the non linear chirp
        fig, ax = plt.subplots(2, 1, sharex=True, height_ratios=[6, 2], figsize=figsize)
        if beam_loss:
            ax[0].plot(np.arange(len(particles_lost) - 1),len(particles.x)- np.cumsum(particles_lost[:-1]))
            if all_particles_ref:
                ax[0].axhline(0, linestyle='--', alpha=0.5)
        else:
            ax[0].plot(np.arange(len(particles_lost) - 1), np.cumsum(particles_lost[:-1]))
        _plot_signal(out_dict, ax=ax[1])
        fig.suptitle('Particle extraction vs rf signal')
        fig.supxlabel('Turns')
        ax[0].set_ylabel('Extracted particles')
        ax[1].set_ylabel('Frequencies')
    else:
        plt.figure(figsize=figsize)
        if beam_loss:
            plt.plot(np.arange(len(particles_lost) - 1), len(particles.x) -np.cumsum(particles_lost[:-1]))

        else:
            plt.plot(np.arange(len(particles_lost) - 1),np.cumsum(particles_lost[:-1]))
        if all_particles_ref:
            plt.axhline(0,linestyle='--',alpha=0.5)
    return None

def plot_flex(out_dict, figsize=(12, 8), filename=None,message='',n_part='all', turn_range=None,s=2,particles_id=None):
    ''' DEFECT : I can't find a straigth forward way to include the limit of the number of particles also for the extracted
    this is related to the fact that there is not a correspondece from the particles object that store the last turn
     to the monitor that records them'''
    if isinstance(out_dict,Rfko):
        out_dict=out_dict.to_dict()


    monitor = out_dict['monitor']
    particles = out_dict['particles']
    if (n_part=='all')&(particles_id is None):
        ids = [x for x in range(out_dict['params']['n_part'])]
    elif particles_id is None:
        ids = np.random.randint(0,out_dict['params']['n_part'],n_part)
    else:
        ids = [x for x in monitor.particle_id[:,0] if x in particles_id ]
      #Similar version with Boolen indexing ------>
        # Tese are EQUIVALENT ONLY if the particles_id in the monitor are always SORTED
        #ids = np.isin(monitor.particle_id[:,0],particles_id)
    if turn_range is not None:
        try:
            #if turn range is only a number it's considered the maximum turn number to plot
            len(turn_range)
        except:
            turn_range = [turn_range]
        if len(turn_range) == 2:
            x = monitor.x[ids, turn_range[0]:turn_range[1]]
            px = monitor.px[ids, turn_range[0]:turn_range[1]]
            x_extr = particles.x
            px_extr = particles.px
            mask_extr = (particles.state == 0) & (particles.at_turn < turn_range[1]) & (
                        particles.at_turn >= turn_range[0])
        else:
            x = monitor.x[ids, :turn_range[0]]
            px = monitor.px[ids, :turn_range[0]]
            mask_extr = (particles.state == 0) & (particles.at_turn < turn_range[0])
            x_extr = particles.x
            px_extr = particles.px

    else:
        x = monitor.x[ids,:]
        px = monitor.px[ids,:]
        x_extr = particles.x
        px_extr = particles.px
        mask_extr = particles.state == 0
    if out_dict['params']['SEPTA_X_MM'] is not None:
        septa = out_dict['params']['SEPTA_X_MM']

    mask_mon = x != 0
    # fig,ax = plt.subplots(figsize=figsize)
    plt.figure(figsize=figsize)
    if turn_range is not None:
        color_array = np.arange(len(x[0, :])) + 1
    else:
        color_array = np.arange(out_dict['params'][
                                    'n_turns']) + 1  # to adjust the scales of particles color to be (1,n_turns)

    colors = np.tile(color_array, (len(ids), 1))  # Fix dimensions
    

    #### SET axes LIMITS
    axmargin = 0.05
    if out_dict['params']['SEPTA_X_MM'] is not None:
        xmin = np.min(np.concatenate((x_extr[mask_extr].flatten(),x[mask_mon],[septa / 1000])))
        xmax = np.max(np.concatenate((x_extr[mask_extr].flatten(),x[mask_mon],[septa / 1000])))
    else:
        xmin = np.min(np.concatenate((x_extr[mask_extr].flatten(), x[mask_mon])))
        xmax = np.max(np.concatenate((x_extr[mask_extr].flatten(), x[mask_mon])))

    ymin = np.min(np.concatenate((px_extr[mask_extr].flatten(),px[mask_mon])))
    ymax = np.max(np.concatenate((px_extr[mask_extr].flatten(),px[mask_mon])))
    plt.xlim(xmin - np.abs(xmin - xmax) *axmargin, xmax + np.abs(xmax-xmin) * axmargin)
    plt.ylim(ymin - np.abs(ymin - ymax) * axmargin, ymax + np.abs(ymax - ymin) * axmargin)

    #PLOT
    plt.scatter(x_extr[mask_extr], px_extr[mask_extr], c=particles.at_turn[mask_extr], marker='P', alpha=0.5,s=s)
    plt.scatter(x[mask_mon], px[mask_mon], c=colors[mask_mon], alpha=0.5,s=s)
    plt.colorbar(label='Turns')
    #### SEPTA PLOT
    if out_dict['params']['SEPTA_X_MM'] is not None:
        plt.axvline(septa / 1000, c="r", linestyle="--")
    if filename is not None:
        plt.savefig(filename+message)
    return None




def stein_static(out_dict, at_turn, rmv_disp=False):
    ''' Create a steinbach diagram at a specific turn'''
    if isinstance(out_dict, Rfko):
        out_dict = out_dict.to_dict()

    twiss = out_dict['twiss']
    line = out_dict['line']
    monitor = out_dict['monitor']
    print('Bakup')
    if hasattr(monitor,'placed_at_element'):
        at_element=monitor.placed_at_element
    else:
        at_element = 'pe.smh57'
    ### PROVO A CREARE UN DIAGRAMMA DI STEINBACH
    S_virtual, S_mu = slwex.Virtual_sextupole_complete(out_dict)
    ######## I have to remove the closed orbit to calculate the amplitudes
    xcopy, pxcopy, delta_all = replace_extracted_val(monitor, delta=True,
                                                     turn=at_turn)  ### processed to place the last measured position on each extracted particle
    # REMOVE CLOSED ORBIT
    x = xcopy[:, at_turn] - twiss.x[twiss.name==at_element]
    px = pxcopy[:, at_turn] - twiss.px[twiss.name==at_element]
    deltas = delta_all[:, at_turn]


    # DISTORTION CORR
    argmin = np.argmin(np.abs(twiss.mux * 2 * np.pi - S_mu))
    Xo = twiss.x[argmin] / np.sqrt(twiss.betx[argmin])
    # there should be the correction from the closed orbit
    Qx_real = twiss.qx - twiss.dqx * deltas - S_virtual*Xo/(2*np.pi)

    # to see it with removed dispersion
    if np.sum(deltas != 0):
        x = x - twiss.dx[twiss.name==at_element] * deltas
        px = px - twiss.dpx[twiss.name==at_element] * deltas

    # parameters for normalization
    betx_monitor = twiss.betx[twiss.name == at_element]
    alfx_monitor = twiss.alfx[twiss.name == at_element]
    Xn = x / np.sqrt(betx_monitor)
    Xpn = (alfx_monitor / np.sqrt(betx_monitor)) * x + np.sqrt(betx_monitor) * px

    amplitude_n = np.sqrt(Xn ** 2 + Xpn ** 2)

    ############# ADDING color for the visualization of the extracted particles
    extracted_mask = monitor.x[:, at_turn] == 0


    dQ = np.linspace(0, 0.06, 500)
    Ax = np.sqrt(48 * np.sqrt(3) * np.pi) * dQ / S_virtual

    plt.figure(figsize=(13, 8))
    plt.scatter(Qx_real, amplitude_n, s=1, c=extracted_mask)
    plt.scatter(dQ + 6 + 1 / 3, Ax, c='r', s=3)
    plt.scatter(6 + 1 / 3 - dQ, Ax, c='r', s=3)
    # plt.savefig(f'fig_wes/Steinbach_Sept_sept{SEPTA_X_MM}_dpp{DPP_FACTOR}_emitx{exn}_Gain{volt}_RF{rf10MHz_enable}')


##############
#        ANIMATIONS
#############

# SISTEMARE EFFETTO, DISPERSIONE, SUL TUNE DELLE PARTICELLE ESTRATTE E SISTEMARE LA NECESSITà DEL FILENAME

def anim_steinbach_(out_dict, filename=None,message='', step=5, SEPTA=None):
    if isinstance(out_dict, Rfko):
        out_dict = out_dict.to_dict()

    # TO SE THE CORRECTION OF TUNE DUE TO DISTORTION
    particles = out_dict['particles']
    monitor = out_dict['monitor']
    twiss = out_dict['twiss']
    #line_df = out_dict['line'].to_pandas()
    data = {
        'at_turn': particles.at_turn,
        'x': particles.x,
        'px': particles.px,
        'delta': particles.delta,
    }
    df = pd.DataFrame(data)
    # extracting the dataframe form, easier to work with
    twiss_df = twiss.to_pandas()
    # Virtual sextupole
    S_virtual, _ = slwex.Virtual_sextupole_complete(out_dict)
    # Resonance line plot
    dQ = np.linspace(0, 0.06, 500) #
    if S_virtual != 0:
        Ax = np.sqrt(48 * np.sqrt(3) * np.pi) * dQ / S_virtual
    else:
        Ax = np.zeros(dQ.shape)

    n_turns = out_dict['params']['n_turns']
    #### figurw init
    fig, ax = plt.subplots(figsize=(12, 8))
    scat = ax.scatter([], [], s=1)

    # Calculating beta and alf for being able to normalize
    betx_monitor = twiss_df[twiss_df['name'] == 'pe.smh57'].betx.iloc[0]
    alfx_monitor = twiss_df[twiss_df['name'] == 'pe.smh57'].alfx.iloc[0]

    xcopy = monitor.x
    pxcopy = monitor.px
    deltas_corr = monitor.delta
    

    def update(frame):
        # a frame is a turn
        at_turn = frame
        if frame%50==0:
            print(f'frame {frame}')
        ax.clear()
        # PLOT RESONANCE LINE
        ax.plot(dQ + 6 + 1 / 3, Ax, c='r')
        ax.plot(6 + 1 / 3 - dQ, Ax, c='r')

        # extracted particles
        extracted_mask = monitor.x[:, at_turn] == 0
        x_extr = df[df['at_turn'] <= at_turn]['x']
        px_extr = df[df['at_turn'] <= at_turn]['px']
        deltas_extr = df[df['at_turn']<=at_turn]['delta']
        # x,px are values at_turn=frame
        # REMOVE CLOSED ORBIT
        x = xcopy[np.logical_not(extracted_mask), at_turn] - twiss_df[twiss_df['name'] == 'pe.smh57'].x.iloc[0]
        px = pxcopy[np.logical_not(extracted_mask), at_turn] - twiss_df[twiss_df['name'] == 'pe.smh57'].px.iloc[0]
        x_extr = x_extr - twiss_df[twiss_df['name'] == 'pe.smh57'].x.iloc[0]
        px_extr = px_extr - twiss_df[twiss_df['name'] == 'pe.smh57'].px.iloc[0]

        # CORRECTION OF THE DISPERSIONAL EFFECTS||
        if np.sum(monitor.delta.flatten()) != 0:
            x = x - twiss_df[twiss_df['name'] == 'pe.smh57'].dx.iloc[0] * deltas_corr[np.logical_not(extracted_mask), at_turn]
            px = px - twiss_df[twiss_df['name'] == 'pe.smh57'].dpx.iloc[0] * deltas_corr[np.logical_not(extracted_mask), at_turn]
            x_extr = x_extr - twiss_df[twiss_df['name'] == 'pe.smh57'].dx.iloc[0] * deltas_extr
            px_extr = px_extr - twiss_df[twiss_df['name'] == 'pe.smh57'].dpx.iloc[0] * deltas_extr
        # NORMALIZE
        Xn = x / np.sqrt(betx_monitor)
        Xpn = (alfx_monitor / np.sqrt(betx_monitor)) * x + np.sqrt(betx_monitor) * px
        X_extr = x_extr / np.sqrt(betx_monitor)
        Px_extr = x_extr * alfx_monitor / np.sqrt(betx_monitor) + px_extr * np.sqrt(betx_monitor)
        # AMPLITUDE
        amplitude_n = np.sqrt(Xn ** 2 + Xpn ** 2)
        amplitude_extr = np.sqrt(X_extr ** 2 + Px_extr ** 2)

        # TUNE--- no distortion correction because it causes problems--->> as the commented block
        Qx_real = twiss.qx + twiss.dqx * deltas_corr[np.logical_not(extracted_mask), at_turn]

        # Qx_real = twiss.qx - twiss.dqx * deltas_corr[np.logical_not(extracted_mask), at_turn] - \
        #         twiss_df[twiss_df['name'] == 'pe.smh57'].x.iloc[
        #            0] * S_virtual / (4 * np.pi * np.sqrt(betx_monitor))

        ## LIMS
        axs_margins = 0.1
        xmin = np.min(np.concatenate((Qx_real,6+1/3-dQ[0])))
        xmax = np.max(np.concatenate( (Qx_real,6+1/3+dQ[-1]) ))
        ymin = np.min(np.concatenate((amplitude_extr,amplitude_n,Ax)) )
        ymax = np.max(np.concatenate((amplitude_extr,amplitude_n,Ax)) )
        ax.set_xlim(xmin-(xmax-xmin)*axs_margins,xmax+(xmax-xmin)*axs_margins)
        ax.set_ylim(ymin -(ymax-ymin)*axs_margins,ymax+(ymax-ymin)*axs_margins)
        Qx_extr = twiss.qx + twiss.dqx * deltas_extr
        ax.set_title(f'Steinbach turn :{frame}/{n_turns}')
        ax.set_xlabel('Amplitude')
        ax.set_ylabel('Tune')
        ax.scatter(Qx_real, amplitude_n, s=1, c='b')
        ax.scatter(Qx_extr, amplitude_extr, s=1, c='g')



        return scat,

    ani = FuncAnimation(fig, update, frames=range(0, n_turns, step), blit=True)
    if filename is None:
        filename = f'part{out_dict["params"]["n_part"]}_DPP{out_dict["params"]["DPP_FACTOR"]}_Volt{out_dict["params"]["volt"]}'

    # plt.show()
    if os.path.isdir('./gif_wes'):
        ani.save(f'./gif_wes/steinbach_{message}_{filename}.gif', dpi=200)
    else:
        ani.save(f'./steinbach_{message}_{filename}.gif', dpi=200)


def anim_steinbach(out_dict, filename=None, message='', step=5, SEPTA=None):
    if isinstance(out_dict, Rfko):
        out_dict = out_dict.to_dict()

    ######
    ######### CREATING SOME VARIABLES
    particles = out_dict['particles']
    monitor = out_dict['monitor']
    twiss = out_dict['twiss']
    # extracting the dataframe form, easier to work with
    twiss_df = twiss.to_pandas()
    n_turns = out_dict['params']['n_turns']

    data = {
        'at_turn': particles.at_turn,
        'x': particles.x,
        'px': particles.px,
        'delta': particles.delta,
    }
    df = pd.DataFrame(data)

    # CALCULATION OF Virtual sextupole
    S_virtual, S_mu = slwex.Virtual_sextupole_complete(out_dict)

    # Resonance line plot
    dQ = np.linspace(0, 0.06, 500)  #
    if S_virtual != 0:
        Ax = np.sqrt(48 * np.sqrt(3) * np.pi) * dQ / S_virtual
    else:
        Ax = np.zeros(dQ.shape)

    #### figure init
    fig, ax = plt.subplots(figsize=(12, 8))
    scat = ax.scatter([], [], s=1)

    # Calculating beta and alf for being able to normalize
    betx_monitor = twiss_df[twiss_df['name'] == 'pe.smh57'].betx.iloc[0]
    alfx_monitor = twiss_df[twiss_df['name'] == 'pe.smh57'].alfx.iloc[0]

    xcopy = monitor.x
    pxcopy = monitor.px
    deltas_corr = monitor.delta

    def update(frame):
        # a frame is a turn
        at_turn = frame
        if frame % 50 == 0:
            print(f'frame {frame}')
        ax.clear()
        # PLOT RESONANCE LINE
        ax.plot(dQ + 6 + 1 / 3, Ax, c='r')
        ax.plot(6 + 1 / 3 - dQ, Ax, c='r')

        # mask extracted particles of the monitor --> 0 coordinates
        extracted_mask = monitor.x[:, at_turn] == 0
        # extracted particles position AT TURN, they retain the coordinates
        x_extr = df[df['at_turn'] <= at_turn]['x']
        px_extr = df[df['at_turn'] <= at_turn]['px']
        deltas_extr = df[df['at_turn'] <= at_turn]['delta']
       

        # coordinate at turn + REMOVE CLOSED ORBIT
        x = xcopy[np.logical_not(extracted_mask), at_turn] - twiss_df[twiss_df['name'] == 'pe.smh57'].x.iloc[0]
        px = pxcopy[np.logical_not(extracted_mask), at_turn] - twiss_df[twiss_df['name'] == 'pe.smh57'].px.iloc[0]
        x_extr = x_extr - twiss_df[twiss_df['name'] == 'pe.smh57'].x.iloc[0]
        px_extr = px_extr - twiss_df[twiss_df['name'] == 'pe.smh57'].px.iloc[0]

        # REMOVE THE DISPERSION EFFECT||
        if np.sum(monitor.delta.flatten()) != 0:
            x = x - twiss_df[twiss_df['name'] == 'pe.smh57'].dx.iloc[0] * deltas_corr[
                np.logical_not(extracted_mask), at_turn]
            px = px - twiss_df[twiss_df['name'] == 'pe.smh57'].dpx.iloc[0] * deltas_corr[
                np.logical_not(extracted_mask), at_turn]
            x_extr = x_extr - twiss_df[twiss_df['name'] == 'pe.smh57'].dx.iloc[0] * deltas_extr
            px_extr = px_extr - twiss_df[twiss_df['name'] == 'pe.smh57'].dpx.iloc[0] * deltas_extr

        # NORMALIZE
        Xn = x / np.sqrt(betx_monitor)
        Xpn = (alfx_monitor / np.sqrt(betx_monitor)) * x + np.sqrt(betx_monitor) * px
        X_extr = x_extr / np.sqrt(betx_monitor)
        Px_extr = x_extr * alfx_monitor / np.sqrt(betx_monitor) + px_extr * np.sqrt(betx_monitor)
        # AMPLITUDE
        amplitude_n = np.sqrt(Xn ** 2 + Xpn ** 2)
        amplitude_extr = np.sqrt(X_extr ** 2 + Px_extr ** 2)

        # TUNE CORRECTIONS commented block
        Xco = twiss_df.x[np.argmin(np.abs(twiss_df.mux * 2 * np.pi - S_mu))] / np.sqrt(betx_monitor)
        Qx_real = twiss.qx + twiss.dqx * deltas_corr[np.logical_not(extracted_mask), at_turn] - S_virtual * Xco / (
                    np.pi * 2)
        Qx_extr = twiss.qx + twiss.dqx * deltas_extr - S_virtual * Xco / (np.pi * 2)
        ## LIMS

        ax.set_xlim(6.25, 6.4)
        # ax.set_ylim()

        ax.set_title(f'Steinbach turn :{frame}/{n_turns}')
        ax.set_xlabel('Amplitude')
        ax.set_ylabel('Tune')
        ax.scatter(Qx_real, amplitude_n, s=1, c='b')
        ax.scatter(Qx_extr, amplitude_extr, s=1, c='g')

        return scat,

    ani = FuncAnimation(fig, update, frames=range(0, n_turns, step), blit=True)
    if filename is None:
        filename = f'part{out_dict["params"]["n_part"]}_DPP{out_dict["params"]["DPP_FACTOR"]}_Volt{out_dict["params"]["volt"]}'

    # plt.show()
    if os.path.isdir('./gif_wes'):
        ani.save(f'./gif_wes/steinbach_{message}_{filename}.gif', dpi=200)
    else:
        ani.save(f'./steinbach_{message}_{filename}.gif', dpi=200)


def anim_steinbach2(out_dict, filename=None, message='', step=5, SEPTA=None):
    ''' Attempt to fo it better, and to have also the adaptive limits for the plot'''
    if isinstance(out_dict, Rfko):
        out_dict = out_dict.to_dict()

    # TO SE THE CORRECTION OF TUNE DUE TO DISTORTION
    particles = out_dict['particles']
    monitor = out_dict['monitor']
    twiss = out_dict['twiss']
    # line_df = out_dict['line'].to_pandas()
    data = {
        'at_turn': particles.at_turn,
        'x': particles.x,
        'px': particles.px,
        'delta': particles.delta,
    }
    df = pd.DataFrame(data)
    # extracting the dataframe form, easier to work with
    twiss_df = twiss.to_pandas()
    # FIXED PLOT
    # Virtual sextupole
    S_virtual, _ = slwex.Virtual_sextupole_complete(out_dict)
    # Resonance line
    dQ = np.linspace(0, 0.06, 500)
    if S_virtual != 0:
        Ax = np.sqrt(48 * np.sqrt(3) * np.pi) * dQ / S_virtual
    else:
        Ax = np.zeros(dQ.shape)

    n_turns = out_dict['params']['n_turns']
    #### figurw init
    fig, ax = plt.subplots(figsize=(12, 8))
    scat = ax.scatter([], [], s=1)

    # Calculating beta and alf for being able to normalize
    betx_monitor = twiss_df[twiss_df['name'] == 'pe.smh57'].betx.iloc[0]
    alfx_monitor = twiss_df[twiss_df['name'] == 'pe.smh57'].alfx.iloc[0]


    xcopy = monitor.x
    pxcopy = monitor.px
    deltas_corr = monitor.delta
    X,PX,X_p,PX_p = xh.Normalize_monitor(out_dict,normalize_particles=True)




    def update(frame):
        # a frame is a turn
        at_turn = frame
        if frame % 50 == 0:
            print(f'frame {frame}')
        ax.clear()
        # PLOT RESONANCE LINE
        ax.plot(dQ + 6 + 1 / 3, Ax, c='r')
        ax.plot(6 + 1 / 3 - dQ, Ax, c='r')

        # extracted particles
        extracted_mask = monitor.x[:, at_turn] == 0
        print(df['at_turn'] <= at_turn)
        X_extr = X_p[df['at_turn'] <= at_turn]
        PX_extr = PX_p[df['at_turn'] <= at_turn]
        deltas_extr = df[df['at_turn'] <= at_turn]['delta']

        X_turn = X[:,at_turn]
        PX_turn = PX[:,at_turn]


        # CORRECTION OF THE DISPERSIONAL EFFECTS||
        if np.sum(monitor.delta.flatten()) != 0:
            corrx = (monitor.delta[:,at_turn]*twiss_df[twiss_df.name=='pe.smh57'].dx)/np.sqrt(betx_monitor)
            corrpx = monitor.delta[:,at_turn]*twiss_df[twiss_df.name=='pe.smh57'].dpx*np.sqrt(betx_monitor)
            X_turn -= corrx
            PX_turn-= corrx*alfx_monitor+corrpx
            X_extr -= corrx
            PX_extr -= corrx*alfx_monitor+corrpx



        # AMPLITUDE
        amplitude_n = np.sqrt(X_turn ** 2 + PX_turn ** 2)
        amplitude_extr = np.sqrt(X_extr ** 2 + PX_extr ** 2)

        # TUNE--- no distortion correction because it causes problems--->> as the commented block
        Qx_real = twiss.qx + twiss.dqx * deltas_corr[np.logical_not(extracted_mask), at_turn]

        # Qx_real = twiss.qx - twiss.dqx * deltas_corr[np.logical_not(extracted_mask), at_turn] - \
        #         twiss_df[twiss_df['name'] == 'pe.smh57'].x.iloc[
        #            0] * S_virtual / (4 * np.pi * np.sqrt(betx_monitor))

        ## LIMS
        axs_margins = 0.1
        xmin = np.min(np.concatenate((Qx_real, 6 + 1 / 3 - dQ[0])))
        xmax = np.max(np.concatenate((Qx_real, 6 + 1 / 3 + dQ[-1])))
        ymin = np.min(np.concatenate((np.sqrt(X_extr ** 2 + PX_extr ** 2).flatten(), np.sqrt((X-corrx) ** 2 + (PX-corrx*alfx_monitor+corrpx) ** 2), Ax)))
        ymax = np.max(np.concatenate((np.sqrt(X_extr ** 2 + PX_extr ** 2).flatten(), np.sqrt((X-corrx) ** 2 + (PX-corrx*alfx_monitor+corrpx) ** 2), Ax)))
        ax.set_xlim(xmin - (xmax - xmin) * axs_margins, xmax + (xmax - xmin) * axs_margins)
        ax.set_ylim(ymin - (ymax - ymin) * axs_margins, ymax + (ymax - ymin) * axs_margins)
        Qx_extr = twiss.qx + twiss.dqx * deltas_extr
        ax.set_title(f'Steinbach turn :{frame}/{n_turns}')
        ax.set_xlabel('Amplitude')
        ax.set_ylabel('Tune')
        ax.scatter(Qx_real, amplitude_n, s=1, c='b')
        ax.scatter(Qx_extr, amplitude_extr, s=1, c='g')

        return scat,

    ani = FuncAnimation(fig, update, frames=range(0, n_turns, step), blit=True)
    if filename is None:
        filename = f'part{out_dict["params"]["n_part"]}_DPP{out_dict["params"]["DPP_FACTOR"]}_Volt{out_dict["params"]["volt"]}'

    # plt.show()
    if os.path.isdir('./gif_wes'):
        ani.save(f'./gif_wes/steinbach_{message}_{filename}.gif', dpi=200)
    else:
        ani.save(f'./steinbach_{message}_{filename}.gif', dpi=200)


def anim_ph_space(out_dict, filename=None,message='', dispersion=False, step=5):
    '''  MAKE ANIMATION OF THE PHASE SPACE AT SEPTA NON-NORMALIZED,
    if dispersion == True it also plots the phase space shifted for the dispersional effect
    '''
    if isinstance(out_dict, Rfko):
        out_dict = out_dict.to_dict()

    particles = out_dict['particles']
    monitor = out_dict['monitor']
    SEPTA_X_MM = out_dict['params']['SEPTA_X_MM'] 

    # UTILE PER EVITARE GROSSI BUG CREDO
    data = {
        'at_turn': particles.at_turn,
        'x': particles.x,
        'px': particles.px,
        'delta': particles.delta,
    }
    n_turns = out_dict['params']['n_turns']
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(8, 6))
    scat = ax.scatter([], [], s=2)

    def update(frame):
        # a frame is a turn
        at_turn = frame
        if frame%50==0:
            print(f'frame {frame}')
        ax.clear()
        # position of EXTRACTED particles
        x_extr = df[df['at_turn'] <= at_turn]['x']  #
        px_extr = df[df['at_turn'] <= at_turn]['px']  #
        delta_extr = df[df['at_turn']<=at_turn]['delta']
        mask = monitor.x[:, at_turn] != 0  # mask on the monitor array, for the extracted particles (at_turn)
        ## particles position
        x_pres = monitor.x[mask, at_turn]
        px_pres = monitor.px[mask, at_turn]

        # TOLGO LA DISPERSIONE
        if dispersion:
            twiss_df = out_dict['line'].twiss(method='4d').to_pandas()
            x_pres_nodisp = x_pres - monitor.delta[mask, at_turn] * twiss_df[twiss_df.name == 'pe.smh57'].dx.iloc[0]
            px_pres_nodisp = px_pres - monitor.delta[mask, at_turn] * twiss_df[twiss_df.name == 'pe.smh57'].dpx.iloc[0]
            x_extr_nodisp = x_extr-delta_extr * twiss_df[twiss_df.name == 'pe.smh57'].dx.iloc[0]
            px_extr_nodisp = px_extr-delta_extr * twiss_df[twiss_df.name == 'pe.smh57'].dpx.iloc[0]
        ax.text(0.1, 0.9, f'{len(x_extr)} extracted', transform=ax.transAxes)
        ax.set_title(f'Phase space turn :{frame}/{n_turns}')
        ax.set_xlabel('x')
        ax.set_ylabel('px')
        axmargin = 0.05
        if SEPTA_X_MM is not None:
            ax.axvline(SEPTA_X_MM / 1000, c="r", linestyle="--")

        # XAXES LIMITS
        if SEPTA_X_MM is not None: # NOT GENERAL TO SET ONLY THE MINIMUM RESPECTIVE TO THE SEPTA
            xmin = np.min(np.concatenate((monitor.x.flatten(), np.array([SEPTA_X_MM / 1000]),particles.x.flatten())))
            xmax = np.max(np.concatenate((monitor.x.flatten(), np.array([SEPTA_X_MM / 1000]),particles.x.flatten())))
        else:
            xmin = np.min(monitor.x.flatten())
            xmax = np.max(monitor.x.flatten())
        ax.set_xlim(xmin - np.abs(xmin - xmax) *axmargin, xmax + np.abs(xmax-xmin) * axmargin)
        # YLIMITS
        ymin = np.min(monitor.px.flatten())
        ymax = np.max(monitor.px.flatten())
        ax.set_ylim(ymin - np.abs(ymin-ymax) * axmargin, ymax + np.abs(ymax-ymin) * axmargin)

        ax.scatter(x_extr, px_extr, c='g', s=2)
        ax.scatter(x_pres, px_pres, c='b', s=2, label='dispersion')
        if dispersion:
            ax.scatter(x_pres_nodisp, px_pres_nodisp, c='r', s=1, alpha=0.5, label='no_dispersion')
            ax.scatter(x_extr_nodisp,px_extr_nodisp,c='c',s=1,alpha=0.5)
            ax.legend(loc='lower left')

        return scat,

    ani = FuncAnimation(fig, update, frames=range(0, n_turns, step), blit=True)
    if filename is None:
        try:
            filename = f'n_part{out_dict["params"]["n_part"]}_QXtarget{out_dict["params"]["QX_TARGET"]}_Volt{out_dict["params"]["volt"]}_duration{out_dict["params"]["duration"]}'
        except:
            filename = f'n_part{out_dict["params"]["n_part"]}_QXtarget{out_dict["twiss"].qx}_Volt{out_dict["params"]["volt"]}_duration{out_dict["params"]["duration"]}'

    if os.path.isdir('./gif_wes'):
        ani.save(f'./gif_wes/ph_space_{message}_{filename}.gif', dpi=200)
    else:
        ani.save(f'./gif_wes/ph_space_{message}_{filename}.gif', dpi=200)

    return None

def plot_kick(rfko,particles_id=None):
    '''prototype'''
    kicks = rfko.kick_monitors[0].px - rfko.kick_monitors[1].px
    if particles_id is None:
        plt.plot(kicks)
        plt.xlabel('turns')
        plt.ylabel('Kick')
        plt.title('Kick vs Particle ID')
        plt.show()
    else:
        plt.plot(kicks[particles_id,:])
        plt.xlabel('turns')
        plt.ylabel('Kick')
        plt.title('Kick turns')
        plt.show()

def _plot_signal(out_dict, ax=None):
    # it works, it has to be improved, but it ok
    ### for now I don't care the sampling frequency, it doesn need to be representative in this respect
    f_rev = 1 / out_dict['twiss'].T_rev0  # better than using the one saved in the params, cause maybe the twiss is more updated
    f_start = out_dict['params']['freq_start_ratio'] * f_rev
    f_stop = out_dict['params']['freq_end_ratio'] * f_rev
    n_turn = out_dict['params']['n_turns']
    if out_dict['params']['chirp_type']=='linear':
        sim_time = n_turn / f_rev
        duration = out_dict['params']['duration']
        rep_time = sim_time / duration
        signal_f = np.tile(np.linspace(f_start, f_stop, 1000), round(rep_time))  # UN IDEA PER RIPETERE I LSEGNALE
        turns = np.linspace(0, n_turn, len(signal_f))
        if ax is None:
            plt.plot(turns, signal_f)
        else:
            ax.plot(turns, signal_f)
    else:
        sim_time = n_turn / f_rev
        duration = out_dict['params']['duration']
        rep_time = sim_time / duration
        signal_nonlin = np.concatenate((np.linspace(f_start, f_stop, 500),np.zeros(500)))
        signal_f = np.tile(signal_nonlin, round(rep_time))  # UN IDEA PER RIPETERE I LSEGNALE
        turns = np.linspace(0, n_turn, len(signal_f))
        if ax is None:
            plt.plot(turns, signal_f)
        else:
            ax.plot(turns, signal_f)


        return None
