# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:57:48 2022
S
@author: zways
"""
from library import *
from library import Etape
from library import g_CST
import numpy as np
import math
from bille import Bille
from plateau import Plateau
from graphic_engine import Graphic_engine
from copy import deepcopy

class Simulation_engine():
    
    def __init__(self,timeStep=epsilon_t,a=8e-3,f=20,vi=-0.3,ei=Etape.CHUTE,zi=6e-3):
        self.dt=timeStep
        self.bille=Bille(v_i=vi, z_i= zi,etape_i=ei)
        self.bille.init()
        self.plateau=Plateau(amplitude=a,frequence=f)
        self.time= 0
        self.traj=None
        self.graphic=Graphic_engine(timeStep)
         #il faut utiliser la commande deepcopy pour stocker de maniere durable les objets car python fait des passages par reference des objets qu'il stocke
        self.evenements=[[self.bille.get_etape(),0,deepcopy(self.bille),deepcopy(self.plateau)]]
        
        
    ###############SIMULATION ET GENERATION D'EVENEMENTS################################

    def isColle(self):
        return self.bille.get_etape()==Etape.COLLE.name

    def isChute(self):
        return self.bille.get_etape()==Etape.CHUTE.name
        
    def is_decollage(self):
        return abs(self.plateau.A*self.plateau.w**2)  > g_CST
    
    #fonction dont on trouve la racine dans la methode zero_chute
    def func_to_root(self,t,ti):
        #on manie le temps relatif t pour la chute libre de la bille et le temps global t+ti pour l'oscillation du plateau
        return -g_CST/2*t**2+self.bille.v*t+self.bille.z -self.plateau.A*np.cos(self.plateau.w*(t+ti)) 

    # calcule le temps de chute de la bille avant de rencontrer le plateau en avancant pas à pas
    def zero_chute(self,ti, dt=epsilon_t):
        t=0
        res=1
        while (res>0):
            t +=dt
            res = self.func_to_root(t,ti)
        #lorsque la bille a traversé le plateau, on revient en arriere d'un pas de temps et on a le temps de chute
        t -= dt
        return t+ti       
        
    # retourne le moment de décollage
    def zero_colle(self,ti, dt=epsilon_t):
        #donne l'angle associé à l'acceleration g sur le cercle trigonometrique
        beta= math.acos(g_CST/(self.plateau.A*self.plateau.w**2))/self.plateau.w
        #permet de trouver le nombre de tours effectués sur le cercle trigonometrique au temps ti
        k0=np.floor(self.plateau.w*(ti+beta)/(2*np.pi))+1
        #donne la solution associée au temps de decollage pour un temps de collage ti
        tf= np.pi*2*(k0)/(self.plateau.w)-beta
        return tf
   

 
    #transitions d'etat de la bille #
    def setColle(self,ti,tf):
        self.tick(ti,tf)
        self.bille.set_etape(Etape.COLLE)
        self.evenements.append([Etape.COLLE.name,tf,deepcopy(self.bille),deepcopy(self.plateau)])

    def setChute(self,ti,tf):
        self.tick(ti,tf)
        self.bille.set_etape(Etape.CHUTE)
        self.evenements.append([Etape.CHUTE.name,tf,deepcopy(self.bille),deepcopy(self.plateau)])
        
       
    def setChoc(self,ti): 
        tf=self.zero_chute(ti)
        self.tick(ti,tf)
        self.bille.set_etape(Etape.CHOC)
        #le choc étant ponctuel, on peut directement placer la bille dans son nouvel état
        self.tick(ti,tf)
        self.evenements.append([Etape.CHOC.name,tf,deepcopy(self.bille),deepcopy(self.plateau)])
        # si il se passe moins de 0.01 sec entre 2 chocs, ou que la vitesse de la bille apres choc n'est pas assez  importante pour décoller
        # la bille reste collée au plateau
        if ((self.bille.v)<=(self.plateau.v) or (tf-ti)<1e-2 ):
            self.evenements.pop()
            tf=self.evenements[-1][1]
            self.evenements[-1][0]=Etape.COLLE.name
            self.evenements[-1][2].z=self.evenements[-1][3].z
            self.evenements[-1][2].v=self.evenements[-1][3].v
            self.evenements[-1][2].a=self.evenements[-1][3].a
            self.evenements[-1][2].set_etape(Etape.COLLE)
            self.bille.set_etape(Etape.COLLE)
            
        else : #sinon, la bille est en chute libre
            self.bille.set_etape(Etape.CHUTE)
            self.evenements.append([Etape.CHUTE.name,tf,deepcopy(self.bille),deepcopy(self.plateau)])
        return tf

    #on calcule le prochain état 
    def next_step(self,t):
        # si la bille est collée alors on calcule son décollage
        if self.isColle():
            if self.is_decollage():
                tf=self.zero_colle(t)
                self.setChute(t,tf)
                return tf
            else :
                print("la bille reste collée")
                self.setColle(t,t+1)
                return t+1
        else:                      
            #Si la bille est en chute libre, on calcule son temps d'aterrisage
            tf= self.setChoc(t)
            return tf
        
    #on crée tous les evenements de simulation
    def create_events(self,nb_events=100,tfinal=10000):
        for i in range(nb_events):
            self.time=self.next_step(self.time)
            if (tfinal<self.time):
                break
            # if(i % 500 ==0):
            #     print('===================='+str(i))
            
        #on ajoute les evenements au moteur graphique
        self.graphic.evenements = self.evenements
    
    #permet de mettre à jour les etats de la bille et du plateau au temps tf en partant du temps ti
    def tick(self,ti,tf) :
        self.plateau.tick(tf)
        self.bille.tick(tf-ti,self.plateau.z,self.plateau.v,self.plateau.a)
        
        
        
        
        
        
        ######CALCUL ET ANALYSE DE DONNEES##########
        
    def bifurcation(self, plot=False):
        z_bs=[] #tableau final des hauteurs de bille
        z_plateau=[]#tableau des hauteurs de plateau
        z_maxi=[]#tableau des hauteurs maximales de bille sur chaque portion de chute libre
        t_tots=[]#tableau final des temps
        t_maxi=[]#z_maxi pour les temps
        z_b=[]
        dif_zp_zb=[]
        nb_event=len(self.evenements)-1

        for i in range(int(np.ceil(2*nb_event/3)),nb_event):# on enleve les 2/3 des premiers evenements qui interviennent avant une stabilité tres fine
            #on recupere les variables du tableau d'evenements
            ti=self.evenements[i][1]
            tf=self.evenements[i+1][1]
            plateau=self.evenements[i][3]
            bille=self.evenements[i][2]
            ######on calcule la trajectoire de la bille et du blateau entre 2 evenements
            t=np.arange(ti,tf,self.dt)
            t_res=t-ti
            plateau.tick(t)
             # on ajoute les trajectoires calculées au fur et a mesure
            z_b=bille.traj_r(t_res,plateau.z)
            z_bs=np.concatenate((z_bs, z_b))
            t_tots=np.concatenate((t_tots, t))
            z_plateau=np.concatenate((z_plateau, plateau.z))
           
            if (self.evenements[i][0] =='CHUTE'):
                dif_zp_zb=z_b-plateau.z
                idx=np.argmax(dif_zp_zb)
                # on ajoute les extremas de hauteurs sur chaque portion parabolique
                z_maxi.append(dif_zp_zb[idx])
                t_maxi.append(t[idx])
                # plt.plot(t,z_b,c="k",label="bille")
                # plt.plot(t,plateau.z,c="r",label="plateau")
        plt.show()
        #traitement sur la taille du tableau
        t2=np.concatenate((t_maxi[1:],[0]))
        delta_t=t2-t_maxi

        # self.dt=self.dt[]
        if (plot):
            #on trace de diagramme de bifurcation
            plt.scatter(delta_t,z_maxi,marker=".")
            plt.show()
        return z_maxi[:-1], delta_t[:-1],z_bs
    
    
    
    def attracteur(self):
        z_maxi=[]#tableau des hauteurs maximales de bille sur chaque portion de chute libre
        t_maxi=[]#z_maxi pour les temps
        z_bs=[] #tableau final des hauteurs de bille
        dif_zp_zb=[]
        nb_event=len(self.evenements)-1

        for i in range(10,nb_event):# on enleve les 10 premiers evenements qui interviennent avant stabilité
            #on recupere les variables du tableau d'evenements
            ti=self.evenements[i][1]
            tf=self.evenements[i+1][1]
            plateau=self.evenements[i][3]
            bille=self.evenements[i][2]
            ######on calcule la trajectoire de la bille et du blateau entre 2 evenements
            t=np.arange(ti,tf,self.dt)
            t_res=t-ti
            plateau.tick(t)
            z_b=bille.traj_r(t_res,plateau.z)
            if (self.evenements[i][0] =='CHUTE'):
            # on ajoute les trajectoires calculées au fur et a mesure

                dif_zp_zb=z_b-plateau.z
                idx=np.argmax(dif_zp_zb)

                z_maxi.append(dif_zp_zb[idx])
                t_maxi.append(t[idx])
                # plt.plot(t,z_b,c="k",label="bille")
                # plt.plot(t,plateau.z,c="r",label="plateau")
                
        plt.show()

                
        t2=np.concatenate((t_maxi[1:],[0]))
        delta_t=t2-t_maxi


        return z_maxi[:-1], delta_t[:-1]
    
    def calc_traj_tot(self):
        z_bs=[]
        t_tots=[]
        z_b=[]
        nb_event=len(self.evenements)-1
        for i in range(nb_event):
            #on recupere les variables du tableau d'evenements
            ti=self.evenements[i][1]
            tf=self.evenements[i+1][1]
            plateau=self.evenements[i][3]
            bille=self.evenements[i][2]
            ######on calcule la trajectoire de la bille et du blateau entre 2 evenements
            t=np.arange(ti,tf,self.dt)
            t_res=t-ti
            plateau.tick(t)
            z_b=bille.traj_r(t_res,plateau.z)
            # on ajoute les trajectoires calculées au fur et a mesure
            z_bs=np.concatenate((z_bs, z_b))
            t_tots=np.concatenate((t_tots, t))
            
        return z_bs,t_tots
    
    def calc_periode(self, nb_rebonds):
        t_periode=[]
        nb_event=len(self.evenements)-1
        j=0
        for i in range(10,nb_event): # on enleve les 10 premiers evenements qui interviennent avant stabilité
            ti=self.evenements[i][1]
            
            if (self.evenements[i][0] =='CHOC'):
                if (0==j%nb_rebonds):
                    #on stocke les temps tous les nb_rebonds chocs
                    t_periode.append(ti)
                j+=1
        t_periode=np.array(t_periode)
        #on calcule le temps entre chaque temps stocké consecutifs
        t_periode=np.diff(t_periode)
        #on calcule la moyenn et l'ecart type
        periode_mean=t_periode.mean()
        std=t_periode.std()
        
        return periode_mean,std
    
    
    
        