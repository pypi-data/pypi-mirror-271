
import numpy as np
import inspect
import xtrack as xt




from . import xsuite_helper as xh




def track(outdict, turns=10):
    x_part = []
    px_part = []
    line = outdict['line']
    particles = outdict['particles']
    for n in np.arange(turns):
        line.track(particles, num_turns=1)
        x_part.append(particles.x)
        px_part.append(particles.px)

    return np.array(x_part).transpose(), np.array(px_part).transpose()



def match_tune(rfko,targetx):
    ''' one of the only functions that has the class paradigm'''
    twiss_bf = rfko.line.twiss(method='4d')
    if rfko.sim_params['targetx'] is not None:
        if (targetx-rfko.sim_params['targetx'])<1e-5:
            pass
            #logger.info(f"The given value is different from the previous->{rfko.sim_params['targetx']} ")
    else:
        if (targetx-6.320)<1e-5:
            pass
            # logger.info(f"The given value is different from the previous->{6.320} ")

    rfko.line.match(method='4d', n_steps_max=30, vary=[xt.Vary('kf', step=1e-9), xt.Vary('kd', step=1e-9)],
                    targets=[xt.Target('qx', targetx, tol=0.000005),
                             xt.Target('qy', twiss_bf.qy, tol=0.005)])

    # logger.debug('twiss before matching is stored in twiss_prev attribute')
    rfko.twiss_prev = twiss_bf
    rfko.twiss = rfko.line.twiss(method='4d')


def matching(outdict, targetx=None ,extraction=True ,qse=False ,bumpers=False):
    ''' TODO
    - add the possibility to match the chromaticity
    '''
    line = outdict['line']
    knobs = ['k1prbhf', 'k1prbhd', 'k2prmp', 'k2prmpj']

    # Value matched to the measurements TUNES OF BARE MACHINE
    vals = [0.05714293659989464, -0.05719922125376693, 0.010731455338789136, -0.019018243990104253]
    for i in range(len(knobs)):
        line.vars[knobs[i]] = vals[i]

    if qse:
        line.vars['kprqse'] = 0.09088224  # Value from LSA try length
    if bumpers:
        line.vars['kpebsw23'] = 0  # from LSA not --> -0.001570859932
        line.vars['kpebsw57'] = 5.544860897340004E-4  # from LSA
    if extraction:
        ####### EXTRACTION UNITS
        line.vars['kpebsw23'] = 0  # from LSA not --> -0.001570859932
        line.vars['kpebsw57'] = 5.544860897340004E-4  # from LSA
        line.vars['kprqse'] = 0.09088224  # Value from LSA try length
        line.vars['kprxse'] = 1.4193310000000103  # value at the steady from LSA

        if targetx is None:  ### STANDARD QXTARGET TUNE {6.32 }

            line.vars['kf'] =  0.002252965399686161
            line.vars['kd'] = -0.009766502523392236
            twiss = line.twiss(method='4d')
            outdict['twiss'] = twiss
            print(f'--> standard value Qx = {twiss.qx}')
        elif targetx =='Not':
            # This leaves everything as it is after activating the extraction elements without changing anything else
            print(f'--> Horizontal Tune just after activating the exctraction elements')
            outdict['twiss'] = line.twiss(method='4d')

        else: # TUNE WITH THE LOW ENERGY QUADRUPOLES
            print(f'-->the target qx is {targetx}')
            line.match(method='4d', n_steps_max=30, vary=[xt.Vary('kf', step=1e-9), xt.Vary('kd', step=1e-9)],
                       targets=[xt.Target('qx', targetx, tol=0.000005), xt.Target('qy', outdict['twiss'].qy, tol=0.005)])
            twiss = line.twiss(method='4d')
            print(f'-->after match {twiss.qx}')
            outdict['twiss'] = twiss



def insert_monitor(line, at_index, n_part=10, n_turns=500, name='monitor'):
    line.unfreeze()
    monitor = xt.ParticlesMonitor(
        num_particles=n_part,
        start_at_turn=0,
        stop_at_turn=n_turns,
        auto_to_numpy=True)

    line.insert_element(index=at_index, element=monitor, name=name)
    return monitor


def build_part(line, A=None,X=None,PX=None ,x_ax=False, px_ax=False,s=None, ramping_sex=False,give_normalized=False,**args):
    """ Building particles at specified amplitudes or at specified, absolute normalized coordinates """
    if (A is None)&((X is None)&(PX is None)): # Sanity check
        print('------give values for A or X and PX-----')
        return None
    if A is not None:
        if isinstance(A,np.float64):
            size = 1
        else:
            size = len(A)

        if x_ax:
            x_n = A
            px_n = np.zeros(size)
        elif px_ax:
            px_n = A
            x_n = np.zeros(size)
        else:
            px_n = A / np.sqrt(2)
            x_n = A / np.sqrt(2)

    elif(X is not None)&(PX is not None): # Thanks to the sanity check there are no other cases
        #assert len(X)==len(PX),'X and PX must be the same length'
        x_n = X
        px_n = PX
    ## A check for the tracker

    if line.tracker is None:
        line.build_tracker()
    if ramping_sex:
        xse_names = ['pr.xse01.a', 'pr.xse01.b', 'pr.xse07']
        setter = xt.MultiSetter(line, xse_names, field='k2')  # multisetter obj
        xse0 = setter.get_values()  # initial/nominal values
        setter.set_values([0., 0., 0.])  # changes of value

    twiss = line.twiss(method='4d')
    betx = twiss.betx[0]
    alfx = twiss.alfx[0]
    xc = twiss.x[0]
    pxc = twiss.px[0]
    x = np.sqrt(betx)*x_n +xc
    px = (px_n-x_n*alfx)/np.sqrt(betx) +pxc
    #px = px_n/np.sqrt(betx)-x*alfx/betx +pxc
    additional_args = {key:val for key,val in args.items() if key in inspect.getfullargspec(line.build_particles).args}
    ## PARTICLE REF ALREADY CREATED WITH THE LINE
    if give_normalized:
        particles = line.build_particles(method='4d', x_norm=x_n, px_norm=px_n,**additional_args)
    else:
        particles = line.build_particles(method='4d', x=x, px=px,**additional_args)

    if ramping_sex:
        setter.set_values(xse0)
    return particles



def octupoles_off(rfko):
    ''' Quite restrictive assumpion that sextupoles are only on multipoles'''
    oct_names_dict = xh.find_multipole_component(rfko.line.to_pandas(), 'octupole')
    ### I know the only octupoles are non zero in the multipoles
    oct_names = oct_names_dict['multipoles']
    setter = xt.MultiSetter(rfko.line, oct_names, field='knl',index=3)  # initialize the setter with the octupoles coordinate
    # val0 = setter.get_values()  # get init values
    setter.set_values(np.zeros(len(oct_names)))  # set to zero
    rfko.twiss = rfko.line.twiss(method='4d')

