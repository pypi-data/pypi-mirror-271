
import logging
import scipy
import inspect
import os
import xtrack as xt
import xpart as xp
import xobjects as xo


from . import line_setup
from . import xsuite_helper as xh
from . import slowex_helper as slwex
from . import phy_helper as ph
from . import utility
#from bare_mach_setup import matching,insert_rfko,insert_septa_monitor

import copy # used only in check_optics
import matplotlib.pyplot as plt # only for check_optics
import numpy as np # only for check_optics
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()








class Rfko:
    '''TODO : 1. changing the parameters of the simulation after the .matching causes problems related to the _check_parameters method,
        due to the turn overriding by the time. So SUPERCAREFUl especially when changing the number of turns
        2. Create rules for the the different simullations type'''

    def __init__(self,line_type='bare_machine',ions=True,E_kin=0.650,logging_level=None,build_line=True,line_dir='mad_file',
                 fast_bare_machine=False,**sim_params):
        ''' By default, it initializes For the energy of the Ions with 650Mev/nucleon
         '''
        self.line_type = line_type
        # BETTER TO KEEP PARAMETER TIED UP IN DICTIONARIES
        # self.ions = ions
        # self.E_kin = E_kin
        self.line_params = dict(E_kin = E_kin,ions = ions)
        self.sim_params = dict(third_frev=1/3,extraction = True,targetx = None,debunched_co=True,n_part=1000,
                    n_turns=1000,DPP_FACTOR=2.35e-3, exn=2.64399538e-06, eyn= 4.252611276914e-07,
                    SEPTA_X_MM=-60,freq_start_ratio=90/100,freq_end_ratio=110/100,gain=0,sampling_freq=1e9,
                    duration=1/1000,time=None,chirp_type='linear',emittance_norm=True,ctx = xo.ContextCpu())
        keys = self.sim_params.keys()
        self.sim_params.update({key: val for key,val in sim_params.items() if key in keys})


        self.sim_type = 'static' # 'ramping_sex', 'quad_ripples', 'quad_ripples_ramping_sex' for now these are the allowe type


        ################################# LOGGING
        if logging_level is None: # This way is definitely not the best
            self.logging_level = 'INFO'
        else:
            self.logging_level = logging_level
        if 'logger' not in self.__dict__:
            self.logger = logger
        if 'handler' not in self.__dict__:
            # To prevent stupid bugs of the logging module
            self.handler = handler
            self.handler.setLevel(self.logging_level)
            self.logger.addHandler(self.handler)

        self.logger.setLevel(self.logging_level)
        self.logger.info(f"logger instance level is set to {self.logging_level}, to change it use the method set_logging")
        self.logger.info('By default line is built at initialization, otherwise use build_line=False')
        if build_line:
            self.build_line(dir=line_dir,fast_bare_machine=fast_bare_machine)

    def set_logging(self,level):
        allowed_string= ['INFO','DEBUG','WARNING','ERROR','CRITICAL']
        allowed_digit = [10,20,30,40,50]
        assert (level in allowed_string)|(level in allowed_digit), 'The level is not recognized'
        self.logger.setLevel(level)
        self.handler.setLevel(level)


    def set_simulation_params(self,interactive=False,param_dict=None):
        nolist = ['N','No','n','no']
        if interactive:
            self.logger.info('Choice, use N for skipping the choice')
            for key,val in self.sim_params.items():
                Type = type(val)
                inp = input(f'Actual : {key}= {val}-->')
                if inp in nolist:
                    continue
                else:
                    # The following CAN THROW AN ERROR IF THE TYPE CANNOT BE TRANSFORMED
                    self.sim_params[key] = Type(inp) # This takes care of teìhe input type
        else:
            assert param_dict is not None, 'Enter a dictionary'
            assert set(self.sim_params.keys())==set(param_dict.keys()), 'The entered dictionary is not compatible'
            self.sim_params = param_dict

    def _check_params(self):
        ''' Check internal consistency of params
        - between params
        - params-against other attibutes and their properties
        TODO - check targetx with twiss, - septa presence with SEPTA_X_MM - n_turns/n_part  with Monitor
            - HENON MAP CASE

        :return:
        '''
        rfko_params = ['duration','sampling_feq','freq_start_ratio','freq_end_ratio','chirp_type']
        henon_exclude = ['SEPTA_X_MM','debunched_co','third_frev']

        assert 'twiss' in self.__dict__, 'No twiss, Matching method has not been called?'
        # The same parameter is interpreted as normalize em or not depending on the value of
        # 'emittance_norm'
        if self.sim_params['emittance_norm']:
            self.sim_params['ex'] = self.sim_params['exn']/(self.line_params['gamma']*self.line_params['beta'])
            self.sim_params['ey'] = self.sim_params['eyn']/(self.line_params['gamma']*self.line_params['beta'])
        else:
            self.logger.info(f'The emittance in the sim_params attribute is considered as non-normalized')
            self.sim_params['ex'] = self.sim_params['exn']
            self.sim_params['ey'] = self.sim_params['eyn']

        trev = self.twiss['T_rev0']
        self.sim_params['revT'] = trev
        if self.sim_params['time'] is not None:
            self.sim_params['n_turns'] =self.sim_params['time']/trev
            self.logger.info(f"Time parameter ovveride number of turns = {self.sim_params['n_turns']}")
        else:
            self.sim_params['time']= self.sim_params['n_turns']*trev

        allowed_sim_type =   ['static' ,'ramping_sex', 'quad_ripples', 'quad_ripples_ramping_sex']
        while self.sim_type not in ['static' ,'ramping_sex', 'quad_ripples', 'quad_ripples_ramping_sex']:
            self.logger.error(f'Simulation type : {self.sim_type} not recognized')
            inp = input(f'type one of the recognized ones : {allowed_sim_type}')
            self.sim_type=inp

        if self.sim_type in ['quad_ripples','quad_ripples_ramping_sex']:
            self.logger.warning('Quadruole ripples not implemented yet, change to static or ramping_sex')

    def build_line(self,dir='mad_file',madout=False,print_info=False,fast_bare_machine=False,**kwargs):
        ''' Load the bare machine madx files, defining the energy of the beam, creates the line object (attribute line)'''
        assert (self.line_type=='bare_machine')|(self.line_type=='henon_map'), self.logger.error('Only bare_machine and henon_map are viable options')
        ### PATH CHECK
        if (self.line_type=='bare_machine')&(not os.path.exists(dir)):
            path = utility.search_folder('.', dir)
            assert path is not None, f'No {dir} such folder found, can t find the mad file to initialize the line'
        ## IMPORT FROM DF -- FASTER (only standard values allowed)
        if (fast_bare_machine) & (self.line_type=='bare_machine'):
            self.logger.info('OPTION FAST, IMPORT FROM JSON --- STILL TO TEST----NOT WORKING '
                             'only valid for standard beam energy: ion with Enucl = 650 Mev params of beam energy')
            self.line_params.update(ph.energy())
            self.line = xt.Line.from_json(f'{dir}/bare_mach_line.json')
            return None

        elif self.line_type=='bare_machine':
            if os.path.exists(dir): # REMOVE THIS CHECK FOR REDUNDANCY
                lined = line_setup.build_line_baremachine(E_nucleons=self.line_params['E_kin'],dir=dir,
                                                          ions=self.line_params['ions'],
                                                          madout=madout,print_info=print_info)
            else:
                path = utility.search_folder('.',dir)
                assert path is not None, f'No {dir} such folder found, can t find the mad file to initialize the line'
                lined = line_setup.build_line_baremachine(E_nucleons=self.line_params['E_kin'], dir=path,
                                                              ions=self.line_params['ions'],
                                                              madout=madout, print_info=print_info)
        if self.line_type=='henon_map':
            arguments = {key:val for key,val in kwargs.items()
                         if key in inspect.getfullargspec(line_setup.henon_map_line).args}
            if len(arguments.keys())==0:
                self.logger.info('Henon map initialized with default values, look at setup values to know which ones')
            lined = line_setup.henon_map_line(**arguments)
            self.henon_params = lined['henon_params']

        self.line = lined['line']
        self.line_params.update(lined['params'])

    def matching(self,tune_knobs0=None,extraction_eles = True,targetx = None,kd=None,kf=None):
        ''' 1. Match bare machine to the measure tunes and chromaticity (using the specified tune_knobs, Default is reccomended)
            2. Activate extraction elements to measured values (option extraction_eles to skip this)
            3. Fine tune the final desired HORIZONTAL tune (to the targetx value)
            -----------------
            TODO: 1. GENERAL KNOBS, 2. QUICK REFERENCE TO THE MEASURED TUNES,
                '''
        assert self.line_type!='henon_map', ('With the Henon map is not possible to match, '
                                             'gives directly the values you need to the method build_line')
        if targetx is not None:
            self.sim_params['targetx'] = targetx
        if tune_knobs0 is None:
            tune_knobs0 = ['k1prbhf', 'k1prbhd', 'k2prmp', 'k2prmpj']
        else:
            self.logger.error('Not implemented for custom knobs yet')

        # Value matched to the measurements TUNES OF BARE MACHINE
        vals = [0.05714293659989464, -0.05719922125376693, 0.010731455338789136, -0.019018243990104253]
        self.logger.debug(f'Use the {tune_knobs0} to match the tunes and chromas values measured in CHIMERA')
        for i in range(len(tune_knobs0)):
            self.line.vars[tune_knobs0[i]] = vals[i]

        if extraction_eles:
            ####### EXTRACTION UNITS
            self.line.vars['kpebsw23'] = 0  # from LSA not --> -0.001570859932
            self.line.vars['kpebsw57'] = 5.544860897340004E-4  # from LSA
            self.line.vars['kprqse'] = 0.09088224  # Value from LSA try length
            self.line.vars['kprxse'] = 1.4193310000000103  # value at the steady from LSA
            # no if
            twiss_bf_leq = self.line.twiss(method='4d')
            self.logger.debug(f'After the activation of extraction elements the tune is = {round(twiss_bf_leq.qx,6)}')

            if self.sim_params['targetx'] is None:  ### STANDARD QXTARGET {6.32 }
                if (kd is not None)|(kf is not None):
                    self.logger.info('params directly given!')
                    self.line.vars['kf'] = kf
                    self.line.vars['kd'] = kd
                    std_target = False
                else:
                    self.line.vars['kf'] = 0.002252965399686161
                    self.line.vars['kd'] = -0.009766502523392236
                    std_target=True

                twiss = self.line.twiss(method='4d')
                self.twiss = twiss
                self.logger.info(f'The tune will be used : {twiss.qx}')
                if std_target:
                    self.sim_params['targetx']=6.32
                else:
                    self.sim_params['targetx'] = round(twiss.qx,5)
            else:
                # IF NOT USING DEFAULT VALUES, or specified values, It actually does the matching
                self.line.match(method='4d', n_steps_max=30, vary=[xt.Vary('kf', step=1e-9), xt.Vary('kd', step=1e-9)],
                           targets=[xt.Target('qx', self.sim_params['targetx'], tol=0.000005),
                                    xt.Target('qy', twiss_bf_leq.qy, tol=0.005)])
                twiss = self.line.twiss(method='4d')
                self.logger.info(f'The target qx is {targetx} --> After match {twiss.qx}')

                self.twiss = twiss
        else:
            if self.sim_params['targetx'] is not None:
                twiss_bf = self.line.twiss(method='4d')
                self.line.match(method='4d', n_steps_max=30, vary=[xt.Vary('kf', step=1e-9), xt.Vary('kd', step=1e-9)],
                                targets=[xt.Target('qx', self.sim_params['targetx'], tol=0.000005),
                                         xt.Target('qy', twiss_bf.qy, tol=0.005)])
            elif (kd is not None)&(kf is not None):
                self.logger.info('params directly given!')
                self.line.vars['kf'] = kf
                self.line.vars['kd'] = kd
            else:
                self.line.vars['kf'] = 0.002252965399686161
                self.line.vars['kd'] = -0.009766502523392236
                self.logger.info('standard value for kf and kd, which for extraction line would give tunex = 6.32')

            self.logger.warning('The extraction element are not activated')
            self.twiss = self.line.twiss(method='4d')
            self.logger.info(f'Tunes : qx={self.twiss.qx}, qy={self.twiss.qy} || Chromaticities : dqx={self.twiss.dqx}, dqy={self.twiss.dqy}')
            self.sim_params['targetx']=self.twiss.qx
        # I COULD CALL A CHECK PARAMS HERE!
        self._check_params()


    def insert_monitor(self,at_index='pe.smh57',name='SEPTA_MONITOR',start_at_turn=0,
                       stop_at_turn=None,num_particles=None,at_s=None,**monitor_args):

        if stop_at_turn is None:
            stop_at_turn = self.sim_params['n_turns']
        if (num_particles is None)&('particle_id_range' not in monitor_args.keys()):
            num_particles= self.sim_params['n_part']
        # probably needed :
        # assert (num-particles is None('particle_id_range' not in monitor_args.keys())
        if at_s is not None:
            at_index = None

        monitor = xt.ParticlesMonitor(
            num_particles=num_particles,start_at_turn=start_at_turn,
            stop_at_turn=stop_at_turn,auto_to_numpy=True,**monitor_args)

        if self.line_type=='henon_map':
            at_s = None
            at_index = 'Henon_sextupole'
        monitor.placed_at_element = at_index # This is not a predefined attribute of the monitor class but it is actualy quite important in practice
        self.line.unfreeze()
        self.line.insert_element(index=at_index, at_s=at_s,element=monitor, name=name)
        self.monitor = monitor

    def insert_rfko(self,name='EXCITER',at_index='pr.kfb97',**rfko_args):
        ############## shortening the notation
        pc = self.line_params['pc']
        beta = self.line_params['beta']
        Brho = self.line_params['Brho']
        charge = self.line_params['charge']
        duration = self.sim_params['duration']
        sampling_freq = self.sim_params['sampling_freq']
        # Kick angle
        max_kick_angle = slwex.kick_angle(self.sim_params['gain'],Brho,pc,beta,charge)
        self.sim_params['kick_angle'] = max_kick_angle
        frev = 1/self.twiss['T_rev0']
        # FREQUANCIES SCANNED
        start_freq = frev * self.sim_params['freq_start_ratio'] * self.sim_params['third_frev']
        end_freq = frev * self.sim_params['freq_end_ratio'] * self.sim_params['third_frev']
        if self.sim_params['chirp_type'] == 'linear':
            t, chirp_signal = ph.generate_chirp(start_freq, end_freq, duration, sampling_freq)
        else:
            t, chirp_signal = ph.generate_chirp_non_linear(start_freq, end_freq, duration, sampling_freq)

        self.line.unfreeze()

        # Exciter config; the duration parameter tells it to repeat the chirp_signal
        # PROBLEM WITH TIME!
        rfko_exciter = xt.Exciter(
            _context=self.sim_params['ctx'],
            samples=chirp_signal,
            sampling_frequency=sampling_freq,
            frev=frev,
            duration=float(self.sim_params['time']),
            start_turn=0,
            knl=[max_kick_angle]
        )

        self.line.insert_element(
            element=rfko_exciter,
            name=name,
            index= at_index
        )
        self.exciter = rfko_exciter


    def insert_septa(self,at_index='pe.smh57',name='SEPTUM'):
        septum = xt.LimitRect(
            min_x=self.sim_params['SEPTA_X_MM'] * 0.001)
        self.line.unfreeze()
        self.line.insert_element(element=septum,name=name,index=at_index)

    def build_particles(self):
        ''' TODO : 1.QUAD_RIPPLES+RAMPING_SEX CASE not considered yet'''
        # EASIER TO TREAT IN A COMPLETELY DIFFERENT WAY THIS CASE
        if self.line_type=='henon_map':
            delta_array = scipy.stats.norm.rvs(loc=0, scale=self.sim_params['DPP_FACTOR'],
                                               size=int(self.sim_params['n_part']))
            # To remove orbit x at the sextupole ?
            sigmas, sigmas_p = xp.generate_2D_gaussian(int(self.sim_params['n_part']))
            if self.line.tracker is None:
                self.line.build_tracker(self.sim_params['ctx'])
            particles = self.line.build_particles(
                method='4d',
                delta=delta_array,
                nemitt_x=self.sim_params['exn'],
                nemitt_y=self.sim_params['eyn'],
                x_norm=sigmas,
                px_norm=sigmas_p,
                y_norm=sigmas,
                py_norm=sigmas_p,
            )
            self.particles = particles
            self.logger.info('DONE')
            return None


        if self.sim_type == 'ramping_sex':
            xse_names = ['pr.xse01.a', 'pr.xse01.b', 'pr.xse07']
            setter = xt.MultiSetter(self.line, xse_names, field='k2')  # multisetter obj
            xse0 = setter.get_values()  # initial/nominal values
            setter.set_values([0., 0., 0.])  # changes of value

        twiss_df = self.twiss.to_pandas()
        sigmas, sigmas_p = xp.generate_2D_gaussian(int(self.sim_params['n_part']))

        z_array = scipy.stats.uniform.rvs(loc=0,
                                          scale=self.twiss['circumference'],
                                          size=int(self.sim_params['n_part']))

        # momentum off set will be gauss distributed along zero and DPP_FACTOR will be the standard deviation
        delta_array = scipy.stats.norm.rvs(loc=0, scale=self.sim_params['DPP_FACTOR'], size=int(self.sim_params['n_part']))
        if self.sim_params['debunched_co']:
            # Transport the particles along the line adding the orbit distortion to each point
            sigmas, sigmas_p = xh.nearest_betx(twiss_df, sigmas, sigmas_p, z_array)
        if self.line.tracker is None:
            self.line.build_tracker(self.sim_params['ctx'])
        # match_at_s=z_array, # instead of zeta
        # at_element='ps$start', # because of the previous is needed
        particles = self.line.build_particles(
            method='4d',
            zeta=z_array, # instead of zeta
            delta=delta_array,
            nemitt_x=self.sim_params['exn'],
            nemitt_y=self.sim_params['eyn'],
            x_norm=sigmas,
            px_norm=sigmas_p,
            y_norm=sigmas,
            py_norm=sigmas_p,
        )
        # particles.zeta = z_array
        # particles.delta = delta_array
        if self.sim_type == 'ramping_sex':
            # RESET THE LINE TO THE NOMINAL VALUES
            setter.set_values(xse0)

        self.particles = particles


    def build_particles_custom(self,A=None,X=None,PX=None,xaxis=False,pxaxis=False,s=None,denormalize =True,**args):
        '''
        Building particles at custom position either specifying an amplitude or specific coordinates.
        By default the coordinates are considered in the normalized phase space and for avoiding giving an emittance
        (for few particles it is not a real 'meaningful' parameter) they are DENORMALIZED and then fed.
        :param A: amplitudes in the normalized phase space of the generated particles
        :param X: X coordinate in Normalized and centered reference system
        :param PX: PX coordinate in Normalized and centered reference system
        :param xaxis: (only if A is given) if true particles lying on xaxis
        :param pxaxis: same as previous
        :param s:
        :param args:
        :return:
        '''
        assert (A is not None) | ((X is not None) & (PX is not None)), self.logger.error('No coordinates specified')  # Sanity check

        if A is not None: # AMPLITUDES GIVEN
            if isinstance(A, np.float64):
                size = 1
            else:
                size = len(A)
            if xaxis:
                x_n = A
                px_n = np.zeros(size)
            elif pxaxis:
                px_n = A
                x_n = np.zeros(size)
            else:
                px_n = A / np.sqrt(2)
                x_n = A / np.sqrt(2)
            if s is not None:
                assert len(s) ==size

        else: # Coordinates given

            assert (X is not None)&(PX is not None),'Both coordinates needed X,PX'
            if (not isinstance(X,np.float64))|(not isinstance(PX,np.float64)):
                assert len(X)==len(PX), 'Different sizes not allowed'
            else:
                assert (isinstance(X,np.float64))&(isinstance(PX,np.float64)),\
                    'one is a single number and the other not, pay attention that both are float'
            x_n = X
            px_n = PX

        if self.line.tracker is None:
            self.line.build_tracker()
        if (self.sim_type == 'ramping_sex')&(self.line_type!='henon_map'):
            xse_names = ['pr.xse01.a', 'pr.xse01.b', 'pr.xse07']
            setter = xt.MultiSetter(self.line, xse_names, field='k2')  # multisetter obj
            xse0 = setter.get_values()  # initial/nominal values
            setter.set_values([0., 0., 0.])  # changes of value
            self.twiss = self.line.twiss(method='4d')

        if ('twiss' not in self.__dict__)&(self.line_type!='henon_map'):
            self.twiss = self.line.twiss(method='4d')
        # Assumes all the particles are generates at the sape position along the line
        if s is None:
            s = np.zeros(size)
        if (denormalize)|(A is not None):
            # if A is given it is always considered in the normalized space and referred to the closed orbit
            x, px = xh.DEnormalize_points(self, X=x_n, PX=px_n, at_s=s[0])
        else:
            x = x_n
            px = px_n

        additional_args = {key: val for key, val in args.items() if
                           key in inspect.getfullargspec(self.line.build_particles).args}

        particles = self.line.build_particles(method='4d', x=x, px=px,zeta=s, **additional_args)

        self.particles= particles
        if (self.sim_type == 'ramping_sex')&(self.line_type!='henon_map'):
            setter.set_values(xse0)
            self.twiss = self.line.twiss(method='4d')


    def setup_line(self,rfko=True,monitor=True,septa=True,build_particles=True):
        message = ''
        if ('twiss' not in self.__dict__)&(self.line_type!='henon_map'):
            self.matching()
            message+= 'Matching'
        if self.line_type=='henon_map':
            septa = False
            rfko= False

        if monitor:
            self.insert_monitor()
            message= message+'-monitor'
        if septa:
            self.insert_septa()
            message= message+'-septa'
        else:
            # For avoiding the plot of it in plotting1.plot_flex
            self.sim_params['SEPTA_X_MM']= None
        if rfko:
            self.insert_rfko()
            message= message+'-rfko'
        if self.line.tracker is None:
            self.line.build_tracker(self.sim_params['ctx'])
        if build_particles:
            self.build_particles()
            message= message+'-built_particles'

        self.logger.info(f'{message}  at default positions and names')

    def to_dict(self,monitor=None,particles=None):
        ''' The cases considered are few because the dictionary can always be changed in another moment
        - Monitor: is None or a monitor given
        - Particles: is true or false (this is what it seems I use more
        TODO: automaticaòòy considering if the elemnts are presents'''
        if ('monitor' not in self.__dict__)&(monitor is None):
            monitor = None
        elif monitor is None:
            monitor = self.monitor
        if (particles is None)&('particles' not in self.__dict__):
            particles = None
        elif particles is None:
            particles = self.particles
        if ('twiss' not in self.__dict__)&(self.line_type!='henon_map'):
            self.logger.debug('twiss not present, calculated now')
            self.twiss = self.line.twiss(method='4d')
        if self.line_type=='henon_map':
            outdict = dict(line=self.line, henon_params=self.henon_params, params=self.sim_params, line_params=self.line_params)
        else:
            outdict = dict(line=self.line,twiss=self.twiss,params=self.sim_params,line_params=self.line_params)
        if monitor is not None:
            outdict['monitor'] = monitor
        if particles is not None:
            outdict['particles'] = particles
        return outdict

    # def to_dict__(self, monitor=None, particles=True):
    #     ''' The cases considered are few because the dictionary can always be changed in another moment
    #     - Monitor: is None or a monitor given
    #     - Particles: is true or false (this is what it seems I use more
    #     TODO: automaticaòòy considering if the elemnts are presents'''
    #     if ('monitor' not in self.__dict__) & (monitor is None):
    #         monitor = None
    #     if (particles is None) & ('particles' not in self.__dict__)
    #
    #     elif particles & (monitor is None):
    #
    #         return dict(line=self.line, twiss=self.twiss,
    #                     params=self.sim_params, monitor=self.monitor,
    #                     particles=self.particles)
    #
    #     elif (particles is False) & (monitor is None):
    #         return dict(line=self.line, twiss=self.twiss,
    #                     params=self.sim_params, monitor=self.monitor,
    #                     )
    #     elif (particles is False) & (monitor is not None):
    #         return dict(line=self.line, twiss=self.twiss,
    #                     params=self.sim_params, monitor=monitor)
    #     elif particles & (monitor is not None):
    #         return dict(line=self.line, twiss=self.twiss,
    #                     params=self.sim_params, monitor=monitor,
    #                     particles=self.particles)

    def check_optics(self,plot=True):
        ''' A sanity check for the linear optics. It makes a small tacking to insure circles in the normalize phase space'''
        line = self.line.copy()
        # Turn off the bumpers and extraction  components
        line.vars['kpebsw23'] = 0
        line.vars['kpebsw57'] =0
        line.vars['kprqse'] = 0
        line.vars['kprxse'] = 0
        sigmas, sigmas_p = xp.generate_2D_gaussian(int(self.sim_params['n_part']))

        line.unfreeze()
        monitor = xt.ParticlesMonitor(
            num_particles=50,
            start_at_turn=0,
            stop_at_turn=100,
            auto_to_numpy=True)
        line.insert_element(index='ps$start', element=monitor, name='check_opt')
        if line.tracker is None:
            line.build_tracker(self.sim_params['ctx'])

        particles = line.build_particles(
            method='4d',
            x=sigmas,
            px=sigmas_p,
            y=sigmas,
            py=sigmas_p,
        )

        line.track(particles,num_turns=100)
        if self.line_type!='henon_map':
            Monitor = xh.Normalize_monitor(dict(line=line,monitor=monitor,
                                            twiss=line.twiss(method='4d')),
                                            at_element='ps$start')


        Radius = np.sqrt(Monitor.x**2+Monitor.px**2)
        self.logger.debug(f"the shape of the radius matrix is {Radius.shape}")
        # if plot:
        #     fig,ax = plt.subplots(2,1,figsize=(10,8),height_ratios=[2,1])
        #     ax[0].set_aspect('equal')
        #     ax[0].scatter(Monitor.x,Monitor.px)
        #     ax[1].plot(Radius[0,:]) # plotting only one particle?
        if plot:
            fig,ax = plt.subplots(figsize=(10,10))
            ax.set_aspect('equal')
            ax.scatter(Monitor.x,Monitor.px)

        else :
            return Radius

    def add_kick_checks(self,start_at_turn=0,stop_at_turn=None,num_particles=None,**monitor_args):
        '''Adding 2 monitor just before and after the rfko exciter to check if the kick is as expected'''
        if stop_at_turn is None:
            stop_at_turn = self.sim_params['n_turns']
        if (num_particles is None)&('particle_id_range' not in monitor_args.keys()):
            num_particles= self.sim_params['n_part']

        #probably needed :
        # assert (num-particles is None('particle_id_range' not in monitor_args.keys())

        monitor_bf = xt.ParticlesMonitor(
            num_particles=num_particles,start_at_turn=start_at_turn,
            stop_at_turn=stop_at_turn,auto_to_numpy=True,**monitor_args)
        monitor_aft = xt.ParticlesMonitor(
            num_particles=num_particles,start_at_turn=start_at_turn,
            stop_at_turn=stop_at_turn,auto_to_numpy=True,**monitor_args)
        self.line.unfreeze()
        self.line.insert_element(element= monitor_bf,name='kickm_bf',index='drift_pr.kfb97..1')
        self.line.insert_element(element= monitor_aft,name='kickm_aft',index='drift_pr.kfb97..2')
        self.kick_monitors = [monitor_bf,monitor_aft]