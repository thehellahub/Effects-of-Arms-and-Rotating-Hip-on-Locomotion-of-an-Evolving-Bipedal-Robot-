import sys
from simulation import SIMULATION

try:
	directOrGUI = sys.argv[1]
except:
	directOrGUI = "DIRECT"
simulation = SIMULATION(directOrGUI)
simulation.Run()
simulation.Get_Fitness()