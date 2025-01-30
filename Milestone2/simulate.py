import time
import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())


#p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")


p.loadSDF("world.sdf")

#left foot
#right foot
#lower left leg
#lower right leg
#upper left leg
#upper right leg
#upper left arm
#upper right arm
#lower left arm
#lower right arm
pyrosim.Prepare_To_Simulate(robotId)
LFootSensorValues 		= np.zeros(c.ITERATIONS)
RFootSensorValues 		= np.zeros(c.ITERATIONS)
LowerLlegSensorValues	= np.zeros(c.ITERATIONS)
LowerRlegSensorValues	= np.zeros(c.ITERATIONS)
UpperLlegSensorValues	= np.zeros(c.ITERATIONS)
UpperRlegSensorValues	= np.zeros(c.ITERATIONS)
LowerLarmSensorValues	= np.zeros(c.ITERATIONS)
LowerRarmSensorValues	= np.zeros(c.ITERATIONS)
UpperLarmSensorValues	= np.zeros(c.ITERATIONS)
UpperRarmSensorValues	= np.zeros(c.ITERATIONS)
NeckSensorValues		= np.zeros(c.ITERATIONS)
for i in range(0,c.ITERATIONS):

	p.stepSimulation()
	
	time.sleep(1/60)

	NeckSensorValues[i]		= pyrosim.Get_Touch_Sensor_Value_For_Link("Neck")
	LFootSensorValues[i]		= pyrosim.Get_Touch_Sensor_Value_For_Link("LFoot") 
	RFootSensorValues[i]		= pyrosim.Get_Touch_Sensor_Value_For_Link("RFoot")
	LowerLlegSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("LowerLleg")
	LowerRlegSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("LowerRleg")
	UpperLlegSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("UpperLleg")
	UpperRlegSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("UpperRleg")
	LFootSensorValues[i]		= pyrosim.Get_Touch_Sensor_Value_For_Link("LFoot")

	if c.ARMS:
		LowerLarmSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("LLowerArm")
		LowerRarmSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("RLowerArm")
		UpperLarmSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("LUpperArm")
		UpperRarmSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("RUpperArm")

	print(f"\n\nNeck sensor value: {NeckSensorValues[i]}")
	print(f"Left foot sensor value: {LFootSensorValues[i]}")
	print(f"Right foot sensor value: {RFootSensorValues[i]}")
	print(f"Lower left leg sensor value: {LowerLlegSensorValues[i]}")
	print(f"Lower right leg sensor value: {LowerRlegSensorValues[i]}")
	print(f"Upper left leg sensor value: {UpperLlegSensorValues[i]}")
	print(f"Upper right leg sensor value: {UpperRlegSensorValues[i]}")

	if c.ARMS:
		print(f"Lower left arm sensor value: {LowerLarmSensorValues[i]}")
		print(f"Lower right arm sensor value: {LowerRarmSensorValues[i]}")
		print(f"Upper left arm sensor value: {UpperLarmSensorValues[i]}")
		print(f"Upper right arm sensor value: {UpperRarmSensorValues[i]}")

	print(i)

p.disconnect()
