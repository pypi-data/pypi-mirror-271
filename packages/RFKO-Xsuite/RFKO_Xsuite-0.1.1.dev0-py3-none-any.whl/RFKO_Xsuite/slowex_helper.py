
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap

from . import xsuite_helper as xh
from . import phy_helper as ph
from .Rfko import Rfko

def kobay(x, px, dq=0.005, S=77):
    # x and px must be normalized
    H = 3 * np.pi * dq * (x ** 2 + px ** 2) + 1 / 4 * S * (3 * x * px ** 2 - x ** 3)
    return H

def tri_geom(rfko, interpolate=True,sqrt=True,negate_s=True):
    '''TO ADD DISPERSION CORRECTION
    TODO : BUGS 1. works better wit the wrong correction orbit (betx)
        2. it works better without the interpolation
        3. change of sign also is a problem'''
    if isinstance(rfko,Rfko):
        rfko = rfko.to_dict()


    twiss = rfko['twiss']

    twiss_df = twiss.to_pandas()
    S_str, S_mu = Virtual_sextupole_complete(rfko)  # compute sextupole strength and mu
    if negate_s:
        S_str = - S_str
    argmin = np.argmin(np.abs(twiss_df.mux * 2 * np.pi - S_mu))
    if interpolate:

        betx_old = twiss_df.iloc[argmin]['betx']
        betx = np.interp(S_mu,twiss.mux*2*np.pi,twiss.betx)
        if sqrt:
            Xo_old = twiss_df.iloc[argmin]['x'] / np.sqrt(betx_old)
            Xo = np.interp(S_mu, twiss.mux * 2 * np.pi, twiss.x) / np.sqrt(betx)
        else:
            Xo_old = twiss_df.iloc[argmin]['x'] / betx_old
            Xo = np.interp(S_mu,twiss.mux*2*np.pi,twiss.x)/betx

    else:
        if sqrt:
            betx =  twiss_df.iloc[argmin]['betx']
            Xo = twiss_df.iloc[argmin]['x'] / np.sqrt(betx) # There should be the sqrt on betx, a ctually!
        else:
            Xo = twiss_df.iloc[argmin]['x'] / twiss_df.iloc[argmin]['betx'] # There should be the sqrt on betx, actually!

    # tune
    dq0 = (twiss.qx - 6 - 1 / 3)  # normal as without distorsions and dispersion
    dq = dq0 -S_str * Xo / (2 * np.pi)  # distortion correction--- SIGN CHANGE BECAUSE OF THE DIFFERENCEs IN CONVENTIONS
    if S_str==0:
        Hsep = 0
        ampl_sep=0
    else:
        Hsep = ((4*np.pi*dq)**3) /( S_str**2)
        ampl_sep = np.sqrt(48 * np.pi * np.sqrt(3)) * np.abs(dq / S_str)
    return dict(stable_amp=ampl_sep, tune_distance=dq,S=S_str,S_mu=S_mu,Hsep=Hsep)



def Virtual_sextupole(out_dict, plot=False, figsize=(12, 8)):
    if isinstance(out_dict,Rfko):
        out_dict = out_dict.to_dict()
    # take al sextupoles
    line_df = out_dict['line'].to_pandas()
    twiss_df = out_dict['twiss'].to_pandas()
    Sex = line_df[line_df['element_type'] == 'Sextupole'].copy()
    # initialize a list
    S_list = []
    mux_list = []
    # iter sextupole to extract the parameters
    for x in Sex['name']:

        beta = twiss_df[twiss_df['name'] == x]['betx'].iloc[0]  # BETA --- versione senza float
        k = Sex[Sex['name'] == x]['element'].iloc[
            0].k2  # .iloc serve ad estrarre il valore senno me lo tralla come serie
        # kn = k/rigidity   # normalize the sextupole strength --------------------- PROVO SENZA NORMALIZZARE
        l = Sex[Sex['name'] == x]['element'].iloc[0].length  # same for .iloc
        S = 1 / 2 * k * l * beta ** (3 / 2)
        S_list.append(S)
        mux = twiss_df[twiss_df['name'] == x].mux.iloc[0] * (
                    2 * np.pi)  # CONVERSIONE IN RADIANTI è necessaria perchè mux è in unità di radianti
        mux_list.append(mux)

    S_list_np = np.array(S_list)
    mux_list_np = np.array(mux_list)

    virtual_strength = np.sqrt(
        np.sum(S_list_np * np.cos(3 * mux_list_np)) ** 2 + np.sum(S_list_np * np.sin(3 * mux_list_np)) ** 2)
    virtual_mux = (1 / 3) * np.arctan(
        np.sum(S_list_np * np.sin(3 * mux_list_np)) / np.sum(S_list_np * np.cos(3 * mux_list_np)))

    # POLAR PLOT, NOT WORKING BY NOW (TOO many components anyway)
    if plot:

        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=figsize)
        for i in range(len(mux_list_np)):
            ax.plot([(3 * mux_list_np[i]) % (2 * np.pi), (3 * mux_list_np[i]) % (2 * np.pi)], [0, S_list_np[i]],
                    color='r', linewidth=1)

        ax.plot([virtual_mux, virtual_mux], [0, virtual_strength], color='g', linewidth=1)
    return virtual_strength, virtual_mux


def Virtual_sextupole_complete(out_dict, plot=False, figsize=(12, 8),integrate_k2=True):
    ''' Only on epossible doubt about the function which is: The component K2 are already considering the length??'''
    # take all the sextupoles componentes along the line, hopefully
    if isinstance(out_dict,Rfko):
        out_dict = out_dict.to_dict()

    line_df = out_dict['line'].to_pandas()
    twiss_df = out_dict['twiss'].to_pandas()

    nz_name_dict = xh.find_multipole_component(line_df, order='Sextupole')

    sex_direct = nz_name_dict['direct']
    sex_mult = nz_name_dict['multipoles']
    sex_combf = nz_name_dict['combf_knl']
    sex_quad_knl = nz_name_dict['quad_mult']

    # initialize a list
    S_list = []
    mux_list = []

    # iter sextupole to extract the parameters
    for x in sex_direct:
        # beta = float(twiss_df[twiss_df['name']==x]['betx'])
        beta = twiss_df[twiss_df['name'] == x]['betx'].iloc[0]
        k = line_df[line_df.name == x].element.iloc[0].k2
        # kn = k/rigidity   # normalize the sextupole strength --------------------- It is already normalized
        l = line_df[line_df.name == x].element.iloc[0].length
        S = 1 / 2 * k * l * beta ** (3 / 2)
        S_list.append(S)
        mux = twiss_df[twiss_df['name'] == x].mux.iloc[0] * (2 * np.pi)
        mux_list.append(mux)

    for li in [sex_mult, sex_combf, sex_quad_knl]:
        for x in li:
            beta = twiss_df[twiss_df['name'] == x]['betx'].iloc[0]
            k = line_df[line_df.name == x].element.iloc[
                0].knl[2]
            S = (1 / 2) * k *  beta ** (3 / 2)
            S_list.append(S)
            mux = twiss_df[twiss_df['name'] == x].mux.iloc[0] * (2 * np.pi)  # conversion in radians, mux is in unit of tune cycles
            mux_list.append(mux)

    S_list_np = np.array(S_list)
    mux_list_np = np.array(mux_list)

    if np.sum(S_list)==0:
        print('virtual sextupole  is zero, there are no sextupoles components along the line')
        return 0,0

    virtual_strength = np.sqrt(np.sum(S_list_np * np.cos(3 * mux_list_np)) ** 2 + np.sum(S_list_np * np.sin(3 * mux_list_np)) ** 2)

    virtual_mux = (1/3)*np.arctan(np.sum(S_list_np * np.sin(3 * mux_list_np))/np.sum(S_list_np * np.cos(3 * mux_list_np)))

    # POLAR PLOT
    if plot:
        plt.figure(figsize=figsize)
        fig,ax = plt.subplots(subplot_kw={'projection': 'polar'},figsize=figsize)
        for i in range(len(mux_list_np)):
            ax.plot([(3 * mux_list_np[i]) % (2 * np.pi),(3 * mux_list_np[i]) % (2 * np.pi)], [0,S_list_np[i]], color='r', linewidth=1)
        ax.plot([virtual_mux,virtual_mux],[0,virtual_strength],color='g',linewidth=1)
    return virtual_strength,virtual_mux




def H_amplitude(outdict):
    ''' Action of tracked particles????'''
    Monitor = xh.Normalize_monitor(outdict,center=True,normalize_particles=False,keep_zeroes=True)
    tri_dict = tri_geom(outdict)
    dq = tri_dict['tune_distance']
    # Temporary look for the opposite sign in S, if it is better or not
    S = - tri_dict['S']
    Hvals=[]
    for x in range(Monitor.x.shape[0]):
        Hvals.append(kobay(Monitor.x[x,:],Monitor.px[x,:],S=S,dq=dq))

    return np.array(Hvals)




def kick_angle(gain=1, Brho=None, pc=None, beta=None, charge=None):
    ''' Personal Version of the calculations
    - Errors1 corr : include the charge molteplicity in the electric deflection
    - Error2 corr : calculating the current it add the sqrt(2) factor again

    '''
    # VERSION FOR THE IONS and the energy of the baremachine
    if Brho is None:  # if nothing is given uses the standard energies (Ions 650 Mev/nucl)
        rel_par = ph.energy()
        Brho = rel_par['Brho']  # Tm
        pc = rel_par['pc']  # Gev
        beta = rel_par['beta']
        charge = rel_par['charge']
    # PARAMETER OF TFB
    P = 5e3  # W, TFB peak power / electrode
    Z = 100  # Ohm, TFB impedance / electrode
    L = 935e-3  # m, TFB length
    r = 70e-3  # m, TFB separation

    ## Constants
    mu0 = 4 * np.pi * (10 ** -7)  # H/m, vacuum permeability

    # Electric Field
    Vp = np.sqrt(P * Z * 2)  # peak voltage
    V = Vp * gain
    Efield = V / r  # adjusted for gain

    # Magnetic Field
    I = V / Z  # current corrected? CORR2
    # I = np.sqrt((V ** 2 / Z) / Z * 2)  # current
    Hfield = (2 * I) / (2 * np.pi * r)  # adjusted for gain
    Bfield = Hfield * mu0

    # ANGLE
    theta_M = Bfield * L / (Brho)  # easiest version
    theta_E = np.arctan(charge * Efield * L / (pc * beta * 1e9))  ###  cleaner version CORR1
    theta = theta_E + theta_M


    return theta


def kick_angle_(gain=1, Brho=None, pc=None, beta=None, charge=None):
    ''' TO CHECK BEHAVIOURS

    '''
    # VERSION FOR THE IONS and the energy of the baremachine
    if Brho is None:  # if nothing is given uses the standard energies (Ions 650 Mev/nucl)
        rel_par = ph.energy()
        Brho = rel_par['Brho']  # Tm
        pc = rel_par['pc']  # Gev
        beta = rel_par['beta']
        charge = rel_par['charge']
    # PARAMETER OF TFB
    P = 5e3  # W, TFB peak power / electrode
    Z = 100  # Ohm, TFB impedance / electrode
    L = 935e-3  # m, TFB length
    r = 70e-3  # m, TFB separation

    ## Constants
    mu0 = 4 * np.pi * (10 ** -7)  # H/m, vacuum permeability

    # Electric Field
    # Vp = np.sqrt(P * Z * 2)  # peak voltage
    Vp = np.sqrt(P * Z) # 1000 V
    print(Vp)
    V = Vp * gain
    Efield = V / r  # adjusted for gain

    # Magnetic Field
    I = V / Z  # current corrected? CORR2
    # I = np.sqrt((V ** 2 / Z) / Z * 2)  # current
    # Hfield = (2 * I) / (2 * np.pi * r)  # adjusted for gain
    Hfield = I / (2 * np.pi * r)  # adjusted for gain

    Bfield = Hfield * mu0

    # ANGLE
    theta_M = Bfield * L / (Brho)  # easiest version
    theta_E = np.arctan(charge*Efield * L / (pc * beta * 1e9))  ###  cleaner version CORR1
    theta = theta_E + theta_M
    print(f' theta E {theta_E}')
    print(f' theta M {theta_M}')
    return theta


def transform_to_vs(rfko,monitor=None):
    ''' Transform the particles recorded at a monitor to the virtual sextupole position, Normalizing also
    TODO ROTATING THE PARTICLES TOO'''
    if monitor is not None:
        if hasattr(rfko,'monitor'):
            mon_temp = rfko.monitor
        rfko.monitor = monitor
    assert hasattr(rfko, 'monitor'), 'Missing monitor'

    Monitor = xh.Normalize_monitor(rfko,center=True,normalize_particles=False,keep_zeroes=True)
    tri_g = tri_geom(rfko)
    assert hasattr(rfko.monitor,'placed_at_element'), rfko.logger.error('monitor has no attribute .placed_at_element')
    dmu  = rfko.twiss.mux[rfko.twiss.name==rfko.monitor.placed_at_element]*2*np.pi-  tri_g['S_mu']
    Xr,PXr = ph.rotate(Monitor.x,Monitor.px,dmu=-dmu[0])
    # the angle is positive when rotating FROM the sextupole, but in this casE it is TO the sextupole
    try: # in case the monitor was given I change and then revert the changes
        rfko.monitor = mon_temp
    except:
        pass
    return Xr,PXr

def action_angle(rfko,monitor=None):
    ''' different version, with the formula from Neidemar's presentation'''
    ## Transform to the VS coordinates
    X,PX = transform_to_vs(rfko,monitor=monitor)
    trig = tri_geom(rfko)
    S = trig['S']
    dq = trig['tune_distance']
    H_turns = kobay(X,PX,S=S,dq=dq) # This is for every turn
    action = X**2+PX**2
    # H = np.mean(H_turns,axis=1)
    ## TO COMPLETE
    rfko.logger.info('Version action-angle Neidemar')
    angle = np.arctan(-PX/X) + np.pi/2
    mask = X>0
    rfko.logger.info('Difference?')
    angle[mask] = angle[mask] + np.pi
    return action,angle




