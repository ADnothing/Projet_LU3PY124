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



freqx=[] #ce qui va contenir les différentes amplitudes pour la biffuracation
h=[] #ce qui va contenir la hauteur des rebonds pour la biffurcation
dt=[] #ce qui va contenir le temps entre deux rebonds pour la biffurcation
Lyap = [] #ce qui va contenir les exposants de lyapunov pour chaques fréquences
j=0 #simple conteur pour informer l'utilisateur de la progression
As = np.linspace(0.280e-3,0.600e-3, 500) #array qui contient chauqe fréquences étudié

#Boucle qui compute la simulation pour chaque fréquence
for freq in As:
    print('===================='+str(j))
    #run 'normal'
    MyEngine=Simulation_engine(a=freq,f=30)
    #run avec un écart pour lyapunov
    MyEngine2=Simulation_engine(a=freq,f=30, vi=-0.3+1e-5)

    MyEngine.create_events(50)
    hmean,dtmean,z1,_,_ = MyEngine.graphic.render(phase=0)
    
    for i in range(len(hmean)):
        freqx.append(freq)
        h.append(hmean[i])
        
    for i in range(len(dtmean)):
        freqx.append(freq)
        dt.append(dtmean[i]*freq)
        h.append(hmean[i])
        #print(i)
        
    MyEngine2.create_events(50)
    _,_,z2,_,_ = MyEngine2.graphic.render(phase=0)
    
    #Donne l'indice max à prendre pour le fit du calcul de l'exposant de lyapunov
    N = min(len(z1), len(z2))

    #on délimite les arrays des trajectoires (on supprime les 100 premiers points qui divergent en 0 à cause du log)
    z1 = z1[100:N]
    z2 = z2[100:N]    
    
    #Lyapunov
    #On fait le fit linéaire du log de la différence relative entre les deux trajectoires
    from scipy.optimize import curve_fit
    mod_lin = lambda x, a, b: a*x + b
    delta = abs(z1 - z2)
    T = np.arange(0,len(delta),1)*epsilon_t

    popt, pcov = curve_fit(mod_lin, T, np.log(delta+1e-10))
    A,B = popt
    
    #print(A)
    Lyap.append(A)
    
    
    j+=1

#Plot de Lyapunov + biffurcation
fig = plt.figure(2, figsize=(10,10))
plt.gcf().subplots_adjust(hspace = 0.003)
lyapunov = plt.subplot(2,1,2)
for ind in range(len(As)):
    if Lyap[ind] < 0:
        mask = freqx==As[ind]
        plt.scatter(np.array(freqx)[mask], np.array(h)[mask], color='Black', marker='.')
    else:
        mask = freqx==As[ind]
        plt.scatter(np.array(freqx)[mask], np.array(h)[mask], color='Red', marker='.')

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
