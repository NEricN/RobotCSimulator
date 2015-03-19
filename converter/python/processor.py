import os
import sys
import re
import vrep

REG_MAPPINGS = [("#pragma\sconfig\(Motor,\s*port([\d]+)\s*,\s*([^\s,]+)\s*,[^\)]+\)", r"#define \2 \1"),
               ("#pragma\sconfig\(Sensor,\s*dgt([\d]+)\s*,\s*([^,\s]+)\s*,[^\)]+\)", r"#define \2 \1"),
               ("#pragma\sconfig\(Sensor,\s*in([\d]+)\s*,\s*([^,\s]+)\s*,[^\)]+\)", r"#define \2 \1"),
               ("port([\d\d?])", r"\1"),
               ("motor\[\s*([^\s\]]+)\]\s*=\s*([^\s;]+)\s*;", r"driveMotor(\1, \2);"),
               ("nMotorEncoder\[\s*([^\s\]]+)\]\s*=\s*([^\s;]+)\s*;", r"setEncoder(\1, \2);"),
               ("nMotorEncoder\[\s*([^\s\]]+)\]", r"getEncoder(\1)"),
               ("SensorValue\[\s*([^\s\]]+)\]", r"getSensor(\1)"),
               ("task\s+main\s*\(\s*\)", "int studentMain()")]
STRING_MAPPINGS = [("wait1MSec", "Sleep"),
                   ("wait1Msec", "Sleep"),
                   ("sleep", "Sleep")]

def checkVrep():
    print("Checking if V-REP is open...")
    vrepCheck = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
    if vrepCheck == -1:
        print("V-REP not open. Opening V-REP...")
        os.system("call ..\\..\\scripts\\launcher.bat")
    else:
        print("V-REP is already open. Continuing.")
        vrep.simxFinish(vrepCheck)

def processFile(string):
    #replace one liners
    for pair in REG_MAPPINGS:
        string = re.sub(pair[0], pair[1], string)
    for pair in STRING_MAPPINGS:
        string = string.replace(pair[0], pair[1])

    #append c code to top
    string = open("../resources/header.c", "r").read() + string + open("../resources/footer.c", "r").read()
    return string

def processAndRun(fileName):
    try:
        source = open(fileName, 'r')
        print("Calling " + fileName + "...")
    except:
        source = open("../../studentCode/"+fileName, "r")
        print("Calling " + fileName + " from local directory...")
    target = open('tmp/temp.c', 'w')

    sourceSource = source.read()

    target.write(processFile(sourceSource))

    target.close()

    checkVrep()

    pythonPath = sys.executable.replace("\python.exe", "")

    #TODO: allow users to use libraries and headers of their own
    os.system("gcc tmp/temp.c -I"+pythonPath+"/include -L"+pythonPath+"/libs -lpython27" +" -o tmp/temp.exe -m32")

    if(os.path.exists("tmp\\temp.exe")):
        os.system("tmp\\temp.exe")
        os.remove("tmp\\temp.exe")
    else:
        print("Program could not be compiled. You may have used an unsupported API call, or your program doesn't normally compile.")

if __name__ == "__main__":
    processAndRun(sys.argv[1] if len(sys.argv) > 1 else 'main.c')