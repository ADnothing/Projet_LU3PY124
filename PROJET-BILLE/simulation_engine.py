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
        self.evenements=[[self.bille.get_etape(),0,deepcopy(self.bille),deepcopy(self.plateau)]]
        
    def isColle(self):
        return self.bille.get_etape()==Etape.COLLE.name

    def isChute(self):
        return self.bille.get_etape()==Etape.CHUTE.name
        
    def is_decollage(self):
        return abs(self.plateau.A*self.plateau.w**2)  > g_CST
    
    def func_to_root(self,t,ti):
        return -g_CST/2*t**2+self.bille.v*t+self.bille.z -self.plateau.A*np.cos(self.plateau.w*(t+ti))

    def zero_chute(self,ti, dt=epsilon_t):
        
        t=0
        res=1
        while (res>0):
            # and (t < 10*np.pi*2/self.plateau.w)
            t +=dt
            res = self.func_to_root(t,ti)
            

        t -= dt
        return t+ti

    def func2(self, ti,t):
        return -self.plateau.w**2 *self.plateau.A*np.cos(self.plateau.w*(t+ti))+g_CST
        
        
        
    # retourne le momoent de décollage
    def zero_colle(self,ti, dt=epsilon_t):

        beta= math.acos(g_CST/(self.plateau.A*self.plateau.w**2))/self.plateau.w
        k0=np.floor(self.plateau.w*(ti+beta)/(2*np.pi))+1
        tf= np.pi*2*(k0)/(self.plateau.w)-beta
        return tf

    def zero_max(self,ti):

        k0=np.floor(self.plateau.w*(ti)/(2*np.pi))+1
        tf= np.pi*2*(k0)/(self.plateau.w)
        return tf
        

 

    def setColle(self,ti,tf):
        self.tick(ti,tf)
        self.bille.set_etape(Etape.COLLE)
        self.evenements.append([Etape.COLLE.name,tf,deepcopy(self.bille),deepcopy(self.plateau)])

    def setChute(self,ti,tf):
        self.tick(ti,tf)
        self.bille.set_etape(Etape.CHUTE)
        self.evenements.append([Etape.CHUTE.name,tf,deepcopy(self.bille),deepcopy(self.plateau),self.zero_max(ti)])
        
        #resoudre a=g
        
    def setChoc(self,ti):
        
        tf=self.zero_chute(ti)
        self.tick(ti,tf)
        # print("bille et plateau",self.bille.z,self.plateau.z)

        self.bille.set_etape(Etape.CHOC)
        # print("avant choc v=",self.bille.v)
        self.tick(ti,tf)
        # print("apres choc v=",self.bille.v)
        self.evenements.append([Etape.CHOC.name,tf,deepcopy(self.bille),deepcopy(self.plateau)])

        if ((self.bille.v)<=(self.plateau.v) ):
            # or (tf-ti)<1e-2
            
            self.evenements.pop()
            tf=self.evenements[-1][1]
            self.evenements[-1][0]=Etape.COLLE.name
            # self.time=
            self.evenements[-1][2].z=self.evenements[-1][3].z
            self.evenements[-1][2].v=self.evenements[-1][3].v
            self.evenements[-1][2].a=self.evenements[-1][3].a
            self.evenements[-1][2].set_etape(Etape.COLLE)
            self.bille.set_etape(Etape.COLLE)
            
        else : 
            self.bille.set_etape(Etape.CHUTE)
            self.evenements.append([Etape.CHUTE.name,tf,deepcopy(self.bille),deepcopy(self.plateau),self.zero_max(ti)])
        return tf

    
    def next_step(self,t):
        # print(self.evenements[-1][0] , " : ",self.evenements[-1][1] )
        # self.graphic.render()
        if self.isColle():
            if self.is_decollage():
                tf=self.zero_colle(t)
                self.setChute(t,tf)
                return tf
            else :
                print("la bille reste collée")
                self.setColle(t,t+1)
                return t+1
        else:                                   #on est en chute libre
            tf= self.setChoc(t)
            return tf
        
    
    def create_events(self,nb_events=100):
        for i in range(nb_events):
            self.time=self.next_step(self.time)
            if(i % 500 ==0):
                print('===================='+str(i))
            
        #TODO self.clean()  
        
        self.graphic.evenements = self.evenements
    
    def tick(self,ti,tf) :
        self.plateau.tick(tf)
        self.bille.tick(tf-ti,self.plateau.z,self.plateau.v,self.plateau.a)
    