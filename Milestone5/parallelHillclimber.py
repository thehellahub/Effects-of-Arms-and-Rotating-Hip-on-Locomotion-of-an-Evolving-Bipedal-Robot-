import copy
import os
import sys
import time
from solution import SOLUTION
import constants as c
import numpy as np


class PARALLEL_HILL_CLIMBER:


    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        os.system("rm tmp*.txt")

        self.parents                            = {}
        self.parent__2__fitness                 = {}
        self.nextAvailableID                    = 0
        self.fitness                            = -999
        self.bestIdx                            = 0 ;# index of the "best" parent
        for i in range(c.POPULATION_SIZE):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
            self.parent__2__fitness[i] = []


    def Print(self):
        for i in range(len(self.parents)):
            print(f"\n\nParent {i} fitness: {self.parents[i].fitness}, Child {i} fitness: {self.children[i].fitness}, Brain: {self.parents[i].brain}\n")

    def Evolve_For_One_Generation(self,mode):

        self.Spawn()
        
        self.Mutate()
        
        self.Evaluate(self.children)
        
        self.Print()

        i = 0
        for parent in self.parents:
            self.parent__2__fitness[i].append(self.parents[i].fitness)
            i+=1
        
        self.Select()

    def Evolve(self):
        self.Evaluate(self.parents)
        pcount = 0
        for parent in self.parents:
            self.parent = self.parents[parent]
            gcount = 0
            for currentGeneration in range(c.NUMBER_OF_GENERATIONS):
                self.Evolve_For_One_Generation("DIRECT")

    def Show_Best(self, gui):
        best = -999999999
        for parent in self.parents:
            if self.parents[parent].fitness > best:
                self.bestIdx = parent
                best = self.parents[parent].fitness

        # Show best sim
        if gui:
            self.parents[self.bestIdx].Start_Simulation("GUI")

        # Save best fitness as field
        self.fitness = self.parents[self.bestIdx].fitness

        # Check to see if the fitness is the best one we've recorded
        try:
            with open('best_fitness_score_on_record.txt', 'r') as f:
                result = f.readline()
                if result == '':
                    self.best_fitness_score_on_record = -999
                else:
                    self.best_fitness_score_on_record = float(result)
        except Exception as e:
            print(e)
            sys.exit()
            self.best_fitness_score_on_record = -999

        # If this is the best fitness we've seen on record, record it and capture the weights too
        if self.parents[self.bestIdx].fitness > self.best_fitness_score_on_record:

            # Saving the weights. We'll use these later when we want to evolve from a pre-existing NN (brain)
            file = open("best_weights_on_record.txt", "wb")
            np.save(file, self.parents[self.bestIdx].weights)
            file.close()

            # Write fitness to file
            best_fitness_file = open("best_fitness_score_on_record.txt", "w")
            best_fitness_file.write(str(self.parents[self.bestIdx].fitness))
            best_fitness_file.close()


    def Spawn(self):
        self.children = {}
        for i in range(len(self.parents)):
            self.child = copy.deepcopy(self.parents[i])
            self.child.Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
            self.children[i] = self.child


    def Mutate(self):
        for child in self.children:
            self.children[child].Mutate()


    def Select(self):
        for index in self.parents:
            if self.parents[index].fitness < self.children[index].fitness:
                self.parents[index] = self.children[index]

        if self.child.fitness > self.parent.fitness:
            self.parent = self.child


    def Evaluate(self, solutions):

        for solution in solutions:
            solutions[solution].Start_Simulation("DIRECT")

        for solution in solutions:
            solutions[solution].Wait_For_Simulation_To_End()




            