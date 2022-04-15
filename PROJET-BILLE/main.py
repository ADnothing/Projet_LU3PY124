# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:10:28 2022

@author: zways
"""
from library import *
from simulation_engine import Simulation_engine
from scipy.optimize import fsolve

def attracteur_render ():
    MyEngine=Simulation_engine(a=0.465e-3,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)
    MyEngine.create_events(300)
    hmean, dtmean=MyEngine.attracteur()
    # plt.xlim(0.03,0.035)
    plt.plot(dtmean, hmean, ',')
    plt.show()
    return dtmean,hmean

def bifurcation_render():
    amplitudex=[]
    h=[]
    j=1
    
    for amplitude in np.linspace(0.280e-3,0.600e-3, 10):
        print('===================='+str(j))
        MyEngine=Simulation_engine(a=amplitude,f=30)
    
        MyEngine.create_events(200)
        hmean, dtmean, z_bs =MyEngine.bifurcation()
        for i in range(len(hmean)):
            amplitudex.append(amplitude)
            h.append(hmean[i])
        j=j+1
        for i in range(len(dtmean)):
            amplitudex.append(amplitude)
            h.append(hmean[i])
    plt.plot(amplitudex, h, ',')
    plt.show()
    
    return amplitudex , h

attracteur_render()
bifurcation_render()