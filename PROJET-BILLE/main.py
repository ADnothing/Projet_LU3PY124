# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:10:28 2022

@author: zways
"""
from library import *
from simulation_engine import Simulation_engine
from scipy.optimize import fsolve

MyEngine=Simulation_engine(a=0.46e-3,f=30)
MyEngine.create_events(20)
hmean, dtmean, z_bs, z_p, ttot=MyEngine.graphic.render(phase=1)


# freqx=[]
# h=[]
# dt=[]
# j=1
# for freq in np.linspace(0.280e-3,0.600e-3, 100):
#     print('===================='+str(j))
#     MyEngine=Simulation_engine(a=freq,f=30)

#     MyEngine.create_events(50)
#     hmean, dtmean=MyEngine.graphic.render(phase=1)
#     # for i in range(len(hmean)):
#     #     freqx.append(freq)
#     #     h.append(hmean[i])
#     j=j+1
#     for i in range(len(dtmean)):
#         freqx.append(freq)
#         dt.append(dtmean[i]*freq)
#         h.append(hmean[i])
#         print(i)

# # plt.scatter(freqx, h)
# plt.scatter(freqx, dt, '.')
