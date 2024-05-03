

########### COULD WORK ALSO WITHOUT THESE??
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

from matplotlib.cm import ScalarMappable

from .utility import replace_null

from .slowex_helper import Virtual_sextupole_complete
from .xsuite_helper import Normalize_monitor

import inspect

#######################
##########         STATIC PLOT FUNCTIONS
########################


def stable_tri_plot(dq, S=77, figsize=(12, 8), dmu=None, linewidth=3, translation_vector=None,c='r',**args):
    ''' dmu : defines the rotation angle, which for positive values correspond to a clock-wise rotation
    '''
    eps = 6 * np.pi * dq
    # crossing points
    ABx = - 2 / 3 * eps / S
    ABpx = -eps * 2 / (S * np.sqrt(3))
    ACx = - 2 / 3 * eps / S
    ACpx = eps * 2 / (S * np.sqrt(3))
    CBx = (4 / 3) * eps / S
    CBpx = 0

    #more_params = args
    #plot_params = [arg for arg in args if arg in inspect.getfullargspec(plt.plot).args]
    plot_args = {key:val for key,val in args.items() if key in inspect.getfullargspec(plt.plot).args}
    # print(f'eps = {eps}   AB = {ABx},{ABpx}  AC = {ACx},{ACpx}, CB = {CBx},{CBpx}')
    if dmu is not None: # Here there is a bug ost likely because the rotations becomes distorted
        dmu = dmu % (2 * np.pi)
        # dmu must be in rads
        rotation_matrix = np.array([[np.cos(dmu), np.sin(dmu)], [-np.sin(dmu), np.cos(dmu)]])
        ABx_r = rotation_matrix.dot(np.array([ABx, ABpx]))[0]
        ABpx_r = rotation_matrix.dot(np.array([ABx, ABpx]))[1]
        ACx_r = rotation_matrix.dot(np.array([ACx, ACpx]))[0]
        ACpx_r = rotation_matrix.dot(np.array([ACx, ACpx]))[1]
        CBx_r = rotation_matrix.dot(np.array([CBx, CBpx]))[0]
        CBpx_r = rotation_matrix.dot(np.array([CBx, CBpx]))[1]

    if translation_vector is not None:  # POCO TESTATO
        if dmu is not None:
            ABx_r += translation_vector[0]
            ACx_r += translation_vector[0]
            CBx_r += translation_vector[0]

            ABpx_r += translation_vector[1]
            ACpx_r += translation_vector[1]
            CBpx_r += translation_vector[1]

        else:
            ABx += translation_vector[0]
            ACx += translation_vector[0]
            CBx += translation_vector[0]

            ABpx += translation_vector[1]
            ACpx += translation_vector[1]
            CBpx += translation_vector[1]


    # plt.figure(figsize=(12, 8)) # LEFT OUT FOR PLOTTING ON TOP OF THE RESULT! NECESSARY FOR ADDING IT TO ANOTHER PLOTTING FUNCTION
    if dmu is not None:
        plt.plot([ABx_r, ACx_r], [ABpx_r, ACpx_r], linewidth=linewidth, c=c,**plot_args)
        plt.plot([ABx_r, CBx_r], [ABpx_r, CBpx_r], linewidth=linewidth, c=c,**plot_args)
        plt.plot([CBx_r, ACx_r], [CBpx_r, ACpx_r], linewidth=linewidth, c=c,**plot_args)
    else:
        plt.plot([ABx, ACx], [ABpx, ACpx], linewidth=linewidth, c=c,**plot_args)
        plt.plot([ABx, CBx], [ABpx, CBpx], linewidth=linewidth, c=c,**plot_args)
        plt.plot([CBx, ACx], [CBpx, ACpx], linewidth=linewidth, c=c,**plot_args)
        print('--- custom plt argument under test')

######### THIS ONE DEALS WITH MULTIPLE TRIANGLE PLOTS
def stable_tri_plot2(dq, S=77, figsize=(12, 8), dmu=None, linewidth=3, translation_vectors=None,c='r',colorbar=False):
    eps = 6 * np.pi * dq
    ABx = []
    ABpx = []
    ACx = []
    ACpx = []
    CBx = []
    CBpx = []
    for ind,x in enumerate(eps):
        
        # crossing points
        ABx.append(- 2 / 3 * x / S)
        ABpx.append(-x * 2 / (S * np.sqrt(3)))
    
        ACx.append(- 2 / 3 * x / S)
        ACpx.append(x * 2 / (S * np.sqrt(3)))
    
        CBx.append((4 / 3) * x / S)
        CBpx.append(0)

    # print(f'raggio_before = {np.sqrt(ABx ** 2 + ABpx ** 2)}')

    # print(f'eps = {eps}   AB = {ABx},{ABpx}  AC = {ACx},{ACpx}, CB = {CBx},{CBpx}')
    if dmu is not None:
        dmu = dmu % (2 * np.pi)
        # dmu must be in rads
        rotation_matrix = np.array([[np.cos(dmu), np.sin(dmu)], [-np.sin(dmu), np.cos(dmu)]])
        ABx_r = []
        ABpx_r = []
        ACx_r = []
        ACpx_r = []
        CBx_r = []
        CBpx_r = []
                
        for i in range(len(dq)):
            ABx_r.append(rotation_matrix.dot(np.array([ABx[i], ABpx[i]]))[0])
            ABpx_r.append(rotation_matrix.dot(np.array([ABx[i], ABpx[i]]))[1])
            ACx_r.append(rotation_matrix.dot(np.array([ACx[i], ACpx[i]]))[0])
            ACpx_r.append(rotation_matrix.dot(np.array([ACx[i], ACpx[i]]))[1])
            CBx_r.append(rotation_matrix.dot(np.array([CBx[i], CBpx[i]]))[0])
            CBpx_r.append(rotation_matrix.dot(np.array([CBx[i], CBpx[i]]))[1])

    if translation_vectors is not None:  # PENSO NON SERVANO CAMBIAMENTI
        if dmu is not None:
            ABx_r += translation_vectors[:,0]
            ACx_r += translation_vectors[:,0]
            CBx_r += translation_vectors[:,0]

            ABpx_r += translation_vectors[:,1]
            ACpx_r += translation_vectors[:,1]
            CBpx_r += translation_vectors[:,1]

        else:
            ABx += translation_vectors[:,0]
            ACx += translation_vectors[:,0]
            CBx += translation_vectors[:,0]

            ABpx += translation_vectors[:,1]
            ACpx += translation_vectors[:,1]
            CBpx += translation_vectors[:,1]

    # print(f'raggio_after = {np.sqrt(ABx ** 2 + ABpx ** 2)}')
    # plt.figure(figsize=(12, 8)) # LEFT OUT FOR PLOTTING ON TOP OF THE RESULT! NECESSARY FOR ADDING IT TO ANOTHER PLOTTING FUNCTION
    if dmu is not None:
        for ind in range(len(dq)):
            plt.plot([ABx_r[ind], ACx_r[ind]], [ABpx_r[ind], ACpx_r[ind]], linewidth=linewidth, c=c[ind])
            plt.plot([ABx_r[ind], CBx_r[ind]], [ABpx_r[ind], CBpx_r[ind]], linewidth=linewidth, c=c[ind])
            plt.plot([CBx_r[ind], ACx_r[ind]], [CBpx_r[ind], ACpx_r[ind]], linewidth=linewidth, c=c[ind])
    else:
        for ind in range(len(dq)):
            plt.plot([ABx[ind], ACx[ind]], [ABpx[ind], ACpx[ind]], linewidth=linewidth, c=c[ind])
            plt.plot([ABx[ind], CBx[ind]], [ABpx[ind], CBpx[ind]], linewidth=linewidth, c=c[ind])
            plt.plot([CBx[ind], ACx[ind]], [CBpx[ind], ACpx[ind]], linewidth=linewidth, c=c[ind])


def plot_stable(out_dict, s=2,**norm_arg):
    twiss_df = out_dict['twiss'].to_pandas()
    monitor = out_dict['monitor']
    S_strength, S_mu = Virtual_sextupole_complete(out_dict)  # compute sextupole strength and mu
    dmu = twiss_df[twiss_df.name == 'pe.smh57'].mux.iloc[0] * 2 * np.pi - S_mu
    # dmu from the virtual sextupole to know the rotation
    Monitor = Normalize_monitor(out_dict, normalize_particles=False, center=True,**norm_arg)
    color = np.arange(out_dict['params']['n_turns'])
    colors = np.tile(color, (out_dict['params']['n_part'], 1))
    extracted_mask = Monitor.x != 0
    argmin = np.argmin(np.abs(twiss_df.mux * 2 * np.pi - S_mu))
    Xo = twiss_df.iloc[argmin]['x'] / twiss_df.iloc[argmin]['betx']
    ## CLOSED ORBIT CAUSES A CHANGE IN TUNE SHIFT
    dq0 = (out_dict['twiss'].qx - 6 - 1 / 3)  # normal as without distorsions and dispersion
    dq = dq0 - S_strength * Xo / (2 * np.pi)  # distortion correction

    plt.scatter(Monitor.x[extracted_mask], Monitor.px[extracted_mask], s=s, c=colors[extracted_mask])
    plt.colorbar(label='Turns')
    # PROBLEMAAAA SEGNO-ORIENTAMENTO TRIANGOLO
    stable_tri_plot(-dq, S_strength, dmu=dmu)


########### PER LA DISPERSIONE, PLOT STATICI

def plot_dispersion(out_dict,npart=10,norm=False,figsize=(10,8),centered=False):
    ''' To fix:
    - centering is not good
    - remove the extracted now using replace_null

    :param out_dict:
    :param npart:
    :param norm:
    :param figsize:
    :param centered:
    :return:
    '''
    monitor = out_dict['monitor']
    twiss_df = out_dict['twiss'].to_pandas()
    #particles = out_dict['particles']
    
    part_id = np.random.randint(0,out_dict['params']['n_part'],npart)
    deltas = monitor.delta[part_id,:]
    # DISPERSION
    dx = twiss_df[twiss_df.name == 'pe.smh57'].dx.iloc[0]
    dpx = twiss_df[twiss_df.name == 'pe.smh57'].dpx.iloc[0]
    # CLODED ORBIT
    xc = twiss_df[twiss_df.name == 'pe.smh57'].x.iloc[0]
    pxc = twiss_df[twiss_df.name == 'pe.smh57'].px.iloc[0]
    
    if (norm is False)&(centered is False):
        x = replace_null(monitor.x[part_id,:])
        px = replace_null(monitor.px[part_id,:])
    elif (norm is False)&(centered is True):
        x = replace_null(monitor.x[part_id, :]) - dx * deltas -xc
        px = replace_null(monitor.px[part_id, :]) - dpx * deltas -pxc

    else: # this should be replaced by the normalizing function
        betx = twiss_df[twiss_df.name=='pe.smh57'].betx.iloc[0]
        alfx = twiss_df[twiss_df.name=='pe.smh57'].alfx.iloc[0]
        if centered is False:
            x = replace_null(monitor.x[part_id,:])/np.sqrt(betx)
            px = x*alfx +replace_null(monitor.px[part_id,:])*np.sqrt(betx)
        else:
            x = (replace_null(monitor.x[part_id, :]) - dx * deltas-xc) / np.sqrt(betx)
            px = x * alfx + (replace_null(monitor.px[part_id, :]) - dpx * deltas-pxc) * np.sqrt(betx)

    plt.figure(figsize=figsize)
    plt.scatter(x,px,c=deltas,s=2)
    plt.colorbar(label='Momentum spread')


def plot_dispersion_n(out_dict, npart=10, norm=False, figsize=(10, 8), centered=False):
    ''' To fix:
    - centering is not good
    - remove the extracted now using replace_null

    :param out_dict:
    :param npart:
    :param norm:
    :param figsize:
    :param centered:
    :return:
    '''
    monitor = out_dict['monitor']
    twiss_df = out_dict['twiss'].to_pandas()
    # particles = out_dict['particles']

    part_id = np.random.randint(0, out_dict['params']['n_part'], npart)
    deltas = monitor.delta[part_id, :]
    # DISPERSION
    dx = twiss_df[twiss_df.name == 'pe.smh57'].dx.iloc[0]
    dpx = twiss_df[twiss_df.name == 'pe.smh57'].dpx.iloc[0]
    # CLODED ORBIT
    xc = twiss_df[twiss_df.name == 'pe.smh57'].x.iloc[0]
    pxc = twiss_df[twiss_df.name == 'pe.smh57'].px.iloc[0]

    if norm|centered:
        monitor = Normalize_monitor(out_dict,center=centered,normalize_particles=False)

    x = monitor.x[part_id,:]
    px = monitor.px[part_id,:]
    mask0 = x!=0

    #
    # if (norm is False) & (centered is False):
    #     x = replace_null(monitor.x[part_id, :])
    #     px = replace_null(monitor.px[part_id, :])
    # elif (norm is False) & (centered is True):
    #     x = replace_null(monitor.x[part_id, :]) - dx * deltas - xc
    #     px = replace_null(monitor.px[part_id, :]) - dpx * deltas - pxc
    #
    # else:  # this should be replaced by the normalizing function
    #     betx = twiss_df[twiss_df.name == 'pe.smh57'].betx.iloc[0]
    #     alfx = twiss_df[twiss_df.name == 'pe.smh57'].alfx.iloc[0]
    #     if centered is False:
    #         x = replace_null(monitor.x[part_id, :]) / np.sqrt(betx)
    #         px = x * alfx + replace_null(monitor.px[part_id, :]) * np.sqrt(betx)
    #     else:
    #         x = (replace_null(monitor.x[part_id, :]) - dx * deltas - xc) / np.sqrt(betx)
    #         px = x * alfx + (replace_null(monitor.px[part_id, :]) - dpx * deltas - pxc) * np.sqrt(betx)

    plt.figure(figsize=figsize)
    plt.scatter(x[mask0], px[mask0], c=deltas, s=2)
    plt.colorbar(label='Momentum spread')


#### NON FUNZIONAAA male!!
def plot_stable_disp(out_dict, n_part= 10, s=2,ids=None,ret_ids=False,figsize=(8,6)):
    twiss_df = out_dict['twiss'].to_pandas()
    monitor = out_dict['monitor']
    ###
    S_strength, S_mu = Virtual_sextupole_complete(out_dict)  # compute sextupole strength and mu
    dmu = twiss_df[twiss_df.name == 'pe.smh57'].mux.iloc[
              0] * 2 * np.pi - S_mu  # dmu from the virtual sextupole to know the rotation
    if ids is None:
        ids = np.random.randint(0,out_dict['params']['n_part'],n_part)
    
    ## remove closed orbit
    xo = twiss_df[twiss_df.name == 'pe.smh57'].x.iloc[0]
    pxo = twiss_df[twiss_df.name == 'pe.smh57'].px.iloc[0]
    x = replace_null(monitor.x[ids, :]) # basta se modifico solo queste
    px =replace_null( monitor.px[ids, :])##

  #  extracted_mask = monitor.x[:, at_turn] == 0

    # NORMALIZATION of coordinates
    betx = twiss_df[twiss_df.name == 'pe.smh57'].betx.iloc[0]
    alfx = twiss_df[twiss_df.name == 'pe.smh57'].alfx.iloc[0]
    X = x / np.sqrt(betx)
    PX = alfx * x / np.sqrt(betx) + np.sqrt(betx) * px
    Xo = xo / np.sqrt(betx)
    PXo = alfx * xo / np.sqrt(betx) + np.sqrt(betx) * pxo

    X_corr = X - Xo
    PX_corr = PX - PXo

    ## CLOSED ORBIT CAUSES A CHANGE IN TUNE SHIFT
    dq0 = (out_dict['twiss'].qx - 6 - 1 / 3)  # normal as without distorsions and dispersion
    dq = dq0  + monitor.delta[ids,0]*out_dict['twiss'].dqx - S_strength / (4 * np.pi) * Xo  # distortion correction
    # print(f'dq = {dq}, dmu = {dmu}')
    Dx = monitor.delta[ids, 0] * twiss_df[twiss_df.name == 'pe.smh57'].dx.iloc[0]
    Dpx = monitor.delta[ids, 0] * twiss_df[twiss_df.name == 'pe.smh57'].dpx.iloc[0]
    # NORMALIZE DISPERSION
    Dx = Dx/np.sqrt(betx)
    Dpx = Dx*alfx + Dpx*np.sqrt(betx)
    
    
    # plt.axvline(out_dict['params']['SEPTA_X_MM']/(1000*np.sqrt(betx))-Xo,c='r',linestyle='--')
    # cm = ScalarMappable()
    # colors_tri = cm.to_rgba(monitor.delta[ids, 0])
    # cm2 = ScalarMappable()
    # color_part = cm2.to_rgba(monitor.delta[ids, :])
    # plt.scatter(X_corr, PX_corr, s=s,c=cm2.to_rgba(monitor.delta[ids, :].flatten()))  # funziona solo se appiattisco uno degli array
    # stable_tri_plot2(-dq,S_strength, translation_vectors=np.array([Dx, Dpx]).transpose(),dmu=dmu, c=cm.to_rgba(monitor.delta[ids, 0]),linewidth=1)
    # #plt.colorbar(cm)
    # if ret_ids:
    #     return ids

    cm = ScalarMappable()
    colors_tri = cm.to_rgba(monitor.delta[ids, 0])
    cm2 = ScalarMappable()
    color_part = cm2.to_rgba(monitor.delta[ids, :])
    fig, ax = plt.subplots(figsize=figsize)
    plt.axvline(out_dict['params']['SEPTA_X_MM'] / (1000 * np.sqrt(betx)) - Xo, c='r', linestyle='--')
    ax.scatter(X_corr, PX_corr, s=s,
               c=cm2.to_rgba(monitor.delta[ids, :].flatten()))  # funziona solo se appiattisco uno degli array
    stable_tri_plot2(dq, S_strength, translation_vectors=np.array([Dx, Dpx]).transpose(), dmu=dmu,
                     c=cm.to_rgba(monitor.delta[ids, 0]), linewidth=1, ax=ax)
    plt.colorbar(cm, ax=ax)
    if ret_ids:
        return ids
      
    


##############
#        ANIMATIONS
#############


def anim_ph_space_stable(out_dict, filename=None, message='',step=5):
    particles = out_dict['particles']
    monitor = out_dict['monitor']
    twiss_df = out_dict['line'].twiss(method='4d').to_pandas()
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
    fig, ax = plt.subplots(figsize=(12, 8))
    scat = ax.scatter([], [], s=2)

    betx = twiss_df[twiss_df['name'] == 'pe.smh57'].betx.iloc[0]
    alfx = twiss_df[twiss_df['name'] == 'pe.smh57'].alfx.iloc[0]
    x = replace_null(monitor.x)
    px = replace_null(monitor.px)
    deltas = replace_null(monitor.delta)
    ## STABLE TRIANGLE RELATED
    S_strength, S_mu = Virtual_sextupole_complete(out_dict)  # compute sextupole strength and mu
    dmu = twiss_df[twiss_df.name == 'pe.smh57'].mux.iloc[
              0] * 2 * np.pi - S_mu  # dmu from the virtual sextupole to know the rotation
    dq0 = (out_dict['twiss'].qx - 6 - 1 / 3)  # normal as without distorsions and dispersion

    ########
    xc = twiss_df[twiss_df['name'] == 'pe.smh57'].x.iloc[0]
    pxc = twiss_df[twiss_df['name'] == 'pe.smh57'].px.iloc[0]
    # REMOVE CLOSED ORBIT and dispersion distortion
    if np.sum(monitor.delta[:, :].flatten()) != 0:
        dx = twiss_df[twiss_df['name'] == 'pe.smh57'].dx.iloc[0] / np.sqrt(betx)
        dpx = twiss_df[twiss_df['name'] == 'pe.smh57'].dpx.iloc[0]
        X = (x - xc - deltas * dx) / np.sqrt(betx)
        PX = (x - xc - deltas * dx) * alfx / np.sqrt(betx) + (px - pxc - deltas * dpx) * np.sqrt(
            betx)
    else:
        X = (x - xc) / np.sqrt(betx)
        PX = (x - xc) * alfx / np.sqrt(betx) + (px - pxc) * np.sqrt(
            betx)
    SEPTA_scaled = np.array([SEPTA_X_MM / (np.sqrt(betx) * 1000) - xc / np.sqrt(betx)])
    # dq = dq0 - S_strength *xc/ (4 * np.pi*np.sqrt(betx))-twiss_df[twiss_df.name=='pe.smh57'].dx*deltas   # distortion correction
    dq = dq0 - S_strength * xc / (4 * np.pi * np.sqrt(betx))  # distortion correction

    def update(frame):
        # a frame is a turn
        at_turn = frame
        if frame%50==0:
            print(f'frame {frame}')
        ax.clear()
        # position of EXTRACTED particles
        x_extr = df[df['at_turn'] <= at_turn]['x']  #
        px_extr = df[df['at_turn'] <= at_turn]['px']  #
        X_extr = (x_extr - xc) / np.sqrt(betx)
        Px_extr = (x_extr - xc) * alfx / np.sqrt(betx) + (px_extr - pxc) * np.sqrt(betx)

        mask = monitor.x[:, at_turn] != 0  # mask on the monitor array, for the extracted particles (at_turn)

        ax.text(0.1, 0.9, f'{len(x_extr)} extracted', transform=ax.transAxes)
        ax.set_title(f'Phase space turn :{frame}/{n_turns}')
        ax.set_xlabel('x')
        ax.set_ylabel('px')
        ax.axvline(SEPTA_scaled, c="r", linestyle="--")

        # XAXES LIMITS

        axes_margin = 0.1
        # print(f'{SEPTA_scaled} shape of x ={x_for_limits.shape}')
        xmin = np.min(np.concatenate((X.flatten(), SEPTA_scaled)))
        xmax = np.max(X)
        ax.set_xlim(xmin - np.abs((xmin-xmax) * axes_margin), xmax + np.abs((xmax-xmin) * axes_margin))
        # Yaxes LIMITS
        ymin = np.min(PX)
        ymax = np.max(PX)
        ax.set_ylim(ymin - np.abs((ymin-ymax) * axes_margin), ymax + np.abs((ymax-ymin) * axes_margin))

        # ax.scatter(X_extr, PX_extr, c='g', s=2)
        ax.scatter(X[mask, at_turn], PX[mask, at_turn], c='b', s=2)
        ax.scatter(X_extr, Px_extr, c='r', s=2)
        stable_tri_plot(dq, S_strength, dmu=dmu)

        return scat,

    ani = FuncAnimation(fig, update, frames=range(0, n_turns, step), blit=True)
    if filename is None:
        filename = f'part{out_dict["params"]["n_part"]}_DPP{out_dict["params"]["DPP_FACTOR"]}_Volt{out_dict["params"]["volt"]}'

    
    if os.path.isdir('./gif_wes'):
        ani.save(f'./gif_wes/ph_space_stable_tri_{message}_{filename}.gif', dpi=200)
    else:
        ani.save(f'./gif_wes/ph_space_stable_tri_{message}_{filename}.gif', dpi=200)

    return None

######### ANIMATION DISPERSION

def anim_ph_space_disp(out_dict, filename=None, message='',dispersion=False, step=5):
    '''  MAKE ANIMATION OF THE PHASE SPACE AT SEPTA NON-NORMALIZED,
    if dispersion == True it also plots the phase space shifted for the dispersional effect
    '''
    particles = out_dict['particles']
    monitor = out_dict['monitor']
    SEPTA_X_MM = out_dict['params']['SEPTA_X_MM']  # funzionerà?

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
    cmap = ScalarMappable()
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
        
        ax.scatter(x_extr, px_extr, c=delta_extr, s=2)
        if dispersion is False:
            #ax.scatter(x_pres, px_pres, c=monitor.delta[mask, at_turn], s=2, label='dispersion')
            ax.scatter(x_pres, px_pres, c=cmap.to_rgba(monitor.delta[mask, at_turn]), s=2, label='dispersion')
            
        if dispersion:
            ax.scatter(x_pres_nodisp, px_pres_nodisp, c='r', s=1, alpha=0.5, label='no_dispersion')
            ax.scatter(x_extr_nodisp,px_extr_nodisp,c='c',s=1,alpha=0.5)
            ax.legend(loc='lower left')
        
            

        return scat,

    ani = FuncAnimation(fig, update, frames=range(0, n_turns, step), blit=True)
    plt.colorbar(cmap,label='Dispersion',ax=ax)
    if filename is None:

        filename = f'n_part{out_dict["params"]["n_part"]}_QX{out_dict["twiss"].qx}_Volt{out_dict["params"]["volt"]}_duration{out_dict["params"]["duration"]}'

    if os.path.isdir('./gif_wes'):
        ani.save(f'./gif_wes/ph_space_disp_{message}_{filename}.gif', dpi=200)
    else:
        ani.save(f'./gif_wes/ph_space_{message}_{filename}.gif', dpi=200)

    return None

def anim_ph_space_dyn(out_dict, filename=None,message='', step=5):
    particles = out_dict['particles']
    monitor = out_dict['monitor']
    twiss_df = out_dict['line'].twiss(method='4d').to_pandas()
    SEPTA_X_MM = out_dict['params']['SEPTA_X_MM']
    if 'dynamic_twiss' not in out_dict.keys():
        print('ERROR not possible to use this plot')
        return None

    # UTILE PER EVITARE GROSSI BUG CREDO
    data = {
        'at_turn': particles.at_turn,
        'x': particles.x,
        'px': particles.px,
        'delta': particles.delta,
    }
    n_turns = out_dict['params']['n_turns']
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(12, 8))
    scat = ax.scatter([], [], s=2)

    betx = twiss_df[twiss_df['name'] == 'pe.smh57'].betx.iloc[0]
    alfx = twiss_df[twiss_df['name'] == 'pe.smh57'].alfx.iloc[0]

    x = replace_null(monitor.x)
    px = replace_null(monitor.px)
    deltas = replace_null(monitor.delta)
    
    ########
    xc = twiss_df[twiss_df['name'] == 'pe.smh57'].x.iloc[0]
    pxc = twiss_df[twiss_df['name'] == 'pe.smh57'].px.iloc[0]
    SEPTA_scaled = np.array([SEPTA_X_MM / (np.sqrt(betx) * 1000) - xc / np.sqrt(betx)])
    if np.sum(monitor.delta[:, :].flatten()) != 0:
        dx = twiss_df[twiss_df['name'] == 'pe.smh57'].dx.iloc[0] / np.sqrt(betx)
        dpx = twiss_df[twiss_df['name'] == 'pe.smh57'].dpx.iloc[0]
        X = (x - xc - deltas * dx) / np.sqrt(betx)
        PX = (x - xc - deltas * dx) * alfx / np.sqrt(betx) + (px - pxc - deltas * dpx) * np.sqrt(
            betx)
    else:
        X = (x - xc) / np.sqrt(betx)
        PX = (x - xc) * alfx / np.sqrt(betx) + (px - pxc) * np.sqrt(
            betx)
        
    ## STABLE TRIANGLE RELATED
    S_strength, S_mu = Virtual_sextupole_complete(out_dict)  # compute sextupole strength and mu
    dmu = twiss_df[twiss_df.name == 'pe.smh57'].mux.iloc[
                      0] * 2 * np.pi - S_mu  # dmu from the virtual sextupole to know the rotation
    dq0 = (out_dict['twiss'].qx - 6 - 1 / 3)  # normal as without distorsions and dispersion
    dq = dq0 - S_strength * xc / (4 * np.pi * np.sqrt(betx))  # distortion correction

            
    def update(frame):
        # a frame is a turn
        at_turn = frame
        if frame % 50 == 0:
            print(f'frame {frame}')
        ax.clear()
        if frame < out_dict['params']['dynamic_sextupole']:
            ### CONTINUE
            twiss_dyn = out_dict['dynamic_twiss'][f'twiss_{frame+1}']
            line_dyn = out_dict['dynamic_line'][f'line_{frame+1}']
            twiss_df_dyn = twiss_dyn.to_pandas()
            
            S_strength_loc, S_mu_loc = Virtual_sextupole_complete(dict(line=line_dyn,twiss=twiss_dyn))  # compute sextupole strength and mu
            dmu_loc = twiss_df_dyn[twiss_df_dyn.name == 'pe.smh57'].mux.iloc[
                      0] * 2 * np.pi - S_mu_loc  # dmu from the virtual sextupole to know the rotation
            dq0_loc = (twiss_dyn.qx - 6 - 1 / 3)  # normal as without distorsions and dispersion
            dq_loc = dq0_loc - S_strength_loc * xc / (4 * np.pi * np.sqrt(betx))  # distortion correction

            

            
            # dq = dq0 - S_strength *xc/ (4 * np.pi*np.sqrt(betx))-twiss_df[twiss_df.name=='pe.smh57'].dx*deltas   # distortion correction
            
        # position of EXTRACTED particles
        x_extr = df[df['at_turn'] <= at_turn]['x']  #
        px_extr = df[df['at_turn'] <= at_turn]['px']  #
        X_extr = (x_extr - xc) / np.sqrt(betx)
        Px_extr = (x_extr - xc) * alfx / np.sqrt(betx) + (px_extr - pxc) * np.sqrt(betx)

        mask = monitor.x[:, at_turn] != 0  # mask on the monitor array, for the extracted particles (at_turn)

        # X_extr = (x_extr-xc) / np.sqrt(betx)
        # PX_extr = (x_extr-xc) * alfx / np.sqrt(betx) + (px_extr-pxc) / np.sqrt(betx)

        ax.text(0.1, 0.9, f'{len(x_extr)} extracted', transform=ax.transAxes)
        ax.set_title(f'Phase space turn :{frame}/{n_turns}')
        ax.set_xlabel('x')
        ax.set_ylabel('px')
        ax.axvline(SEPTA_scaled, c="r", linestyle="--")

        # XAXES LIMITS

        axes_margin = 0.1
        # print(f'{SEPTA_scaled} shape of x ={x_for_limits.shape}')
        xmin = np.min(np.concatenate((X.flatten(), SEPTA_scaled)))
        xmax = np.max(x)
        ax.set_xlim(xmin - np.abs((xmin - xmax) * axes_margin), xmax + np.abs((xmax - xmin) * axes_margin))

        # Yaxes LIMITS
        ymin = np.min(PX)
        ymax = np.max(PX)
        ax.set_ylim(ymin - np.abs((ymin - ymax) * axes_margin), ymax + np.abs((ymax - ymin) * axes_margin))

        # ax.scatter(X_extr, PX_extr, c='g', s=2)
        ax.scatter(X[mask, at_turn], PX[mask, at_turn], c='b', s=2)
        ax.scatter(X_extr, Px_extr, c='r', s=2)
        if frame < out_dict['params']['dynamic_sextupole']:
            stable_tri_plot(dq_loc, S_strength_loc, dmu=dmu_loc)
        else:
            stable_tri_plot(dq, S_strength, dmu=dmu)

        return scat,

    ani = FuncAnimation(fig, update, frames=range(0, n_turns, step), blit=True)
    if filename is None:
        filename = f'n_part{out_dict["params"]["n_part"]}_QX{out_dict["twiss"].qx}_Volt{out_dict["params"]["volt"]}_duration{out_dict["params"]["duration"]}__adiabatic_turns_{out_dict["params"]["dynamic_sextupole"]}'
    if os.path.isdir('./gif_wes'):
        ani.save(f'./gif_wes/ph_space_stable_dyn_{message}_{filename}.gif', dpi=200)
    else:
        ani.save(f'./gif_wes/ph_space_stable_dyn_{message}_{filename}.gif', dpi=200)

    return None



