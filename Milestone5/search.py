import os
import constants as c
import numpy as np
from parallelHillclimber import PARALLEL_HILL_CLIMBER

class PHC_Wrapper:

    def __init__(self):

    	# Initialize the record for best fitness scores
        with open("best_fitness_score_on_record.txt", "w") as fitness_file:
            fitness_file.writelines("")
        with open("best_fitness_score_on_record.txt", "w") as fitness_file:
            fitness_file.writelines("")

        # Delete NN weights previous runs
        os.system("rm best_weights_on_record.txt")
        
        self.phc_run__2__fitness_scores_per_generation = dict()
        self.phc_fitness_scores = list()
        for i in range(c.PHC_RUNS):
            phc = PARALLEL_HILL_CLIMBER()
            phc.Evolve()
            phc.Show_Best(gui=False)
            self.phc_fitness_scores.append(phc.fitness)
            self.phc_run__2__fitness_scores_per_generation = phc.parent__2__fitness

        if c.SHOW_BEST:
        	input("\nEnter key to see GUI\n")
        	phc.Show_Best(gui=True)

        print("\nFitness Scores:")
        for fitness in self.phc_fitness_scores:
            print(fitness)


PHC_Wrapper()