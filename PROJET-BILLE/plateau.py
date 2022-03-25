# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:58:07 2022

@author: zways
"""
from library import *

class Plateau():
    def __init__(self,a_i=0,v_i=0, z_i=0,amplitude=1e-3,frequence=20):
        self.a=a_i
        self.v=v_i
        self.z=z_i
        self.A=amplitude  #amplitude en m
        self.w=2*np.pi*frequence  #frequence en Hz
        
    def tick(self,t):
        self.a= -self.A * self.w**2  * np.cos(self.w*t)
        self.v=-self.A*self.w *np.sin(self.w*t)
        self.z= self.A*np.cos(self.w*t)
        
    def traj_r(self,t):
        return self.A*np.cos(self.w*t)
    
    def a_r(self,t):
        return -self.A * self.w**2  * np.cos(self.w*t)