
import numpy as np

# ==================================================================================
# import data
# given raw signal x, y, z with sample rate 50Hz
# x = [x(0), x(1), ..., x(i), x(i+1), ..., x(n)]
# y = [y(0), y(1), ..., y(i), y(i+1), ..., y(n)]
# z = [z(0), z(1), ..., z(i), z(i+1), ..., z(n)]
# len(x) == len(y) == len(z)


# ==================================================================================
# discrete fourier transform
def bandpass( signal, lowcut, highcut, fs ):
    # define frequency domain
    L = len(signal)
    F = [fs*((2*i+1)/L) for i in range(L+1)]       # frequency domain
    # find the indices of lowcut & highcut
    ilowcut = np.where(np.array(F)>lowcut)[0][0]   # cut off index of high pass
    ihighcut = np.where(np.array(F)>highcut)[0][0] # cut off index of low pass
    # FFT
    P = np.fft.fft( signal )
    # high pass
    P[:ilowcut] = 0
    P[L-ilowcut:] = 0
    # low pass
    P[ihighcut:L-ihighcut] = 0
    # inverse FFT
    Y = np.abs(np.fft.ifft(P)) 
    return Y

L = len(x)         # data length
fs = 50            # sample rate
slice_len = 32     # slice raw signal

low = fs/slice_len # 50/32 Hz for high pass
high = 40          # 40    Hz for low  pass

acc2 = []
for i in range(L//fs):
                                     # ith second x = [x(i+1), x(i+2), ..., x(i+32), ..., x(i+50)]
    slice_x = x[i*fs:i*fs+slice_len] #      slice_x = [x(i+1), x(i+2), ..., x(i+32)]
    slice_y = y[i*fs:i*fs+slice_len] #      slice_y = [y(i+1), y(i+2), ..., y(i+32)]
    slice_z = z[i*fs:i*fs+slice_len] #      slice_z = [z(i+1), z(i+2), ..., z(i+32)]

    xf2 = bandpass( slice_x, low, high, fs )
    yf2 = bandpass( slice_y, low, high, fs )
    zf2 = bandpass( slice_z, low, high, fs )
    
    # block average per second
    acc2 += [sum([(xf2[i]**2 + yf2[i]**2 + zf2[i]**2)**0.5 for i in range(slice_len)])/slice_len]

# ==================================================================================
