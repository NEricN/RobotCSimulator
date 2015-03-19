====INSTRUCTIONS
To Run:
1. Run "simulator.bat"
2. Open your file (can be anywhere).
3. Go tools->build system, and select RobotC.
4. To run the code, run tols->build, or press ctrl-B.

====WARNINGS:
Do not have infinite loops. Behavior is undefined and you might have to restart V-REP.

====SUPPORTED API CALLS
motor[motor] = something
nMotorEncoder[encoder] = something
nMotorEncoder[encoder]
SensorValue(sensor)
sleep(milliseconds)
wait1MSec(milliseconds)

Using any ROBOTC api outside of these calls will result in undefined behavior.

====KNOWN ISSUES
-The robot may fail to push moveable objects
  -Mass of objects is uncalibrated - your 0.5kg robot might be trying to push a 500kg table

If the simulator lags, please also email ericnguyen@pioneers.berkeley.edu, along with your computer specs.
If you have a request, email ericnguyen@pioneers.berkeley.edu.