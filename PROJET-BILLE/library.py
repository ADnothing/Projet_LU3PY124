# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 16:01:05 2022

@author: zways
"""
#plateau and simulation_engine
import math
#bille
from enum import Enum
class Etape(Enum):
     COLLE = 1
     CHUTE_LIBRE=2
     CHOC=3