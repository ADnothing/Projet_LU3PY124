# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:10:28 2022

@author: zways
"""
import numpy as np 
from library import *
from simulation_engine import Simulation_engine
from scipy.optimize import fsolve


MyEngine=Simulation_engine()

MyEngine.create_events(30)
t1, h, hmean, hstd=MyEngine.graphic.render()

# W = np.arange(0, 100, 0.1)
# A = np.arange(0, 100, 0.1)

# W, A = np.meshgrid(W, A)

t2=np.concatenate((t1[1:],[0]))
dt=t2-t1
dt=dt[3:-1]

plt.scatter(dt, h[3:-1])
plt.xlabel("Différence temporelle entre deux rebonds (s)")
plt.ylabel("Hauteur du rebond (m)")
plt.xlim(0, 0.1)
plt.ylim(0, 0.01)
