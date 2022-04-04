# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:10:28 2022

@author: zways
"""
from library import *
from simulation_engine import Simulation_engine
from scipy.optimize import fsolve

# MyEngine=Simulation_engine(a=0.600e-3,f=30,vi=0.9,ei=Etape.CHUTE,zi=0.600e-3)

# MyEngine=Simulation_engine(a=0.4535e-3,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)

# MyEngine.create_events(30)
# hmean, dtmean, z_bs, z_p, ttot=MyEngine.graphic.render(phase=1)


freqx=[]
h=[]
dt=[]
j=1
for freq in np.linspace(0.435e-3,0.4600e-3, 100):
    print('===================='+str(j))
    MyEngine=Simulation_engine(a=freq,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)
    MyEngine.create_events(200)
    hmean, dtmean, z_bs, z_p, ttot=MyEngine.graphic.calcul(False)
    # MyEngine.graphic.render()
    j=j+1
    for i in range(len(dtmean)):
        freqx.append(freq)
        dt.append(dtmean[i]*freq)
        h.append(hmean[i])

plt.plot(freqx, h,".")
plt.show()
#plt.scatter(freqx, dt)
