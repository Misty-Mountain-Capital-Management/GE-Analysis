# Attempting to use fourier transforms to predict the market
# Will it work? Who the fuck knows...

from rs_ge import *
import json
import numpy as np
import matplotlib.pyplot as plt

prices = get_data(13190)['prices']
N = len(prices)
f = np.fft.fft(prices)

freqs = np.fft.fftfreq(N)

t = np.arange(0, N)
recon = np.zeros(N)

for coef, freq in zip(f, freqs):
    if coef:
        recon += coef.real * np.cos(2 * np.pi * freq * t)
        recon -= coef.imag * np.sin(2 * np.pi * freq * t)

#Dirty hack to get them to the same height:
ratio = prices[0] / recon[0]
recon *= ratio

reals = f.real
imags = f.imag


price_line, = plt.plot(prices)
reconstructed, = plt.plot(recon)
plt.legend([price_line, reconstructed], ['Original Prices', 'Reconstructed from DFT'])
plt.xlabel('Time (days)')
plt.ylabel('Price (gp)')
plt.grid()
plt.show()
