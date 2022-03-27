# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:10:28 2022

@author: zways
"""
from library import *
from simulation_engine import Simulation_engine
from scipy.optimize import fsolve

freqx=[]
h=[]
dt=[]
for freq in np.linspace(1e-3, 5e-2, 20):
    MyEngine=Simulation_engine(a=freq,f=20)

    MyEngine.create_events(50)
    hmean, dtmean=MyEngine.graphic.render(phase=0)
    # for i in range(len(hmean)):
    #     freqx.append(freq)
    #     h.append(hmean[i])
    for i in range(len(dtmean)):
        freqx.append(freq)
        dt.append(dtmean[i]*freq)

# plt.scatter(freqx, h)
plt.scatter(freqx, dt)
