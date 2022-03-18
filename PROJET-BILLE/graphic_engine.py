# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 15:58:37 2022

@author: zways
"""

from library import *
from copy import deepcopy

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
            t_res=t-ti
            plateau=self.evenements[i][3]
            bille=self.evenements[i][2]
            
            plateau.tick(t)
            z_b=bille.traj_r(t_res,plateau.z)
            if (self.evenements[i][0] =='CHOC'):
                print(bille.z)
                plt.scatter(ti,bille.z,c="k",marker='o',label="bille")
                plt.title(bille.z)
                # plt.show()
            else:
                plt.plot(t,z_b,c="k",label="bille")
                plt.plot(t,plateau.z,c="r",label="plateau")
        # plt.legend()
        plt.ylim(-2,2)
        plt.show()
        
    # def render(self):
    #     z_b=[]
    #     for i in range(len(self.evenements)-1):
    #         ti=self.evenements[i][1]
    #         tf=self.evenements[i+1][1]
    #         t=np.arange(0,tf-ti,self.dt)
    #         plateau=self.evenements[i][3]
    #         bille=self.evenements[i][2]
            