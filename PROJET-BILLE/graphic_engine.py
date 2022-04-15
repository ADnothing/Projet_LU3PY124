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
        # self.La=np.array([])
        # self.Lamean=np.array([])
        # self.Lastd=np.array([])



    
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
            if (self.evenements[i][0] !='CHOC'):
                if self.evenements[i][0] =='CHUTE' :
                    plt.scatter(ti,bille.z,c="k",marker='+',label="bille")
    
                plt.plot(t,z_b,c="k",label="bille")
                plt.plot(t,plateau.z,c="r",label="plateau")
    
                # plt.plot(t,plateau.a+g_CST,c="purple",label="plateau")
    
    
            else :
                plt.scatter(ti,bille.z,c="blue",marker='x',label="choc")
                
        # plt.legend()
        # plt.xlim(3.4,3.7)
        # plt.ylim(-plateau.A ,1.5*plateau.A )
        plt.grid()
        plt.show()
            