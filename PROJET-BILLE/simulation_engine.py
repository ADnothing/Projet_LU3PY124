# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:57:48 2022

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

class Simulation_engine():
    def __init__(self,timeStep=10e-4):
        self.dt=timeStep
        self.time=0
        self.bille=Bille()
        self.plateau=Plateau(frequence=10)
        self.traj=None
        self.graphic=Graphic_engine(timeStep)
        self.evenements=[[self.bille.get_etape(),0,self.bille,self.plateau]]
        
    def isColle(self):
        return self.bille.get_etape()==Etape.COLLE.name

    def isChute(self):
        return self.bille.get_etape()==Etape.CHUTE.name
        
    def is_decollage(self):
        return self.plateau.A*self.plateau.w**2  > g_CST
    
    def func_to_root(self,t,ti):
        return -g_CST/2*t**2+self.bille.v*t+self.bille.z -self.plateau.A*np.sin(self.plateau.w*(t+ti))

    def zero_chute(self,ti, dt=epsilon_t):
        print(self.bille.v**2+2*g_CST*self.bille.z)
        r_poly = (self.bille.v+math.sqrt(self.bille.v**2+2*g_CST*self.bille.z))/g_CST
        t=np.arange(0+dt,r_poly+4*np.pi/self.plateau.w,dt)
        y=self.func_to_root(t,ti)
        idx = np.argwhere(np.diff(np.sign(y))).flatten()

        return t[idx[0]]+ti
    
    def zero_colle(self,ti, dt=epsilon_t):
        t=ti+np.arange(dt,2*np.pi/self.plateau.w,dt)
        y=self.plateau.A*self.plateau.w**2 *np.sin(self.plateau.w*t)
        idx = np.argwhere(np.diff(np.sign(y))).flatten()
        
        self.plateau.tick(t[idx[0]]-dt)
        
        if self.plateau.a - g_CST< 0 :
            return t[idx[0]]
        else :
            t=np.arange(t[idx[0]],t[idx[0]]+2*np.pi/self.plateau.w,dt)
            y=self.plateau.A*self.plateau.self.plateau.w**2 *np.sin(self.plateau.w*t)
            idx = np.argwhere(np.diff(np.sign(y))).flatten()
            return t[idx[0]]
 

    def setColle(self,ti):
        self.tick(ti)

        # self.plateau.tick(ti)
        # self.bille.tick(ti,self.plateau.z,self.plateau.v,self.plateau.a)
        self.bille.set_etape(Etape.COLLE)
        self.evenements.append([Etape.COLLE.name,ti,self.bille,self.plateau])

    def setChute(self,ti):
        self.tick(ti)
        # self.plateau.tick(ti)
        # self.bille.tick(ti,self.plateau.z,self.plateau.v,self.plateau.a)
        self.bille.set_etape(Etape.CHUTE)
        self.evenements.append([Etape.CHUTE.name,ti,self.bille,self.plateau])
        #resoudre a=g
        
    def setChoc(self,ti):
        
        tf=self.zero_chute(ti)
        self.tick(tf)
        # self.plateau.tick(tf)
        # self.bille.tick(tf,self.plateau.z,self.plateau.v,self.plateau.a)
        self.bille.set_etape(Etape.CHOC)
        self.tick(tf)
        self.evenements.append([Etape.CHOC.name,tf,self.bille,self.plateau])

        if (self.bille.v)<(self.plateau.v) or (tf-ti)<10e-2:
            self.bille.set_etape(Etape.COLLE)
            self.evenements.append([Etape.COLLE.name,tf,self.bille,self.plateau])
        else : 
            self.bille.set_etape(Etape.CHUTE)
            self.evenements.append([Etape.CHUTE.name,tf,self.bille,self.plateau])
        return tf

    
    def next_step(self,t):
        
        print(self.bille.get_etape()," : ", self.time)

        if self.isColle():
            if self.is_decollage():
                tf=self.zero_colle(t)
                self.setChute(tf)
                return tf
            else :
                print("la bille reste collée")
                self.setColle(t+1)
                return t+1
        else:                                   #on est en chute libre
            tf= self.setChoc(t)
            return tf
        
    
    def create_events(self,nb_events=100):
        for i in range(nb_events):
            self.time=self.next_step(self.time)
            
        self.graphic.evenements=self.evenements
    
    def tick(self,t) :
        self.plateau.tick(t)
        self.bille.tick(t,self.plateau.z,self.plateau.v,self.plateau.a)
    