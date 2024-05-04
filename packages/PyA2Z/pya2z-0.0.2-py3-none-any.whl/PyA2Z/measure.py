import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits as F
import scipy as sc
import scipy.signal
from numpy.fft import fft, fftfreq, fftshift, fft2
from numpy.random import SeedSequence
from scipy.stats import chi2
import arviz as az
import pymc as pm
from astropy.timeseries import LombScargle
import astropy.table as tab

plt.rcParams.update({'font.size': 10,'font.family':'serif','axes.linewidth':2,'xtick.labelsize' : 9,
'ytick.labelsize' : 9,'xtick.major.size' : 9,
'ytick.major.size' : 9,'xtick.minor.size' : 5,
'ytick.minor.size' : 5,'ytick.minor.visible': True,'xtick.minor.visible': True,'xtick.top': True,'ytick.right': True,'xtick.direction': 'in','ytick.direction': 'in'})

def model_gauss(f, nu_max, sigma, A, c):
    '''returns a gaussian function = A*np.exp(-(f-nu_max)**2/(2*sigma**2))+c
    f is the array of frequencies and the remaining arguments are parameters'''
    return np.abs(A)*np.exp(-(f-nu_max)**2/(2*sigma**2))+c

def PSD_to_amp(freq, PSD):
    '''Computes the amplitude when provided with the array of frequencies and PSD.
    parameters:
        -freq, array of frequencies
        -PSD, array of the values taken by the PSD
    returns:
        - the array of the amplitudes'''
    fs = freq[-1]*2
    n = len(freq)
    return np.sqrt(n*fs*PSD)

def model_env(f, nu_max, sigma, A, c):
    '''returns a gaussian function = A*np.exp(-(f-nu_max)**2/(2*sigma**2))+c
    f is the array of frequencies and the remaining arguments are parameters'''
    return np.abs(A)*np.exp(-(f-nu_max)**2/(2*sigma**2))*np.sinc(f/(2*f[-1]))**2+c

def numax_to_deltanu(numax):
    '''estimates a rough value of deltanu based on the scaling laws
    parameter:-numax (µHz)
    returns:-deltanu (µHz)'''
    estimate = 0.29*(numax)**(0.77)
    return estimate
    
def deltanu_to_numax(deltanu):
    '''scaling relation providing numax when given deltanu'''
    return 5.45*deltanu**(1/0.77)

def adaptative_box(fcenter):
    '''
    Computes the width of the box in which the PSD of the PSD will be computed.
    Parameters:
        -fcenter, float, central frequency of the box in µHz

    '''
    return 0.6*fcenter**(0.8)

def PSD_from_fits(filename):
    '''This first function allows the user to import fits files into the program:
        parameter: -filename, the name of the fits file
        returns: -the frequency in µHz (array) assuming the fits file is in Hertz
                - The PSD in ppm^2/µHz assuming it is its unity in the fits file'''
    spect, hdr = F.getdata(filename, header=True)
    freq, PSD = zip(*spect)
    if freq[0]==0:
        freq = freq[1::]
        PSD = PSD[1::]
    return np.asarray(freq)*10**6, np.asarray(PSD)

def lc_from_fits(filename):
    '''This first function allows the user to import fits files into the program:
        parameter: -filename, the name of the fits file
        returns: -the times in s (array) assuming the fits file is in days
                - The lc in ppm² assuming it is its unity in the fits file'''
    curve, hdr = F.getdata(filename, header=True)
    t, lc = zip(*curve) 
    return np.asarray(t)*3600*24, np.asarray(lc)*np.sqrt(2)/10**3

def DSP1D(t, X):
    '''properly computes the PSD of a time series DSP1D(t,X)
    parameter:-t, time (or anything playing the same role) array
    -X, time series (or anything playing the same role)array
    returns: -freq
    -PSD
    -t'''
    TF = fft(X)
    h = t[1]-t[0]
    l = fftfreq(len(t), h)
    TF, freq = fftshift(TF), fftshift(l)
    # On multiplie par h^2 (car python ne le prend pas en compte) et divisons par le temps de simulation
    DSP = np.abs(TF)**2*h/len(t)
    return (freq, DSP, t)

def DSP1D_med(t, X):
    '''properly computes the PSD of a time series DSP1D(t,X) with the median dt
    parameter:-t, time (or anything playing the same role) array
    -X, time series (or anything playing the same role)array
    returns: -freq
    -PSD'''
    TF = fft(X)
    h = np.median(t[1::]-t[0:len(t)-1])
    l = fftfreq(len(t), h)
    TF, freq = fftshift(TF), fftshift(l)
    # On multiplie par h^2 (car python ne le prend pas en compte) et divisons par le temps de simulation
    DSP = np.abs(TF)**2*h/len(t)
    return freq, DSP

def lc_to_PSD(t,lc):
    '''computes the PSD of a lightcurve with Fourier transform and dt = median(dt):
        parameters:
            -t, ndarray, array of sampling times in seconds
            -lc, ndarray, array of values in ppm²
        returns:
            -freq, ndarray, in µHz
            -PSD, ndarray, in ppm²/µHz'''
    freq,PSD = DSP1D_med(t,lc)
    return freq[len(freq)//2+1::]*10**6,PSD[len(freq)//2+1::]

def sc_to_lc(t,lc,int_time=29.4*60):
    '''
    Rebins a short cadence in a long cadence timeseries

    Parameters
    ----------
    t : ndarray
        time array in seconds
    lc : ndarray
        lightcurve
    int_time : float, optional
        integration time of the long cadence in seconds. The default is 29.4*60 (29.4min Kepler long cadence).

    Returns
    -------
    new_t : ndarray
        new time array in seconds.
    new_lc : ndarray
        new lightcurve array

    '''
    dt = np.median(t[1::]-t[0:len(t)-1])
    dt_lc = int_time
    n_bin = round(dt_lc/dt)
    if n_bin==0:
        print('Please choose a sampling period greater than the original one')
    new_lc = []
    new_t = []
    for i in range(int(len(lc)/n_bin)):
        new_lc.append(np.sum(lc[i*n_bin:i*n_bin+n_bin]))
        new_t.append(t[i*n_bin])
    return np.array(new_t),np.array(new_lc)/n_bin

def rebinned_PSD(t,lc,int_time=29.4*60):
    '''
    Computes the PSD of the rebin of a lightcurve with greater integration time (example: short cadence to long cadence)

    Parameters
    ----------
    t : ndarray
        time array in seconds.
    lc : ndarray
        lightcurve values.
    int_time : float, optional
        integration time of the long cadence in seconds. The default is 29.4*60 (29.4min Kepler long cadence).

    Returns
    -------
    new_freq : ndarray
        new frequency array.
    new_PSD : ndarray
        resbinned PSD.

    '''
    new_t,new_lc = sc_to_lc(t,lc,int_time=int_time)
    new_freq,new_PSD = lc_to_PSD(new_t,new_lc)
    return new_freq,new_PSD
    
def hl_envelopes_idx(s, dmin=1, dmax=1, split=False):
    """
    Input :
    s: 1d-array, data signal from which to extract high and low envelopes
    dmin, dmax: int, optional, size of chunks, use this if the size of the input signal is too big
    split: bool, optional, if True, split the signal in half along its mean, might help to generate the envelope in some cases
    Output :
    lmin,lmax : high/low envelope idx of input signal s
    """

    # locals min      
    lmin = (np.diff(np.sign(np.diff(s))) > 0).nonzero()[0] + 1 
    # locals max
    lmax = (np.diff(np.sign(np.diff(s))) < 0).nonzero()[0] + 1 
    
    if split:
        # s_mid is zero if s centered around x-axis or more generally mean of signal
        s_mid = np.mean(s) 
        # pre-sorting of locals min based on relative position with respect to s_mid 
        lmin = lmin[s[lmin]<s_mid]
        # pre-sorting of local max based on relative position with respect to s_mid 
        lmax = lmax[s[lmax]>s_mid]

    # global min of dmin-chunks of locals min 
    lmin = lmin[[i+np.argmin(s[lmin[i:i+dmin]]) for i in range(0,len(lmin),dmin)]]
    # global max of dmax-chunks of locals max 
    lmax = lmax[[i+np.argmax(s[lmax[i:i+dmax]]) for i in range(0,len(lmax),dmax)]]
    
    return lmin,lmax
    
def smooth_bkg(freq, PSD, filter_width=0.1):
    '''This function returns an estimate of the background noise of a PSD using the same
    method as the LightKurve library: median filtering
    parameters: -freq array of frequencies in µHz
    -PSD, array of the PSD in ppm^2/µHz
    -filter_width, automatically set to 0.1
    returns: - an array corresponding to the smoothed noise background'''
    count = np.zeros(len(freq), dtype=int)
    bkg = np.zeros_like(freq)
    x0 = np.log10(freq[0])
    corr_factor = (8.0 / 9.0) ** 3
    while x0 < np.log10(freq[-1]):
        # l'array de booléens m agit comme la boîte de taille filter_width qui se déplace au fur et à mesure évitant de faire des slices.
        m = np.abs(np.log10(freq) - x0) < filter_width
        if len(bkg[m] > 0):
            bkg[m] += np.nanmedian(PSD[m]) / corr_factor #correction factor due to the chi squared statistics
            count[m] += 1
        x0 += 0.5 * filter_width
    bkg /= count
    return bkg

def snr_PSD(freq, PSD, remove_peaks=False):
    '''divides the PSD by the smoothed noise background leaving us with the signal to noise ratio
    Parameter:-freq, array of frequencies in micro Hertz
                - PSD in ppm2/µHz'''
    if remove_peaks:
        bkg = smooth_bkg(freq, PSD)
        snr = PSD/bkg
        return peak_remover_1(freq,snr)
    return PSD/smooth_bkg(freq, PSD)
    
def norm_collapse(X, Y, Z):
    '''collapses a 2D function along the Y axis and normalizes it by the number of non 0 elements, that's to say, sums 
    all the contributions on the interval of autocorrelation for each central frequency
    parameters:-X, array of the X values
    -Y, array of the Y values
    -Z array of arrays: Z=f(X,Y)
    returns:-X, same as before
    -A, the collapsed function (1D)'''
    A = []
    nx = len(X)
    ny = len(Y)
    for i in range(nx):
        s = 0
        norm = 0
        for j in range(ny):
            elem = Z[j][i]
            s += elem
            norm += int(not elem==0)
        A.append(s/max(norm,1))
    return X, A

def collapse(X, Y, Z):
    '''collapses a 2D function along the Y axis, that's to say, sums 
    all the contributions on the interval of autocorrelation for each central frequency
    parameters:-X, array of the X values
    -Y, array of the Y values
    -Z array of arrays: Z=f(X,Y)
    returns:-X, same as before
    -A, the collapsed function (1D)'''
    A = []
    for i in range(len(X)):
        s = 0
        for j in range(len(Y)):
            s += Z[j][i]
        A.append(s)
    return X, A

def collapse_2(X, Y, Z):
    '''collapses the 2D autocorrelation (or any function of the same format for that matter) along the Y axis, that's to say, sums 
    all the contributions on the interval of autocorrelation for each central frequency
    parameters:-X, array of the X values
    -Y, array of the Y values
    -Z array of arrays: Z=f(X,Y)
    returns:-X, same as before
    -A, the collapsed function (1D)'''
    A = []
    for i in range(len(X)):
        s = 0
        for j in range(len(Y[i])):
            s += Z[i][j]
        A.append(s)#déja normalisé dans sliding PSD
    return X, A

def smooth(y, box_pts=20):
    '''quick and dirty way of smoothing a function, useful for initial guesses
    smooth(array,box_pts=20)
    parameters:-array of the values of the function
    -box size: size of the convolution filter
    returns: -array of the smoothed function'''
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def hanning(freq, fcenter, deltanuguess, gamma):
    '''Generates an array hanning filter centenred on fcenter and of width gamma*deltanuguess
    parameters:
        - freq, freq array of the frequencies in µHz
        - fcenter, center frequency in µHz
        - deltanuguess, width in µHz
        - gamma, width parameter
    returns:
        - wind, array containing the filter (to be multiplied with the data)'''
    largeur = gamma*deltanuguess
    wind = np.ones(len(freq))
    ind1 = np.where(freq >= fcenter-largeur/2)[0][0]
    ind2 = np.where(freq >= fcenter+largeur/2)[0][0]
    for i in range(len(freq)):
        if i < ind1 or i > ind2:
            wind[i] = 0
        else:
            wind[i] = 0.5+0.5 * \
                np.cos(2*np.pi*(freq[i]-fcenter)/largeur)
    return wind

def hanning_2(freq, fcenter, width):
    '''Generates an array hanning filter centenred on fcenter and of width gamma*deltanuguess
    parameters:
        - freq, freq array of the frequencies in µHz
        - fcenter, center frequency in µHz
        - deltanuguess, width in µHz
        - gamma, width parameter
    returns:
        - wind, array containing the filter (to be multiplied with the data)'''
    largeur = width
    wind = np.ones(len(freq))
    ind1 = np.where(freq >= fcenter-largeur/2)[0][0]
    ind2 = np.where(freq >= fcenter+largeur/2)[0][0]
    for i in range(len(freq)):
        if i < ind1 or i > ind2:
            wind[i] = 0
        else:
            wind[i] = 0.5+0.5 * \
                np.cos(2*np.pi*(freq[i]-fcenter)/largeur)
    return wind

def PSD_to_timeseries(freq, PSD, plot=True):
    '''Computes a believable time series given a PSD with random phase
    parameters:
        -freq, ndarray, array of the frequencies in µHz
        -PSD, ndarray, array of the values taken by the PSD in ppm^2/µHz
        -plot, Boolean, if True plot the time series with the time in days
    returns:
        -time, ndarray, time values in 1/µHz
        -values,ndarray, values taken by the time series'''
    fs = freq[-1]*2
    n = len(freq)
    Amp = np.sqrt(n*fs*PSD)*2
    phase = np.random.rand(len(freq))
    phase = phase*2*np.pi
    phase[0] = 0
    phase[-1] = 0
    Ampc = Amp*np.exp(1j*phase)
    Ampc = Amp
    freq2 = np.concatenate(
        (np.array([freq[0]]), freq[::-1], -freq))
    Amp2 = np.concatenate(
        (np.array([Amp[0]]), Ampc, np.conjugate(Ampc[::-1])))
    values = np.real((np.fft.ifft(Amp2)))
    values = np.fft.ifftshift(values)
    time = np.linspace(0, 1/fs*len(values), len(values))
    if plot:
        figtemps = plt.figure(figsize=(20, 8))
        plt.plot(time*10**6/(3600*24), values)
        plt.xlabel("time (days)")
        plt.ylabel('Amplitude')
        plt.title('Time series')
        plt.legend()
        plt.grid(linestyle='--')
        plt.show()
    return time, values

def acf_matrix(freq, PSD,SNR=False, scaling_rel_deltanu=numax_to_deltanu, gamma=4,fracstep=0.3,fdebut=0.05):
    '''Computes the EACF matrix based on the acf of the inverse FFT of the PSD
    parameters:
        - freq, ndarray, array of the frequencies in µHz
        - PSD, ndarray, array of the values taken by the PSD in ppm^2/µHz
        - scaling_rel_deltanu, function, gives an estimate of dnu given numax based on the scaling relations
        - gamma, float, hanning filter width parameter
        - fracstep, fraction of dnu of which the filter moves every iteration of the acf calculation
        - fdebut, float, central frequency (µHz) at which the matrix begins to be constructed'''    
    if not SNR:
        snr = snr_PSD(freq, PSD)
    else:
        snr = PSD
    Z = []
    X = []
    fcenter = fdebut
    deltanuguess = scaling_rel_deltanu(fcenter)
    largeur = max(gamma*deltanuguess,0.1)
    while fcenter < freq[len(freq)//2]:
        H = hanning(freq, fcenter, deltanuguess, gamma)
        filtered_snr = H*snr
        inverse_fourier_time, inverse_fourier_PSD = PSD_to_timeseries(
            freq, filtered_snr, plot=False)
        acf = np.correlate(inverse_fourier_PSD,
                           inverse_fourier_PSD, mode='full')
        acf2 = acf[len(acf)//2::]
        acf2 = np.array(acf2)/max(acf2)
        inv_time2 = np.linspace(0, inverse_fourier_time[::len(
            inverse_fourier_time)//2][-1], len(acf2))
        X.append(fcenter)
        # je tente un smooth pour avoir un plot potable
        Z.append(smooth(np.abs(acf2)))
        fcenter += deltanuguess*fracstep
        deltanuguess = scaling_rel_deltanu(fcenter)
        largeur = gamma*deltanuguess
        print(fcenter)
    Y = inv_time2
    return X, Y, np.asarray(Z)
    
def proba_chi_squared(freq,snr, dfreqac=adaptative_box, step=100,plot=False):
    '''Computes the probability that a signal in a sliding box is due to a chi squared noise p(data|chi squared)
    parameters: 
        - snr, array of the snr
        - freq, array of the frequencies in µHz
        - dfreqac interval of computation of the PSD function in µHz
        - step displacement of the interval for each iteration, number of points
    returns: 
        -freq, ndarray
        -prob, ndarray'''
    prob = []
    #m = np.mean(snr)
    #print(m)
    snr = snr#*1/(freq[-1]*len(snr)) =>déja fait
    snr = np.concatenate((snr,snr[::-1],np.array([np.mean(snr)])))
    freq = np.concatenate((freq,freq+freq[-1],np.array([freq[-1]])))
    X = []
    df = (freq[1]-freq[0])
    #n = int(dfreqac/df)
    n = int(5/df)
    fcenter = (n/2)*df
    i = 0
    while fcenter<freq[-1]:#+dfreqac(fcenter)/2 < freq[-1]:
        n = int(max(dfreqac(fcenter), 5)/df)
        data = snr[i*step:i*step+n]
        m = np.mean(snr)
        F = freq[i*step:i*step+n]
        fcenter = (i*step+n/2)*df
        M = max(data)
        proba = 1-(1-np.exp(-M/m))**n
        X.append(fcenter)
        prob.append(proba)
        i += 1
    if plot:
        plt.plot(freq,snr/max(snr))
        plt.plot(X,prob)
    return X, np.array(prob)
    
def acf_matrix_fft(freq, PSD,SNR=False, scaling_rel_deltanu=numax_to_deltanu, gamma=4,fracstep=0.3,fdebut=20):
    '''Computes the EACF matrix based on the FFT method on the inverse FFT of the PSD
    parameters:
        - freq, ndarray, array of the frequencies in µHz
        - PSD, ndarray, array of the values taken by the PSD in ppm^2/µHz
        - scaling_rel_deltanu, function, gives an estimate of dnu given numax based on the scaling relations
        - gamma, float, hanning filter width parameter
        - fracstep, fraction of dnu of which the filter moves every iteration of the acf calculation
        - fdebut, float, central frequency (µHz) at which the matrix begins to be constructed'''
    if not SNR:
        snr = snr_PSD(freq, PSD)
    else:
        snr=PSD
    Z = []
    X = []
    fcenter = fdebut
    deltanuguess = scaling_rel_deltanu(fcenter)
    largeur = max(gamma*deltanuguess,0.05)
    while fcenter < freq[len(freq)//2]:
        H = hanning(freq, fcenter, deltanuguess, gamma)
        filtered_snr = H*snr
        inverse_fourier_time, inverse_fourier_PSD = PSD_to_timeseries(
            freq, filtered_snr, plot=False)
        acf = sc.signal.correlate(
            inverse_fourier_PSD, inverse_fourier_PSD, mode='full', method='auto')
        acf2 = acf[len(acf)//2::]
        acf2 = np.array(acf2)/max(acf2)
        X.append(fcenter)
        # je tente un smooth pour avoir un plot potable
        Z.append(smooth(np.abs(acf2)))
        fcenter += deltanuguess*fracstep
        deltanuguess = scaling_rel_deltanu(fcenter)
        largeur = gamma*deltanuguess
        #print(fcenter)
    inv_time2 = np.linspace(0, inverse_fourier_time[-1], len(acf2))
    return X, inv_time2, np.asarray(Z)

def DSP2_matrix(freq, PSD,SNR=False, scaling_rel_deltanu=numax_to_deltanu, gamma=4,fracstep=0.3,fdebut=20,f_fin=None):
    '''Computes the EACF matrix based PSD of the PSD
    parameters:
        - freq, ndarray, array of the frequencies in µHz
        - PSD, ndarray, array of the values taken by the PSD in ppm^2/µHz
        - scaling_rel_deltanu, function, gives an estimate of dnu given numax based on the scaling relations
        - gamma, float, hanning filter width parameter
        - fracstep, fraction of dnu of which the filter moves every iteration of the acf calculation
        - fdebut, float, central frequency (µHz) at which the matrix begins to be constructed'''    
    
    if not SNR:
        snr = snr_PSD(freq, PSD)
    else:
        snr=PSD
    Z = []
    X = []
    fcenter = fdebut
    deltanuguess = scaling_rel_deltanu(fcenter)
    largeur = max(gamma*deltanuguess,0.05)
    if f_fin!=None:
        lim=f_fin
    else:
        lim = freq[len(freq)//2]
    while fcenter < lim:
        H = hanning(freq, fcenter, deltanuguess, gamma)
        filtered_snr = H*snr
        inverse_fourier_time, acf, A = DSP1D(freq, filtered_snr)
        acf2 = acf[len(acf)//2::]
        acf2 = np.array(acf2)/max(acf2)
        inv_time2 = np.linspace(0, inverse_fourier_time[-1], len(acf2))
        X.append(fcenter)
        Z.append(np.abs(acf2))
        fcenter += deltanuguess*fracstep
        deltanuguess = scaling_rel_deltanu(fcenter)
        largeur = gamma*deltanuguess
    Y = inv_time2
    return X, Y, np.asarray(Z)

def acf_matrix_direct(freq, PSD,SNR=False, scaling_rel_deltanu=numax_to_deltanu, gamma=4,fracstep=0.3,fdebut=0.05):
    '''Computes the EACF matrix based on the direct convolution method on the inverse FFT of the PSD
    parameters:
        - freq, ndarray, array of the frequencies in µHz
        - PSD, ndarray, array of the values taken by the PSD in ppm^2/µHz
        - scaling_rel_deltanu, function, gives an estimate of dnu given numax based on the scaling relations
        - gamma, float, hanning filter width parameter
        - fracstep, fraction of dnu of which the filter moves every iteration of the acf calculation
        - fdebut, float, central frequency (µHz) at which the matrix begins to be constructed'''
    if not SNR:
        snr = snr_PSD(freq, PSD)
    else:
        snr=PSD
    Z = []
    X = []
    fcenter = fdebut
    deltanuguess = scaling_rel_deltanu(fcenter)
    largeur = max(gamma*deltanuguess,0.1)
    while fcenter < freq[len(freq)//2]:
        H = hanning(freq, fcenter, deltanuguess, gamma)
        filtered_snr = H*snr
        inverse_fourier_time, inverse_fourier_PSD = PSD_to_timeseries(
            freq, filtered_snr, plot=False)
        acf = np.correlate(inverse_fourier_PSD,
                           inverse_fourier_PSD, mode='full')
        acf2 = acf[len(acf)//2::]
        acf2 = np.array(acf2)/max(acf2)
        inv_time2 = np.linspace(0, inverse_fourier_time[::len(
            inverse_fourier_time)//2][-1], len(acf2))
        X.append(fcenter)
        # je tente un smooth pour avoir un plot potable
        Z.append(smooth(np.abs(acf2)))
        fcenter += deltanuguess*fracstep
        deltanuguess = scaling_rel_deltanu(fcenter)
        largeur = gamma*deltanuguess
        print(fcenter)
    Y = inv_time2
    return X, Y, np.asarray(Z)

def selection_matrix(X, Y, Z, harmonique, scaling_rel_deltanu=numax_to_deltanu,marge=0.5):
    '''Selects a stripe of the EACF matrix around the harmonic n/dnu that you want to study based on scaling relations:
        parameters:
            -X, ndarray, array of the central frequencies at which the acf was computed (µHz)
            -Y, ndarray, array of the frequency periodicities (1/µHz)
            -Z, ndarray, matric containing the EACF functions
            -harmonique, integer, number of the harmonic (n/dnu) you want to isolate to measure
            global seismic parameters [typically 2]
            -scaling_rel_deltanu, function, function that implements the scaling relation dnu=f(numax)
            -marge, float, determines the width of the selected stripe'''
    Z2 = np.ndarray.copy(Z)
    B1 = []
    B2 = []
    for i in range(len(X)):
        fcenter = X[i]
        borne2 = min((harmonique+marge)/(scaling_rel_deltanu(fcenter)),max(Y)-0.01)
        borne1 = min(max(harmonique-marge,harmonique/4)/(scaling_rel_deltanu(fcenter)),max(Y)-0.01)
        ind1 = np.where(Y > borne1)[0][0]
        ind2 = np.where(Y > borne2)[0][0]
        mask = np.concatenate((np.zeros(ind1), np.ones(ind2-ind1), np.zeros(len(Y)-ind2)))
        Z2[i] = Z2[i]*mask
        B1.append(borne1)
        B2.append(borne2)
    return Z2,B1,B2



def seismic_parameters(freq,PSD,SNR=False,harmonique=2,scaling_rel_deltanu=numax_to_deltanu,scaling_rel_numax=deltanu_to_numax, gamma=4, method='A2Z',plot=True,log_scale=False,marge=0.5,fracstep=1,f_start=5,depressed_ratio=False,save_fig=False,fig_name='None',f_end=None,lim_matrix = None):
    '''This function provides a measure of νmax and ∆ν based on the EACF method (Mosser et al.)
        Parameters:
            -freq: ndarray, frequency array in μHz
            -PSD: ndarray, PSD array in ppm2/μHz
            -SNR: Boolean, If set to True the function processes the PSD as an SNR, set to False by default
            -harmonique: int, selects which harmonique to analyse eg if harmonique=2 the program will measure ∆ν thanks to
            the ∆ν
            2 harmonic in the EACF matrix, by default set tp 2
            -scaling_rel_deltanu: function, scaling relation used to determine ∆ν with νmax, by default uses the implemented one
            -gamma: float, Number of deltanu to use when filterning the PSD during the construction of the EACF matrix, by
            default set to 4
            -method: string, Selects the method to use for computing the EACF, A2Z computes the PSD of the successive filtered
            snr while fft_acf and direct_acf both compute the autocorrelation function of the inverse FFT of those filtered snr2
            -plot: Boolean, if True, plots a figure that summarises the measures done, True by default
            -log_scale: Boolean, if True plots the y axis of the summary figure in logarithmic scale, False by default
            -marge: float, quantifies the width of the filter based on the scaling relations applied to the EACF matrix before col-
            lapsing it on both axis, set to 0.5 by default
            -fracstep: float, The hanning filter moves by fracstep*∆νest at every step, decreasing fracstep hence enhances the res-
            olution of the EACF, 1 by default
            -f_start: float, the frequency at which the EACF starts being computed in μHz
            -f_end: float, the frequency at which the EACF ends in μHz
        Returns:
            -numax: float, the computed value of νmax, same as numaxtrue if the star is not super-Nyquist in μHz
            -deltanu: float, the measure of deltanu in μHz
            -sigmanm: float, value of the sigma of the gaussian function fitted for the computation of νmax in μHz
            -sigma: float, value of the sigma of the gaussian function fitted for the computation of ∆ν in μHz'''
    
    fdebut,f_fin = f_start,f_end
    
    freq = np.concatenate((freq,freq+freq[-1]))
    PSD = np.concatenate((PSD,PSD[::-1]))
    if method=='fft_acf':
        X,Y,Z = acf_matrix_fft(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut)#peut-être regarder influence phase sur timeseries
    elif method=='A2Z':
        X,Y,Z = DSP2_matrix(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut,f_fin)
    elif method=='direct_acf':
        X,Y,Z = acf_matrix_direct(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut)
    else:
        print("please choose a valid method")
        return None
    Z2,B1,B2 = selection_matrix(X, Y, Z, harmonique, scaling_rel_deltanu,marge)
    period_freq,Amp_deltanu = collapse(Y,X,Z2)
    fcenter_list,Amp_numax = norm_collapse(X,Y,np.transpose(Z2))
    fcenter_list = np.array(fcenter_list)
    Amp_deltanu = np.asarray(Amp_deltanu)/max(Amp_deltanu)
    indice = np.where(Amp_deltanu == 1)[0][0]
    maxi = period_freq[indice]
    indice_debut = np.where(Amp_deltanu >= 1/2)[0][0]-1
    sigma1 = maxi-period_freq[indice_debut]
    deltanu, sigma, Amp, c = sc.optimize.curve_fit(model_gauss, period_freq, Amp_deltanu, p0=[maxi, sigma1, 1, np.mean(Amp_deltanu)], method='lm')[0]
    deltanu = harmonique/deltanu
    Amp_numax = np.asarray(Amp_numax)/max(Amp_numax)
    numax1 = deltanu_to_numax(deltanu)
    ind_numax = np.where(fcenter_list>=numax1)[0][0]
    sigm_ind = np.where(fcenter_list>=min(numax1+deltanu,fcenter_list[-1]))[0][0]
    Amp_numax2 = Amp_numax[max(0,ind_numax-sigm_ind):min(ind_numax+sigm_ind,len(fcenter_list)-1)]
    fcenter_list2 = fcenter_list[max(0,ind_numax-sigm_ind):min(ind_numax+sigm_ind,len(fcenter_list)-1)]
    Amp_numax2 = Amp_numax2/max(Amp_numax2)
    indice_debut = np.where(Amp_numax2 >= 1/2)[0][0]-1
    sigma1 = numax1-fcenter_list[indice_debut]
    numax, sigma_nm, Amp_nm, c2 = sc.optimize.curve_fit(model_gauss, fcenter_list2, Amp_numax2*(fcenter_list2>numax1*0.5)*(fcenter_list2<numax1*1.6), p0=[numax1, sigma1, 1, 0], method='lm')[0]
    deltanu = harmonique/deltanu
    deltanu=deltanu
    
    if depressed_ratio:
        snr=snr_PSD(freq,PSD)
        H = hanning(freq, numax, harmonique/deltanu, gamma)
        filtered_snr = H*snr
        TF = fft(filtered_snr)
        h = freq[1]-freq[0]
        l = fftfreq(len(freq), h)
        TF, freq = fftshift(TF), fftshift(l)
        inverse_fourier_time, tf = freq, np.abs(TF)
        tf2 = tf[len(tf)//2::]
        inv_time2 = np.linspace(0, inverse_fourier_time[-1], len(tf2))
        x1 = tf2
        dist=np.where(inv_time2>0.85*deltanu/harmonique)[0][0]
        peaks, _ = sc.signal.find_peaks(np.log(tf2),distance=dist)
        test=tf2[peaks[1]]/tf2[peaks[0]]
        
        envelopel,envelopeh = hl_envelopes_idx(tf2[peaks],dmin=2,dmax=2)
        #plt.plot((inv_time2[peaks])[envelopeh],(tf2[peaks])[envelopeh])
        imp_1 = (tf2[peaks])[envelopel]
        #plt.plot((inv_time2[peaks])[envelopel],imp_1)       
        pair = sc.interpolate.interp1d((inv_time2[peaks])[envelopeh],(tf2[peaks])[envelopeh],fill_value='extrapolate')
        #plt.plot(inv_time2[peaks][0::2],impair_1)
        pair_array = sc.ndimage.gaussian_filter1d(pair(inv_time2),5)
        impair = sc.interpolate.interp1d((inv_time2[peaks])[envelopel],imp_1,fill_value='extrapolate')
        impair_array = sc.ndimage.gaussian_filter1d(impair(inv_time2),5)
        test_2 = np.mean(pair_array[0:10]/impair_array[0:10])
        # plt.plot(inv_time2,tf2)
        # plt.plot(inv_time2[peaks],tf2[peaks],linestyle='None',marker='x')
    
    if plot or save_fig:
        fig = plt.figure(layout="constrained",figsize=(5.5,5),dpi=100)
        axd = fig.subplot_mosaic(
            """
            a.
            Ab
            cc
            """,
            # set the height ratios between the rows
            height_ratios=[ 1, 3.5,1],
            # set the width ratios between the columns
            width_ratios=[ 3.5,1]
        )
        
        axd['b'].plot(Amp_numax/max(Amp_numax),fcenter_list,label='measure',color='black')
        axd['b'].grid()
        axd['b'].set_ylim(min(X),max(X))
        axd['a'].plot(period_freq,Amp_deltanu/max(Amp_deltanu),label='measure',color='k')
        if lim_matrix!=None:
            axd['a'].set_xlim(0,lim_matrix)
        else:
            axd['a'].set_xlim(0,min(5,max(Y)))
        axd['a'].tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
        axd['b'].tick_params(
            axis='y',          
            which='both',     
            left=False,      
            right=False,         
            labelleft=False) 
        axd['a'].plot(period_freq,model_gauss(period_freq,deltanu, sigma, Amp, c),color='red',label='gaussian fit')
        axd['b'].plot(model_gauss(fcenter_list,numax, sigma_nm, Amp_nm, c2),fcenter_list,color='red',label='fit')
        axd['a'].axvline(deltanu,color='red')
        axd['b'].axhline(numax,color='teal')
        if log_scale:
            axd['b'].set_yscale('log')
            axd['A'].set_yscale('log')
            
        axd['b'].legend()
        axd['a'].grid()
        axd['a'].legend()
        axd['A'].contourf(Y,X,(np.abs(Z))**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z'))+np.abs(Z2)**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z')),norm='log',cmap='plasma')
        axd['A'].contourf(Y,X,np.abs(Z2)**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z')),norm='log',cmap='plasma',alpha=0.1)
        axd['A'].plot(B2,X,color='black',linestyle='dotted')
        axd['A'].plot(B1,X,color='black',linestyle='dotted')
        if lim_matrix!=None:
            axd['A'].set_xlim(0,lim_matrix)
        else:
            axd['A'].set_xlim(0,min(5,max(Y)))
        
        axd['A'].axvline(deltanu, label=r'$\Delta\nu/$'+str(harmonique)+' ≈ '+str(1/deltanu)[0:4] +' +/- ' + str(np.abs(harmonique/(sigma1*deltanu)))[0:4]+'µHz', color='red')
        axd['A'].axhline(numax, label=r'$\nu_{max}$ ≈ '+str(numax)[0:5] +' +/- ' + str(np.abs(sigma_nm))[0:4]+'µHz', color='teal')
        axd['A'].set_xlabel('Lag (1/µHz)')
        axd['A'].legend()
        axd['A'].set_ylabel('Central frequency (µHz)')
        axd['c'].plot(freq,PSD,color='b')
        axd['c'].set_xlabel('Frequency (µHz)')
        axd['c'].set_ylabel('PSD'+'\n'+' (ppm²/µHz)')
        axd['c'].set_xscale('log')
        axd['c'].set_yscale('log')
        axd['c'].axvline(numax,color='red')
        plt.suptitle(method)

        if plot:
            plt.show()

        if not plot:
            plt.close(fig)    

        print(axd)
        if save_fig:
            fig.savefig(fig_name)
            print('Is it coming here? yes no who knows?')

            plt.close(fig)
    
    if depressed_ratio:
        return numax, harmonique/deltanu, np.abs(sigma_nm), np.abs(harmonique/(sigma1*deltanu)),test,test_2
    
    return numax, harmonique/deltanu, np.abs(sigma_nm), np.abs(harmonique/(sigma1*deltanu))

def compute_echelle(deltanu, freq, PSD, numax, sigmanm, plot=True,SNR=False):
    '''Computes and returns the echelle diagramm:
        parameters:
            -deltanu
            -freq, ndarray of the frequencies
            -PSD, ndarray of the PSD values
            -numax
            -sigmanm (sigma of gaussian fit on numax)
            -plot, if true, plots the echelle diagramm
        returns:
            -deltanu, liste of th frequencies from 0 to deltanu
            -freq, list of the first frequency of each slice of length deltanu
            -Z, matrix, the amplitude of the échelle diagram
            -slices, int, number of slices in the echelle diagram'''
    sigmanm = sigmanm
    if SNR:
        snr=PSD
    else:
        snr = snr_PSD(freq, PSD)
    ecart1 = 4.3*sigmanm  # largeur de gaussienne à 10%
    if numax+ecart1 >= freq[-1]:
        ecart2 = freq[-2]-numax
    else:
        ecart2 = ecart1
    indiceinit1 = np.where(freq >= numax-ecart1)[0][0]
    indicefin1 = np.where(freq >= numax+ecart2)[0][0]
    freq_ech = freq[indiceinit1:indicefin1]
    snr_ech = smooth(snr[indiceinit1:indicefin1], 5)**0.7
    freq_ech = freq[indiceinit1:indicefin1]
    M = []
    df = freq_ech[1]-freq_ech[0]
    l_dnu = int(deltanu/df)
    deltanu_liste = []
    freq_deb = []
    for i in range(l_dnu):
        deltanu_liste.append((i*df+freq_ech[0]) % (deltanu))
    acc = 0
    while len(np.where(freq_ech > freq_ech[0]+deltanu*(acc+1))[0]) > 0:
        ind1 = np.where(freq_ech >=
                        freq_ech[0]+deltanu*(acc))[0][0]
        M.append(snr_ech[ind1:ind1+l_dnu])
        freq_deb.append(freq_ech[ind1])
        acc += 1
    Z = [m for _, m in sorted(zip(deltanu_liste, np.transpose(np.asarray(M))))]
    Z = np.transpose(np.asarray(Z))
    deltanu_liste2 = np.sort(np.asarray(deltanu_liste))
    freq_deb = np.asarray(freq_deb)
    if plot:
        fig_ech = plt.figure(figsize=(20, 10))
        plt.title("echelle diagram")
        plt.xlabel(r'frequency mod $\Delta\nu$')
        plt.ylabel('frequency [µHz]')
        plt.pcolormesh(deltanu_liste2, freq_deb, Z, cmap='Blues')
        plt.show()
    return deltanu_liste2, freq_deb, Z, acc

def compute_echelle_2(deltanu, freq, PSD, numax, sigmanm, plot=True,vline=None, SNR=False):
    '''Computes and returns the echelle diagramm:
        parameters:
            -deltanu
            -freq, ndarray of the frequencies
            -PSD, ndarray of the PSD values
            -numax
            -sigmanm (sigma of gaussian fit on numax)
            -plot, if true, plots the echelle diagramm
        returns:
            -deltanu, liste of th frequencies from 0 to deltanu
            -freq, list of the first frequency of each slice of length deltanu
            -Z, matrix, the amplitude of the échelle diagram
            -slices, int, number of slices in the echelle diagram'''
    sigmanm = sigmanm
    if SNR:
        snr=PSD
    else:
        snr = snr_PSD(freq, PSD)
    ecart1 = 4.3*sigmanm  # largeur de gaussienne à 10%
    if numax+ecart1 >= freq[-1]:
        ecart2 = freq[-2]-numax
    else:
        ecart2 = ecart1
    indiceinit1 = np.where((freq >= numax-ecart1)*(freq%deltanu<0.1))[0][0]
    indicefin1 = np.where(freq >= numax+ecart2)[0][0]
    freq_ech = freq[indiceinit1:indicefin1]
    snr_ech = smooth(snr[indiceinit1:indicefin1], 5)**0.7
    M = []
    df = freq_ech[1]-freq_ech[0]
    l_dnu = int(deltanu/df)
    deltanu_liste = []
    freq_deb = []
    for i in range(l_dnu):
        deltanu_liste.append((i*df+freq_ech[0]) % (deltanu))
        # deltanu_liste.append(i*df/u.uHz)
    acc = 0
    while len(np.where(freq_ech > freq_ech[0]+deltanu*(acc+1))[0]) > 0:
        ind1 = np.where(freq_ech >=
                        freq_ech[0]+deltanu*(acc))[0][0]
        M.append(snr_ech[ind1:ind1+l_dnu])
        freq_deb.append(freq_ech[ind1])
        acc += 1
    Z = [m for _, m in sorted(zip(deltanu_liste, np.transpose(np.asarray(M))))]
    Z = np.transpose(np.asarray(Z))
    deltanu_liste2 = np.sort(np.asarray(deltanu_liste))
    freq_deb = np.asarray(freq_deb-np.array(deltanu_liste)[0])
    if plot:
        fig_ech = plt.figure(figsize=(20, 10))
        plt.title("echelle diagram")
        plt.xlabel(r'frequency mod $\Delta\nu\approx$'+str(round(deltanu,1))+' µHz')
        plt.ylabel('frequency [µHz]')
        plt.pcolormesh(deltanu_liste2, freq_deb, Z, cmap='Blues')
        if vline!=None:
            plt.axvline(vline,linestyle='dotted',linewidth=0.5,color='red')
            plt.scatter(vline*np.ones_like(freq_deb),vline+freq_deb,color='red')
        plt.show()
    return deltanu_liste2, freq_deb, Z, acc

def seismic_parameters_EACF_A2Z(freq,PSD,SNR=False,harmonique=2,scaling_rel_deltanu=numax_to_deltanu,scaling_rel_numax=deltanu_to_numax, gamma=4, method='A2Z',plot=True,log_scale=False,marge=0.5,fracstep=1,fdebut=5,depressed_ratio=False,save_fig=False,fig_name='None',echelle=False):
    '''This function provides a measure of νmax and ∆ν based on the EACF method (Mosser et al.)
        Parameters:
            -freq: ndarray, frequency array in μHz
            -PSD: ndarray, PSD array in ppm2/μHz
            -SNR: Boolean, If set to True the function processes the PSD as an SNR, set to False by default
            -harmonique: int, selects which harmonique to analyse eg if harmonique=2 the program will measure ∆ν thanks to
            the ∆ν
            2 harmonic in the EACF matrix, by default set tp 2
            -scaling_rel_deltanu: function, scaling relation used to determine ∆ν with νmax, by default uses the implemented one
            -gamma: float, Number of deltanu to use when filterning the PSD during the construction of the EACF matrix, by
            default set to 4
            -method: string, Selects the method to use for computing the EACF, A2Z computes the PSD of the successive filtered
            snr while fft_acf and direct_acf both compute the autocorrelation function of the inverse FFT of those filtered snr2
            -plot: Boolean, if True, plots a figure that summarises the measures done, True by default
            -log_scale: Boolean, if True plots the y axis of the summary figure in logarithmic scale, False by default
            -marge: float, quantifies the width of the filter based on the scaling relations applied to the EACF matrix before col-
            lapsing it on both axis, set to 0.5 by default
            -fracstep: float, The hanning filter moves by fracstep*∆νest at every step, decreasing fracstep hence enhances the res-
            olution of the EACF, 1 by default
            -fdebut: float, the frequency at which the EACF starts being computed in μHz
        Returns:
            -numax: float, the computed value of νmax, same as numaxtrue if the star is not super-Nyquist in μHz
            -deltanu: float, the measure of deltanu in μHz
            -sigmanm: float, value of the sigma of the gaussian function fitted for the computation of νmax in μHz
            -sigma: float, value of the sigma of the gaussian function fitted for the computation of ∆ν in μHz'''
    
    original_freq = freq
    original_snr = snr_PSD(freq, PSD)
    original_PSD = PSD
    test,numax_A2Z,nm_A2Z,dnu_A2Z,sigmanm, sigma = parameters_A2Z_4(freq, PSD,plot=False,super_Nyq=True)
    
    freq = np.concatenate((freq,freq+freq[-1]))
    PSD = np.concatenate((PSD,PSD[::-1]))
    if method=='fft_acf':
        X,Y,Z = acf_matrix_fft(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut)#peut-être regarder influence phase sur timeseries
    elif method=='A2Z':
        X,Y,Z = DSP2_matrix(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut)
    elif method=='direct_acf':
        X,Y,Z = acf_matrix_direct(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut)
    else:
        print("please choose a valid method")
        return None
    
    Z2,B1,B2 = selection_matrix(X, Y, Z, harmonique, scaling_rel_deltanu,marge)
    period_freq,Amp_deltanu = collapse(Y,X,Z2)
    fcenter_list,Amp_numax = norm_collapse(X,Y,np.transpose(Z2))
    fcenter_list = np.array(fcenter_list)
    Amp_deltanu = np.asarray(Amp_deltanu)/max(Amp_deltanu)
    indice = np.where(Amp_deltanu == 1)[0][0]
    maxi = period_freq[indice]
    indice_debut = np.where(Amp_deltanu >= 1/2)[0][0]-1
    sigma1 = maxi-period_freq[indice_debut]
    deltanu, sigma, Amp, c = sc.optimize.curve_fit(model_gauss, period_freq, Amp_deltanu, p0=[maxi, sigma1, 1, np.mean(Amp_deltanu)], method='lm')[0]
    
    deltanu = harmonique/deltanu
    Amp_numax = np.asarray(Amp_numax)/max(Amp_numax)
    numax1 = deltanu_to_numax(deltanu)
    ind_numax = np.where(fcenter_list>=numax1)[0][0]
    sigm_ind = np.where(fcenter_list>=min(numax1+deltanu,fcenter_list[-1]))[0][0]
    Amp_numax2 = Amp_numax[max(0,ind_numax-sigm_ind):min(ind_numax+sigm_ind,len(fcenter_list)-1)]
    fcenter_list2 = fcenter_list[max(0,ind_numax-sigm_ind):min(ind_numax+sigm_ind,len(fcenter_list)-1)]
    Amp_numax2 = Amp_numax2/max(Amp_numax2)
    indice_debut = np.where(Amp_numax2 >= 1/2)[0][0]-1
    sigma1 = numax1-fcenter_list[indice_debut]
    numax, sigma_nm, Amp_nm, c2 = sc.optimize.curve_fit(model_gauss, fcenter_list2, Amp_numax2, p0=[numax1, sigma1, 1, 0], method='lm')[0]
    deltanu = harmonique/deltanu
    deltanu=deltanu
    
    if depressed_ratio:
        snr=snr_PSD(freq,PSD)
        H = hanning(freq, numax, harmonique/deltanu, gamma)
        filtered_snr = H*snr
        TF = fft(filtered_snr)
        h = freq[1]-freq[0]
        l = fftfreq(len(freq), h)
        TF, freq = fftshift(TF), fftshift(l)
        inverse_fourier_time, tf = freq, np.abs(TF)
        tf2 = tf[len(tf)//2::]
        inv_time2 = np.linspace(0, inverse_fourier_time[-1], len(tf2))
        x1 = tf2
        dist=np.where(inv_time2>0.85*deltanu/harmonique)[0][0]
        peaks, _ = sc.signal.find_peaks(np.log(tf2),distance=dist)
        test=tf2[peaks[1]]/tf2[peaks[0]]
        
        envelopel,envelopeh = hl_envelopes_idx(tf2[peaks],dmin=2,dmax=2)
        #plt.plot((inv_time2[peaks])[envelopeh],(tf2[peaks])[envelopeh])
        imp_1 = (tf2[peaks])[envelopel]
        #plt.plot((inv_time2[peaks])[envelopel],imp_1)       
        pair = sc.interpolate.interp1d((inv_time2[peaks])[envelopeh],(tf2[peaks])[envelopeh],fill_value='extrapolate')
        #plt.plot(inv_time2[peaks][0::2],impair_1)
        pair_array = sc.ndimage.gaussian_filter1d(pair(inv_time2),5)
        impair = sc.interpolate.interp1d((inv_time2[peaks])[envelopel],imp_1,fill_value='extrapolate')
        impair_array = sc.ndimage.gaussian_filter1d(impair(inv_time2),5)
        test_2 = np.mean(pair_array[0:10]/impair_array[0:10])
        # plt.plot(inv_time2,tf2)
        # plt.plot(inv_time2[peaks],tf2[peaks],linestyle='None',marker='x')
    
    if plot:
        
        if not echelle:
            fig = plt.figure(layout="constrained",figsize=(11,13))
            axd = fig.subplot_mosaic(
                """
                a.
                Ab
                cc
                """,
                # set the height ratios between the rows
                height_ratios=[ 1, 4,1.5],
                # set the width ratios between the columns
                width_ratios=[ 3.5,1]
            )
        if echelle:
            fig = plt.figure(layout="constrained",figsize=(20,13))
            axd = fig.subplot_mosaic(
                """
                a.d
                Abd
                Abe
                cce
                """,
                # set the height ratios between the rows
                height_ratios=[ 1, 2,2,1.5],
                # set the width ratios between the columns
                width_ratios=[ 3.5,1,3.5]
            )
            
        axd['b'].plot(Amp_numax/max(Amp_numax),fcenter_list,label='measure')
        axd['b'].grid()
        axd['b'].set_ylim(min(X),max(X))
        axd['a'].plot(period_freq,Amp_deltanu/max(Amp_deltanu),label='measure')
        axd['a'].set_xlim(0,5)
        axd['a'].tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
        axd['b'].tick_params(
            axis='y',          
            which='both',     
            left=False,      
            right=False,         
            labelleft=False) 
        axd['a'].plot(period_freq,model_gauss(period_freq,deltanu, sigma, Amp, c),color='orange',label='gaussian fit')
        axd['b'].plot(model_gauss(fcenter_list,numax, sigma_nm, Amp_nm, c2),fcenter_list,color='orange',label='fit')
        axd['a'].axvline(deltanu,color='red')
        axd['b'].axhline(numax,color='teal')
        if log_scale:
            axd['b'].set_yscale('log')
            axd['A'].set_yscale('log')
            
        axd['b'].legend()
        axd['a'].grid()
        axd['a'].legend()
        axd['A'].contourf(Y,X,(np.abs(Z))**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z'))+np.abs(Z2)**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z')),norm='log',cmap='plasma')
        axd['A'].contourf(Y,X,np.abs(Z2)**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z')),norm='log',cmap='plasma',alpha=0.1)
        axd['A'].plot(B2,X,color='black',linestyle='dotted')
        axd['A'].plot(B1,X,color='black',linestyle='dotted')
        axd['A'].set_xlim(0,5)
        
        axd['A'].axvline(deltanu, label=r'$\Delta\nu/$'+str(harmonique)+' ≈ '+str(1/deltanu)[0:4] +' +/- ' + str(np.abs(harmonique/(sigma1*deltanu)))[0:4]+'µHz', color='red')
        axd['A'].axhline(numax, label=r'$\nu_{max}$ ≈ '+str(numax)[0:5] +' +/- ' + str(np.abs(sigma_nm))[0:4]+'µHz', color='teal')
        axd['A'].set_xlabel('frequency periodicity (1/µHz)')
        axd['A'].legend()
        axd['A'].set_ylabel('central frequency (µHz)')
        
        axd['c'].plot(original_freq,original_PSD, color='blue')
        bkg = smooth_bkg(original_freq, original_PSD)
        numax_ind = np.where(original_freq>numax)[0][0]
        axd['c'].plot(original_freq,(model_gauss(original_freq, numax_A2Z, sigmanm, max(original_snr),0)+bkg),color='pink')
        axd['c'].axvline(numax,color='red',label=r'$\nu_{max,EACF}$ ≈ '+str(numax)[0:5]+' µHz'+r' $\Delta\nu_{EACF}\approx$ '+str(harmonique/deltanu)[0:5]+'µHz')
        axd['c'].axvline(numax_A2Z,color='green',label=r'$\nu_{max,A2Z}$ ≈ '+str(numax_A2Z)[0:5]+' µHz'+r' $\Delta\nu_{A2Z}\approx$ '+str(dnu_A2Z)[0:5]+'µHz')
        axd['c'].set_yscale('log')
        axd['c'].set_xscale('log')
        axd['c'].legend()
        axd['c'].grid()
        if echelle:
            deltanu_liste_A2Z, freq_deb_A2Z, Z_A2Z, acc = compute_echelle(dnu_A2Z, freq, PSD, numax_A2Z, sigma_nm,plot=False)
            axd['d'].pcolormesh(deltanu_liste_A2Z, freq_deb_A2Z, Z_A2Z, cmap='Blues')
            axd['d'].set_title('A2Z')
            axd['d'].set_ylabel('frequency (µHz)')
            deltanu_liste, freq_deb, Z, acc = compute_echelle(harmonique/deltanu, freq, PSD, numax, sigma_nm,plot=False)
            axd['e'].pcolormesh(deltanu_liste, freq_deb, Z, cmap='Blues')
            axd['e'].set_title('A2Z')
            axd['e'].set_xlabel(r'frequency mod $\Delta\nu$ (µHz)')
            axd['e'].set_ylabel('frequency (µHz)')
        plt.suptitle(method)
        plt.show()
        print(axd)
        if save_fig:
            fig.savefig(fig_name)
            plt.close(fig)
    
    if depressed_ratio:
        return numax, harmonique/deltanu, np.abs(sigma_nm), np.abs(harmonique/(sigma1*deltanu)),test,test_2
    
    return numax, harmonique/deltanu, np.abs(sigma_nm), np.abs(harmonique/(sigma1*deltanu))

def paramatrix_plot(freq,PSD,SNR=False,harmonique=2,scaling_rel_deltanu=numax_to_deltanu,scaling_rel_numax=deltanu_to_numax, gamma=4, method='A2Z',fracstep=1,marge=0.5,fdebut=3,log_scale=False):
    '''Plots the EACF matrix from fdebut to the Nyquist frequency.
    Parameters:
        Parameters:
            -freq: ndarray, frequency array in μHz
            -PSD: ndarray, PSD array in ppm2/μHz
            -SNR: Boolean, If set to True the function processes the PSD as an SNR, set to False by default
            -harmonique: int, selects which harmonique to analyse eg if harmonique=2 the program will measure ∆ν thanks to
            the ∆ν
            2 harmonic in the EACF matrix, by default set tp 2
            -scaling_rel_deltanu: function, scaling relation used to determine ∆ν with νmax, by default uses the implemented one
            -gamma: float, Number of deltanu to use when filterning the PSD during the construction of the EACF matrix, by
            default set to 4
            -method: string, Selects the method to use for computing the EACF, A2Z computes the PSD of the successive filtered
            snr while fft_acf and direct_acf both compute the autocorrelation function of the inverse FFT of those filtered snr2
            -plot: Boolean, if True, plots a figure that summarises the measures done, True by default
            -log_scale: Boolean, if True plots the y axis of the summary figure in logarithmic scale, False by default
            -marge: float, quantifies the width of the filter based on the scaling relations applied to the EACF matrix before col-
            lapsing it on both axis, set to 0.5 by default
            -fracstep: float, The hanning filter moves by fracstep*∆νest at every step, decreasing fracstep hence enhances the res-
            olution of the EACF, 1 by default
            -fdebut: float, the frequency at which the EACF starts being computed in μHz
        '''
    freq = np.concatenate((freq,freq+freq[-1]))
    PSD = np.concatenate((PSD,PSD[::-1]))
    plot=True
    if method=='fft_acf':
        X,Y,Z = acf_matrix_fft(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut)#peut-être regarder influence phase sur timeseries
    elif method=='A2Z':
        X,Y,Z = DSP2_matrix(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut)
    elif method=='direct_acf':
        X,Y,Z = acf_matrix_direct(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut)
    else:
        print("please choose a valid method")
        return None
    Z2,B1,B2 = selection_matrix(X, Y, Z, harmonique, scaling_rel_deltanu,marge)
    period_freq,Amp_deltanu = collapse(Y,X,Z2)
    fcenter_list,Amp_numax = norm_collapse(X,Y,np.transpose(Z2))
    
    
    if plot:
        axd = plt.figure(layout="constrained",figsize=(11,10)).subplot_mosaic(
            """
            a.
            Ab
            """,
            # set the height ratios between the rows
            height_ratios=[ 1, 3.5],
            # set the width ratios between the columns
            width_ratios=[ 3.5,1]
        )
        
        axd['b'].plot(Amp_numax/max(Amp_numax),fcenter_list,label='measure')
        axd['b'].grid()
        axd['b'].set_ylim(min(X),max(X))
        axd['a'].plot(period_freq,Amp_deltanu/max(Amp_deltanu),label='measure')
        axd['a'].set_xlim(0,min(5,max(Y)))
        axd['a'].tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
        axd['b'].tick_params(
            axis='y',          
            which='both',     
            left=False,      
            right=False,         
            labelleft=False) 
        axd['b'].legend()
        axd['a'].grid()
        axd['a'].legend()
        axd['A'].contourf(Y,X,(np.abs(Z))**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z'))+np.abs(Z2)**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z')),norm='log',cmap='plasma')
        axd['A'].contourf(Y,X,np.abs(Z2)**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z')),norm='log',cmap='plasma',alpha=0.1)
        axd['A'].plot(B2,X,color='black',linestyle='dotted')
        axd['A'].plot(B1,X,color='black',linestyle='dotted')
        axd['A'].set_xlim(0,min(5,max(Y)))
        axd['A'].set_xlabel('frequency periodicity (1/µHz)')
        axd['A'].set_ylabel('central frequency (µHz)')
        if log_scale:
            axd['b'].set_yscale('log')
            axd['A'].set_yscale('log')
        plt.suptitle(method)
        plt.show()
    
def paramatrix_plot_sn(freq,PSD,SNR=False,harmonique=2,scaling_rel_deltanu=numax_to_deltanu,scaling_rel_numax=deltanu_to_numax, gamma=4, method='fft_acf',fracstep=1,marge=0.5,fdebut=20):
    '''Plots the EACF matrix from fdebut to twice the Nyquist frequency.
        Parameters:
            -freq: ndarray, frequency array in μHz
            -PSD: ndarray, PSD array in ppm2/μHz
            -SNR: Boolean, If set to True the function processes the PSD as an SNR, set to False by default
            -harmonique: int, selects which harmonique to analyse eg if harmonique=2 the program will measure ∆ν thanks to
            the ∆ν
            2 harmonic in the EACF matrix, by default set tp 2
            -scaling_rel_deltanu: function, scaling relation used to determine ∆ν with νmax, by default uses the implemented one
            -gamma: float, Number of deltanu to use when filterning the PSD during the construction of the EACF matrix, by
            default set to 4
            -method: string, Selects the method to use for computing the EACF, A2Z computes the PSD of the successive filtered
            snr while fft_acf and direct_acf both compute the autocorrelation function of the inverse FFT of those filtered snr2
            -plot: Boolean, if True, plots a figure that summarises the measures done, True by default
            -log_scale: Boolean, if True plots the y axis of the summary figure in logarithmic scale, False by default
            -marge: float, quantifies the width of the filter based on the scaling relations applied to the EACF matrix before col-
            lapsing it on both axis, set to 0.5 by default
            -fracstep: float, The hanning filter moves by fracstep*∆νest at every step, decreasing fracstep hence enhances the res-
            olution of the EACF, 1 by default
            -fdebut: float, the frequency at which the EACF starts being computed in μHz
        '''
    freq = np.concatenate((freq,freq+freq[-1]))
    PSD = np.concatenate((PSD,PSD[::-1]))
    plot=True
    if method=='fft_acf':
        X,Y,Z = acf_matrix_fft(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut)#peut-être regarder influence phase sur timeseries
    elif method=='A2Z':
        X,Y,Z = DSP2_matrix(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut)
    elif method=='direct_acf':
        X,Y,Z = acf_matrix_direct(freq,PSD,SNR,scaling_rel_deltanu,gamma,fracstep,fdebut)
    else:
        print("please choose a valid method")
        return None
    Z = np.concatenate((Z,Z[::-1]))
    X = np.asarray(X)
    X = np.concatenate((X,X+X[-1]))
    Z2,B1,B2 = selection_matrix(X, Y, Z, harmonique, scaling_rel_deltanu,marge)
    period_freq,Amp_deltanu = collapse(Y,X,Z2)
    fcenter_list,Amp_numax = norm_collapse(X,Y,np.transpose(Z2))
    
    
    if plot:
        axd = plt.figure(layout="constrained",figsize=(11,10)).subplot_mosaic(
            """
            a.
            Ab
            """,
            # set the height ratios between the rows
            height_ratios=[ 1, 3.5],
            # set the width ratios between the columns
            width_ratios=[ 3.5,1]
        )
        
        axd['b'].plot(Amp_numax/max(Amp_numax),fcenter_list,label='measure')
        axd['b'].grid()
        axd['b'].set_ylim(min(X),max(X))
        axd['a'].plot(period_freq,Amp_deltanu/max(Amp_deltanu),label='measure')
        axd['a'].set_xlim(0,1)
        axd['a'].tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
        axd['b'].tick_params(
            axis='y',          
            which='both',     
            left=False,      
            right=False,         
            labelleft=False) 
        axd['b'].legend()
        axd['a'].grid()
        axd['a'].legend()
        axd['A'].contourf(Y,X,(np.abs(Z))**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z'))+np.abs(Z2)**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z')),norm='log',cmap='plasma')
        axd['A'].contourf(Y,X,np.abs(Z2)**(0.55*int(not method=='A2Z')+0.25*int(method=='A2Z')),norm='log',cmap='plasma',alpha=0.1)
        axd['A'].plot(B2,X,color='black',linestyle='dotted')
        axd['A'].plot(B1,X,color='black',linestyle='dotted')
        axd['A'].set_xlim(0,1)
        axd['A'].set_xlabel('frequency periodicity (1/µHz)')
        axd['A'].set_ylabel('central frequency (µHz)')
        plt.suptitle(method)
        plt.show()



def adaptative_box_2(numax):
    '''estimates a rough value of deltanu/4 based on the scaling laws
    parameter:-numax (µHz)
    returns:-deltanu (µHz)'''
    estimate = 0.2*(numax)**(0.83)/3
    return estimate

def sliding_PSD(snr, freq, dfreqac=adaptative_box, step=100,H_0=True):
    '''Computes the DSP on dfreqac intervals and the central frequency of such intervals.
    parameters: -PSD, array of the PSD
        -freq, array of the frequencies in µHz
        -dfreqac, function, function taking the center frequency of the box as an argument and returning the frequency interval in μHz on which to perform the sliding PSD
        -step displacement of the interval for each iteration, number of points
    returns: 
        -X the array of the central frequencies
        -Y the array of the interval of computation of the PSDs
        -Z the matrix containing the PSDs'''

    Z = []
    X = []
    Y = []
    proba = []
    df = (freq[1]-freq[0])
    #n = int(dfreqac/df)
    n = int(5/df)
    fcenter = (n/2)*df
    i = 0
    while fcenter+dfreqac(fcenter)/2 < freq[-1]:
        n = int(max(dfreqac(fcenter), 20)/df)
        data = snr[i*step:i*step+n]
        F = freq[i*step:i*step+n]
        fcenter = (i*step+n/2)*df
        inv_freq, PSD, t = DSP1D(F, data)
        X.append(fcenter)
        Z.append(np.asarray(PSD/n))
        Y.append(inv_freq)
        i += 1
        if H_0:
            m = np.mean(snr)
            M = max(data)
            proba.append(1-(1-np.exp(-M/m))**n)
    if H_0:
        return X, np.asarray(Y, dtype=object), np.asarray(Z, dtype=object),np.asarray(proba)
    return X, np.asarray(Y, dtype=object), np.asarray(Z, dtype=object)

def sliding_power(snr, freq, dfreqac=adaptative_box, step=100):
    '''Computes the DSP on dfreqac intervals and the central frequency of such intervals.
    parameters: -PSD, array of the PSD
        -freq, array of the frequencies in µHz
        -dfreqac, function, function taking the center frequency of the box as an argument and returning the frequency interval in μHz on which to perform the sliding PSD
        -step displacement of the interval for each iteration, number of points
    returns: 
        -X the array of the central frequencies
        -Y the array of the interval of computation of the PSDs
        -Z the matrix containing the PSDs'''

    Z = []
    X = []
    Y = []
    df = (freq[1]-freq[0])
    #n = int(dfreqac/df)
    n = int(5/df)
    fcenter = (n/2)*df
    i = 0
    while fcenter+dfreqac(fcenter)/2 < freq[-1]:
        n = int(max(dfreqac(fcenter), 20)/df)
        data = snr[i*step:i*step+n]
        F = freq[i*step:i*step+n]
        fcenter = (i*step+n/2)*df
        X.append(fcenter)
        Z.append(data**2/n)
        Y.append(F)
        i += 1
    return X, np.asarray(Y, dtype=object), np.asarray(Z, dtype=object)

def sliding_PSD_2(snr, freq, dfreqac=adaptative_box, step=100,H_0=False,super_Nyq=False):
    '''Computes the DSP on dfreqac intervals and the central frequency of such intervals.
    parameters: -PSD, array of the PSD
        -freq, array of the frequencies in µHz
        -dfreqac, function, function taking the center frequency of the box as an argument and returning the frequency interval in μHz on which to perform the sliding PSD
        -step displacement of the interval for each iteration, number of points
    returns: 
        -X the array of the central frequencies
        -Y the array of the interval of computation of the PSDs
        -Z the matrix containing the PSDs'''

    Z = []
    X = []
    Y = []
    proba = []
    df = (freq[1]-freq[0])
    #n = int(dfreqac/df)
    n = int(5/df)
    fcenter = (n/2)*df
    i = 0
    while fcenter+dfreqac(fcenter)/2 < freq[-1]:
        n = int(max(dfreqac(fcenter), 20)/df)
        data = snr[i*step:i*step+n]
        # print(data)
        F = freq[i*step:i*step+n]
        # print(F)
        if len(data)<=1:
            break
        fcenter = (i*step+n/2)*df+freq[0]
        inv_freq, PSD, t = DSP1D(F, data)
        if super_Nyq:
            indice_pertinent = np.where(inv_freq >= min(2.5/numax_to_deltanu(fcenter),inv_freq[-1]))[0][0]
            ind_pert_2 = np.where(inv_freq > 0.7/numax_to_deltanu(fcenter))[0][0]
        else:
            indice_pertinent = np.where(inv_freq >= min(2.5/numax_to_deltanu(fcenter),inv_freq[-1]))[0][0]
            ind_pert_2 = np.where(inv_freq > 1.5/numax_to_deltanu(fcenter))[0][0]
        PSD2 = PSD[ind_pert_2:indice_pertinent]
        inv_freq2 = inv_freq[ind_pert_2:indice_pertinent]
        X.append(fcenter)
        Z.append(np.asarray(PSD2/len(PSD2)))
        Y.append(inv_freq2)
        i += 1
        if H_0:
            m = np.mean(snr)
            M = max(data)
            proba.append(1-(1-np.exp(-M/m))**n)
    if H_0:
        return X, np.asarray(Y, dtype=object), np.asarray(Z, dtype=object),np.asarray(proba)
    return X, np.asarray(Y, dtype=object), np.asarray(Z, dtype=object)

def estimate_numax_A2Z(freq, snr, dfreqac=adaptative_box, step=100, plot=True, matrix=False,H_0=True):
    '''This function estimates numax using a sliding PSD and integrating it.
    parameters: 
        -freq the array of the frequencies
        -snr, the array of the PSD (snr works, PSD not so much)
        -dfreqac, function, function taking the center frequency of the box as an argument and returning the frequency interval in μHz on which to perform the sliding PSD
        -step, number of points between each computation of the sliding PSD
        -plot, if true, plot the figure
        -matrix, if True, returns the sliding PSD of the PSD

    returns the parameters of the gaussian curve fit: 
        -numax, float, (µHz)
        -sigma, float, (µHz)
        -Amp, float, (dimensionless: scaled)
        -c, float, (dimensionless)
        -X, the array returned by sliding PSD
        -A, the array of the amplitude of the integrated sliding PSD'''
    if H_0:
        X, Y, Z, proba = sliding_PSD(snr, freq, dfreqac, step,H_0)
        X, A = collapse_2(X, Y, Z)
    else:
        X, Y, Z = sliding_PSD(snr, freq, dfreqac, step,H_0)
        X, A = collapse_2(X, Y, Z)
    A = np.asarray(A)/max(A)
    indice = np.where(A == 1)[0][0]
    numax1 = X[indice]
    indice_debut = np.where(A >= 1/2)[0][0]-1
    sigma1 = numax1-X[indice_debut]
    numax, sigma, Amp, c = sc.optimize.curve_fit(
        model_gauss, X, A, p0=[numax1, sigma1, 1, np.mean(A)], method='lm')[0]
    
    if plot:
        fignumaxA2Z = plt.figure(figsize=(20, 8))
        fig, ax = plt.subplots(2, figsize=(
            20, 16), sharex=True, facecolor='#FFFFFF')
        ax[0].set_xlabel('frequency (µHz)')
        ax[0].set_ylabel('scaled PSD')
        ax[0].set_title('Collapsed sliding PSD and fit')
        ax[0].plot(X, A, label='collapsed sliding PSD')
        ax[0].grid(linestyle='--')
        ax[0].plot(X, model_gauss(X, numax, sigma, Amp, c),
                   label='gaussian fit')
        ax[0].legend()
        ax[1].plot(freq, snr, color='dimgray')
        ax[1].axvline(numax, color='red', label="numax ≈ " +
                      str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
        ax[1].errorbar(numax, 1, xerr=sigma, capsize=10,
                       color='blue', label="error bar")
        ax[1].grid(linestyle='--')
        ax[1].set_title('PSD with the estimate of numax and the error bar')
        ax[1].set_xlabel('frequency (µHz)')
        ax[1].set_ylabel('PSD')
        ax[1].legend()
        plt.show()
        print("numax ≈ "+str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
    if matrix:
        return numax, np.abs(sigma), Amp, c, X, A, Y, Z
    return numax, np.abs(sigma), Amp, c, X, A

def acf(DSP, freq, dfreqac=40, step=100):
    '''Computes the autocorrelations on dfreqac intervals and the central frequency of such intervals.
    parameters: -PSD, array of the PSD
    -freq, array of the frequencies in µHz
    -dfreqac interval of computation of the autocorrelation function in µHz
    -step displacement of the interval for each iteration, without dimension, is just acting on the indexes
    returns: -X the array of the central frequences
    -Y the array of the interval of computation of the acf
    -Z the matrix containing the acfs'''
    pas = step
    dfreqac = dfreqac.value
    Z = []
    X = []
    Y = []
    df = (freq[1]-freq[0])
    n = int(dfreqac/df)
    for i in range(int(len(freq)/pas)-int(n/pas)):
        data = DSP[i*pas:i*pas+n]
        fcenter = (i*pas+n/2)*df
        corr = sc.signal.correlate(data, data, mode='same')
        X.append(fcenter)
        Z.append(np.asarray(corr))
    for j in range(n):
        Y.append(j*df)
    return X, Y, np.transpose(np.asarray(Z))


def estimate_numax_Huber(freq, DSP, dfreqac=30, step=100, plot=True):
    '''Using the collapsed autocorrelation function, the function fits a gaussian
    curve on the max and gives a estimate of numax (cf Huber et al. 2009)
    parameters:-array of frequencies
    -PSD array
    -dfracq, the width of the box on which it compute every acf (µHz)
    -pas, the step the algorithm takes between each acf (number of points)
    -plot, Boolean, True if you want the figure False otherwise
    returns:-numax (µHz)
    -sigma, parameter of the gaussian function fitted on the collapsed acf (µHz)
    -A, the amp of the fit on the collapsed acf
    -c, the constant in the gaussian function'''
    pas = step
    X5, Y5, Z5 = acf(DSP, freq, dfreqac, pas)
    X5, A5 = collapse(X5, Y5, Z5)
    A5 = np.asarray(A5)
    A5 = A5/max(A5)  # normalisation de l'autocorrélation
    smooth_acf = smooth(A5, 20)
    index = np.where(smooth_acf == max(smooth_acf))[0][0]
    nu_max1 = X5[index]
    nu_max, sigma, A, c = sc.optimize.curve_fit(
        model_gauss, X5, smooth_acf, p0=[nu_max1, 100, 1, 0])[0]

    if plot:
        fig, ax = plt.subplots(3, figsize=(
            20, 20), sharex=True, facecolor='#FFFFFF')

        ax[1].plot(X5, A5, label="fonction d'autocorrélation")
        ax[1].plot(X5, model_gauss(X5, nu_max, sigma, A, c),
                   label="ajustement de l'autocorrélation")
        ax[1].set_title("Fonction d'autocorrélation et ajustement")
        ax[1].grid(linestyle='--')
        ax[1].legend()
        ax[2].plot(freq, DSP, color='dimgray')
        ax[2].axvline(nu_max, color='red', label='nu_max')
        ax[2].set_title("Spectre avec fréquence maximale")
        ax[2].grid(linestyle='--')
        ax[0].set_title("Fonction d'autocorrélation 2D")
        ax[0].pcolormesh(X5, Y5, Z5, cmap='Blues')
        ax[0].set_ylabel('frequency lag (µHz)')
        ax[1].set_ylabel('autocorrélation')
        ax[2].set_ylabel('DSP')
        ax[2].set_xlabel("fréquence (µHz)")
        ax[2].errorbar(nu_max, 1, xerr=sigma, capsize=10,
                       color='blue', label="barre d'erreur")
        ax[2].legend()
    print('nu_max ≈ '+str(nu_max)+' +/- '+str(np.abs(sigma))+' µHz')
    return nu_max, np.abs(sigma), A, c

def estimate_numax_A2Z_power(freq, snr, dfreqac=adaptative_box, step=100, plot=True, matrix=False):
    '''This function estimates numax using a sliding PSD and integrating it.
    parameters: 
        -freq the array of the frequencies
        -snr, the array of the PSD (snr works, PSD not so much)
        -dfreqac, function, function taking the center frequency of the box as an argument and returning the frequency interval in μHz on which to perform the sliding PSD
        -step, number of points between each computation of the sliding PSD
        -plot, if true, plot the figure
        -matrix, if True, returns the sliding PSD of the PSD

    returns the parameters of the gaussian curve fit: 
        -numax, float, (µHz)
        -sigma, float, (µHz)
        -Amp, float, (dimensionless: scaled)
        -c, float, (dimensionless)
        -X, the array returned by sliding PSD
        -A, the array of the amplitude of the integrated sliding PSD'''

    X, Y, Z = sliding_power(snr, freq, dfreqac, step)
    X, A = collapse_2(X, Y, Z)
    A = np.asarray(A)/max(A)
    indice = np.where(A == 1)[0][0]
    numax1 = X[indice]
    indice_debut = np.where(A >= 1/2)[0][0]-1
    sigma1 = numax1-X[indice_debut]
    numax, sigma, Amp, c = sc.optimize.curve_fit(
        model_gauss, X, A, p0=[numax1, sigma1, 1, np.mean(A)], method='lm')[0]
    
    if plot:
        fignumaxA2Z = plt.figure(figsize=(20, 8))
        fig, ax = plt.subplots(2, figsize=(
            20, 16), sharex=True, facecolor='#FFFFFF')
        ax[0].set_xlabel('frequency (µHz)')
        ax[0].set_ylabel('scaled PSD')
        ax[0].set_title('Collapsed sliding PSD and fit')
        ax[0].plot(X, A, label='collapsed sliding PSD')
        ax[0].grid(linestyle='--')
        ax[0].plot(X, model_gauss(X, numax, sigma, Amp, c),
                   label='gaussian fit')
        ax[0].legend()
        ax[1].plot(freq, snr, color='dimgray')
        ax[1].axvline(numax, color='red', label="numax ≈ " +
                      str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
        ax[1].errorbar(numax, 1, xerr=np.abs(sigma), capsize=10,
                       color='blue', label="error bar")
        ax[1].grid(linestyle='--')
        ax[1].set_title('PSD with the estimate of numax and the error bar')
        ax[1].set_xlabel('frequency (µHz)')
        ax[1].set_ylabel('PSD')
        ax[1].legend()
        plt.show()
        print("numax ≈ "+str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
    if matrix:
        return numax, np.abs(sigma), Amp, c, X, A, Y, Z
    return numax, np.abs(sigma), Amp, c, X, A

def estimate_numax_A2Z_2(freq, snr, dfreqac=adaptative_box, step=100, plot=True, matrix=False,H_0=False, super_Nyq=False,save=False):
    '''This function estimates numax using a sliding PSD and integrating it.
    parameters: 
        -freq the array of the frequencies
        -snr, the array of the PSD (snr works, PSD not so much)
        -dfreqac, function, function taking the center frequency of the box as an argument and returning the frequency interval in μHz on which to perform the sliding PSD
        -step, number of points between each computation of the sliding PSD
        -plot, if true, plot the figure
        -matrix, if True, returns the sliding PSD of the PSD

    returns the parameters of the gaussian curve fit: 
        -numax, float, (µHz)
        -sigma, float, (µHz)
        -Amp, float, (dimensionless: scaled)
        -c, float, (dimensionless)
        -X, the array returned by sliding PSD
        -A, the array of the amplitude of the integrated sliding PSD'''
    if H_0:
        X, Y, Z, proba = sliding_PSD_2(snr, freq, dfreqac, step, H_0,super_Nyq=super_Nyq)
        X, A = collapse_2(X, Y, Z)
    else:
        X, Y, Z = sliding_PSD_2(snr, freq, dfreqac, step, H_0,super_Nyq=super_Nyq)
        X, A = collapse_2(X, Y, Z)
    A = np.asarray(A)/max(A)
    indice = np.where(A == 1)[0][0]
    numax1 = X[indice]
    indice_debut = np.where(A >= 1/2)[0][0]-1
    sigma1 = numax1-X[indice_debut]
    numax, sigma, Amp, c = sc.optimize.curve_fit(
        model_gauss, X, A, p0=[numax1, sigma1, 1, np.mean(A)], method='lm')[0]
    
    if plot:
        fignumaxA2Z = plt.figure(figsize=(20, 8))
        fig, ax = plt.subplots(2, figsize=(
            20, 16), sharex=True, facecolor='#FFFFFF')
        ax[0].set_xlabel('frequency (µHz)')
        ax[0].set_ylabel('scaled PSD')
        ax[0].set_title('Collapsed sliding PSD and fit')
        ax[0].plot(X, A, label='collapsed sliding PSD')
        ax[0].grid(linestyle='--')
        ax[0].plot(X, model_gauss(X, numax, sigma, Amp, c),
                   label='gaussian fit')
        ax[0].legend()
        ax[1].plot(freq, snr, color='dimgray')
        ax[1].axvline(numax, color='red', label="numax ≈ " +
                      str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
        ax[1].errorbar(numax, 1, xerr=sigma, capsize=10,
                       color='blue', label="error bar")
        ax[1].grid(linestyle='--')
        ax[1].set_title('PSD with the estimate of numax and the error bar')
        ax[1].set_xlabel('frequency (µHz)')
        ax[1].set_ylabel('PSD')
        ax[1].legend()
        plt.show()
        print("numax ≈ "+str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
    if matrix:
        return numax, np.abs(sigma), Amp, c, X, A, Y, Z
    if save:
        return fig,numax, np.abs(sigma), Amp, c, X, A
    return numax, np.abs(sigma), Amp, c, X, A



def estimate_numax_A2Z_3(freq, snr, dfreqac=adaptative_box, step=100, plot=True, matrix=False,H_0=False,save=False):
    '''This function estimates numax using a sliding PSD and integrating it.
    parameters: 
        -freq the array of the frequencies
        -snr, the array of the PSD (snr works, PSD not so much)
        -dfreqac, function, function taking the center frequency of the box as an argument and returning the frequency interval in μHz on which to perform the sliding PSD
        -step, number of points between each computation of the sliding PSD
        -plot, if true, plot the figure
        -matrix, if True, returns the sliding PSD of the PSD

    returns the parameters of the gaussian curve fit: 
        -numax, float, (µHz)
        -sigma, float, (µHz)
        -Amp, float, (dimensionless: scaled)
        -c, float, (dimensionless)
        -X, the array returned by sliding PSD
        -A, the array of the amplitude of the integrated sliding PSD'''
    if H_0:
        X, Y, Z, proba = sliding_PSD_2(snr, freq, dfreqac, step, H_0)
        X, A = collapse_2(X, Y, Z)
    else:
        X, Y, Z = sliding_PSD_2(snr, freq, dfreqac, step, H_0)
        X, A = collapse_2(X, Y, Z)
    A = np.asarray(A)/max(A)
    indice = np.where(A == 1)[0][0]
    numax1 = X[indice]
    indice_debut = np.where(A >= 1/2)[0][0]-1
    sigma1 = numax1-X[indice_debut]
    numax, sigma, Amp, c = sc.optimize.curve_fit(
        model_env, X, A, p0=[numax1, sigma1, 1, np.mean(A)], method='lm')[0]
    
    if plot:
        fig, ax = plt.subplots(2, figsize=(
            20, 16), sharex=True, facecolor='#FFFFFF')
        ax[0].set_xlabel('frequency (µHz)')
        ax[0].set_ylabel('scaled PSD')
        ax[0].set_title('Collapsed sliding PSD and fit')
        ax[0].plot(X, A, label='collapsed sliding PSD')
        ax[0].grid(linestyle='--')
        ax[0].plot(X, model_gauss(X, numax, sigma, Amp, c),
                   label='gaussian fit')
        ax[0].legend()
        ax[1].plot(freq, snr, color='dimgray')
        ax[1].axvline(numax, color='red', label="numax ≈ " +
                      str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
        ax[1].errorbar(numax, 1, xerr=sigma, capsize=10,
                       color='blue', label="error bar")
        ax[1].grid(linestyle='--')
        ax[1].set_title('PSD with the estimate of numax and the error bar')
        ax[1].set_xlabel('frequency (µHz)')
        ax[1].set_ylabel('PSD')
        ax[1].legend()
        plt.show()
        print("numax ≈ "+str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
    if matrix:
        return numax, np.abs(sigma), Amp, c, X, A, Y, Z
    if save:
        return fig,numax, np.abs(sigma), Amp, c, X, A
    return numax, np.abs(sigma), Amp, c, X, A

def estimate_numax_A2Z_mc(freq, snr, dfreqac=adaptative_box, step=100, plot=True, matrix=False,super_Nyq=False,save=False):
    '''This function estimates numax using a sliding PSD and integrating it.
    parameters: 
        -freq the array of the frequencies
        -snr, the array of the PSD (snr works, PSD not so much)
        -dfreqac, function, function taking the center frequency of the box as an argument and returning the frequency interval in μHz on which to perform the sliding PSD
        -step, number of points between each computation of the sliding PSD
        -plot, if true, plot the figure
        -matrix, if True, returns the sliding PSD of the PSD

    returns the parameters of the gaussian curve fit: 
        -numax, float, (µHz)
        -sigma, float, (µHz)
        -Amp, float, (dimensionless: scaled)
        -c, float, (dimensionless)
        -X, the array returned by sliding PSD
        -A, the array of the amplitude of the integrated sliding PSD'''

    X, Y, Z = sliding_PSD_2(snr, freq, dfreqac, step, H_0=False,super_Nyq=super_Nyq)
    X, A = collapse_2(X, Y, Z)
    A = np.asarray(A)/max(A)
    indice = np.where(A == 1)[0][0]
    numax1 = X[indice]
    indice_debut = np.where(A >= 1/2)[0][0]-1
    sigma1 = numax1-X[indice_debut]
    sigma1 = sigma1/2.355
    model = pm.Model()
    numax1, sigma1, Amp, c = sc.optimize.curve_fit(
         model_gauss, X, A, p0=[numax1, sigma1, 1, np.mean(A)], method='lm')[0]
    with model:
        numaxmc = pm.Normal('numaxmc',mu=numax1,sigma=0.5*numax1)
        sigma = pm.Normal('sigma',mu=sigma1,sigma=0.1)
        c = pm.Normal('c',mu=np.mean(A),sigma=0.1)
        Amp = pm.Normal('Amp',mu=1,sigma=0.1)
        mu = np.exp(-((X-numaxmc)/(np.sqrt(2)*sigma))**2)*Amp +c
        sigma2 = pm.HalfNormal('sigma2',sigma=2*np.std(A))
        Y_obs = pm.Normal('Y_obs',mu=mu,sigma=sigma2,observed=A)
        idata = pm.sample(5000)
    s = az.summary(idata)
    numax = s['mean']['numaxmc']
    gauche = s['hdi_3%']['numaxmc']
    droite = s['hdi_97%']['numaxmc']
    error_l,error_h = numax-gauche,droite-numax
    Amp = s['mean']['Amp']
    sigma = s['mean']['sigma']
    c = s['mean']['c']
    
    if plot:
        fignumaxA2Z = plt.figure(figsize=(20, 8))
        fig, ax = plt.subplots(2, figsize=(
            20, 16), sharex=True, facecolor='#FFFFFF')
        ax[0].set_xlabel('frequency (µHz)')
        ax[0].set_ylabel('scaled PSD')
        ax[0].set_title('Collapsed sliding PSD and fit')
        ax[0].plot(X, A, label='collapsed sliding PSD')
        ax[0].grid(linestyle='--')
        ax[0].plot(X, model_gauss(X, numax, sigma, Amp, c),
                   label='gaussian fit')
        ax[0].legend()
        ax[1].plot(freq, snr, color='dimgray')
        ax[1].axvline(numax, color='red', label="numax ≈ " +
                      str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
        ax[1].errorbar(numax, 1, xerr=sigma, capsize=10,
                       color='blue', label="error bar")
        ax[1].grid(linestyle='--')
        ax[1].set_title('PSD with the estimate of numax and the error bar')
        ax[1].set_xlabel('frequency (µHz)')
        ax[1].set_ylabel('PSD')
        ax[1].legend()
        plt.show()
        print("numax ≈ "+str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
    if matrix:
        return numax,error_l,error_h, np.abs(sigma), Amp, c, X, A, Y, Z
    if save:
        return fig,numax,error_l,error_h, np.abs(sigma), Amp, c, X, A
    return numax,error_l,error_h, np.abs(sigma), Amp, c, X, A


def super_Nyquist(numax, deltanu, nuNy, scaling_rel_numax=deltanu_to_numax):
    '''provided numax, deltanu, nuNy (Nyquist frequency) and a scaling relation, test if the star is super Nyquist or not:
        parameters:
            -numax
            -deltanu
            -nuNy
            -scaling_rel_numax: scaling relation providing numax when given deltanu
        '''
    numax2 = 2*nuNy-numax
    nu_est = scaling_rel_numax(deltanu)
    supnyq = (np.abs(numax2-nu_est) < np.abs(numax-nu_est))
    if supnyq:
        return supnyq, numax2
    else:
        return supnyq, numax
 
def super_Nyq_recovery(freq, PSD, plot=True, scaling_rel_numax=deltanu_to_numax, scaling_rel_deltanu=numax_to_deltanu):
    '''Recovers the spectrum of strictly super Nyquist stars if super-Nyquist
    parameters:'
    -freq, the array of the frequencies
    -PSD, the array of the PSD (snr works, PSD not so much)
    -plot, if true, will plot the mirrored (or not) snr and PSD
    -scaling_rel_numax, the scaling relation to use to estimate numax with deltanu, by default uses the one already implemented
    -scaling_rel_deltanu, the scaling relation to use to estimate deltanu with numax, by default uses the one already implemented

    returns:
        -the mirrored freq if super-Nyquist
        -the mirrored PSD if super-Nyquist
        -the true numax
        -sigmanm (sigma of gaussian fit on numax)
        -sigma (sigma of gaussian fit on deltanu)'''
    snr = snr_PSD(freq, PSD)
    test, numaxtrue, numax, deltanu, sigmanm, sigma = parameters_A2Z_5(freq, PSD,super_Nyq=True)
    print(test)
    if test:
        PSD = PSD[::-1]
        # diviser PSD par le sinc!!!=> sélectionner les pics d'abord
        snr = snr[::-1]
        nuNy = freq[-1]
        # freq = 2*nuNy-freq
        # freq = np.sort(freq)
        freq = freq+freq[-1]
        if plot:
            fig, ax = plt.subplots(2, figsize=(
                20, 16), sharex=True, facecolor='#FFFFFF')
            ax[0].plot(freq, PSD, color='#444444')
            ax[0].grid(linestyle='--')
            ax[0].set_title(
                'PSD of the super-Nyquist star with correct frequencies')
            ax[0].set_xlabel('frequency (µHz)')
            ax[0].set_ylabel('PSD')
            ax[1].plot(freq, snr, color='#444444')
            ax[1].grid(linestyle='--')
            ax[1].set_title(
                'snr of the super-Nyquist star with correct frequencies')
            ax[1].set_xlabel('frequency (µHz)')
            ax[1].set_ylabel('snr')
            ax[1].axvline(numaxtrue, color='red', label='numax')
            ax[1].legend()
            plt.show()
        return freq, PSD, numaxtrue, deltanu, sigmanm, sigma, test
    if plot:
        fig, ax = plt.subplots(2, figsize=(
            20, 24), sharex=True, facecolor='#FFFFFF')
        ax[0].plot(freq, PSD, color='#444444')
        ax[0].grid(linestyle='--')
        ax[0].set_title('Same PSD as before')
        ax[0].set_xlabel('frequency (µHz)')
        ax[0].set_ylabel('PSD')
        ax[1].plot(freq, snr, color='#444444')
        ax[1].grid(linestyle='--')
        ax[1].set_title('same snr as before')
        ax[1].set_xlabel('frequency (µHz)')
        ax[1].set_ylabel('snr')
        ax[1].axvline(numaxtrue, color='red', label='numax')
        ax[1].legend()
        plt.show()
    return freq, PSD, numax, deltanu, sigmanm, sigma, test

def correct_apo_theo(freq,numes):
    x= numes
    a = 2*freq[-1]/np.pi
    m = (x*np.cos(x/a)-a*np.sin(x/a))/(x*a*np.sin(x/a))*0.0113*2
    numax = (-1+np.sqrt(1+4*m*x))/(2*m)
    return numax
    
def estimate_numax_A2Z_max(freq, snr, dfreqac=adaptative_box, step=100, plot=True, matrix=False, super_Nyq=False,fit=True):
    '''This function estimates numax using a sliding PSD and integrating it.
    parameters: 
        -freq the array of the frequencies
        -snr, the array of the PSD (snr works, PSD not so much)
        -dfreqac, function, function taking the center frequency of the box as an argument and returning the frequency interval in μHz on which to perform the sliding PSD
        -step, number of points between each computation of the sliding PSD
        -plot, if true, plot the figure
        -matrix, if True, returns the sliding PSD of the PSD

    returns the parameters of the gaussian curve fit: 
        -numax, float, (µHz)
        -sigma, float, (µHz)
        -Amp, float, (dimensionless: scaled)
        -c, float, (dimensionless)
        -X, the array returned by sliding PSD
        -A, the array of the amplitude of the integrated sliding PSD'''
    X, Y, Z = sliding_PSD_2(snr, freq, dfreqac, step, H_0=False,super_Nyq=super_Nyq)
    A = [max(liste) for liste in Z]
    A = np.asarray(A)
    indice = np.where(A == np.max(A))[0][0]
    numax1 = X[indice]
    indice_debut = np.where(A >= np.max(A)/2)[0][0]-1
    sigma1 = numax1-X[indice_debut]
    # print(sigma1)
    if fit:
        numax, sigma, Amp, c = sc.optimize.curve_fit(
            model_gauss, X, A, p0=[numax1, sigma1, max(A), np.mean(A)], method='lm')[0]
    
    if plot:
        fignumaxA2Z = plt.figure(figsize=(20, 8))
        fig, ax = plt.subplots(2, figsize=(
            20, 16), sharex=True, facecolor='#FFFFFF')
        ax[0].set_xlabel('frequency (µHz)')
        ax[0].set_ylabel('scaled PSD')
        ax[0].set_title('Collapsed sliding PSD and fit')
        ax[0].plot(X, A, label='collapsed sliding PSD')
        ax[0].grid(linestyle='--')
        if fit:
            ax[0].plot(X, model_gauss(X, numax, sigma, Amp, c),
                       label='gaussian fit')
        ax[0].legend()
        ax[1].plot(freq, snr, color='dimgray')
        ax[1].axvline(numax, color='red', label="numax ≈ " +
                      str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
        ax[1].errorbar(numax, 1, xerr=sigma, capsize=10,
                       color='blue', label="error bar")
        ax[1].grid(linestyle='--')
        ax[1].set_title('PSD with the estimate of numax and the error bar')
        ax[1].set_xlabel('frequency (µHz)')
        ax[1].set_ylabel('PSD')
        ax[1].legend()
        plt.show()
        print("numax ≈ "+str(numax)+' +/- '+str(np.abs(sigma))+"µHz")
    if matrix:
        return numax, np.abs(sigma), Amp, c, X, A, Y, Z
    if not fit:
        return X, A
    return numax, np.abs(sigma), Amp, c, X, A
    
def global_parameters_A2Z(freq, PSD, SNR=False, dfreqac=adaptative_box, step=100, plot=True, super_Nyq=False, Droopy=False, save=False, path=None, filename=None, echelle=False, scaling_rel_numax=deltanu_to_numax, scaling_rel_deltanu=numax_to_deltanu,remove_peaks=False,correct_apo=False,MCMC=False,f_start=0,f_end=None,max_est=False):#,threshold_apo=0.05):
    '''Computes delta_nu and nu_max using the A2Z method
    
    parameters:
        -freq, the array of the frequencies
        -PSD, the array of the PSD
        -SNR, boolean, if set to true use the SNR instead of the PSD in the function
        -dfreqac, the function computing the interval of frequency at each iteration of the algorithm
        -step, number of points between each computation of the sliding PSD
        -plot, if true, plot the figure
        -superNyq, if True checks if the stars is super Nyquist or not and returns the true numax and the test(Boolean)
        -Droopy,if true, returns the depressed_ratio of the star that's to says the ratio between the amplitude of the second peak (deltanu)/first peak(deltanu/2) in the PSD of the PSD, if the second is too small returns 0: if high, criteria for detecting a depressed star
        -save, if true saves the figure in the indicated directory
        -path, if save is true, path of the directory where to save the figures
        -filename, name of the figure if save=True
        -echelle, if True, will add the echelle diagramm to the figure
        -scaling_rel_numax, the scaling relation to use to estimate numax with deltanu, by default uses the one already implemented
        -scaling_rel_deltanu, the scaling relation to use to estimate deltanu with numax, by default uses the one already implemented
        -MCMC: if true estimates numax with a MCMC sampling
        

    returns:
        -test (True if super Nyquist False otherwise) [provided super_Nyq=True]
        -numaxtrue correct numax [provided super_Nyq==True]
        -numax (same as numaxtrue if not Super Nyquist)
        -deltanu
        -sigmanm (sigma of gaussian fit on numax)
        -sigma (sigma of gaussian fit on 1/deltanu)
        -depressed_ratio [provided Droopy==True]
    '''
    if not SNR:
        snr = snr_PSD(freq, PSD,remove_peaks=remove_peaks)
    else:
        snr=PSD
    nuNy = freq[-1]
    ind_deb = np.where(freq>f_start)[0][0]
    
    if f_end!=None and f_end<freq[-1]:
        ind_fin = np.where(freq>=f_end)[0][0]
        freq,snr = freq[ind_deb:ind_fin],snr[ind_deb:ind_fin]

    if f_end==None:
        ind_fin = len(freq)-1
        freq,snr = freq[ind_deb:ind_fin],snr[ind_deb:ind_fin]
    
    if not MCMC and not max_est:
        numax, sigmanm, Ampnm, cnm, Xnm, Anm = estimate_numax_A2Z_2(freq, snr, dfreqac, step, False,super_Nyq=super_Nyq)
    
    if MCMC:
        numax,error_l,error_h, sigmanm, Ampnm, cnm, Xnm, Anm = estimate_numax_A2Z_mc(
            freq, snr, dfreqac, step,plot=False,super_Nyq=super_Nyq)
        
    if max_est:
        numax, sigmanm, Ampnm, cnm, Xnm, Anm = estimate_numax_A2Z_max(freq, snr, dfreqac, step, False,super_Nyq=super_Nyq)
    
    pourcents = 10
    facteur = 2*np.sqrt(2*np.log(100/pourcents))
    #facteur = 4.3
    ecart1 = facteur*sigmanm  # largeur de gaussienne à n%
    if numax+ecart1 >= freq[-1]:
        ecart2 = freq[-2]-numax
    else:
        ecart2 = ecart1
    
    
    indiceinit1 = np.where(freq >= numax-ecart1)[0][0] #selection des fréquences d'intérêt pour mesurer deltanu (à full width at 10% of the maximum) (remplacer par statistical test?)
    indicefin1 = np.where(freq >= numax+ecart2)[0][0]
    
    mask = hanning_2(np.concatenate((freq,freq+freq[-1])), numax, ecart1*2)
    mask = mask[0:len(mask)//2]
    
    inv_freq2, DSP_deltanu, t = DSP1D(
        freq, snr*mask)
    freq2 = 1/inv_freq2[len(inv_freq2)//2+2:len(inv_freq2)]
    DSP_deltanu2 = DSP_deltanu[len(inv_freq2)//2+2:len(inv_freq2)]
    inv_freq2 = inv_freq2[len(inv_freq2)//2+2:len(inv_freq2)]
    
    # pour éviter le bruit à basse fréquence on se cantonne à exploiter la DSP avec la borne inférieure donnée par une fraction du deltanu obtenu par relation d'échelle.
    if super_Nyq:
        indice_pertinent = np.where(inv_freq2 > 2.7/scaling_rel_deltanu(numax))[0][0]
        ind_pert_2 = np.where(inv_freq2 > 0.65/scaling_rel_deltanu(numax))[0][0]
    else:
        indice_pertinent = np.where(inv_freq2 > 2.7/scaling_rel_deltanu(numax))[0][0]
        ind_pert_2 = np.where(inv_freq2 > 1.5/scaling_rel_deltanu(numax))[0][0]
    freq2 = freq2[ind_pert_2:indice_pertinent]
    inv_freq2 = inv_freq2[ind_pert_2:indice_pertinent]
    DSP_deltanu2 = DSP_deltanu2[ind_pert_2:indice_pertinent]
    DSP_deltanu2 = np.asarray(DSP_deltanu2)/max(DSP_deltanu2)
    index_peak_array = sc.signal.find_peaks(DSP_deltanu2, height=2.5/4)[0]
    if len(index_peak_array) == 2:
        Droopy_ratio = DSP_deltanu2[index_peak_array[-2]
                                    ]/DSP_deltanu2[index_peak_array[-1]]
    else:
        Droopy_ratio = 0
    if np.abs(Droopy_ratio-1)>0.3:
        index_peak_array = sc.signal.find_peaks(DSP_deltanu2, height=3.5/4)[0]
    
    index_peak = index_peak_array[-1]
    deltanu1 = inv_freq2[index_peak]
    
# =============================================================================
#     Test pour éviter dnu/3
# =============================================================================
    if super_Nyq and numax<200:
        index_peak = np.where(DSP_deltanu2==max(DSP_deltanu2))[0][0]
        deltanu1 = inv_freq2[index_peak]
# =============================================================================
#     fin du test
# =============================================================================
    
    #sigma1 = 1.5*2.355/(0.25*numax)#par la TF sigma envelope ~ 1/sigma pic dans TF
    sigma1 = sc.signal.peak_widths(DSP_deltanu2,index_peak_array,rel_height=0.5)[0][-1]*(inv_freq2[1]-inv_freq2[0])/2.355
    #print(sigma1)
    p0 = [(deltanu1), sigma1, 1, 0.5]

    deltanu, sigma, Amp, c = sc.optimize.curve_fit(
        model_gauss, inv_freq2, DSP_deltanu2, p0=p0)[0]



    if super_Nyq:
        nuNy = freq[-1]
        test, numaxtrue = super_Nyquist(
            numax, 2/deltanu, nuNy, scaling_rel_numax)
    
    if correct_apo and super_Nyq:
        if test:
            corrected_snr = np.concatenate((snr*0, snr[::-1]))
            freq2 = np.concatenate((freq,freq+freq[-1]))
            PSD2 = np.concatenate((PSD*0, PSD[::-1]))
        else:
            corrected_snr = snr
            PSD2 = PSD
            freq2 = freq
        
        #numax_theo = correct_apo_theo(freq, numaxtrue)
        #envelope = model_gauss(freq2, numax_theo, sigmanm, 1, 0)
        envelope = model_gauss(freq2, numaxtrue, sigmanm, 1, 0)
        rectangle = []
        
        threshold_height = model_gauss(
            numax+facteur*sigmanm, numax, sigmanm, 1, 0)
        for val in envelope:
            if val > threshold_height:
                rectangle.append(1)
            else:
                rectangle.append(0)
        rectangle = np.array(rectangle)

        filtered_snr = corrected_snr*rectangle
        f = np.zeros(len(freq2))
        eta = np.sinc(freq2/(2*nuNy))
        #threshold_apo = (0.09+(max(snr)/np.std(snr))/2500)*eta**2
        threshold_apo = 0.13*eta**2
        h = np.mean(2*snr)*np.log(1/threshold_apo)#H_0 chi_squared test: 2*snr follows a chi squared law but not snr (cf histogram) idk why though
        peaks_indexes = sc.signal.find_peaks(filtered_snr, height=h)[0]
        f = np.zeros(len(freq2))
        for i in peaks_indexes:
            f[i] = 1
        ans = PSD2*f
        # complément aux pics *a et a barre en théorie des ensembles*
        comp_ans = PSD2*np.abs(f-1)
        # sinc de numpy tq = sin(pi*x)/(pi*x)
        nuNy=freq[-1]
        
        correct_peaks = ans/eta**2
        correct_PSD = comp_ans+correct_peaks
        # plt.plot(correct_PSD)
        if test:
            correct_snr = np.concatenate((np.zeros_like(freq),snr_PSD(freq, (correct_PSD[len(freq)::])[::-1])[::-1]))
            correct_snr2 = np.concatenate((sc.stats.chi2.rvs(df=2,size=len(freq))/2,snr_PSD(freq, (correct_PSD[len(freq)::])[::-1])[::-1]))
        else:
            correct_snr = snr_PSD(freq2,correct_PSD)
            correct_snr2 = correct_snr
        
        numax_correct, sigmanm_correct, Ampnm_correct, cnm_correct, Xnm_correct, Anm_correct = estimate_numax_A2Z_power(freq2, correct_snr2,plot=False)#mesurer avec uniquement excès de puissance
    
    if echelle:
        ecart3 = 4.3*sigmanm  # largeur de gaussienne à 10%
        if numax+ecart3 >= freq[-1]:
            ecart4 = freq[-2]-numax
        else:
            ecart4 = ecart3
        
        # nuNy = freq[-1]
        
        indiceinit2 = np.where(freq >= numax-ecart3)[0][0] #selection des fréquences d'intérêt pour mesurer deltanu (à full width at 10% of the maximum) (remplacer par statistical test?)
        indicefin2 = np.where(freq >= numax+ecart4)[0][0]
        if super_Nyq and test:
            freq_ech = -(freq[indiceinit2:indicefin2])[::-1]+2*nuNy
            snr_ech = smooth((snr[indiceinit2:indicefin2])[::-1], 5)**0.7
            M = []
            df = freq_ech[1]-freq_ech[0]
            l_dnu = int((2/deltanu)/df)
            deltanu_liste = []
            freq_deb = []
            for i in range(l_dnu):
                deltanu_liste.append((i*df+freq_ech[0]) % (2/deltanu))
                # deltanu_liste.append(i*df/u.uHz)
            acc = 0
            while len(np.where(freq_ech > freq_ech[0]+2/deltanu*(acc+1))[0]) > 0:
                ind1 = np.where(freq_ech >
                                freq_ech[0]+2/deltanu*(acc))[0][0]
                M.append(snr_ech[ind1:ind1+l_dnu])
                freq_deb.append(freq_ech[ind1])
                acc += 1
            Z = [m for _, m in sorted(
                zip(deltanu_liste, np.transpose(np.asarray(M))))]
            Z = np.transpose(np.asarray(Z))
            deltanu_liste2 = np.sort(np.asarray(deltanu_liste))
            freq_deb = np.asarray(freq_deb)
        
        else:
            freq_ech = freq[indiceinit2:indicefin2]
            snr_ech = smooth(snr[indiceinit2:indicefin2], 5)**0.7
            M = []
            df = freq_ech[1]-freq_ech[0]
            l_dnu = int((2/deltanu)/df)
            deltanu_liste = []
            freq_deb = []
            for i in range(l_dnu):
                deltanu_liste.append((i*df+freq_ech[0]) % (2/deltanu))
                # deltanu_liste.append(i*df/u.uHz)
            acc = 0
            while len(np.where(freq_ech > freq_ech[0]+2/deltanu*(acc+1))[0]) > 0:
                ind1 = np.where(freq_ech >
                                freq_ech[0]+2/deltanu*(acc))[0][0]
                M.append(snr_ech[ind1:ind1+l_dnu])
                freq_deb.append(freq_ech[ind1])
                acc += 1
            Z = [m for _, m in sorted(
                zip(deltanu_liste, np.transpose(np.asarray(M))))]
            Z = np.transpose(np.asarray(Z))
            deltanu_liste2 = np.sort(np.asarray(deltanu_liste))
            freq_deb = np.asarray(freq_deb)
        
    if plot or save:
        if echelle and not(correct_apo and super_Nyq):
            fig, ax = plt.subplots(4, figsize=(10, 20), facecolor='#FFFFFF',dpi=100)
        elif not(correct_apo and super_Nyq):
            fig, ax = plt.subplots(3, figsize=(10, 12.5), facecolor='#FFFFFF',dpi=100)
        if not correct_apo or not super_Nyq:
            if save:
                fig.suptitle(filename)
            ax[0].set_xlabel('Frequency (µHz)')
            ax[0].set_ylabel('Scaled sliding PSD')
            ax[0].set_title('Collapsed sliding PSD and fit')
            ax[0].plot(Xnm, Anm, label='Collapsed sliding PSD',color='black')
            ax[0].grid(linestyle='--')
            ax[0].plot(Xnm, model_gauss(Xnm, numax,
                       sigmanm, Ampnm, cnm), label='gaussian fit',color='red')
            ax[0].set_xlim(0,freq[-1])
            ax[0].legend()
            ax[1].plot(freq, snr, color='dimgray')
            ax[1].axvline(numax, color='red',
                          label=r"$\nu_{max}$ ≈ "+str(round(numax,2))+' +/- '+str(round(1/deltanu,2))+"µHz")
            ax[1].errorbar(numax, 1, xerr=1/deltanu, capsize=10,
                           color='blue', label="error bar")
            ax[1].grid(linestyle='--')
            ax[1].set_title(r'PSD with the computed $\nu_{max}$ and the error bar')
            ax[1].set_xlabel('Frequency (µHz)')
            ax[1].set_ylabel('PSD (SNR)')
            ax[1].set_xlim(0,freq[-1])
            ax[1].legend()
            ax[2].plot(inv_freq2, DSP_deltanu2, label=r'PSD around $\nu_{max}$',color='black')
            ax[2].set_title(r'PSD around $\nu_{max}$ for determining $\Delta\nu$')
            ax[2].set_ylabel('Scaled PS2')
            ax[2].set_xlabel('Frequency periodicity (1/µHz)')
            ax[2].plot(inv_freq2, model_gauss(inv_freq2, deltanu, sigma, Amp, c),
                       label=r'gaussian fit at $\Delta\nu/2$',color='r')
            ax[2].grid(linestyle='--')
            ax[2].axvline(deltanu, label=r'$\Delta\nu/2$ ≈ '+str(round(1/deltanu,3)) +
                          ' +/- ' + str(round(np.abs(sigma)*(1/deltanu)**2,3))+'µHz', color='blue')
            ax[2].legend()
            if echelle:
                ax[3].pcolormesh(deltanu_liste2, freq_deb, Z, cmap='Blues')
                ax[3].set_title('Echelle diagram')
                ax[3].set_xlabel(r'Frequency mod $\Delta\nu$ (µHz)')
                ax[3].set_ylabel('Frequency (µHz)')
            if super_Nyq:
                if test:
                    ax[1].text(10, max(snr)//2, r'Super Nyquist, $\nu_{max}$ ≈'+str(numaxtrue)[0:5]+' +/- '+str(
                        np.abs(sigmanm))[0:5]+"µHz", style='normal', bbox={'facecolor': 'grey', 'alpha': 0.1, 'pad': 10})
                else:
                    ax[1].text(10, max(snr)//2, 'Not super Nyquist', style='normal',
                               bbox={'facecolor': 'white', 'alpha': 0.3, 'pad': 10})
            
        if correct_apo and super_Nyq:
            fig = plt.figure(layout="tight",figsize=(40,25))
            ax = fig.subplot_mosaic(
                """
                ab
                cd
                ef
                """,
                # set the height ratios between the rows
                height_ratios=[1, 1, 1],
                # set the width ratios between the columns
                width_ratios=[1,1]
            )
            if save:
                fig.suptitle(filename)
            ax['a'].set_xlabel('frequency (µHz)')
            ax['a'].set_ylabel('scaled PSD')
            ax['a'].set_title('Collapsed sliding PSD and fit')
            ax['a'].plot(Xnm, Anm, label='collapsed sliding PSD')
            ax['a'].grid(linestyle='--')
            ax['a'].plot(Xnm, model_gauss(Xnm, numax,
                       sigmanm, Ampnm, cnm), label='gaussian fit')
            ax['a'].set_xlim(0,freq[-1])
            ax['a'].legend()
            ax['c'].plot(freq, snr, color='dimgray')
            ax['c'].axvline(numax, color='red',
                          label=r"$\nu_{max}$ ≈ "+str(numax)[0:5]+' +/- '+str(np.abs(sigmanm))[0:5]+"µHz")
            ax['c'].errorbar(numax, 1, xerr=sigmanm, capsize=10,
                           color='blue', label="error bar")
            ax['c'].grid(linestyle='--')
            ax['c'].set_title(r'snr with the computed $\nu_{max}$ and the error bar')
            ax['c'].set_xlabel('frequency (µHz)')
            ax['c'].set_ylabel('snr')
            ax['c'].set_xlim(0,freq[-1])
            ax['c'].legend()
            ax['e'].plot(inv_freq2, DSP_deltanu2, label=r'PSD around $\nu_{max}$')
            ax['e'].set_title(r'PSD around $\nu_{max}$ for determining $\Delta\nu$')
            ax['e'].set_ylabel('scaled PSD')
            ax['e'].set_xlabel('frequency periodicity (1/µHz)')
            ax['e'].plot(inv_freq2, model_gauss(inv_freq2, deltanu, sigma, Amp, c),
                       label=r'gaussian fit at $\Delta\nu/2$')
            ax['e'].grid(linestyle='--')
            ax['e'].axvline(deltanu, label=r'$\Delta\nu/2$ ≈ '+str(1/deltanu)[0:5] +
                          ' +/- ' + str(np.abs(sigma)*(1/deltanu)**2)[0:5]+'µHz', color='red')
            ax['e'].legend()
            if echelle:
                ax['b'].pcolormesh(deltanu_liste2, freq_deb, Z, cmap='Blues')
                ax['b'].set_title('échelle diagram')
                ax['b'].set_xlabel(r'frequency mod $\Delta\nu$ (µHz)')
                ax['b'].set_ylabel('frequency (µHz)')
            if test:
                ax['c'].text(10, max(snr)//2, r'Super Nyquist, $\nu_{max}$ ≈'+str(numaxtrue)[0:5]+' +/- '+str(
                        np.abs(sigmanm))[0:5]+"µHz", style='normal', bbox={'facecolor': 'grey', 'alpha': 0.1, 'pad': 10})
            else:
                ax['c'].text(10, max(snr)//2, 'Not super Nyquist', style='normal',
                                bbox={'facecolor': 'white', 'alpha': 0.3, 'pad': 10})
            ax['f'].plot(freq2, correct_snr, color='#555555', label='recovered snr')
            ax['f'].grid()
            ax['f'].set_title('recovered snr')
            ax['f'].set_xlabel('frequency (µHz)')
            ax['f'].set_ylabel(r'snr (ppm$^2$/µHz)')
            if test:
                ax['f'].set_xlim(nuNy,2*nuNy)
            else:
                ax['f'].set_xlim(0,nuNy)
                
            ax['f'].axvline(numax_correct,color='red',label=r'$\nu_{max}$ apodized≈'+str(numax_correct)[0:5]+' +/- '+str(sigmanm_correct)[0:5]+' µHz')
            ax['f'].plot(Xnm_correct, model_gauss(Xnm_correct, numax_correct,
                       sigmanm_correct, Ampnm_correct, cnm_correct)*max(correct_snr), label='gaussian fit',alpha=0.5,color='orange')
            ax['f'].plot(Xnm_correct,Anm_correct*max(correct_snr), label=r'$\nu_{max}$ apodized',alpha=0.3,color='blue')
            ax['f'].legend()
            if test:
                ax['d'].set_xlim(nuNy,2*nuNy)
            else:
                ax['d'].set_xlim(0,nuNy)
            ax['d'].plot(freq2, corrected_snr, color='#555555',
                       label='(symetrized) original snr')
            ax['d'].plot(freq2,eta**2*max(corrected_snr),color='teal',label='apodization')
            ax['d'].set_title('(symetrized) original snr')
            ax['d'].plot(freq2, rectangle*max(corrected_snr),
                       color='orange', label='filtering window')
            ax['d'].plot(freq2,h, label='threshold',color='red')
            ax['d'].set_ylim(0,max(corrected_snr)*1.03)
            ax['d'].set_xlabel('frequency (µHz)')
            ax['d'].set_ylabel(r'snr (ppm$^2$/µHz)')
            
            ax['d'].grid()
            ax['d'].legend(loc='best')
            
        if save:
            fig.savefig(path+filename)
            plt.close(fig)
        if not plot:
            plt.close(fig)
        if plot:
            plt.show()
    print("numax ≈ "+str(numax)+' +/- '+str(np.abs(sigmanm))+"µHz")
    print('deltanu ≈ '+str(2/deltanu)+' +/- ' + str(np.abs(sigma))+'µHz')
    if super_Nyq:

        if Droopy:

            print("After super Nyquist test, numax ≈ " +
                  str(numaxtrue)[0:5]+' +/- '+str(np.abs(sigmanm))[0:5]+"µHz")
            index_peak_array = sc.signal.find_peaks(DSP_deltanu2, height=2.5/4)[0]
            
            if correct_apo:
                return test,numax_correct, numaxtrue, numax, 2/deltanu, np.abs(sigmanm_correct), np.abs(sigmanm), np.abs(sigma), Droopy_ratio
            else:
                return test, numaxtrue, numax, 2/deltanu, np.abs(sigmanm), np.abs(sigma), Droopy_ratio
        print("After super Nyquist test, numax ≈ " +
              str(numaxtrue)[0:5]+' +/- '+str(np.abs(sigmanm))[0:5]+"µHz")
        if correct_apo:
            return test,numax_correct, numaxtrue, numax, 2/deltanu, np.abs(sigmanm_correct), np.abs(sigmanm), np.abs(sigma)
        return test, numaxtrue, numax, 2/deltanu, np.abs(sigmanm), np.abs(sigma)

    if Droopy:

        if len(index_peak_array) == 2:
            Droopy_ratio = DSP_deltanu2[index_peak_array[-2]
                                        ]/DSP_deltanu2[index_peak_array[-1]]
        else:
            Droopy_ratio = 0
        return numax, 2/deltanu, np.abs(sigmanm), np.abs(sigma), Droopy_ratio

    return numax, 2/deltanu, np.abs(sigmanm), np.abs(sigma)
      
def super_Nyq_recovery(freq, PSD, plot=True, scaling_rel_numax=deltanu_to_numax, scaling_rel_deltanu=numax_to_deltanu):
    '''Recovers the spectrum of strictly super Nyquist stars if super-Nyquist
    parameters:'
    -freq, the array of the frequencies
    -PSD, the array of the PSD (snr works, PSD not so much)
    -plot, if true, will plot the mirrored (or not) snr and PSD
    -scaling_rel_numax, the scaling relation to use to estimate numax with deltanu, by default uses the one already implemented
    -scaling_rel_deltanu, the scaling relation to use to estimate deltanu with numax, by default uses the one already implemented

    returns:
        -the mirrored freq if super-Nyquist
        -the mirrored PSD if super-Nyquist
        -the true numax
        -sigmanm (sigma of gaussian fit on numax)
        -sigma (sigma of gaussian fit on deltanu)'''
    snr = snr_PSD(freq, PSD)
    test, numaxtrue, numax, deltanu, sigmanm, sigma = parameters_A2Z_5(freq, PSD,super_Nyq=True)#, plot=False, super_Nyq=True, scaling_rel_numax=deltanu_to_numax, scaling_rel_deltanu=numax_to_deltanu)
    print(test)
    if test:
        PSD = PSD[::-1]
        # diviser PSD par le sinc!!!=> sélectionner les pics d'abord
        snr = snr[::-1]
        nuNy = freq[-1]
        # freq = 2*nuNy-freq
        # freq = np.sort(freq)
        freq = freq+freq[-1]
        if plot:
            fig, ax = plt.subplots(2, figsize=(
                20, 16), sharex=True, facecolor='#FFFFFF')
            ax[0].plot(freq, PSD, color='#444444')
            ax[0].grid(linestyle='--')
            ax[0].set_title(
                'PSD of the super-Nyquist star with correct frequencies')
            ax[0].set_xlabel('frequency (µHz)')
            ax[0].set_ylabel('PSD')
            ax[1].plot(freq, snr, color='#444444')
            ax[1].grid(linestyle='--')
            ax[1].set_title(
                'snr of the super-Nyquist star with correct frequencies')
            ax[1].set_xlabel('frequency (µHz)')
            ax[1].set_ylabel('snr')
            ax[1].axvline(numaxtrue, color='red', label='numax')
            ax[1].legend()
            plt.show()
        return freq, PSD, numaxtrue, deltanu, sigmanm, sigma, test
    if plot:
        fig, ax = plt.subplots(2, figsize=(
            20, 24), sharex=True, facecolor='#FFFFFF')
        ax[0].plot(freq, PSD, color='#444444')
        ax[0].grid(linestyle='--')
        ax[0].set_title('Same PSD as before')
        ax[0].set_xlabel('frequency (µHz)')
        ax[0].set_ylabel('PSD')
        ax[1].plot(freq, snr, color='#444444')
        ax[1].grid(linestyle='--')
        ax[1].set_title('same snr as before')
        ax[1].set_xlabel('frequency (µHz)')
        ax[1].set_ylabel('snr')
        ax[1].axvline(numaxtrue, color='red', label='numax')
        ax[1].legend()
        plt.show()
    return freq, PSD, numax, deltanu, sigmanm, sigma, test
        
def true_amplitude_2(freq, PSD, threshold=0.05, width=3, scaling_rel_numax=deltanu_to_numax, scaling_rel_deltanu=numax_to_deltanu, return_snr=False, save=False, path=None, filename=None, plot=True):
    '''mirrors the PSD if necessary and rescales the peaks based on the apodization:
    parameters:
        -threshold, float, threshold_peaks = threshold*std(snr)
        -width, float, width of the rectangle window used fir selecting the peaks= width*sigmanm
        -freq, the array of the frequencies
        -PSD, the array of the PSD (snr works, PSD not so much)
        -plot, if true, will plot the mirrored (or not) snr and PSD
        -scaling_rel_numax, the scaling relation to use to estimate numax with deltanu, by default uses the one already implemented
        -scaling_rel_deltanu, the scaling relation to use to estimate deltanu with numax, by default uses the one already implemented
        -plot, Boolean, if True, plots the filter parameters and the original snr along with the corrected snr
    returns:
        -correct freq and PSD arrays (with snr if return_snr)'''
    freq2, PSD2, numax, deltanu, sigmanm, sigma, test = super_Nyq_recovery(
        freq, PSD, plot=False, scaling_rel_numax=scaling_rel_numax, scaling_rel_deltanu=scaling_rel_deltanu)
    nuNy = freq[-1]
    if test:
        snr = snr_PSD(freq, PSD2[::-1])[::-1]
    else:
        snr = snr_PSD(freq, PSD2)

    envelope = model_gauss(freq2, numax, sigmanm, 1, 0)
    rectangle = []
    threshold_height = model_gauss(
        numax+width*sigmanm, numax, sigmanm, 1, 0)
    for val in envelope:
        if val > threshold_height:
            rectangle.append(1)
        else:
            rectangle.append(0)
    rectangle = np.array(rectangle)

    filtered_snr = snr*rectangle
    f = np.zeros(len(freq2))
    h = np.mean(2*snr)*np.log(1/threshold)#H_0 chi_squared test: 2*snr follows a chi squared law but not snr (cf histogram) idk why though
    peaks_indexes = sc.signal.find_peaks(filtered_snr, height=h)[0]
    f = np.zeros(len(freq2))
    for i in peaks_indexes:
        f[i] = 1
    ans = PSD2*f
    # complément aux pics *a et a barre en théorie des ensembles*
    comp_ans = PSD2*np.abs(f-1)
    # sinc de numpy tq = sin(pi*x)/(pi*x)
    eta = np.sinc(freq2/(2*nuNy))
    correct_peaks = ans/eta**2
    correct_PSD = comp_ans+correct_peaks
    correct_snr = snr_PSD(freq, correct_PSD[::-1])[::-1]
    if save:
        with open(path + filename + '_snr.' + 'txt', 'w') as file:
            for freqi, snri in zip(freq2, correct_snr):
                file.writelines(str(freqi)+';'+str(snri)+'\n')
        with open(path + filename + '.' + 'txt', 'w') as file:
            for freqi, PSDi in zip(freq2, correct_PSD):
                file.writelines(str(freqi)+';'+str(PSDi)+'\n')

    if plot:

        figtrue, ax = plt.subplots(2, sharex=True, figsize=(20, 10))
        ax[0].plot(freq2, correct_snr, color='#555555', label='recovered snr')
        ax[0].grid()
        ax[0].set_title('recovered snr')
        ax[0].set_xlabel('frequency (µHz)')
        ax[0].set_ylabel(r'snr (ppm$^2$/µHz)')
        ax[0].legend()
        ax[1].plot(freq2, snr, color='#555555',
                   label='(symetrized) original snr')
        ax[1].set_title('(symetrized) original snr')
        ax[1].plot(freq2, rectangle*max(snr),
                   color='orange', label='filtering window')
        ax[1].axhline(h, label='threshold of peak selection (at '+str((1-threshold)*100)+'%)')
        ax[1].set_xlabel('frequency (µHz)')
        ax[1].set_ylabel(r'snr (ppm$^2$/µHz)')
        ax[1].grid()
        ax[1].legend()

    if return_snr:
        return freq2, correct_PSD, correct_snr
    return freq2, correct_PSD

def height_peak_echelle(deltanu, freq, PSD, numax, sigmanm):
    '''returns -amplitude/sqrt(slices) of an echelle diagram, can be used for refining the value of deltanu (has to be minimized)
        parameters:
            -deltanu,float,deltanu in µHz
            -freq, ndarray, array of frequencies in µHz
            -PSD, ndarray, array of the values taken by the PSD in ppm2/µHz
            -numax, float, numax in µHz
            -sigmanm, float, sigmanm (sigma of the gaussian fit around numax/gaussian p-mode envelope) in µHz'''
    dnu_l, f_l, Z, slices = compute_echelle(
        deltanu, freq, PSD, numax, sigmanm, plot=False)
    X, A = collapse(dnu_l, f_l, Z)
    A = np.asarray(A)
    peaks = sc.signal.find_peaks(A, height=3*max(A)/4, prominence=0.5)[0]
    s = 0
    prominence = sc.signal.peak_prominences(A, peaks)[0]
    peak = np.asarray([peaks[np.where(prominence == max(prominence))[0][0]]])
    s = A[peak[0]]**2/slices
    return -np.sqrt(s)

def deltanu_refinement(deltanu, freq, PSD, numax, sigmanm, sigma):
    '''gives a refined value of deltanu provided that an analysis has already been perfomed before.
    parameters:
        -deltanu,float,deltanu in µHz
        -freq, ndarray, array of frequencies in µHz
        -PSD, ndarray, array of the values taken by the PSD in ppm2/µHz
        -numax, float, numax in µHz
        -sigmanm, float, sigmanm (sigma of the gaussian fit around numax/gaussian p-mode envelope) in µHz
        -sigma, float, sigma of the gaussian fit for the measure of deltanu in parameters_A2Z
    returns:
        -deltanu, float, refined value of deltanu'''
    mini = height_peak_echelle(deltanu, freq, PSD, numax, sigmanm)
    deltanu_m = deltanu
    for i in range(400):
        deltanu_2 = deltanu-2*sigma+i*sigma/100
        val = height_peak_echelle(deltanu_2, freq, PSD, numax, sigmanm)
        if val < mini:
            print(val)
            mini = val
            deltanu_m = deltanu_2
    return deltanu_m
    

