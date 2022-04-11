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
        self.z_maxi=[]
        self.t_maxi=[]
        self.z_bs=[]
        self.z_plateau=[]
        self.t_tot=[]
        self.La=np.array([])
        self.Lamean=np.array([])
        self.Lastd=np.array([])

    def final(self,z_bille,z_plateau,t):
        plt.plot(t,z_bille,c="k")
        plt.plot(t,z_plateau,c="r")
        plt.show()
        
   
        
    def calcul(self, plot=False):
        z_bs=[]
        t_tots=[]
        z_ps=[]
        z_b=[]
        dif_zp_zb=[]
        nb_event=len(self.evenements)-1

        # for i in range(int(np.ceil(2*nb_event/3)),nb_event):
        for i in range(10,nb_event):
            ti=self.evenements[i][1]
            tf=self.evenements[i+1][1]
            t=np.arange(ti,tf,self.dt)
            t_res=t-ti
            plateau=self.evenements[i][3]
            bille=self.evenements[i][2]
            
            plateau.tick(t)
            z_b=bille.traj_r(t_res,plateau.z)
            self.z_bs=np.concatenate((self.z_bs, z_b))
            self.t_tot=np.concatenate((self.t_tot, t))
            self.z_plateau=np.concatenate((self.z_plateau, plateau.z))
            
            if (self.evenements[i][0] =='CHUTE'):
                dif_zp_zb=z_b-plateau.z
                idx=np.argmax(dif_zp_zb)

                self.z_maxi.append(dif_zp_zb[idx])
                self.t_maxi.append(t[idx])
                # plt.plot(t,z_b,c="k",label="bille")
                # plt.plot(t,plateau.z,c="r",label="plateau")
                
        plt.show()

                
        t2=np.concatenate((self.t_maxi[1:],[0]))
        self.dt=t2-self.t_maxi

        # self.dt=self.dt[]
        if (plot):
            plt.scatter(self.dt,self.z_maxi,marker=".")
            plt.show()

        return self.z_maxi[:-1], self.dt[:-1],self.z_bs , self.z_plateau, self.t_tot
    
    
    
    def attracteur(self):
        z_bs=[]
        t_tots=[]
        z_ps=[]
        z_b=[]
        dif_zp_zb=[]
        nb_event=len(self.evenements)-1

        # for i in range(int(np.ceil(2*nb_event/3)),nb_event):
        for i in range(10,nb_event):
            ti=self.evenements[i][1]
            tf=self.evenements[i+1][1]
            t=np.arange(ti,tf,self.dt)
            t_res=t-ti
            plateau=self.evenements[i][3]
            bille=self.evenements[i][2]
            
            plateau.tick(t)
            z_b=bille.traj_r(t_res,plateau.z)
            if (self.evenements[i][0] =='CHUTE'):
                dif_zp_zb=z_b-plateau.z
                idx=np.argmax(dif_zp_zb)

                self.z_maxi.append(dif_zp_zb[idx])
                self.t_maxi.append(t[idx])
                # plt.plot(t,z_b,c="k",label="bille")
                # plt.plot(t,plateau.z,c="r",label="plateau")
                
        plt.show()

                
        t2=np.concatenate((self.t_maxi[1:],[0]))
        self.dt=t2-self.t_maxi

        # self.dt=self.dt[]


        return self.z_maxi[:-1], self.dt[:-1]
        

    
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
            