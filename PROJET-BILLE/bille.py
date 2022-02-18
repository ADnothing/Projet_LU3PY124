# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:58:19 2022

@author: zways
"""
from library import *


class Etape(Enum):
     COLLE = 1
     CHUTE_LIBRE=2
     CHOC=3

class Bille():
    def __init__(self,amortissement=0.5,v_i=0, z_i= 10e-1,a_i=0,etape_i=Etape.COLLE):
        self.mu=amortissement    #coeff d'amortissement sans unité
        self.a=a_i      #acceleration en m/s^2
        self.v=v_i      #vitesse en m/s
        self.z=z_i      #hauteur en m
        self.g=9.81     #m/s²
        self.etape=etape_i
        self.traj=None
        self.trajTab=[]
        
        def trajcolle(t, z, v, a):
            self.z=z
            self.v=v
            self.a=a
            
        def trajchute(t, z, v, a):
            self.z=-self.g/2*t**2+self.v*t+self.z
            self.v=-self.g*t+self.v
            self.a=-self.g
            
        def trajchoc(t, z, v, a):
            self.z=z
            self.v=v-self.mu*(self.v-v)
        
        self.trajTab.append(trajcolle)
        self.trajTab.append(trajchute)
        self.trajTab.append(trajchoc)
        
    def get_etape(self):
        return self.etape.name
    
    def set_etape(self,nouvelle_etape):
        self.etape= Etape.nouvelle_etape
        self.traj=self.trajTab[etape.value]
    
    def tick(self, t, z, v, a) :
        self.traj(t)
       