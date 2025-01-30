import pyrosim.pyrosim as pyrosim
import constants as c

def Create_World():

    pyrosim.Start_SDF("world.sdf")

    length = 1
    width  = 1
    height = 1

    x = 10
    y = 10
    z = 0.5

    pyrosim.Send_Cube(name=f"Box", pos=[x,y,z] , size=[length,width,height])

    pyrosim.End()

def Create_Body():

    pyrosim.Start_URDF("body.urdf")

    

    # Head
    head_position   =  c.FOOT_HEIGHT + c.SHIN_HEIGHT + c.THIGH_HEIGHT + c.TORSO_HEIGHT + c.NECK_HEIGHT + c.HEAD_HEIGHT
    
    pyrosim.Send_Cube(name="Head",  pos=[0, 0, head_position], size=[1, 1, c.HEAD_HEIGHT])
    
    # Neck
    pyrosim.Send_Joint(name="Head_Neck", parent="Head", child="Neck", type="revolute",\
                       position=[0, 0, head_position-(c.HEAD_HEIGHT*c.NECK_HEIGHT)], jointAxis="0 0 1")
    pyrosim.Send_Cube(name="Neck",  pos=[0, 0, -0.25], size=[0.65, .65, c.NECK_HEIGHT])
    
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
    pyrosim.Send_Cube(name="Hip", pos=[0, 0, -0.125],   size=[.75, 2, 0.25])
    

    """  LOWER BODY   """

    # Thighs
    pyrosim.Send_Joint(name="Hip_UpperLleg", parent="Hip", child="UpperLleg", type="revolute",
                       position=[0,-0.625,-0.25], jointAxis="0 1 0")

    pyrosim.Send_Cube(name="UpperLleg", pos=[0, 0, (-1)*(c.THIGH_HEIGHT/2)], size=[0.65, 0.65, c.THIGH_HEIGHT])

    pyrosim.Send_Joint(name="Hip_UpperRleg", parent="Hip", child="UpperRleg", type="revolute",
                       position=[0,0.625,-0.25], jointAxis="0 1 0")

    pyrosim.Send_Cube(name="UpperRleg", pos=[0, 0, (-1)*(c.THIGH_HEIGHT/2)], size=[0.65, 0.65, c.THIGH_HEIGHT])


    # ''' Shins '''
    pyrosim.Send_Joint(name="UpperLleg_LowerLleg", parent="UpperLleg", child="LowerLleg", type="revolute",
                       position=[0, 0, -1*(c.THIGH_HEIGHT)], jointAxis="0 1 0")
    
    pyrosim.Send_Cube(name="LowerLleg", pos=[0, 0, (-1)*(c.SHIN_HEIGHT/2)], size=[.5, .5, c.SHIN_HEIGHT])

    pyrosim.Send_Joint(name="UpperRleg_LowerRleg", parent="UpperRleg", child="LowerRleg", type="revolute",
                       position=[0, 0, -1*(c.THIGH_HEIGHT)], jointAxis="0 1 0")

    pyrosim.Send_Cube(name="LowerRleg", pos=[0, 0, (-1)*(c.SHIN_HEIGHT/2)], size=[.5, .5, c.SHIN_HEIGHT])


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

Create_World()
Create_Body()


