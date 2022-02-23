# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:57:48 2022

@author: zways
"""
from library import *
from library import Etape
from library import g_CST

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
        
    def isColle(self):
        return self.bille.get_etape()==Etape.COLLE

    def isChute(self):
        return self.bille.get_etape()==Etape.CHUTE
        
    def newton_raphson(self, f, fprime, x, eps, cmax):
        """ Méthode de Newton-Raphson avec compteur. """
        compteur = 0
        while abs(f(x)) > eps and compteur < cmax:
            compteur += 1
            x = x - f(x) / fprime(x)
        return x, compteur

    def setColle(self,ti):
        self.bille.set_etape(Etape.COLLE)
        
    def setChute(self,ti):
        self.bille.set_etape(Etape.CHUTE)
        #TODO
        #self.evenements.append[self.bille.get_etape(),ti,tf,self.bille,self.plateau]
        #resoudre a=g
        
    def setChoc(self,ti):
        #adrien
        #tf=
        self.bille.set_etape(Etape.CHOC)
        self.evenements.append[Etape.CHOC,ti,ti,self.bille,self.plateau]

        if (self.bille.v)<(self.plateau.v) or (tf-ti)<10e-2:
            self.bille.set_etape(Etape.COLLE)
            self.evenements.append[Etape.COLLE,ti,ti,self.bille,self.plateau]
        else : 
            self.bille.set_etape(Etape.CHUTE)
            #self.evenements.append[self.bille.get_etape(),ti,tf,self.bille,self.plateau]

        
    def next_step(self,t):
        if self.isColle():
            if (self.plateau.a) > g_CST :
                self.evenements[-1][2]=t
                self.setChute(t)
        elif self.isChute():
            self.setChoc(t)
        
        
    
    def tick(self) :
        self.time +=self.dt
        self.plateau.tick()
        self.bille.tick(t, self.plateau.z, self.plateau.v, self.plateau.a)
    