# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 16:01:05 2022

@author: zways
"""
#plateau and simulation_engine
import math
import matplotlib.pyplot as plt
import numpy as np
#bille
from enum import Enum
class Etape(Enum):
     COLLE = 1
     CHUTE=2
     CHOC=3

epsilon_t = 5e-6
g_CST = 9.81     #m/s² 
