# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:10:28 2022

@author: zways
"""
from library import *
from simulation_engine import Simulation_engine

w=50
MyEngine=Simulation_engine()        
t=np.linspace(0,0.45,1000)
y=-g_CST/2*t**2+10*t 

y2=np.sin(w*t+np.pi)
plt.plot(t,y)
plt.plot(t,y2)