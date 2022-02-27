# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:10:28 2022

@author: zways
"""
from library import *
from simulation_engine import Simulation_engine
from scipy.optimize import fsolve


MyEngine=Simulation_engine()        

MyEngine.create_events(4)
# MyEngine.graphic.render()