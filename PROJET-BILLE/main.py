# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:10:28 2022

@author: zways
"""
from library import *
from simulation_engine import Simulation_engine
from scipy.optimize import fsolve

# MyEngine=Simulation_engine(a=0.600e-3,f=30,vi=0.9,ei=Etape.CHUTE,zi=0.600e-3)

<<<<<<< Updated upstream
# MyEngine=Simulation_engine(a=0.4535e-3,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)

# MyEngine.create_events(30)
# hmean, dtmean, z_bs, z_p, ttot=MyEngine.graphic.render(phase=1)
=======
MyEngine=Simulation_engine(a=0.4535e-3,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)

MyEngine.create_events(30)
hmean, dtmean, z_bs, z_p, ttot, v_b=MyEngine.graphic.render(phase=1)
>>>>>>> Stashed changes


freqx=[]
h=[]
dt=[]
j=1
<<<<<<< Updated upstream
for freq in np.linspace(0.435e-3,0.4600e-3, 100):
    print('===================='+str(j))
    MyEngine=Simulation_engine(a=freq,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)
    MyEngine.create_events(200)
    hmean, dtmean, z_bs, z_p, ttot=MyEngine.graphic.calcul(False)
    # MyEngine.graphic.render()
=======
for freq in np.linspace(0.280e-3,0.600e-3, 100):
    print('===================='+str(j))
    MyEngine=Simulation_engine(a=freq,f=30)

    MyEngine.create_events(50)
    hmean, dtmean=MyEngine.graphic.render(phase=1)
    # for i in range(len(hmean)):
    #     freqx.append(freq)
    #     h.append(hmean[i])
>>>>>>> Stashed changes
    j=j+1
    for i in range(len(dtmean)):
        freqx.append(freq)
        dt.append(dtmean[i]*freq)
        h.append(hmean[i])
<<<<<<< Updated upstream

plt.plot(freqx, h,".")
plt.show()
#plt.scatter(freqx, dt)
=======
        print(i)

# plt.scatter(freqx, h)
plt.scatter(freqx, dt, '.')
>>>>>>> Stashed changes
