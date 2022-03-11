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
    def __init__(self,timeStep=10e-4):
        self.dt=timeStep
        self.bille=Bille()
        self.plateau=Plateau()
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
        return -g_CST/2*t**2+self.bille.v*t+self.bille.z -self.plateau.A*np.sin(self.plateau.w*(t+ti))

    def zero_chute(self,ti, dt=epsilon_t):
        r_poly = (self.bille.v+math.sqrt(self.bille.v**2+2*g_CST*self.bille.z))/g_CST
        t=np.arange(dt,r_poly+4*np.pi/self.plateau.w,dt) #TODO faire mieux
        y=self.func_to_root(t,ti)
        idx = np.argwhere(np.diff(np.sign(y))).flatten()
        
        # plt.plot(t,y)
        # plt.show()

        return t[idx[0]]+ti
    
    # retourne le momoent de décollage
    def zero_colle(self,ti, dt=epsilon_t):

        t=ti+np.arange(dt,2*np.pi/self.plateau.w,dt) #on part de dt sinon premiere racine
        
        self.plateau.tick(t)
        
        a=-self.plateau.a
        v=self.plateau.v
        z=self.plateau.z
        # zb=self.bille.traj_r(t,z)
        # plt.plot(t,z,label="z plateau")
        # plt.plot(t,a-g_CST,label="a")
        # plt.plot(t,v,label="v")

        # plt.legend()
        # plt.show()
        
        
        idx = np.argwhere(np.diff(np.sign(a-g_CST)) ).flatten()
        # idx = np.argwhere( np.logical_and(np.diff(np.sign(a)), (v[:-1]>0))).flatten()

        

        self.plateau.tick(t[idx[0]])
        
        # if self.plateau.a  < g_CST :
        #     return t[idx[0]]
        # else :
        #     t=np.arange(t[idx[0]],t[idx[0]]+2*np.pi/self.plateau.w,dt)
        #     a=self.plateau.A*self.plateau.self.plateau.w**2 *np.sin(self.plateau.w*t)
        #     idx = np.argwhere(np.diff(np.sign(a))).flatten()
            
        #     plt.plot(t,a)
        #     plt.show()
        return t[idx[0]]
 

    def setColle(self,ti):
        self.tick(ti)

        # self.plateau.tick(ti)
        # self.bille.tick(ti,self.plateau.z,self.plateau.v,self.plateau.a)
        self.bille.set_etape(Etape.COLLE)
        self.evenements.append([Etape.COLLE.name,ti,deepcopy(self.bille),deepcopy(self.plateau)])

    def setChute(self,ti):
        self.tick(ti)
        # self.plateau.tick(ti)
        # self.bille.tick(ti,self.plateau.z,self.plateau.v,self.plateau.a)
        self.bille.set_etape(Etape.CHUTE)
        self.evenements.append([Etape.CHUTE.name,ti,deepcopy(self.bille),deepcopy(self.plateau)])
        #resoudre a=g
        
    def setChoc(self,ti):
        
        tf=self.zero_chute(ti)
        self.tick(tf)
        # self.plateau.tick(tf)
        # self.bille.tick(tf,self.plateau.z,self.plateau.v,self.plateau.a)
        self.bille.set_etape(Etape.CHOC)
        self.tick(tf)
        self.evenements.append([Etape.CHOC.name,tf,deepcopy(self.bille),deepcopy(self.plateau)])

        if (self.bille.v)<(self.plateau.v) or (tf-ti)<10e-2:
            self.bille.set_etape(Etape.COLLE)
            self.evenements.append([Etape.COLLE.name,tf,deepcopy(self.bille),deepcopy(self.plateau)])
        else : 
            self.bille.set_etape(Etape.CHUTE)
            self.evenements.append([Etape.CHUTE.name,tf,deepcopy(self.bille),deepcopy(self.plateau)])
        return tf

    
    def next_step(self,t):
        print(self.evenements[-1][0] , " : ",self.evenements[-1][1] )
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
        
        self.graphic.evenements = self.evenements
    
    def tick(self,t) :
        self.plateau.tick(t)
        self.bille.tick(t,self.plateau.z,self.plateau.v,self.plateau.a)
    