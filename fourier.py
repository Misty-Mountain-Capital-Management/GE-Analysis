# Attempting to use fourier transforms to predict the market
# Will it work? Who the fuck knows...

from rs_ge import *
import json
import numpy as np
import matplotlib.pyplot as plt

prices = get_data(245)['prices']
N = len(prices)
f = np.fft.fft(prices)
freqs = np.fft.fftfreq(N)

t = np.arange(0, N)
recon = np.zeros(N)

for coef, freq in zip(f, freqs):
    if coef:
        recon += coef.real * np.cos(freq * t)
        recon += coef.imag * np.sin(freq * t)

plt.plot(recon)
plt.grid()
plt.show()
