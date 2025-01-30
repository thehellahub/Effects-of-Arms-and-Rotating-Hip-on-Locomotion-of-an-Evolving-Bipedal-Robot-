from search import PHC_Wrapper
import constants as c

fitness_scores = []

for i in range(c.NUM_PHC_WRAPPERS):
    run = PHC_Wrapper()
    fitness_scores.append(run.fitness_scores)

print("\nfitness_scores:")
for run in fitness_scores:
    print(run)

if c.ARMS and c.ROTATING_HIP:
    with open("arms_and_rotating_hip_phc_fitness.csv", "a+") as file:
        for i in range(c.PHC_RUNS):
            for run in fitness_scores:
                file.write(str(run[i]) + ",")
            file.write("\n")

elif c.ARMS and not c.ROTATING_HIP:
    with open("arms_and_no_rotating_hip_phc_fitness.csv", "a+") as file:
        for i in range(c.PHC_RUNS):
            for run in fitness_scores:
                file.write(str(run[i]) + ",")
            file.write("\n")

elif not c.ARMS and c.ROTATING_HIP:
    with open("no_arms_and_rotating_hip_phc_fitness.csv", "a+") as file:
        for i in range(c.PHC_RUNS):
            for run in fitness_scores:
                file.write(str(run[i]) + ",")
            file.write("\n")

elif not c.ARMS and not c.ROTATING_HIP:
    with open("no_arms_and_no_rotating_hip_phc_fitness.csv", "a+") as file:
        for i in range(c.PHC_RUNS):
            for run in fitness_scores:
                file.write(str(run[i]) + ",")
            file.write("\n")