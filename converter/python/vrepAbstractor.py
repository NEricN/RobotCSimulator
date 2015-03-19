import vrep
#import os

GLOBALS = {'clientID' : -1}
SENSOR_FN = {}
SENSOR_TYPE = ["DIG_SONAR", "DIG_TOUCH", "ANG_LINE", "ANG_GYRO", "ANG_ACC"]

#Robot configuration
MOTOR = {1 : 0, 2: 0} #1 is left, 2 is right
ENCODER = {4: 1, 5: 2} #translation from encoder port to motor port
SENSOR = {3: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12:0}
SENSOR_TYPE = {3: "DIG_SONAR", 6: "DIG_TOUCH", 7: "ANG_LINE", 8: "ANG_LINE", 9: "ANG_GYRO", 10: "ANG_ACC", 11: "ANG_ACC", 12: "ANG_ACC"}

#API FUNCS
def init():
    print("Connecting to simulator...")
    vrep.simxFinish(-1)
    GLOBALS['clientID'] = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
    if GLOBALS['clientID'] == -1:
        #should probably do some fail stuff
        print("Connection failed. Retrying...")
        GLOBALS['clientID'] = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
        if GLOBALS['clientID'] == -1:
            print("Connection failed. Is V-REP on?\nRunning program without simulator.")
            #os.system("..\\..\\scripts\\launcher.bat")
            #GLOBALS['clientID'] = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
            return -1
    print("Connected to simulator. Running program.\n====START OF USER OUTPUT")
    #vrep.simxPauseCommunication(GLOBALS['clientID'], 1)
    vrep.simxRemoveUI(GLOBALS['clientID'], -1, vrep.simx_opmode_oneshot_wait)
    vrep.simxStopSimulation(GLOBALS['clientID'], vrep.simx_opmode_oneshot_wait)
    #vrep.simxPauseCommunication(GLOBALS['clientID'], 0)
    MOTOR[1] = vrep.simxGetObjectHandle(GLOBALS['clientID'], "BackLeftWheel#", vrep.simx_opmode_oneshot_wait)[1]
    MOTOR[2] = vrep.simxGetObjectHandle(GLOBALS['clientID'], "BackRightWheel#", vrep.simx_opmode_oneshot_wait)[1]
    SENSOR[3] = vrep.simxGetObjectHandle(GLOBALS['clientID'], "DigitalSonarSensor#", vrep.simx_opmode_oneshot_wait)[1]
    SENSOR[6] = vrep.simxGetObjectHandle(GLOBALS['clientID'], "DigitalTouchSensor#", vrep.simx_opmode_oneshot_wait)[1]
    SENSOR[7] = vrep.simxGetObjectHandle(GLOBALS['clientID'], "AnalogLineFollower#", vrep.simx_opmode_oneshot_wait)[1]
    SENSOR[8] = vrep.simxGetObjectHandle(GLOBALS['clientID'], "AnalogLineFollower0#", vrep.simx_opmode_oneshot_wait)[1]
    SENSOR[9] = "gyroAngle"
    SENSOR[10] = "accelerometerX"
    SENSOR[11] = "accelerometerY"
    SENSOR[12] = "accelerometerZ"

    vrep.simxStartSimulation(GLOBALS['clientID'], vrep.simx_opmode_oneshot_wait)


def de_init():
    print("\n====END OF USER OUTPUT")
    if GLOBALS['clientID'] != -1:
        print("Finalizing simulation...")
        vrep.simxPauseSimulation(GLOBALS['clientID'], vrep.simx_opmode_oneshot_wait)
        vrep.simxFinish(GLOBALS['clientID'])
        print("Simulation finished.")
    else:
        print("Program finished running.")

#ROBOTC equivalent: motor[blah] = blah
def set_motor(motor, speed):
    speed = max(min(speed, 255),-255)
    speed = speed/100.0
    vrep.simxSetJointTargetVelocity(GLOBALS['clientID'], MOTOR[motor], speed, vrep.simx_opmode_oneshot_wait)

#ROBOTC equivalent: SensorValue(blah) (parenthesis, not brackets!)
def get_sensor(port):
    #TODO: return value depending on type of sensor=`
    return SENSOR_FN[SENSOR_TYPE[port]](port)
    #return vrep.simxReadVisionSensor(GLOBALS['clientID'], SENSOR[port], vrep.simx_opmode_oneshot_wait)[1] #for infrared/line following

#ROBOTC equivalent: nMotorEncoder[blah] = blargh
def set_encoder(motor, value):
    vrep.simxSetJointPosition(GLOBALS['clientID'], MOTOR[motor], value, vrep.simx_opmode_oneshot_wait)[1]

#ROBOTC equivalent: nMotorEncoder[blah] (without the equal sign)
def get_encoder(motor):
    return get_digital_encoder(motor)

#INTERNAL FUNCS
def get_digital_touch(port):
    return int(vrep.simxReadProximitySensor(0, port, vrep.simx_opmode_oneshot_wait)[1])
SENSOR_FN["DIG_TOUCH"] = get_digital_touch

def get_digital_sonar(port):
    readVal = vrep.simxReadProximitySensor(GLOBALS['clientID'], SENSOR[port], vrep.simx_opmode_oneshot_wait)
    if not readVal[1]:
        return -1
    dist = int((reduce(lambda x,y: x+y, map(lambda x: x**2, readVal[2]))**0.5)*100)
    return dist if dist < 256 else -1
SENSOR_FN["DIG_SONAR"] = get_digital_sonar

def get_digital_encoder(port):
    return int((180/math.pi)*vrep.simxGetJointPosition(GLOBALS['clientID'], MOTOR[motor], vrep.simx_opmode_oneshot_wait)[1])

#impossible
def get_analog_light(port):
    pass

def get_analog_potentiometer(port):
    pass

#hax
def get_analog_line_follower(port):
    return 4095*(vrep.simxReadProximitySensor(GLOBALS['clientID'], SENSOR[port], vrep.simx_opmode_oneshot_wait)[1])
SENSOR_FN["ANG_LINE"] = get_analog_line_follower

def get_analog_gyro_sensor(port):
    return int(100*(180.0/(math.pi))*vrep.simxGetFloatSignal(GLOBALS['clientID'], SENSOR[port], vrep.simx_opmode_oneshot_wait)[1])
SENSOR_FN["ANG_GYRO"] = get_analog_gyro_sensor

def get_analog_accelerometer_sensor(port):
    return int(4095*vrep.simxGetFloatSignal(GLOBALS['clientID'], SENSOR[port], vrep.simx_opmode_oneshot_wait)[1])
SENSOR_FN["ANG_ACC"] = get_analog_accelerometer_sensor

def reset_analog_gyro_sensor(port):
    vrep.simxSetFloatSignal(GLOBALS['clientID'], SENSOR[port], 0, vrep.simx_opmode_oneshot_wait)