import sys
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
from sensor import SENSOR
from motor import MOTOR


class ROBOT:
    
    def __init__(self, directOrGUI):
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.nn = NEURAL_NETWORK("brain.nndf")
        self.directOrGUI = directOrGUI
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = dict()
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Think(self):
        self.nn.Update()
        if self.directOrGUI != 'DIRECT':
            self.nn.Print()

    def Prepare_To_Act(self):
        self.motors = dict()
        for jointName in pyrosim.jointNamesToIndices:
            jointName = jointName.decode('ASCII')
            #print(f"Joint name is: {jointName}")
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, index):
        for linkName in self.sensors:
            SENSOR.Get_Value(self.sensors[linkName], index)

    def Act(self, index):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                MOTOR.Set_Value(self.motors[jointName], desiredAngle, self.robotId)
                #print(f"\nNeuron name is: {neuronName}, joint name is: {jointName}, \
                #        desired angle is: {desiredAngle}")


    def Get_Fitness(self):

        self.stateOfLinkZero  = p.getLinkState(self.robotId,0)

        positionOfLinkZero    = self.stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        zCoordinateOfLinkZero = positionOfLinkZero[2]

        with open('fitness.txt', 'w') as f:
            f.write(str(xCoordinateOfLinkZero * zCoordinateOfLinkZero))