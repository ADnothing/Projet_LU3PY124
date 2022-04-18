# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 16:01:05 2022

@author: zways
"""
#plateau and simulation_engine
import math
import matplotlib.pyplot as plt
import numpy as np
#etats de la bille
from enum import Enum
class Etape(Enum):
     COLLE = 1
     CHUTE=2
     CHOC=3
#constante de simulation
epsilon_t = 5e-6

#constante physique
g_CST = 9.81     #m/s² 

