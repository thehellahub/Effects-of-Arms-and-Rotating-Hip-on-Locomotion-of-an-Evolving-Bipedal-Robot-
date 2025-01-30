from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER:

    def __init__(self):
        self.parent = SOLUTION()

    def Show_Best(self):
        self.Evolve_For_One_Generation("GUI")
        print(f"Parent Fitness: {self.parent.fitness}")

    def Evolve(self):
        self.parent.Evaluate("GUI")
        for currentGeneration in range(c.NUMBER_OF_GENERATIONS):
            self.Evolve_For_One_Generation("DIRECT")

    def Print(self):
        print(f"\n\n### Parent fitness: {self.parent.fitness}, Child fitness: {self.child.fitness}\n")

    def Evolve_For_One_Generation(self,mode):
        self.Spawn()

        self.Mutate()

        self.child.Evaluate(mode)

        self.Print()

        self.Select()

    def Spawn(self):
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        self.parent.Mutate()

    def Select(self):
        if self.child.fitness > self.parent.fitness:
            self.parent = self.child