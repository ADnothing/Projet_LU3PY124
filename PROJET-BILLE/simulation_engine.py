# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:57:48 2022

@author: zways
"""
from library import *
from bille import Bille
from plateau import Plateau
from graphic_engine import Graphic_engine

class Simulation_engine():
    def __init__(self,timeStep=10e-5):
        self.dt=timeStep
        self.time=0
        self.bille=Bille()
        self.plateau=Plateau()
        self.traj=None
        self.graphic=Graphic_engine()  
        self.evenements=[]
        
    def next_step(ti):
        if (self.bille.get_etape()==Etape.COLLE):
            if (self.plateau.a) > g :
                self.bille.set_etape(Etape.CHUTE)
                #TODO
                #self.evenements.append[self.bille.get_etape(),ti,tf,self.bille,self.plateau]
                #resoudre a=g
                
        elif (self.bille.get_etape()==Etape.CHUTE):
            #adrien
            #tf=
            self.bille.set_etape(Etape.CHOC)
            if (self.bille.v)<(self.plateau.v) or (tf-ti)<10e-2:
                self.bille.set_etape(Etape.COLLE)
        #TODO    
        else ():
            self.bille.set_etape(Etape.CHOC)
        
        #self.evenements.append[self.bille.get_etape(),ti,tf,self.bille,self.plateau]
        
    
    def tick(self) :
        self.time +=self.dt
        self.plateau.tick()
        self.bille.tick(t, self.plateau.z, self.plateau.v, self.plateau.a)
    