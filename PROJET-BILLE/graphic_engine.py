# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:58:37 2022

@author: zways
"""

from library import *

class Graphic_engine():
    def __init__(self,dt):
        self.dt=dt
        self.evenements=[]
    
    def final(self,z_bille,z_plateau,t):
        plt.plot(t,z_bille,c="k")
        plt.plot(t,z_plateau,c="r")
        plt.show()
        
    def render(self):
        z_b=[]
        for i in range(len(self.evenements)-1):
            ti=self.evenements[i][1]
            tf=self.evenements[i+1][1]
            t=np.arange(ti,tf,self.dt)
            plateau=self.evenements[i][3]
            bille=self.evenements[i][2]
            plateau.tick(t)
            z_b=bille.traj_r(t,plateau.z)
            plt.plot(t,z_b,c="k")
            plt.plot(t,plateau.z,c="r")
            plt.show()