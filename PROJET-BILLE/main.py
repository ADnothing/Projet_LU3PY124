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
for freq in np.arange(16, 25, 0.5):
    MyEngine=Simulation_engine(a=1e-3,f=freq)

    MyEngine.create_events(200)
    hmean=MyEngine.graphic.render(phase=0)
    for i in range(len(hmean)):
        freqx.append(freq)
        h.append(hmean[i])

plt.scatter(freqx, h)
