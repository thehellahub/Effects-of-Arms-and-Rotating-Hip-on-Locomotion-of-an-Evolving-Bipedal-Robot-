import os
import sys
import pybullet as p
import pyrosim.pyrosim as pyrosim
import time
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c
from sensor import SENSOR
from motor import MOTOR


class ROBOT:
    
    def __init__(self, GUI, solutionID):
        self.solutionID = solutionID
        self.robotId = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.nn = NEURAL_NETWORK(f"brain{solutionID}.nndf")
        self.directOrGUI = GUI
        self.Prepare_To_Sense()
        self.Prepare_To_Act()
        os.system("rm brain{}.nndf".format(self.solutionID))
        self.start_time_standing = time.time()
        self.end_time_standing = None

    def Check_If_Standing(self):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        basePosition = basePositionAndOrientation[0]
        zPosition_of_head = basePosition[2]
        if zPosition_of_head < (c.FOOT_HEIGHT + c.SHIN_HEIGHT + c.THIGH_HEIGHT + c.TORSO_HEIGHT + c.NECK_HEIGHT + c.HEAD_HEIGHT) / 2:
            self.end_time_standing = time.time()

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
        self.Check_If_Standing()


    def Get_Fitness(self):

        self.stateOfLinkZero  = p.getLinkState(self.robotId,0)

        positionOfLinkZero    = self.stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        zCoordinateOfLinkZero = positionOfLinkZero[2]

        # Determine the amount of time robot was standing upright
        if self.end_time_standing is None:
            self.end_time_standing = time.time()

        time_standing_upright = self.end_time_standing - self.start_time_standing

        with open(f'fitness{self.solutionID}.txt', 'w') as f:
            f.write(str(xCoordinateOfLinkZero * zCoordinateOfLinkZero * time_standing_upright))




