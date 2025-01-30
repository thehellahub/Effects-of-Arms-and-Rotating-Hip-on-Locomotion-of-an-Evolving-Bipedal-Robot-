import math
import numpy as np
import pyrosim.pyrosim as pyrosim
import pybullet as p
import constants as c
import numpy as np

class MOTOR:

    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        
        print(f"\n\nFOO: {self.jointName}")

        self.motorValues    = np.linspace(0, 2*math.pi, c.ITERATIONS)
        

        if self.jointName == b"UpperLleg_LowerLleg":
            self.amplitude      = c.AMPLITUDE_LOWERLLEG
            self.frequency      = c.FREQUENCY_LOWERLLEG
            self.offset         = c.PHASEOFFSET_LOWERLLEG
            self.direction      = -1
        elif self.jointName == b'Head_Neck':
            self.amplitude      = c.AMPLITUDE_NECK
            self.frequency      = c.FREQUENCY_NECK
            self.offset         = c.PHASEOFFSET_NECK
            self.direction      = -1
        elif self.jointName == b'Neck_Torso':
            self.amplitude      = c.AMPLITUDE_NECK
            self.frequency      = c.FREQUENCY_NECK
            self.offset         = c.PHASEOFFSET_NECK
            self.direction      = -1
        elif self.jointName == b"Hip_UpperLleg":
            self.amplitude      = c.AMPLITUDE_UPPERLLEG
            self.frequency      = c.FREQUENCY_UPPERLLEG
            self.offset         = c.PHASEOFFSET_UPPERLLEG
            self.direction      = -1
        elif self.jointName == b"UpperRleg_LowerRleg":
            self.amplitude      = c.AMPLITUDE_LOWERRLEG
            self.frequency      = c.FREQUENCY_LOWERRLEG
            self.offset         = c.PHASEOFFSET_LOWERRLEG
            self.direction      = -1
        elif self.jointName == b"Hip_UpperRleg":
            self.amplitude      = c.AMPLITUDE_UPPERRLEG
            self.frequency      = c.FREQUENCY_UPPERRLEG
            self.offset         = c.PHASEOFFSET_UPPERRLEG
            self.direction      = -1
        elif self.jointName == b"LowerLleg_LFoot":
            self.amplitude      = c.AMPLITUDE_LFOOT
            self.frequency      = c.FREQUENCY_LFOOT
            self.offset         = c.PHASEOFFSET_LFOOT
            self.direction      = -1
        elif self.jointName == b"LowerRleg_RFoot":
            self.amplitude      = c.AMPLITUDE_RFOOT
            self.frequency      = c.FREQUENCY_RFOOT
            self.offset         = c.PHASEOFFSET_RFOOT
            self.direction      = -1
        if c.ROTATING_HIP:
            if self.jointName == b"Torso_Hip":
                self.amplitude      = c.AMPLITUDE_HIP
                self.frequency      = c.FREQUENCY_HIP
                self.offset         = c.PHASEOFFSET_HIP
                self.direction      = -1
        if c.ARMS:
            if self.jointName == b"Torso_Lshoulder":
                self.amplitude      = c.AMPLITUDE_LSHOULDER
                self.frequency      = c.FREQUENCY_LSHOULDER
                self.offset         = c.PHASEOFFSET_LSHOULDER
                self.direction      = -1
            elif self.jointName == b"Lshoulder_LUpperArm":
                self.amplitude      = c.AMPLITUDE_UPPERLARM
                self.frequency      = c.FREQUENCY_UPPERLARM
                self.offset         = c.PHASEOFFSET_UPPERLARM
                self.direction      = -1
            elif self.jointName == b"LUpperArm_LLowerArm":
                self.amplitude      = c.AMPLITUDE_LOWERLARM
                self.frequency      = c.FREQUENCY_LOWERLARM
                self.offset         = c.PHASEOFFSET_LOWERLARM
                self.direction      = -1
            elif self.jointName == b"Torso_Rshoulder":
                self.amplitude      = c.AMPLITUDE_RSHOULDER
                self.frequency      = c.FREQUENCY_RSHOULDER
                self.offset         = c.PHASEOFFSET_RSHOULDER
                self.direction      = -1
            elif self.jointName == b"Rshoulder_RUpperArm":
                self.amplitude      = c.AMPLITUDE_UPPERRARM
                self.frequency      = c.FREQUENCY_UPPERRARM
                self.offset         = c.PHASEOFFSET_UPPERRARM
                self.direction      = -1
            elif self.jointName == b"RUpperArm_RLowerArm":
                self.amplitude      = c.AMPLITUDE_LOWERRARM
                self.frequency      = c.FREQUENCY_LOWERRARM
                self.offset         = c.PHASEOFFSET_LOWERRARM
                self.direction      = -1
                print("FOUND YOU")
        
        

    def Set_Value(self, index, robotId):

        self.motorValues[index] = self.amplitude            *  \
                                  np.sin(self.frequency     *  \
                                    self.motorValues[index] +  \
                                    self.offset
                                  )

        pyrosim.Set_Motor_For_Joint(
            bodyIndex       = robotId,
            jointName       = self.jointName,
            controlMode     = p.POSITION_CONTROL,
            targetPosition  = self.direction * self.motorValues[index],
            maxForce        = c.MOTOR_STRENGTH
        )

        # if index == c.ITERATIONS-1:
        #     print(self.motorValues)


    def Save_Values(self):
        np.save(c.MOTOR_STRENGTH, self.motorValues)
