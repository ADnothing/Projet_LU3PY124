# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 19:29:17 2022

@author: Zacharie
"""
import matplotlib.pyplot as plt
import numpy as np

f=np.load("freqx.npz")
h=np.load("h.npz")
f=f.f.arr_0
h=h.f.arr_0

plt.xlim(0.448e-3,0.456e-3)
plt.plot(f, h, ',')

# plt.plot(f, h, ',',alpha=0.02)





# hmean=np.load("hmean.npz")
# dtmean=np.load("dtmean.npz")
# hmean=hmean.f.arr_0
# dtmean=dtmean.f.arr_0


# plt.plot(dtmean[0:400], hmean[0:400], ',')
# plt.plot(dtmean[0:400], hmean[0:400], ',')

# plt.ylim(0.00115,0.0028)
# plt.xlim(0.03125,0.0349)
# plt.plot(dtmean[2000:], hmean[2000:], ',')
# plt.plot(dtmean[:1000], hmean[:1000], ',')
