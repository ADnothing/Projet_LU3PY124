# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:58:19 2022

@author: zways
"""
from library import *

from library import g_CST



class Bille():
    def __init__(self,amortissement=0.1,v_i=0, z_i= 0,a_i=0,etape_i=Etape.COLLE):
        self.mu=amortissement    #coeff d'amortissement sans unité
        self.a=a_i      #acceleration en m/s^2
        self.v=v_i      #vitesse en m/s
        self.z=z_i      #hauteur en m
        self.etape=etape_i
        
        self.trajTab=[] # pour s'actualiser
        
        def trajcolle(t, z, v, a):
            self.z=z
            self.v=v
            self.a=a
            
        def trajchute(t, z, v, a):
            self.z= -g_CST/2*t**2+self.v*t+self.z
            self.v= -g_CST*t+self.v
            self.a= -g_CST
            
        def trajchoc(t, z, v, a):
            self.z= z
            self.v= v-self.mu*(self.v-v)
        
        self.trajTab.append(trajcolle)
        self.trajTab.append(trajchute)
        self.trajTab.append(trajchoc)
        
        self.traj=self.trajTab[etape_i.value-1]
        
        self.trajTab_return=[] # pour rendre une trajectoire
        
        def trajcolle_r(t, z):
            return z
            
            
        def trajchute_r(t, z):
            return -g_CST/2*t**2+self.v*t+self.z

            
        def trajchoc_r(t, z):
            return z
        
        self.trajTab_return.append(trajcolle_r)
        self.trajTab_return.append(trajchute_r)
        self.trajTab_return.append(trajchoc_r)
        
        self.traj_r =self.trajTab_return[etape_i.value-1]

        
    def get_etape(self):
        return self.etape.name
    
    def set_etape(self,nouvelle_etape):
        self.etape= nouvelle_etape
        self.traj=self.trajTab[nouvelle_etape.value-1]
        self.traj_r =self.trajTab_return[nouvelle_etape.value-1]
    
    def tick(self, t, z, v, a) :
        self.traj(t,z,v,a)
    
    
       