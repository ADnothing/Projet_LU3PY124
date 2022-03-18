# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:58:19 2022

@author: zways
"""
from library import *

from library import g_CST



class Bille():
    def __init__(self,amortissement=0.5,v_i=0, z_i= 0,a_i=0,etape_i=Etape.COLLE):
        self.mu=amortissement    #coeff d'amortissement sans unité
        self.a=a_i      #acceleration en m/s^2
        self.v=v_i      #vitesse en m/s
        self.z=z_i      #hauteur en m
        self.etape=etape_i
        
        self.trajTab=[] # pour s'actualiser
        
        self.trajTab_return=[] # pour rendre une trajectoire
        
    
    def trajcolle(self,t, z, v, a):
         self.z=z
         self.v=v
         self.a=a
         
    def trajchute(self,t, z, v, a):
        self.z= -g_CST/2*t**2+self.v*t+self.z
        self.v= -g_CST*t+self.v
        self.a= -g_CST
        
    def trajchoc(self,t, z, v, a):
        self.z= z
        self.v= v-self.mu*(self.v-v)
        
    def trajcolle_r(self,t, z):
           return z
            
            
    def trajchute_r(self,t,z):
        return -g_CST/2*t**2+self.v*t +self.z

        
    def trajchoc_r(self,t, z):
        return z
    
    def init(self):
        
        self.trajTab_return.append(self.trajcolle_r)
        self.trajTab_return.append(self.trajchute_r)
        self.trajTab_return.append(self.trajchoc_r)
        
        self.traj_r =self.trajTab_return[self.etape.value-1]
        
        self.trajTab.append(self.trajcolle)
        self.trajTab.append(self.trajchute)
        self.trajTab.append(self.trajchoc)
        
        self.traj=self.trajTab[self.etape.value-1]
        
        
    def get_etape(self):
        return self.etape.name
    
    def set_etape(self,nouvelle_etape):
        self.etape= nouvelle_etape
        self.traj=self.trajTab[nouvelle_etape.value-1]
        self.traj_r =self.trajTab_return[nouvelle_etape.value-1]
    
    def tick(self, t, z, v, a) :
        self.traj(t,z,v,a)
        