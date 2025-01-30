import os
import constants as c
from hillclimber import HILL_CLIMBER

#for i in range(2):
#    os.system("python generate.py")
#    os.system("python simulate.py")

hc = HILL_CLIMBER()
hc.Evolve()
hc.Show_Best()