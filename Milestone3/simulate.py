import time
import math
import pybullet_data
import pybullet as p
import pyrosim.pyrosim as pyrosim
import constants as c
import numpy as np

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

# Motor strength
motor_strength    		= 80

# Hip Motor Metrics
amplitude_Hip     		= math.pi/4
frequency_Hip     		= 1
phaseOffset_Hip   		= 5
targetAngles_Hip  		= np.linspace(0, 2*math.pi, c.ITERATIONS)

# Left foot
amplitude_LFoot     	= math.pi
frequency_LFoot     	= 2
phaseOffset_LFoot   	= 5
targetAngles_LFoot  	= np.linspace(0, 2*math.pi, c.ITERATIONS)

# Left Leg Motor Metrics
amplitude_LowerLLeg     = math.pi
frequency_LowerLLeg     = 4
phaseOffset_LowerLLeg   = math.pi/4
targetAngles_LowerLLeg  = np.linspace(0, 2*math.pi, c.ITERATIONS)

amplitude_UpperLLeg     = math.pi
frequency_UpperLLeg     = 4
phaseOffset_UpperLLeg   = math.pi/4
targetAngles_UpperLLeg  = np.linspace(0, 2*math.pi, c.ITERATIONS)

# Right foot
amplitude_RFoot     	= math.pi
frequency_RFoot     	= 4
phaseOffset_RFoot   	= math.pi/4
targetAngles_RFoot  	= np.linspace(0, 2*math.pi, c.ITERATIONS)

# Right Leg Motor Metrics
amplitude_LowerRLeg     = math.pi
frequency_LowerRLeg     = 4
phaseOffset_LowerRLeg   = math.pi/4
targetAngles_LowerRLeg  = np.linspace(0, 2*math.pi, c.ITERATIONS)

amplitude_UpperRLeg     = math.pi
frequency_UpperRLeg     = 4
phaseOffset_UpperRLeg   = math.pi/4
targetAngles_UpperRLeg  = np.linspace(0, 2*math.pi, c.ITERATIONS)

# Left shoulder Motor Metrics
amplitude_LShoulder     = math.pi/4
frequency_LShoulder     = 1
phaseOffset_LShoulder   = 5
targetAngles_LShoulder  = np.linspace(0, 2*math.pi, c.ITERATIONS)

# Left arm Motor Metrics
amplitude_LowerLArm     = math.pi/4
frequency_LowerLArm     = 2
phaseOffset_LowerLArm   = math.pi/4
targetAngles_LowerLArm  = np.linspace(0, 2*math.pi, c.ITERATIONS)

amplitude_UpperLArm     = math.pi/4
frequency_UpperLArm     = 2
phaseOffset_UpperLArm   = math.pi/4
targetAngles_UpperLArm  = np.linspace(0, 2*math.pi, c.ITERATIONS)

# Right shoulder Motor Metrics
amplitude_RShoulder     = math.pi/4
frequency_RShoulder     = 1
phaseOffset_RShoulder   = 5
targetAngles_RShoulder  = np.linspace(0, 2*math.pi, c.ITERATIONS)

# Right arm Motor Metrics
amplitude_LowerRArm     = math.pi/4
frequency_LowerRArm     = 2
phaseOffset_LowerRArm   = math.pi/4
targetAngles_LowerRArm  = np.linspace(0, 2*math.pi, c.ITERATIONS)

amplitude_UpperRArm     = math.pi/4
frequency_UpperRArm     = 2
phaseOffset_UpperRArm   = math.pi/4
targetAngles_UpperRArm  = np.linspace(0, 2*math.pi, c.ITERATIONS)


for i in range(0, c.ITERATIONS):
	targetAngles_LFoot[i]  	   = amplitude_LFoot  	  * np.sin(frequency_LFoot  	* targetAngles_LFoot[i]  	 + phaseOffset_LFoot     )
	targetAngles_RFoot[i]  	   = amplitude_RFoot  	  * np.sin(frequency_RFoot  	* targetAngles_RFoot[i]  	 + phaseOffset_RFoot     )
	targetAngles_LowerLLeg[i]  = amplitude_LowerLLeg  * np.sin(frequency_LowerLLeg  * targetAngles_LowerLLeg[i]  + phaseOffset_LowerLLeg )
	targetAngles_UpperLLeg[i]  = amplitude_UpperLLeg  * np.sin(frequency_UpperLLeg  * targetAngles_UpperLLeg[i]  + phaseOffset_UpperLLeg )
	targetAngles_LowerRLeg[i]  = amplitude_LowerRLeg  * np.sin(frequency_LowerRLeg  * targetAngles_LowerRLeg[i]  + phaseOffset_LowerRLeg )
	targetAngles_UpperRLeg[i]  = amplitude_UpperRLeg  * np.sin(frequency_UpperRLeg  * targetAngles_UpperRLeg[i]  + phaseOffset_UpperRLeg )

	if c.ROTATING_HIP:
		targetAngles_Hip[i]  	   = amplitude_Hip  	  * np.sin(frequency_Hip        * targetAngles_Hip[i]        + phaseOffset_Hip       )	

	if c.ARMS:
		targetAngles_LShoulder[i]  = amplitude_LShoulder  * np.sin(frequency_LShoulder  * targetAngles_LShoulder[i]  + phaseOffset_LShoulder )
		targetAngles_RShoulder[i]  = amplitude_RShoulder  * np.sin(frequency_RShoulder  * targetAngles_RShoulder[i]  + phaseOffset_RShoulder )

		targetAngles_UpperLArm[i]  = amplitude_UpperLArm  * np.sin(frequency_UpperLArm  * targetAngles_UpperLArm[i]  + phaseOffset_UpperLArm )
		targetAngles_UpperRArm[i]  = amplitude_UpperRArm  * np.sin(frequency_UpperRArm  * targetAngles_UpperRArm[i]  + phaseOffset_UpperRArm )

		targetAngles_LowerLArm[i]  = amplitude_LowerLArm  * np.sin(frequency_LowerLArm  * targetAngles_LowerLArm[i]  + phaseOffset_LowerLArm )
		targetAngles_LowerRArm[i]  = amplitude_LowerRArm  * np.sin(frequency_LowerRArm  * targetAngles_LowerRArm[i]  + phaseOffset_LowerRArm )


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
for i in range(0,c.ITERATIONS):

	p.stepSimulation()
	
	time.sleep(1/60)

	LFootSensorValues[i]		= pyrosim.Get_Touch_Sensor_Value_For_Link("LFoot") 
	RFootSensorValues[i]		= pyrosim.Get_Touch_Sensor_Value_For_Link("RFoot")
	LowerLlegSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("LowerLleg")
	LowerRlegSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("LowerRleg")
	UpperLlegSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("UpperLleg")
	UpperRlegSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("UpperRleg")

	# Left leg
	pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b"UpperLleg_LowerLleg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetAngles_LowerLLeg[i],
        maxForce=motor_strength)
	pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b"Hip_UpperLleg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetAngles_UpperLLeg[i],
        maxForce=motor_strength)

	# Right leg
	pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b"UpperRleg_LowerRleg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetAngles_LowerRLeg[i],
        maxForce=motor_strength)
	pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b"Hip_UpperRleg",
        controlMode=p.POSITION_CONTROL,
        targetPosition=targetAngles_UpperRLeg[i],
        maxForce=motor_strength)

	# Rotating hip
	if c.ROTATING_HIP:
		pyrosim.Set_Motor_For_Joint(
	        bodyIndex=robotId,
	        jointName=b"Torso_Hip",
	        controlMode=p.POSITION_CONTROL,
	        targetPosition=targetAngles_Hip[i],
	        maxForce=motor_strength)		

	# Arms
	if c.ARMS:
		LowerLarmSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("LLowerArm")
		LowerRarmSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("RLowerArm")
		UpperLarmSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("LUpperArm")
		UpperRarmSensorValues[i]	= pyrosim.Get_Touch_Sensor_Value_For_Link("RUpperArm")

		# Left shoulder
		pyrosim.Set_Motor_For_Joint(
	        bodyIndex=robotId,
	        jointName=b"Torso_Lshoulder",
	        controlMode=p.POSITION_CONTROL,
	        targetPosition=targetAngles_LShoulder[i],
	        maxForce=motor_strength)
		# Left upper arm
		pyrosim.Set_Motor_For_Joint(
	        bodyIndex=robotId,
	        jointName=b"Lshoulder_LUpperArm",
	        controlMode=p.POSITION_CONTROL,
	        targetPosition=targetAngles_LowerLArm[i],
	        maxForce=motor_strength)
		# Left lower arm
		pyrosim.Set_Motor_For_Joint(
	        bodyIndex=robotId,
	        jointName=b"LUpperArm_LLowerArm",
	        controlMode=p.POSITION_CONTROL,
	        targetPosition=targetAngles_UpperLArm[i],
	        maxForce=motor_strength)

		# Right shoulder
		pyrosim.Set_Motor_For_Joint(
	        bodyIndex=robotId,
	        jointName=b"Torso_Rshoulder",
	        controlMode=p.POSITION_CONTROL,
	        targetPosition=targetAngles_RShoulder[i],
	        maxForce=motor_strength)
		# Right upper arm
		pyrosim.Set_Motor_For_Joint(
	        bodyIndex=robotId,
	        jointName=b"Rshoulder_RUpperArm",
	        controlMode=p.POSITION_CONTROL,
	        targetPosition=targetAngles_LowerRArm[i],
	        maxForce=motor_strength)
		# Right lower arm
		pyrosim.Set_Motor_For_Joint(
	        bodyIndex=robotId,
	        jointName=b"RUpperArm_RLowerArm",
	        controlMode=p.POSITION_CONTROL,
	        targetPosition=targetAngles_UpperRArm[i],
	        maxForce=motor_strength)


	print(f"\n\nLeft foot sensor value: {LFootSensorValues[i]}")
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

	print(f"\nLower left leg motor value: {targetAngles_LowerLLeg[i]}")
	print(f"Upper left leg motor value: {targetAngles_UpperLLeg[i]}")
	print(f"Lower right leg motor value: {targetAngles_LowerRLeg[i]}")
	print(f"Upper right leg motor value: {targetAngles_UpperRLeg[i]}")
	
	if c.ROTATING_HIP:
		print(f"Rotating hip motor value: {targetAngles_Hip[i]}")
	if c.ARMS:
		print(f"\nLower left arm motor value: {targetAngles_LowerLArm[i]}")
		print(f"Upper left arm motor value: {targetAngles_UpperLArm[i]}")
		print(f"Left shoulder motor value: {targetAngles_LShoulder[i]}")
		print(f"Lower right arm motor value: {targetAngles_LowerRArm[i]}")
		print(f"Upper right arm motor value: {targetAngles_UpperRArm[i]}")
		print(f"Right shoulder motor value: {targetAngles_RShoulder[i]}")

	print(i)

p.disconnect()
