# General
	* Begin connecting commands and routines into bigger picture functions/tasks.
	* Update certain commands to run using asychronous multitasking.
	* Timekeeping/orbit propagation:
		* As long as the system uses orbit propagation to predict its position and velocity in space, the number of seconds since the orbit epoch specified in the TLE must be kept. This will likely not be feasible using time.monotonic() due to its accuracy tending to drift radically over relatively short spans of time. Restarting the system frequently to mitigate this is undesirable due to the complexity it would add to mode transitions. Consider integrating a real-time clock integrated circuit and using this to count seconds since the orbit epoch. 
		* If using an RTC is not desirable, consider implementing GPS. This will provide accurate time, position, and velocity figures, mitigating the need for orbit propagation for attitude determination. Attitude determination could be employed as a failsafe if a GPS signal can not be found or if onboard GPS equipment malfunctions.

# By library
## BNO055.py
	* No outstanding action items.
## CMD_INDEX.py
	* No outstanding action items.
## CMD_INDEX.py
	* No outstanding action items.
## CMDS_0.py
	* Implement remaining commands.
	* Consider adding a command for downlinking relevant system telemetry (effectively the same as \_209_DOWNLINK_SENSOR_DATA, but for metro M4 information, reaction wheel statuses, power settings, system configurations, etc).
## CMDS_1.py
	* Develop robust logging system.
	* Implement remaining commands.
## CMDS_2.py
	* \_204_QUERY_ATTITUDE: figure out if this is feasible/necessary. Accelerometer measurement accuracy cannot be expected in 0g. Currently needed for certain attitude determination algorithms.
	* Calibration commands (206,207,208): figure out if these are needed. If so, need an automated routine that can also save/load calibration profiles for the IMU. 
	* \_209_DOWNLINK_SENSOR_DATA: this must be done only after an ICD has been developed for the payload interface board so that data can be passed according to an agreed-upon protocol. It should be able to send any information obtainable from the query commands in CMDS_2.
## CMDS_3.py
	* Implement remaining commands.
## CMDS_4.py
	* Implement remaining commands.
	* bdot_controller: update magnetorquer values to reflect real-world measurements. These are currently all set to nominal values. The filter cutoff frequency, gain, etc will likely have to be tweaked as well. 
	* Develop an interface to ORBIT_DYNAMICS 
## CONFIG.py
	* No outstanding action items. Add global variables/configuration constants as required.
## CUBEWHEEL.py
	* Continue to verify code correctness and robustness. Add further commands as necessary.
## HBRIDGE.py
	* No outstanding action items.
## MASTER_PROCESS.py
	* Once all other commands/functions are verified correct, begin combining them and implementing high-level mode transition and communications functions here. 
## ORBIT_DYNAMICS.py
	* No outstanding action items.
## SUNSENSOR.py
	* No outstanding action items.
