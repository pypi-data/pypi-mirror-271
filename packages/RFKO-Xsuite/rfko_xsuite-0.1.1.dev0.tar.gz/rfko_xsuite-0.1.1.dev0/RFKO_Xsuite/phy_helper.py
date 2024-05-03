import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, get_window
from scipy.fft import fft, fftfreq, fftshift
from scipy.signal import find_peaks


def energy(ions=True,E_nuc=.650,E_prot=24):
    ''' All energies in [Gev]
    :param ions: if False considers Protons
    :param E_nuc: Kinetic energy per nucleons
    :return:
    '''
    m_proton_GeV = 0.938272088160
    if ions:
        # Ion properties lead
        A = 208.0
        Z = 82.0
        N = 126.0
        charge = 54.0
        m_neutron_GeV = 0.93957
        m_electron_GeV = 0.000511
        m_u_GeV = 0.9315  # Mean Nucleon mass empirical

        # Mass defect = mass of all constituents - atomic mass
        mass_defect_GeV = Z * m_proton_GeV + N * m_neutron_GeV + (Z - charge) * m_electron_GeV- A * m_u_GeV
        # real mass = mass of actual contituents - mass defect
        E_0 = Z * m_proton_GeV + N * m_neutron_GeV  + (Z - charge) * m_electron_GeV - mass_defect_GeV
        E = E_0 + E_nuc * A
        gamma = E / E_0
        beta = np.sqrt(1 - 1 / gamma ** 2)
        pc = beta * E  ## Gev
        Brho = pc*3.3356/54 #Brho in Tm
        return dict(E_0 = E_0, E_tot = E,beta = beta,gamma = gamma,pc=pc,ions=ions,Brho=Brho,charge=charge)
    else: # Protons
        charge = 1
        E_0 = m_proton_GeV
        E = E_0+ E_prot
        gamma = E/E_0
        beta = np.sqrt(1 - 1 / gamma ** 2)
        pc = beta * E
        Brho = pc * 3.3356 # Brho in Tm
        return dict(E_0=E_0, E_tot=E, beta=beta, gamma=gamma,pc=pc,ions=ions,Brho=Brho,charge=charge)


def twiss_parameters_from_distribution(x, xp):
    """
    This function calculates the Twiss parameters (beta, alpha, gamma) and emittance
    given a distribution of position (x) and angle (xp).

    Args:
        x (numpy.array): A distribution of position
        xp (numpy.array): A distribution of angle

    Returns:
        beta (float): Beta Twiss parameter
        alpha (float): Alpha Twiss parameter
        gamma (float): Gamma Twiss parameter
        epsilon (float): Emittance
    """

    # Calculate averages
    mean_x = np.mean(x)  # average position
    mean_xp = np.mean(xp)  # average angle

    # Calculate second moments
    mean_xx = np.mean(x ** 2)  # second moment of position
    mean_xxp = np.mean(x * xp)  # cross moment
    mean_xpxp = np.mean(xp ** 2)  # second moment of angle

    # Calculate geometric emittance
    # This is done using the formula for geometric emittance, which is the square root of
    # the determinant of the second moment matrix of (x, xp)
    epsilon = np.sqrt(mean_xx * mean_xpxp - mean_xxp ** 2)

    # Calculate Twiss parameters
    beta = mean_xx / epsilon  # Beta is the variance of position divided by emittance
    alpha = -mean_xxp / epsilon  # Alpha is the negative covariance divided by emittance
    gamma = mean_xpxp / epsilon  # Gamma is the variance of angle divided by emittance

    return dict(beta=beta, alpha=alpha, gamma=gamma, epsilon=epsilon)

# Chirps
def generate_chirp(start_freq, end_freq, duration, fs):
    # Time array
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    # Generate chirp signal
    chirp_signal = chirp(t, start_freq, duration, end_freq)

    return t, chirp_signal

# Chirp
def generate_chirp_non_linear(start_freq, end_freq, duration, fs):
    # Time array
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)

    # Half duration
    half_duration = duration / 2

    # Generate two halves of chirp signal
    chirp_signal_first_half = chirp(t[:int(fs * half_duration)], start_freq, half_duration, end_freq)
    chirp_signal_second_half = np.zeros_like(t[int(fs * half_duration):])

    # Concatenate the two halves
    chirp_signal = np.concatenate((chirp_signal_first_half, chirp_signal_second_half))

    return t, chirp_signal


def Ft(signal, time_int, figsize=(10, 8),plot=True,peaks=1,ret_freqs=False,fig_ax=None,verbose=False,
       normalize_dc=False,remove_dc=False,starting_bin=3,bar_plot=False,window='hann'):
    ''' Fourier transform of a signal, taking only positive frequencies'''

    if window is not None:
        ## Suppose it's a valid name for a window type
        window_names = ['boxcar', 'triang', 'blackman', 'hamming', 'hann', 'bartlett',
                        'flattop', 'parzen', 'bohman', 'blackmanharris', 'nuttall', 'barthann']
        assert window in window_names, (f'The window type doesn t correspong to a valid window, '
                                        f'for instance {window_names}')
        Window = get_window(window,len(signal))
        signal = signal * Window
        print('the signal is being windowed')
    yf = fft(signal)
    xf = fftfreq(len(signal), time_int)

    # Using from zero on and only absolute vals
    xf__ = xf[np.argsort(xf)]
    yf__= np.abs(yf[np.argsort(xf)])
    zero_index = len(xf) // 2
    xf = xf__[zero_index:]
    yf = yf__[zero_index:]

    if remove_dc:
        print('remove_dc is not used, use starting_bin tu exclude the firsts instead')
        #just removing the first bins in the plot

    if normalize_dc:
        yf = yf / np.max(yf[0])

    if plot:
        if fig_ax is not None:
            ax = fig_ax
        else:
            fig, ax = plt.subplots(figsize=figsize)
        if bar_plot:
            # barplot
            ax.bar(xf[starting_bin:],yf[starting_bin:],width=xf[1],edgecolor='black')
            ax.set_xlabel("freq [Hz]")
            ax.set_ylabel("Amplitude [arb.]")
        else:
            # lineplot of the fft
            ax.plot(xf[starting_bin:], yf[starting_bin:])
            ax.xaxis.set_tick_params(rotation=50)
            ax.set_xlabel("freq [Hz]")
            ax.set_ylabel("Amplitude [arb.]")

    peakind = []
    cnt = 0
    while len(peakind) == 0:
        # find peaks using a threshold in height
        height = 0.001
        if cnt > 10 :
            peakind, prop = find_peaks(np.abs(yf), height=0)
            if verbose:
                print('--> height set to zero')
            break

        peakind, prop = find_peaks(np.abs(yf), height=height)
        if len(peakind) == 0: # if no peak is found it lowers the height threshold
            height = height - height * 80 / 100
            cnt+=1

    fsort = np.argsort(prop['peak_heights'])
    if verbose:
        print(f'--> the {peaks} heighest peaks are in {xf[peakind[fsort[:-1-peaks:-1]]]}')
        print(f'--> their heights {np.abs(yf[peakind[fsort[:-1-peaks:-1]]])}')
    if plot:
        plt.scatter(xf[peakind[fsort[:-1-peaks:-1]]], np.abs(yf[peakind[fsort[:-1-peaks:-1]]]), c='r')
    if ret_freqs:
        return xf, yf,xf[peakind[fsort[:-1-peaks:-1]]]
    return xf, yf





def rotate(x, px, dmu, center_mean=True):
    ''' Rotate a distribution of points in 2D
    - POSITIVE DMU -> ROTATION CLOCK WISE. x,px must be arrays or matrices
    - the center is the mean of all the values at all the turns, even for different particles
        but this works well if the particles are centered'''

    x_mean = np.mean(x)
    px_mean = np.mean(px)
    if center_mean:
        x = x - x_mean
        px = px - px_mean

    rot_matrix = np.array([[np.cos(dmu), np.sin(dmu)], [-np.sin(dmu), np.cos(dmu)]])
    x_rot = x.copy()
    px_rot = px.copy()
    if x.ndim == 2:
        for i in range(x.shape[0]):
            rotated = rot_matrix.dot([x[i, :], px[i, :]])
            if center_mean:
                x_rot[i, :] = rotated[0] + x_mean
                px_rot[i, :] = rotated[1] + px_mean
            else:
                x_rot[i, :] = rotated[0]
                px_rot[i, :] = rotated[1]
    else:
        rotated = rot_matrix.dot([x, px])
        if center_mean:
            x_rot = rotated[0] + x_mean
            px_rot = rotated[1] + px_mean
        else:
            x_rot = rotated[0]
            px_rot = rotated[1]

    return x_rot, px_rot