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
        self.La=np.array([])
        self.Lamean=np.array([])
        self.Lastd=np.array([])
    
    def final(self,z_bille,z_plateau,t):
        plt.plot(t,z_bille,c="k")
        plt.plot(t,z_plateau,c="r")
        plt.show()
        
###################################
    def periode(self):
        #L = np.round(L, 1)
        # Remove DC component, as proposed by Nils Werner
        L=self.z_maxi
        L -= np.mean(L)
        # Window signal
        #L *= scipy.signal.windows.hann(len(L))
        
        fft = np.fft.rfft(L, norm="ortho")
        
        def abs2(x):
            return x.real**2 + x.imag**2
        
        selfconvol=np.fft.irfft(abs2(fft), norm="ortho")
        selfconvol=selfconvol/selfconvol[0]
        
        
        # let's get a max, assuming a least 4 periods...
        multipleofperiod=np.argmax(selfconvol[1:round(len(L)/4)])
        Ltrunk=L[0:(len(L)//multipleofperiod)*multipleofperiod]
        
        fft = np.fft.rfft(Ltrunk, norm="ortho")
        selfconvol=np.fft.irfft(abs2(fft), norm="ortho")
        selfconvol=selfconvol/selfconvol[0]
        
        
        #get ranges for first min, second max
        fmax=np.max(selfconvol[1:round(len(Ltrunk)/4)])
        fmin=np.min(selfconvol[1:round(len(Ltrunk)/4)])
        xstartmin=1
        while selfconvol[xstartmin]>fmin+0.2*(fmax-fmin) and xstartmin< len(Ltrunk)//4:
            xstartmin=xstartmin+1
        
        xstartmax=xstartmin
        while selfconvol[xstartmax]<fmin+0.7*(fmax-fmin) and xstartmax< len(Ltrunk)//4:
            xstartmax=xstartmax+1
        
        xstartmin=xstartmax
        while selfconvol[xstartmin]>fmin+0.2*(fmax-fmin) and xstartmin< len(Ltrunk)//4:
            xstartmin=xstartmin+1
        
        period=np.argmax(selfconvol[xstartmax:xstartmin])+xstartmax
        
        return period
####################################
        
    def render(self, phase=1):
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
            self.z_bs=np.concatenate((self.z_bs, z_b))
            
            if (self.evenements[i][0] =='CHOC'):
                plt.scatter(ti,bille.z,c="k",marker='o',label="bille")
                plt.title(bille.z)
                
            elif (self.evenements[i][0] =='COLLE'):
                plt.plot(t,z_b,c="k",label="bille")
                plt.plot(t,plateau.z,c="r",label="plateau")
                
            else : #état chute
                if len(z_b)!=0:
                    plt.plot(t,z_b,c="k",label="bille")
                    plt.plot(t,plateau.z,c="r",label="plateau")
                    dif_zp_zb=z_b-plateau.z
                    idx=np.argmax(dif_zp_zb)
                    self.z_maxi.append(dif_zp_zb[idx])
                    self.t_maxi.append(t[idx])
                    
    
        plt.show()        
        plt.scatter(self.t_maxi, self.z_maxi)
        periode=Graphic_engine.periode(self)
        self.La=np.array(self.z_maxi[:math.floor(len(self.z_maxi)/periode)*periode])
        self.La=self.La.reshape(math.floor(len(self.z_maxi)/periode), periode)
        
        self.Lamean=self.La.mean(axis=0)
        self.Lastd=self.La.std(axis=0)
    
        # plt.legend()
        # plt.xlim(3.4,3.7)
        # plt.ylim(-1,0)
        plt.show()
        
        t2=np.concatenate((self.t_maxi[1:],[0]))
        self.dt=t2-self.t_maxi
        self.dt=self.dt[:-1]
        
        self.dta=np.array(self.dt[:math.floor(len(self.dt)/periode)*periode])
        self.dta=self.dta.reshape(math.floor(len(self.dt)/periode), periode)
        self.dtamean=self.La.mean(axis=0)
        
        if phase:
            
            plt.scatter(dt, self.z_maxi[:-1]) 
            plt.xlabel("Différence temporelle entre deux rebonds (s)")
            plt.ylabel("Hauteur du rebond (m)")
            plt.xlim(0, 0.1)
            plt.ylim(0, 0.01)
            plt.show()

        return self.Lamean, self.dtamean
        
        # self.Lamean, self.Lastd
    # def render(self):
    #     z_b=[]
    #     for i in range(len(self.evenements)-1):
    #         ti=self.evenements[i][1]
    #         tf=self.evenements[i+1][1]
    #         t=np.arange(0,tf-ti,self.dt)
    #         plateau=self.evenements[i][3]
    #         bille=self.evenements[i][2]
    
        # def render(self):
        # z_b=[]
        # for i in range(len(self.evenements)-1):
        #     ti=self.evenements[i][1]
        #     tf=self.evenements[i+1][1]
        #     t=np.arange(ti,tf,self.dt)
        #     t_res=t-ti
        #     plateau=self.evenements[i][3]
        #     bille=self.evenements[i][2]
            
        #     plateau.tick(t)
        #     z_b=bille.traj_r(t_res,plateau.z)
        #     if (self.evenements[i][0] !='CHOC'):
        #         if self.evenements[i][0] =='CHUTE' :
        #             plt.scatter(ti,bille.z,c="k",marker='+',label="bille")

        #         plt.plot(t,z_b,c="k",label="bille")
        #         plt.plot(t,plateau.z,c="r",label="plateau")

        #         # plt.plot(t,plateau.a+g_CST,c="purple",label="plateau")


        #     else :
        #         plt.scatter(ti,bille.z,c="blue",marker='x',label="choc")
                
        # # plt.legend()
        # # plt.xlim(3.4,3.7)
        # # plt.ylim(-plateau.A ,1.5*plateau.A )
        # plt.grid()
        # plt.show()
            