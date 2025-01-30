import numpy 
import sys
import time
import os
import random
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np 

class SOLUTION:

    def __init__(self, id):

        self.id = id

        if os.path.exists("best_weights_on_record.txt"):
            # 80% of the time, evolve from a previous brain
            # 20% of the time, evolve a new brain
            # This prevents getting stuck in local optima
            probability = random.randint(1,5)
            print(f"probability is: {probability}")
            if probability != 5:
                self.brain = "Inherited"
                file = open("best_weights_on_record.txt", "rb")
                self.weights = np.load(file)
                file.close()
            else:
                self.brain = "New"
                self.weights = np.random.rand(c.NUMBER_SENSOR_NEURONS, c.NUMBER_MOTOR_NEURONS) * 2 - 1
        else:
            self.brain = "New"
            self.weights = np.random.rand(c.NUMBER_SENSOR_NEURONS, c.NUMBER_MOTOR_NEURONS) * 2 - 1

    def Start_Simulation(self, GUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system(f"python simulate.py {GUI} {self.id}")
    
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists('fitness{}.txt'.format(self.id)):
            time.sleep(0.01)

        try:
            with open('fitness{}.txt'.format(self.id), 'r') as f:
                result = f.readline()
                result = float(result)
        except Exception as e:
            print(e)
            sys.exit()
        self.fitness = result
        #print("\n\nFitness of ID: {}, = {}".format(self.myID, self.fitness))
        os.system("rm fitness{}.txt".format(self.id))

    def Create_World(self):

        pyrosim.Start_SDF("world.sdf")

        length = 1
        width  = 1
        height = 1

        x = 10
        y = 10
        z = 0.5

        pyrosim.Send_Cube(name=f"Box", pos=[x,y,z] , size=[length,width,height])

        pyrosim.End()

    def Create_Body(self):

        pyrosim.Start_URDF("body.urdf")

        

        # Head
        head_position   =  c.FOOT_HEIGHT + c.SHIN_HEIGHT + c.THIGH_HEIGHT + c.TORSO_HEIGHT + c.NECK_HEIGHT + c.HEAD_HEIGHT
        
        pyrosim.Send_Cube(name="Head",  pos=[0, 0, head_position], size=[c.HEAD_DEPTH, c.HEAD_WIDTH, c.HEAD_HEIGHT])
        
        # Neck
        pyrosim.Send_Joint(name="Head_Neck", parent="Head", child="Neck", type="revolute",\
                           position=[0, 0, head_position-(c.HEAD_HEIGHT*c.NECK_HEIGHT)], jointAxis="0 0 1")
        pyrosim.Send_Cube(name="Neck",  pos=[0, 0, -0.25], size=[c.NECK_DEPTH, c.NECK_WIDTH, c.NECK_HEIGHT])
        
        # Torso

        pyrosim.Send_Joint(name="Neck_Torso", parent="Neck", child="Torso", type="revolute",\
                           position=[0, 0, (-1)*c.NECK_HEIGHT], jointAxis="1 0 0")
        
        
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, ((-1)*c.TORSO_HEIGHT)*.5], size=[c.TORSO_DEPTH, c.TORSO_WIDTH, c.TORSO_HEIGHT])

        # Hip
        if c.ROTATING_HIP:
            pyrosim.Send_Joint(name="Torso_Hip", parent="Torso", child="Hip", type="revolute",\
                           position=[0, 0, (c.TORSO_HEIGHT)*-1], jointAxis="0 1 1") # rotates with 0 0 1
        else:
            pyrosim.Send_Joint(name="Torso_Hip", parent="Torso", child="Hip", type="revolute",\
                           position=[0, 0, (c.TORSO_HEIGHT)*-1], jointAxis="0 1 0") # rotates with 0 0 1
        pyrosim.Send_Cube(name="Hip", pos=[0, 0, -0.125],   size=[c.TORSO_DEPTH, c.TORSO_WIDTH, 0.25])
        

        """  LOWER BODY   """

        # Thighs
        pyrosim.Send_Joint(name="Hip_UpperLleg", parent="Hip", child="UpperLleg", type="revolute",
                           position=[0,-0.625,-0.25], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="UpperLleg", pos=[0, 0, (-1)*(c.THIGH_HEIGHT/2)], size=[c.THIGH_DEPTH, c.THIGH_WIDTH, c.THIGH_HEIGHT])

        pyrosim.Send_Joint(name="Hip_UpperRleg", parent="Hip", child="UpperRleg", type="revolute",
                           position=[0,0.625,-0.25], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="UpperRleg", pos=[0, 0, (-1)*(c.THIGH_HEIGHT/2)], size=[c.THIGH_DEPTH, c.THIGH_WIDTH, c.THIGH_HEIGHT])


        # ''' Shins '''
        pyrosim.Send_Joint(name="UpperLleg_LowerLleg", parent="UpperLleg", child="LowerLleg", type="revolute",
                           position=[0, 0, -1*(c.THIGH_HEIGHT)], jointAxis="0 1 0")
        
        pyrosim.Send_Cube(name="LowerLleg", pos=[0, 0, (-1)*(c.SHIN_HEIGHT/2)], size=[c.SHIN_DEPTH, c.SHIN_WIDTH, c.SHIN_HEIGHT])

        pyrosim.Send_Joint(name="UpperRleg_LowerRleg", parent="UpperRleg", child="LowerRleg", type="revolute",
                           position=[0, 0, -1*(c.THIGH_HEIGHT)], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="LowerRleg", pos=[0, 0, (-1)*(c.SHIN_HEIGHT/2)], size=[c.SHIN_DEPTH, c.SHIN_WIDTH, c.SHIN_HEIGHT])


        # # Feet

        pyrosim.Send_Joint(name="LowerLleg_LFoot", parent="LowerLleg", child="LFoot", type="revolute",
                           position=[.15, 0, (-1)*c.SHIN_HEIGHT], jointAxis="0 1 0")

        
        pyrosim.Send_Cube(name="LFoot", pos=[(c.FOOT_LENGTH/4)-(c.FOOT_LENGTH/8),0,(-1)*(c.FOOT_HEIGHT/2)], size=[c.FOOT_LENGTH,.4,c.FOOT_HEIGHT])

        pyrosim.Send_Joint(name="LowerRleg_RFoot", parent="LowerRleg", child="RFoot", type="revolute",
                           position=[.15, 0, (-1)*c.SHIN_HEIGHT], jointAxis="0 1 0")

        pyrosim.Send_Cube(name="RFoot", pos=[(c.FOOT_LENGTH/4)-(c.FOOT_LENGTH/8),0,(-1)*(c.FOOT_HEIGHT/2)], size=[c.FOOT_LENGTH,.4,c.FOOT_HEIGHT])



        # """ UPPER BODY  """

        # # Shoulders and arms
        # #
        if c.ARMS:
            pyrosim.Send_Joint(name="Torso_Lshoulder", parent="Torso", child="Lshoulder", type="revolute",
                               position=[0,(-1)*(c.TORSO_WIDTH/2),-.25], jointAxis="1 1 0")

            
            pyrosim.Send_Cube(name="Lshoulder", pos=[0, (-1)*(c.SHOULDER_WIDTH/2), 0], size=[.5, c.SHOULDER_WIDTH, c.SHOULDER_HEIGHT])


            pyrosim.Send_Joint(name="Torso_Rshoulder", parent="Torso", child="Rshoulder", type="revolute",
                               position=[0,(c.TORSO_WIDTH/2),-.25], jointAxis="1 1 0")

            pyrosim.Send_Cube(name="Rshoulder", pos=[0, (c.SHOULDER_WIDTH/2), 0], size=[.5, c.SHOULDER_WIDTH, c.SHOULDER_HEIGHT])


            # # Arms
            
            pyrosim.Send_Joint(name="Lshoulder_LUpperArm", parent="Lshoulder", child="LUpperArm", type="revolute",
                               position=[0, (-1)*c.SHOULDER_WIDTH, (0.1*c.ARM_HEIGHT)], jointAxis="0 1 0")

            pyrosim.Send_Cube(name="LUpperArm", pos=[0, (-1)*(c.ARM_WIDTH/2), ((-1)*(c.ARM_HEIGHT/2))], size=[.2, c.ARM_WIDTH, c.ARM_HEIGHT])

            pyrosim.Send_Joint(name="LUpperArm_LLowerArm", parent="LUpperArm", child="LLowerArm", type="revolute",
                               position=[0, (-1)*(c.ARM_WIDTH/2), (-1)*(c.ARM_HEIGHT)], jointAxis="0 1 0")

            pyrosim.Send_Cube(name="LLowerArm", pos=[0, 0, (-1)*(c.ARM_HEIGHT/2)], size=[.25, c.ARM_WIDTH, c.ARM_HEIGHT])


            pyrosim.Send_Joint(name="Rshoulder_RUpperArm", parent="Rshoulder", child="RUpperArm", type="revolute",
                               position=[0, c.SHOULDER_WIDTH, (0.1*c.ARM_HEIGHT)], jointAxis="0 1 0")

            pyrosim.Send_Cube(name="RUpperArm", pos=[0, (c.ARM_WIDTH/2), ((-1)*(c.ARM_HEIGHT/2))], size=[.2, c.ARM_WIDTH, c.ARM_HEIGHT])

            pyrosim.Send_Joint(name="RUpperArm_RLowerArm", parent="RUpperArm", child="RLowerArm", type="revolute",
                               position=[0, (c.ARM_WIDTH/2), (-1)*(c.ARM_HEIGHT)], jointAxis="0 1 0")

            pyrosim.Send_Cube(name="RLowerArm", pos=[0, 0, (-1)*(c.ARM_HEIGHT/2)], size=[.25, c.ARM_WIDTH, c.ARM_HEIGHT])

        pyrosim.End()


    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.id}.nndf")

        pyrosim.Send_Sensor_Neuron(name=0, linkName="LFoot")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="RFoot")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="LowerLleg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LowerRleg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="UpperLleg")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="UpperRleg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="Hip")
        #pyrosim.Send_Sensor_Neuron(name=7, linkName="LUpperArm")
        #pyrosim.Send_Sensor_Neuron(name=8, linkName="RUpperArm")
        #pyrosim.Send_Sensor_Neuron(name=9, linkName="LLowerArm")
        #pyrosim.Send_Sensor_Neuron(name=10, linkName="RLowerArm")

        pyrosim.Send_Motor_Neuron(name=11, jointName="LowerLleg_LFoot")
        pyrosim.Send_Motor_Neuron(name=12, jointName="LowerRleg_RFoot")
        pyrosim.Send_Motor_Neuron(name=13, jointName="UpperLleg_LowerLleg")
        pyrosim.Send_Motor_Neuron(name=14, jointName="UpperRleg_LowerRleg")
        pyrosim.Send_Motor_Neuron(name=15, jointName="Torso_Hip")
        pyrosim.Send_Motor_Neuron(name=16, jointName="Hip_UpperLleg")
        pyrosim.Send_Motor_Neuron(name=17, jointName="Hip_UpperRleg")

        #pyrosim.Send_Motor_Neuron(name=18, jointName="Lshoulder_LUpperArm")
        #pyrosim.Send_Motor_Neuron(name=19, jointName="Rshoulder_RUpperArm")
        #pyrosim.Send_Motor_Neuron(name=20, jointName="LUpperArm_LLowerArm")
        #pyrosim.Send_Motor_Neuron(name=21, jointName="RUpperArm_RLowerArm")
        #pyrosim.Send_Motor_Neuron(name=22, jointName="Torso_Lshoulder")
        #pyrosim.Send_Motor_Neuron(name=23, jointName="Torso_Rshoulder")


        for currentRow in range(c.NUMBER_SENSOR_NEURONS):
            for currentColumn in range(c.NUMBER_MOTOR_NEURONS):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow,
                                     targetNeuronName=currentColumn + c.NUMBER_SENSOR_NEURONS,
                                     weight=self.weights[currentRow][currentColumn])

        pyrosim.End()


    def Mutate(self):

        randRow = random.randint(0, 2)

        randColumn = random.randint(0, 1)

        self.weights[randRow][randColumn] = random.random() * 2 - 1

    def Set_ID(self, ID):
        self.id = ID


