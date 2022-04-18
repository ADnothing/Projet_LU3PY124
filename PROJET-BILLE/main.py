# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:10:28 2022

@author: zways
"""
from library import *
from simulation_engine import Simulation_engine
from scipy.optimize import fsolve

def attracteur_render (a=0.460e-3):
    MyEngine=Simulation_engine(a=a,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3) # conditions initiales de simulation
    MyEngine.create_events(1000)
    hmean, dtmean=MyEngine.attracteur() #on calcule l'attracteur étrange sur la base des 1000 evenements calculés
    # plt.xlim(0.03,0.035)
    plt.plot(dtmean, hmean, ',')    #affichage de l'attracteur
    plt.show()
    return dtmean,hmean

def bifurcation_render():
    amplitudex=[]
    h=[]
    j=1
    
    for amplitude in np.linspace(0.400e-3,0.600e-3, 10):
        print('===================='+str(j))                #permet de connaitre l'avancement des simulations
        MyEngine=Simulation_engine(a=amplitude,f=30)        #on genere pour une simulation pour chaque amplitude à etudier
    
        MyEngine.create_events(200)
        hmean, dtmean, z_bs =MyEngine.bifurcation()         #on enregistre toutes les hauteurs liées à une amplitude
        for i in range(len(hmean)):
            amplitudex.append(amplitude)    
            h.append(hmean[i])
        j=j+1

    plt.plot(amplitudex, h, ',')
    plt.show()
    
    return amplitudex , h

def Lyapunov ():
    amplitudex=[] #ce qui va contenir les différentes amplitudes pour la biffuracation
    h=[] #ce qui va contenir la hauteur des rebonds pour la biffurcation
    Lyap = [] #ce qui va contenir les exposants de lyapunov pour chaques fréquences
    j=0 #simple conteur pour informer l'utilisateur de la progression
    As = np.linspace(0.400e-3,0.600e-3, 10) #array qui contient chauqe fréquences étudié
    
    #Boucle qui compute la simulation pour chaque fréquence
    for amplitude in As:
        print('===================='+str(j))
        #run 'normal'
        MyEngine=    MyEngine=Simulation_engine(a=amplitude,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)
        #run avec un écart pour lyapunov
        MyEngine2=Simulation_engine(a=amplitude,f=30,vi=-0.3+1e-5,ei=Etape.CHUTE,zi=6e-3)
    
        MyEngine.create_events(50)
        z1,t1= MyEngine.calc_traj_tot()    
            
        MyEngine2.create_events(50)
        z2,t2 = MyEngine2.calc_traj_tot()
        plt.plot(t1,z1)
        plt.plot(t2,z2)
    
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
        Lyap.append(A)
        j+=1
    

    
    return As,Lyap

# def plot_lyapunov_bifurcation(As,Lyap,amplitudex,h):
    
#         #Plot de Lyapunov + biffurcation
#     fig = plt.figure(2, figsize=(10,10))
#     plt.gcf().subplots_adjust(hspace = 0.003)
#     lyapunov = plt.subplot(2,1,2)
#     Lyap=np.array(Lyap)
    
#     color_cond=np.zeros(shape=Lyap.shape)
    
#     color_cond=np.array(Lyap.shape)
#     color_cond[Lyap<0]="black"
#     color_cond[Lyap>=0]="red"

        
#     plt.ylabel('hauteur \n des rebonds [m]')
#     plt.xlabel('Amplitude [m]')
#     plt.grid()
    
#     plt.subplot(2,1,1)
#     plt.scatter(As,Lyap, color=color_cond, marker='.')
#     plt.axhline(0, color="blue")
#     plt.ylabel('Exposant de Lyapunov')
#     plt.grid()       
#     plt.subplot(2,1,2)
    
#     color_cond=np.array(len(amplitudex))

#     c2=np.repeat(color_cond, amplitudex.size / As.size)

    
    
#     plt.plot(amplitudex, h,color=c2,marker= '.')
#     plt.show()
    

########### DIAGRAMME DE BIFURCATION ###############
# amplitudex , h=bifurcation_render()

########### EXPOSANT DE LYAPUNOV ###################
# As,Lyap=Lyapunov()


# plot_lyapunov_bifurcation(As,Lyap,amplitudex,h)

########## CALCUL DE LA  PERIODICITE DES TRAJECTOIRES POUR 4 REGIMES DIFFERENTS ############

# #1REBOND
MyEngine=Simulation_engine(a=0.350e-3,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)

# #2REBONDS
# MyEngine=Simulation_engine(a=0.425e-3,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)

# #4REBONDS
# MyEngine=Simulation_engine(a=0.448e-3,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)

# #CHAOTIQUE
# MyEngine=Simulation_engine(a=0.470e-3,f=30,vi=-0.3,ei=Etape.CHUTE,zi=6e-3)

nb_event=30
MyEngine.create_events(nb_event)


# mean,std=MyEngine.calc_periode(4)
MyEngine.graphic.render()

# print(mean)
# print(std)
# print(abs(mean-4/30))
# print(mean*30)

