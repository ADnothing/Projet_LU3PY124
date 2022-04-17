# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:10:28 2022

@author: zways
"""
from library import *
from simulation_engine import Simulation_engine
from scipy.optimize import fsolve

# MyEngine=Simulation_engine(a=0.46e-3,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)

# MyEngine.create_events(20)
# hmean, dtmean, z_bs, z_p, ttot=MyEngine.graphic.render(phase=1)



    
# Lyapunov()
def plot_lyapunov_bifurcation():
    for ind in range(len(As)):
        if Lyap[ind] < 0:
            mask = amplitudex==As[ind]
            plt.scatter(np.array(amplitudex)[mask], np.array(h)[mask], color='Black', marker='.')
        else:
            mask = amplitudex==As[ind]
            plt.scatter(np.array(amplitudex)[mask], np.array(h)[mask], color='Red', marker='.')
    
    plt.ylabel('hauteur \n des rebonds [m]')
    plt.xlabel('Amplitude [m]')
    plt.grid()
    
    plt.subplot(2,1,1)
    for ind in range(len(As)):   
        if Lyap[ind] < 0:
            plt.scatter(As[ind],Lyap[ind], color='Black', marker='.') 
        else:
            plt.scatter(As[ind],Lyap[ind], color='Red', marker='.')
    plt.axhline(0, color="blue")
    plt.ylabel('Exposant de Lyapunov')
    plt.grid()       
    plt.show()
