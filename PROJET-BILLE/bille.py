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
    def __init__(self,amortissement=10e-1,v_i=0, z_i= 10e-1,a_i=0,etape_i=Etape.COLLE):
        self.mu=amortissement    #coeff d'amortissement sans unité
        self.a=a_i      #acceleration en m/s^2
        self.v=v_i      #vitesse en m/s
        self.z=z_i      #hauteur en m
        self.etape=etape_i
        
    def get_etape(self):
        return self.etape.name
    
    def set_etape(self,nouvelle_etape):
        self.etape= Etape.nouvelle_etape
    
    def tick(self) :
        print("a")
       