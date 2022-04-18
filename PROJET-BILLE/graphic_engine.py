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

    #permet de tracer graphiquement les trajectoires de la bile et du plateau à partir d'un tableau devenements
    def render(self):
        #tableau des hauteurs de la bille sur une trajectoire
        z_b=[]

        #on parcoure le tableau des evenements
        for i in range(len(self.evenements)-1):
            ######on recupere les variables stockées dans le tableau des evenements
            ti=self.evenements[i][1]
            tf=self.evenements[i+1][1]
            plateau=self.evenements[i][3]
            bille=self.evenements[i][2]
            ######on calcule la trajectoire de la bille et du blateau entre 2 evenements
            t=np.arange(ti,tf,self.dt)
            t_res=t-ti
            plateau.tick(t)
            z_b=bille.traj_r(t_res,plateau.z)
            if (self.evenements[i][0] !='CHOC'):  
                if self.evenements[i][0] =='CHUTE' :
                    plt.scatter(ti,bille.z,c="k",marker='+',label="bille") #on trace le point de décolage du plateau
                #on trace la trajectoire de la bille et du blateau
                plt.plot(t,z_b,c="k",label="bille")
                plt.plot(t,plateau.z,c="r",label="plateau")    
            else :
                #on trace une croix pour les chocs qui sont des evenement ponctuels
                plt.scatter(ti,bille.z,c="blue",marker='x',label="choc")
                
        # plt.legend()
        # plt.xlim(3.4,3.7)
        # plt.ylim(-plateau.A ,1.5*plateau.A )
        plt.grid()
        plt.show()
            