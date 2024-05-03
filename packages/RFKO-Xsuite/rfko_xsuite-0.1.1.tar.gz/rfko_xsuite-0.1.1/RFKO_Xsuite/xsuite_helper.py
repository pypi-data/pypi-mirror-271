import numpy as np
import matplotlib.pyplot as plt
import scipy
from tqdm import tqdm
import time as timing
import logging
logger = logging.getLogger(__name__)


import xtrack as xt
import xpart as xp

from .Rfko import Rfko


def nearest_betx(twiss_df, x, px, zeta):
    ''' Takes point in a transverse plane x-px and an array of longitudinal position in which
    translate those point along the line and add the effect of the closed orbit
    '''
    s = np.array(twiss_df.s)
    for ind in range(len(zeta)):
        nearest_point = s[np.argmin(np.abs(s-zeta[ind]))]
        x[ind] += twiss_df[twiss_df.s == nearest_point].x.iloc[0]
        px[ind] += twiss_df[twiss_df.s == nearest_point].px.iloc[0]

    return x, px

def nearest_betx2(twiss, x, px, zeta):
    ''' BETTER VERSION THAN ONE: Takes point in a transverse plane x-px and an array of longitudinal position in which
    translate those point along the line and add the effect of the closed orbit
    '''

    for i,z in enumerate(zeta):
        x[i] += np.interp(z,twiss.s,twiss.x)
        px[i] += np.interp(z,twiss.s,twiss.px)
    return x, px

def freq_range(outdict, plot=False):
    if isinstance(outdict,Rfko):
        outdict = outdict.to_dict()
    monitor = outdict['monitor']
    twiss = outdict['twiss']
    #twiss_df = twiss.to_pandas()

    freqs = 1 / twiss.T_rev0 - twiss.slip_factor * monitor.delta[monitor.delta != 0] * 1 / twiss.T_rev0
    if plot:
        plt.scatter(monitor.delta[monitor.delta != 0], freqs, s=2)
        plt.axhline(1 / twiss.T_rev0, linestyle='--', c='r')
        plt.title('Frequency range')
    return freqs


def tune_range(outdict, plot=False):
    if isinstance(outdict,Rfko):
        outdict = outdict.to_dict()
    monitor = outdict['monitor']
    twiss = outdict['twiss']
    #twiss_df = twiss.to_pandas()
    if (np.sum(monitor.delta)==0)|(outdict['params']['DPP_FACTOR']!=0):
        #It Means no simulation has been done still and the monitor didn't record any delta
        deltas = outdict['particles'].delta
    else:
        deltas = monitor.delta[monitor.delta != 0]
    tunes = twiss.qx + twiss.dqx *deltas
    if plot:
        plt.scatter(deltas, tunes, s=2)
        plt.axhline(twiss.qx, linestyle='--', c='r')
        plt.title('Tune range')
    return tunes



def find_multipole_component(line_df,order = 'sextupole'):
    ###### IT SEEMS THAT USING DATAFRAMES IS MUCH MORE EFFICIENT

    translation_dict_num = dict(dipole = 0, quadrupole = 1, sextupole = 2, octupole = 3)
    translation_dict_str = dict(dipole = 'Dipole', quadrupole = 'Quadrupole', sextupole = 'Sextupole', octupole = 'Octupole')
    if (order not in translation_dict_num.keys()) and (order not in translation_dict_num.values()) and \
            (order not in translation_dict_str.values()):
        print('Multipole component not recognized')
        return None
    ####### può sembrare un casino ma è piuttosto semplice- migliorarlo? magari con un unico dizionario??
    elif order in translation_dict_num.values():  # se dato come numero
        order_num = order
        order_str = list(translation_dict_num.keys())[
            list(translation_dict_num.values()).index(order)]  # to test for good
        order_corr = translation_dict_str[order_str]  # to have the correct available
    elif order in translation_dict_num.keys():  # se dato come stringa semplice
        order_num = translation_dict_num[order]
        order_str = order
        order_corr = translation_dict_str[order]
    else:  # altri casi già controllati tutti
        order_str = list(translation_dict_str.keys())[list(translation_dict_str.values()).index(order)]
        order_num = translation_dict_num[order_str]
        order_corr = order

    #print(f'order_str = {order_str}, order_num = {order_num}, order_corr = {order_corr}')

    ###### COMINCIA IL DIVERTIMENTO
    strength_attr = 'k'+str(order_num)
    # ELEMENTI DIRETTAMENTE INTERESSATI
    direct_names = line_df[line_df.element_type == order_corr].name # estrae elementi con ordine esplicito ed unico
    nz_direct_names = [i for i in direct_names if getattr(line_df[line_df.name == i].element.iloc[0],strength_attr) != 0]
    # ECCEZIONE QUADRUPOLI, GLI ELEMENTI CHE SONO QUADRUPOLI HANNO COMUNQUE DEFINITO ANCHE UN ARRAY DI COMPONENTI MULTIPOLARI
    quads = line_df[line_df.element_type == 'Quadrupole'].name
    if xt.__version__< '0.50.0' :
        quad_names = [i for i in quads if line_df[line_df.name == i].element.iloc[0]._order >= order_num]
    else:
        quad_names = []
        # in successive versions the quadrupole do not have multipole components,
        # but for compatibility with other functions I include an empty list


    nz_quad_names = [i for i in quad_names if line_df[line_df.name == i].element.iloc[0].knl[order_num]!= 0] # NB non zero anche per ordini diversi dai quadrupoli
    # COMBINED FUNCTION MAGNET
    combf = line_df[line_df.element_type == 'CombinedFunctionMagnet'].name
    combf_names = [i for i in combf if line_df[line_df.name == i].element.iloc[0]._order >= order_num]
    #combf_names seleziona solo quelli che comprendono l'ordine desiderato, per non incorrere il arrori di indice troopo lungo
    nz_combf_names = [i for i in combf_names if line_df[line_df.name == i].element.iloc[0].knl[order_num] != 0]
    # I COMB FUNCTION MAGNET HANNNO UN ALTRA ECCEZZIONE ECCEZZIONALE VERAMENTE : hanno singole componenti dipolo e quadrupolo
    if order_num in [0,1]:
        nz_combf_names_single = [i for i in combf if getattr(line_df[line_df.name == i].element.iloc[0],strength_attr)!=0]

    # MULTIPOLI
    mults = line_df[line_df.element_type == 'Multipole'].name
    mult_names = [i for i in mults if line_df[line_df.name == i].element.iloc[0]._order >= order_num]
    nz_mult_names = [i for i in mult_names if line_df[line_df.name == i].element.iloc[0].knl[order_num] !=0]
    if order_num in [0,1]:
        return dict(multipoles = nz_mult_names,combf_knl = nz_combf_names,quad_mult = nz_quad_names,direct_ele=nz_direct_names,combf_sing = nz_combf_names_single)
    return dict(multipoles = nz_mult_names,combf_knl = nz_combf_names,quad_mult = nz_quad_names,direct=nz_direct_names)



def Normalize_monitor(outdict,at_element='pe.smh57',keep_zeroes=True,center=True,remove_dispersion=True,normalize_particles=False):
    ''' TO ADD
    - Remove dispersion option
    - Particles norm?'''
    if isinstance(outdict,Rfko):
        rfko = outdict
        outdict = rfko.to_dict()

    monitor=outdict['monitor'].copy()
    try: # If the input is outdict referencng rfko raises an error
        if rfko.line_type=='henon_map':
            alfx, betx, _, _ = rfko.henon_params['twiss_params']
            monitor.x = rfko.monitor.x/np.sqrt(betx)
            monitor.px = monitor.x*alfx+ rfko.monitor.px*np.sqrt(betx)
            return monitor
    except:
        pass
    try:
        at_element = outdict['monitor'].placed_at_element
    except:
        pass

    logger.info(f'ELement considered for the normalization {at_element}')
    twiss = outdict['twiss']
    twiss_df = twiss.to_pandas()
    try:
        at_element = monitor.placed_at_element
        print('element considered based on PLACED AT ELEMENT')
    except:
        pass
    ######## CHECK WHAT KIND OF TRACKING HAS BEEN MADE
    if ('line_dynamics' in outdict.keys())|('dynamic_line' in outdict.keys()):
        if normalize_particles:
            logger.warning('dynamical normalization Norm_vary used')
            Monitor,Particles = Norm_vary(outdict,keep_zeroes=keep_zeroes, normalize_particles=normalize_particles,at_element=at_element,center=center,remove_dispersion=remove_dispersion)
            return Monitor,Particles
        else:
            logger.warning('dynamical normalization Norm_vary used')
            Monitor = Norm_vary(outdict,keep_zeroes=keep_zeroes, normalize_particles=normalize_particles,at_element=at_element,center=center)
            return Monitor


    else:
        # If no dynamical twiss is made optics stays constant hence betx,alfx....

        betx = twiss_df[twiss_df.name == at_element].betx.iloc[0]
        alfx = twiss_df[twiss_df.name == at_element].alfx.iloc[0]
        # Remove the orbit distortion and dispersion IF remove_dispersion is True
        if center:
            logger.debug(f'Remove dispersion option is = {remove_dispersion}')
            xc = twiss_df[twiss_df.name == at_element].x.iloc[0] + remove_dispersion*monitor.delta*twiss_df[twiss_df.name== at_element].dx.iloc[0]
            pxc = twiss_df[twiss_df.name == at_element].px.iloc[0]
        else:
            xc=0
            pxc=0

        if keep_zeroes:
            # If a monitor value is exactlty zero it means the particles has been extracted
            mask_null = np.array(monitor.x!=0 )
            X = (monitor.x - np.array(mask_null)*xc)/np.sqrt(betx)
            PX = X*alfx + (monitor.px-mask_null*pxc)*np.sqrt(betx)

        else:
            X = (monitor.x-xc)/np.sqrt(betx)
            PX = X*alfx + (monitor.px-pxc)*np.sqrt(betx)

        monitor.x = X
        monitor.px = PX
        if normalize_particles:
            logger.info('Particles normalization part is still unchecked')
            particles = outdict['particles'].copy()
            if center:
                X_p = (particles.x-xc)/np.sqrt(betx)
                PX_p = X_p*alfx + (particles.px-pxc)*np.sqrt(betx)
            else:
                X_p = (particles.x) / np.sqrt(betx)
                PX_p = X_p * alfx + (particles.px) * np.sqrt(betx)

            particles.x = X_p
            particles.px = PX_p
            return monitor,particles
        else:
            return monitor


def Norm_vary(outdict, keep_zeroes=True, normalize_particles=True, center=False, at_element='pe.smh57',remove_dispersion=True):
    ''' To correeeect absolutely the DISPERSION'''
    monitorc = outdict['monitor'].copy()
    monitor = outdict['monitor']
    partic = outdict['particles'].copy()
    n_turns = outdict['params']['n_turns']
    # out_dict['params']['dynamic_sextupole'] # in each case contains the number of sextupole ramping turns
    if 'twiss_dynamics' in outdict.keys():
        repeat_turns = n_turns
        xc = 0
        pxc = 0
        for n in range(repeat_turns):
            logger.debug('The normalization consider a fully dynamic situation using a different twiss every turn!')
            twiss_df = outdict['twiss_dynamics'][f'twiss_{n}'].to_pandas()
            betx = twiss_df[twiss_df.name == at_element].betx.iloc[0]
            alfx = twiss_df[twiss_df.name == at_element].alfx.iloc[0]
            # center to the distortion
            if center:
                logger.debug(f'Remove dispersion option is = {remove_dispersion}')
                xc = twiss_df[twiss_df.name == at_element].x.iloc[0]+ remove_dispersion*monitor.delta*twiss_df[twiss_df.name== at_element].dx.iloc[0]
                pxc = twiss_df[twiss_df.name == at_element].px.iloc[0]
            if keep_zeroes:
                mask_null = np.array(monitor.x[:, n] != 0)
                Xturn = (monitor.x[:, n] - np.array(mask_null) * xc) / np.sqrt(betx)
                PXturn = Xturn * alfx + (monitor.px[:, n] - mask_null * pxc) * np.sqrt(betx)
            else:
                Xturn = (monitor.x[:, n] - xc) / np.sqrt(betx)
                PXturn = Xturn * alfx + monitor.px[:, n] * np.sqrt(betx)
            if normalize_particles:
                logger.error('Particles normalization is not well working')
                particles = outdict['particles']
                X_pturn = (particles.x[:, n] - xc) / np.sqrt(betx)
                PX_pturn = X_pturn * alfx + (particles.px[:, n] - pxc) * np.sqrt(betx)
                partic.x[:, n] = X_pturn
                partic.px[:, n] = PX_pturn
            monitorc.x[:, n] = Xturn
            monitorc.px[:, n] = PXturn

    elif 'dynamic_twiss' in outdict.keys():
        logger.debug('The normalization consider the sextupole ramping!')
        repeat_turns = n_turns
        ramping_stop = outdict['params']['dynamic_sextupole']
        done_flag = True  # Turn false when the action is done
        xc = 0
        pxc = 0
        twiss_df0 = outdict['twiss'].to_pandas()
        betx0 = twiss_df0[twiss_df0.name == at_element].betx.iloc[0]
        alfx0 = twiss_df0[twiss_df0.name == at_element].alfx.iloc[0]
        dx0 =  twiss_df0[twiss_df0.name == at_element].dx.iloc[0]

        for n in range(repeat_turns):
            if n + 1 <= ramping_stop:
                twiss_df = outdict['dynamic_twiss'][f'twiss_{n + 1}'].to_pandas()
                betx = twiss_df[twiss_df.name == at_element].betx.iloc[0]
                alfx = twiss_df[twiss_df.name == at_element].alfx.iloc[0]
                dx = remove_dispersion*monitor.delta*twiss_df[twiss_df.name== at_element].dx.iloc[0]
            elif done_flag:
                twiss_df = twiss_df0
                betx = betx0
                alfx = alfx0
                dx = dx0
                # ACTION FLAG TO NOT REPEAT EVERYTIME
                done_flag = False

                # center to the distortion
            if center:
                logger.debug(f'Remove dispersion option is : {remove_dispersion}')
                xc = twiss_df[twiss_df.name == at_element].x.iloc[0] + remove_dispersion*monitor.delta[:, n]*dx
                pxc = twiss_df[twiss_df.name == at_element].px.iloc[0]
            if keep_zeroes:
                mask_null = np.array(monitor.x[:, n] != 0)
                Xturn = (monitor.x[:, n] - np.array(mask_null) * xc) / np.sqrt(betx)
                PXturn = Xturn * alfx + (monitor.px[:, n] - mask_null * pxc) * np.sqrt(betx)
            else:
                Xturn = (monitor.x[:, n] - xc) / np.sqrt(betx)
                PXturn = Xturn * alfx + monitor.px[:, n] * np.sqrt(betx)
            if normalize_particles:
                logger.error('The normalization of particles is not correct')
                particles = outdict['particles']
                X_pturn = (particles.x[:, n] - xc) / np.sqrt(betx)
                PX_pturn = X_pturn * alfx + (particles.px[:, n] - pxc) * np.sqrt(betx)
                partic.x[:, n] = X_pturn
                partic.px[:, n] = PX_pturn
            monitorc.x[:, n] = Xturn
            monitorc.px[:, n] = PXturn

    if normalize_particles:
        return monitorc, partic
    else:
        return monitorc






def norm_part(outdict,particles=None, at_element=None,at_s=None):
    ''' Could consider that is noither at_element nor at_s are given I could read the position of the particles'''
    if isinstance(outdict,Rfko):
        outdict = outdict.to_dict(particles=particles)
    assert (at_element is not None)|(at_s is not None), 'Give at_s or at_element'
    assert not (at_element is None)&(at_s is None), 'Give at_s OR at_element' # check description
    if particles is None:
        particles = outdict['particles']
    twiss_df = outdict['twiss'].to_pandas()
    Particles = particles.copy()
    if at_element is not None: # if generated at the same locations
        betx = twiss_df[twiss_df.name == at_element].betx.iloc[0]
        alfx = twiss_df[twiss_df.name == at_element].alfx.iloc[0]
        xc = twiss_df[twiss_df.name == at_element].x.iloc[0]
        pxc = twiss_df[twiss_df.name == at_element].px.iloc[0]
        Particles.x = (particles.x - xc) / np.sqrt(betx)
        Particles.px = Particles.x * alfx + (particles.px - pxc) * np.sqrt(betx)
    else:  # When generated at different amplitudes
        xc = np.interp(at_s, twiss_df.s, twiss_df.x)
        pxc = np.interp(at_s, twiss_df.s, twiss_df.px)
        betx = np.interp(at_s, twiss_df.s, twiss_df.betx)
        alfx = np.interp(at_s, twiss_df.s, twiss_df.alfx)
        Particles.x = (particles.x - xc) / np.sqrt(betx)
        Particles.px = Particles.x * alfx + (particles.px - pxc) * np.sqrt(betx)


    return Particles


def DEnormalize_points(rfko, X=None, PX=None, at_element=None, at_s=None, centered=True):
    '''inverse transform, to denormalize'''
    assert (at_element is not None) | (at_s is not None), 'Choose either at_element or at_s but not both'

    twiss = rfko.twiss
    ref_s = [at_s if (at_s is not None) else twiss.s[twiss.name == at_element]]
    if at_element is not None:
        betx = twiss.betx[twiss.name == at_element]
        alfx = twiss.alfx[twiss.name == at_element]
        xc = twiss.x[twiss.name == at_element]
        pxc = twiss.px[twiss.name == at_element]
    else:
        betx = np.interp(at_s, twiss.s, twiss.betx)
        alfx = np.interp(at_s, twiss.s, twiss.alfx)
        xc = np.interp(at_s, twiss.s, twiss.x)
        pxc = np.interp(at_s, twiss.s, twiss.px)

    if not centered:
        xc = 0
        pxc = 0
    x = X * np.sqrt(betx) + xc
    px = (PX - X * alfx) / np.sqrt(betx) + pxc
    return x, px



def tracking(out_dict, type='first', sextupoles_turns=None, twiss=True,return_time=False):
    ''' Tracking of a line with the outdict convention, 3 different type of tracking

    CHANGES/IMPOROVEMENT NECESSARY
    - third type: turning off all the extraction elements is better (quads)
    - different type (?): to do activate the extraction sextupole after a while


    :param twiss:
    :param out_dict:
    :param type:
    :param sextupoles_turns:
    :return:
    '''
    if isinstance(out_dict,Rfko):
        rfko = out_dict
        out_dict = out_dict.to_dict()

    line = out_dict['line']
    particles = out_dict['particles']
    if line.tracker is None:
        line.build_tracker()
    if type == 'second':
        twiss_dict = dict()
        line_dict = dict()
    # Needed to know the turns
    try:
        n_turns = out_dict['params']['n_turns']
    except:
        print('turns taken from the first particle')
        n_turns = len(out_dict['monitor'].x[0, :])

    if type == 'first':
        print('Extracting sextupoles already active')
        # Tracking 1
        time_before = timing.perf_counter()
        print("> Tracking...")
        for _ in tqdm(range(n_turns)):
            line.track(particles, num_turns=1)
        time_after = timing.perf_counter()
        time_taken = time_after - time_before
        print(f"> Tracking done, {time_taken} seconds elapsed")

        particles_lost_at_each_turn = np.bincount(particles.at_turn)
        print(f'total extracted particles :{np.sum(particles_lost_at_each_turn[:-1])} \n')
        print("! Tracking Complete !")
        if return_time:
            return time_taken

    elif type == 'second':
        #  turns to activate completely the sextupoles
        if sextupoles_turns == None:
            print('turns to activate sextupoles non defined, considering 100 turns')
            sextupoles_turns = 100
        out_dict['params']['dynamic_sextupole'] = sextupoles_turns  #
        xse_names = ['pr.xse01.a', 'pr.xse01.b', 'pr.xse07']
        setter = xt.MultiSetter(line, xse_names, field='k2')  # multisetter obj
        xse0 = setter.get_values()  # initial/nominal values
        it = 0  # counter for the ramp
        ramp = np.linspace(0, 1, sextupoles_turns)
        # 1)Tracking-ramping sextupoles
        time_before = timing.perf_counter()
        print("> Sextupoles adiabatic turning on...")

        for _ in tqdm(range(sextupoles_turns)):
            k2_it = xse0 * ramp[it]
            setter.set_values(k2_it)  # changes of value
            if twiss:
                twiss_dict[f'twiss_{it + 1}'] = line.twiss(method='4d')
            line_dict[f'line_{it + 1}'] = line
            line.track(particles, num_turns=1)
            it += 1
        time_after = timing.perf_counter()
        time_taken = time_after - time_before
        print(f"> sextupoles at nominal value, {time_taken} seconds elapsed")
        if twiss:
            print('calculating twiss')
            out_dict['dynamic_twiss'] = twiss_dict
        out_dict['dynamic_line'] = line_dict

        # 2)Tracking at nominal values
        for _ in tqdm(range(n_turns - sextupoles_turns)):
            line.track(particles, num_turns=1)
        time_after2 = timing.perf_counter()
        time_taken2 = time_after2 - time_before
        print(f"> tracking finished, total time: {time_taken2} seconds")
        particles_lost_at_each_turn = np.bincount(particles.at_turn)
        print(f'total extracted particles :{np.sum(particles_lost_at_each_turn[:-1])} \n')
        if return_time:
            return time_taken+time_taken2


    elif type == 'third':  # EXTRACTION SEXTUPOLES COMPLETELY OFF
        xse_names = ['pr.xse01.a', 'pr.xse01.b', 'pr.xse07']
        # SHOULD TURN OFF ALSO THE EXTRACTION QUADRUPOLEs?!
        setter = xt.MultiSetter(line, xse_names, field='k2')  # multisetter obj
        xse0 = setter.get_values()  # initial/nominal values
        setter.set_values(xse0 * 0)  # set to 0
        ### SHOULD BE RESET TO THE INITIAL VALUE

        # if out:
        #     print('extraction sextupoles off, twiss in outdict replaced')
        #     outdict['twiss'] = line.twiss(method='4d')

        time_before = timing.perf_counter()
        for _ in tqdm(range(n_turns)):
            line.track(particles, num_turns=1)
        time_taken = timing.perf_counter() - time_before
        print(f"> tracking finishes, total time: {time_taken} seconds")
        particles_lost_at_each_turn = np.bincount(particles.at_turn)
        print(f'total extracted particles :{np.sum(particles_lost_at_each_turn[:-1])} \n')
        if return_time:
            return time_taken

    else:  ## FOR A WRONG ENTRY OF THE TYPE PARAMETER
        print('Tracking type not recognized')


def build_particles(line, n_part=1000, DPP_FACTOR=2.35e-3, exn=1.5e-6, eyn=1.5e-6, twiss=None, out_params=False):
    # Bunched is an option that for now I am not using
    if out_params:
        params = locals()
    if twiss is None:
        twiss = line.twiss(method='4d')

    sigmas, sigmas_p = xp.generate_2D_gaussian(int(n_part))

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

    # Debunched creation in the z plane
    z_array = scipy.stats.uniform.rvs(loc=0 - twiss['circumference'] / 2,
                                      scale=twiss['circumference'],
                                      size=int(n_part))
    delta_array = scipy.stats.norm.rvs(loc=0, scale=DPP_FACTOR / 2, size=int(n_part))
    particles.zeta = z_array
    particles.delta = delta_array
    if out_params:
        return particles, params
    else:
        return particles
