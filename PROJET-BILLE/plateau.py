# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:58:07 2022

@author: zways
"""
from library import *

class Plateau():
    def __init__(self,a_i=0,v_i=0, z_i=0,amplitude=1,frequence=10):
        self.a=a_i
        self.v=v_i
        self.z=z_i
        self.A=amplitude  #amplitude en m
        self.w=frequence  #frequence en Hz
        
    def tick(self,t):
        self.a=self.A * self.w**2  * math.cos(self.w*t)
        self.v=self.A*self.w *math.cos(self.w*t)
        self.z= self.A*math.sin(self.w*t)
        