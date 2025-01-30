import os
import constants as c
import numpy as np
import pickle
from datetime import datetime
from collections import OrderedDict
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
        
        start_time = datetime.now()
        self.phc_run__2__fitness_scores_per_generation_of_best_parent = dict()
        self.phc_fitness_scores = list()
        for i in range(c.PHC_RUNS):
            phc = PARALLEL_HILL_CLIMBER()
            phc.Evolve()
            phc.Show_Best(gui=False)
            self.phc_run__2__fitness_scores_per_generation_of_best_parent[i] = phc.parent__2__fitness[phc.bestIdx]
            for fitness_score in phc.parent__2__fitness[phc.bestIdx]:
                best_fitness_score = fitness_score
            self.phc_fitness_scores.append(best_fitness_score)

        # Calculate the duration of this script
        end_time = datetime.now()
        duration = ( (end_time - start_time).total_seconds() ) / 3600

        if c.SHOW_BEST:
        	input("\nEnter key to see GUI\n")
        	phc.Show_Best(gui=True)

        print("\nFitness Scores:")
        for fitness in self.phc_fitness_scores:
            print(fitness)

        print("\nFitness evolution for each PHC run: ")
        for phc_run in self.phc_run__2__fitness_scores_per_generation_of_best_parent.keys():
            print(f"PHC #{phc_run}: {self.phc_run__2__fitness_scores_per_generation_of_best_parent[phc_run]}")

        print(f"\nBest fitness score: {max(self.phc_fitness_scores)}")
        print(f"\nDuration: {duration}")

        # Serialize the information from this PHC_Wrapper class to a file to be post-processed later
        info = dict()
        info["phc_run__2__fitness_scores_per_generation_of_best_parent"] = self.phc_run__2__fitness_scores_per_generation_of_best_parent
        info['best_fitness_score'] = max(self.phc_fitness_scores)
        info['fitness_scores'] = self.phc_fitness_scores
        info["duration"] = duration
        with open(f'arms_{c.ARMS}_RT_{c.ROTATING_HIP}.pkl', 'wb') as file: 
            pickle.dump(info, file)

        # Plot the data from the run
        os.system("python fitness_plotter.py")


PHC_Wrapper()