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
        
        
    def tick(self) :
        self.time +=self.dt
        self.plateau.tick()
        self.bille.tick()