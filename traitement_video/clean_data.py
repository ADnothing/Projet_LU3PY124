# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 17:25:56 2022

@author: zways
"""

import numpy as np
import matplotlib.pyplot as plt

scaling= 4/(615-35)
t=np.load("t2.npz")
y_reflet=np.load("y2_reflet.npz")
y=np.load("y2.npz")


t=t.f.arr_0/1000
y=y.f.arr_0*scaling
y_reflet=y_reflet.f.arr_0*scaling


y_centered=abs(y-y_reflet)/2

from scipy import fftpack
time_step = (np.diff(t)).mean()

period = 1

plt.plot(t,y_centered)
plt.grid()
plt.show()
sig=y_centered
# The FFT of the signal
sig_fft = fftpack.fft(sig)

# And the power (sig_fft is of complex dtype)
power = np.abs(sig_fft)**2

# The corresponding frequencies
sample_freq = fftpack.fftfreq(sig.size, d=time_step)

# Plot the FFT power
plt.figure(figsize=(6, 5))
plt.plot(sample_freq, power)
plt.xlabel('Frequency [Hz]')
plt.ylabel('plower')

# Find the peak frequency: we can focus on only the positive frequencies
pos_mask = np.where(sample_freq > 0)
freqs = sample_freq[pos_mask]
peak_freq = freqs[power[pos_mask].argmax()]
plt.xlim(0,15)
plt.ylim(0,1e6)
# Check that it does indeed correspond to the frequency that we generate
# the signal with
np.allclose(peak_freq, 1./period)

# An inner plot to show the peak frequency
axes = plt.axes([0.55, 0.3, 0.3, 0.5])
plt.title('Peak frequency')
plt.plot(freqs[:8], power[:8])
plt.setp(axes, yticks=[])

# scipy.signal.find_peaks_cwt can also be used for more advanced
# peak detection
plt.show()

high_freq_fft = sig_fft.copy()
high_freq_fft[np.abs(sample_freq) >2* peak_freq] = 0
filtered_sig = fftpack.ifft(high_freq_fft)

plt.figure(figsize=(6, 5))
plt.plot(t, sig, label='Original signal')
plt.plot(t, filtered_sig, linewidth=3, label='Filtered signal')
# t2=np.linspace(0,6,int(1e4))
# plt.plot(t2,10*np.sin(2*np.pi*80*t2))
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.title("Regime 2 rebonds")
plt.legend(loc='best')
# plt.xlim(3,4)
plt.show()
plt.plot(t[:-2],(np.diff(np.diff(filtered_sig)/time_step)/time_step))
plt.show()



sig=10*np.sin(2*np.pi*80*t)
# The FFT of the signal
sig_fft = fftpack.fft(sig)

# And the power (sig_fft is of complex dtype)
power = np.abs(sig_fft)**2

# The corresponding frequencies
sample_freq = fftpack.fftfreq(sig.size, d=time_step)

# Plot the FFT power
plt.figure(figsize=(6, 5))
plt.plot(sample_freq, power)
plt.xlabel('Frequency [Hz]')
plt.ylabel('plower')

# Find the peak frequency: we can focus on only the positive frequencies
pos_mask = np.where(sample_freq > 0)
freqs = sample_freq[pos_mask]
peak_freq = freqs[power[pos_mask].argmax()]
# plt.xlim(0,15)
# plt.ylim(0,1e6)
# Check that it does indeed correspond to the frequency that we generate
# the signal with
np.allclose(peak_freq, 1./period)

# An inner plot to show the peak frequency
axes = plt.axes([0.55, 0.3, 0.3, 0.5])
plt.title('Peak frequency')
plt.plot(freqs[:8], power[:8])
plt.setp(axes, yticks=[])

# scipy.signal.find_peaks_cwt can also be used for more advanced
# peak detection
plt.show()

# plt.xlim(0.7,1.5)
high_freq_fft = sig_fft.copy()
# high_freq_fft[np.abs(sample_freq) >2* peak_freq] = 0
filtered_sig = fftpack.ifft(high_freq_fft)

plt.plot(t[:-2],(np.diff(np.diff(filtered_sig)/time_step)/time_step))
plt.show()