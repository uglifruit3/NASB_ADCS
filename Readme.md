# Naval Academy Standard Bus Attitude and Dynamics Control System (NASB-ADCS)
This is the Github page for the AY23 NASB-ADCS.

## About
---------------
This software is desinged for use on an ADCS implemented using Adafruit CircuitPython-compatible boards. It will support the Naval Academy Standard Bus design as a payload element capable of providing attitude determination and control solutions.

## Installation
---------------
On a GNU/Linux system, connect a compatible Adafruit board via USB and mount it to `/mnt`. After ensuring that the board version is concurrent with that specified in the repository, as root run `# make lib` to install the relevant libraries and executables onto the board. Note that this will erase existing libraries on the board.

## Command List
---------------
Below is a complete list of valid commands that can be issued to the ADCS.

### System commands
* SYSTEM RESET: resets the controller. 
	* Arguments: none.
	* Returns: none.
* IMU RESET: resets the BNO-055 Absolute Orientation Sensor.
	* Arguments: none.
	* Returns: none.
* QUERY SYSTEM OPERATIONAL HEALTH (SOH): checks all power levels and hardware states for normal operation.
	* Arguments: safe mode entry/exit flag (set to true if the system should automatically enter/exit safe hold mode depending on health check results).
	* Returns: notifies sender of health check result and if the system mode has been changed. 
* ENTER SAFE HOLD (SH) MODE: places the system in safe hold mode for minimized power/data usage.
	* Arguments: mode change delay (a time delay in seconds for entering safe hold mode, used for scheduling mode change in advance. Pass as 0 for no delay).
	* Returns: notification of successful mode transition.
* EXIT SAFE HOLD MODE: attempts to transition the system out of safe hold mode; dependent on SOH check outcome.
	* Arguments: force flag (set to true to force transition out of SH mode regardless of SOH check outcome).
	* Returns: notification of mode transition attempt result.
* QUERY MODE: queries the system mode.
	* Arguments: none.
	* Returns: the system mode.
* QUERY FREE MEMORY: checks the amount of free memory on system.
	* Arguments: none.
	* Returns: bytes of free memory.
* QUERY FREE FILESYSTEM STORAGE: checks the amount of free storage available on the controller's filesystem.
	* Arguments: none.
	* Returns: bytes of free filesystem storage.
* QUERY FILESYSTEM CONTENTS: lists the contents of the controller's filesystem.
	* Arguments: file type (the type of file(s) to be listed).
	* Returns: a list of the specified files on the controller's filesystem.
* DELETE FILE: removes the specified file from the filesystem.
	* Arguments: the file to be removed.
	* Returns: whether file was successfully removed.
* DOWNLINK FILE CONTENTS: sends the contents of the specified file to the Payload Interface Board for downlink.
	* Arguments: the file to be transmitted.
	* Returns: none.
* QUERY UPTIME: queries the system uptime.
	* Arguments: none.
	* Returns: the system uptime in seconds.
* QUERY SYSTEM TIME: queries the system's GMT time.
	* Arguments: none.
	* Returns: the system's GMT time.
* SET SYSTEM TIME: sets the system GMT time.
	* Arguments: year, month, day, hour, minute, second.
	* Returns: notification of success or failure.

### Tasking and logging commands
* QUERY TASKLIST: lists the contents of the system task queue.
	* Arguments: maximum priority level (a number corresponding to the highest priority category of tasks to be listed).
	* Returns: a list of tasks in the system task queue.
* SCHEDULE TASK: adds a task to the system task queue.
	* Arguments: command to be executed (any command other than SCHEDULE TASK can be selected), recurrence interval (time in seconds between recurring executions; passed as 0 for no recurrence), delay until start (time in seconds to delay the task's first execution by).
	* Returns: none.
* END TASK: terminates a specified task by deleting it from the system task queue.
	* Arguments: the task to be terminated.
	* Returns: none.
* QUERY LOGS: queries the active logging commands.
	* Arguments: none.
	* Returns: a list of active log commands.
* LOG: recurringly logs the output of a command to a specified file destination.
	* Arguments: command to be logged (any command beginning with QUERY may be selected), destination file name, maximum log entries, recurrence interval (time in seconds between recurring executions; passed as 0 for no recurrence), delay until start (time in seconds to delay the task's first execution by). 
	* Returns: none.
* END LOG: terminates the specified log.
	* Arguments: the log to be terminated.
	* Returns: none.

### Sensor commands
* QUERY MAGNETIC FIELD DATA: obtains magnetic field information from the ADCS.
	* Arguments: none.
	* Returns: the magnetometer measurements of the magnetic field strength about each spacecraft axis (3 values).
* QUERY SUN SENSOR DATA: obtains sun sensor readings from the ADCS.
	* Arguments: none.
	* Returns: the readings from each coarse sun sensor attached to the spacecraft (n values).
* QUERY RATE DATA: obtains attitude rate data from the ADCS.
	* Arguments: none.
	* Returns: the gyroscope measurements of the attitude rate about each spacecraft axis (3 values).
* QUERY ATTITUDE: obtains synthesized spacecraft attitude information from ADCS.
	* Arguments: coordinate system (LVLH, ECI), representation (quaternion, euler angle).
	* Returns: a representation of the satellite's attitude (3 (euler angle) or 4 (quaternion) values).
* QUERY SYSTEM TEMPERATURE: obtains controller temperature in degrees Celcius.
	* Arguments: none.
	* Returns: the controller's temperature in degrees Celcius.
* DOWNLINK SENSOR DATA: sends the result of a sensor command to the Payload Interface Board for downlink.
	* Arguments: the sensor command to be downlinked (any of the sensor commands beginning with QUERY may be selected).

### Actuator commands
* MOMENTUM WHEEL RESET: resets the CubeADCS momentum wheel and brings the wheel to spin-up RPM.
	* Arguments: none.
	* Returns: none.
* QUERY MOMENTUM WHEEL SPEED: queries the CubeADCS momentum wheel's rotational speed.
	* Arguments: none.
	* Returns: the momentum wheel's rotational speed in RPMs.
* MAGNETIC DEVICE RESET: resets the magnetic rods/coil to a low power state.
	* Arguments: none.
	* Returns: none.
* QUERY MAGNETIC DEVICE POWER: queries the power level of each magnetorquer/coil onboard.
	* Arguments: none.
	* Returns: the power level of each magnetorquer/coil in mW.

### Attitude control commands
* DETUMBLE: detumbles the satellite. Executes the ADCS detumbling routine, placing the system in detumble mode.
	* Arguments: maximum magnetic device power (mW per coil/rod), exit condition (none (default), upon stabilization, upon reaching time constraint), time constraint (minutes) (used if time constraint selected as an exit condition). 
	* Returns: none.
* ORIENT TO NADIR: orients the satellite to nadir. Executes the ADCS nadir pointing routine, placing the system in nadir pointing mode.
	* Arguments: maximum magnetic device power (mW per coil/rod), maximum momentum wheel power (mW), exit condition (none (default), upon stabilization, upon reaching time constraint), time constraint (minutes) (used if time constraint selected as an exit condition). 
	* Returns: none.
* TERMINATE ATTITUDE COMMAND: forces the system to terminate an attitude control command if it is currently being executed.
	* Arguments: none.
	* Returns: notification of whether or not a command was terminated.

Note that typically, commands can be issued concurrently. For example, one can command the system to detumble (using the DETUMBLE command) and send attitude data (using SEND ATTITUDE) at the same time, and the system will schedule both tasks to be executed. However, attitude control commands are mutually exclusive. If the system is currently in an attitude control mode and an attitude control command is issued, it will depart from its current mode to execute the new command.

## Table of Command Priorities and Statuses

Command                       | Index | Task Precedence | Development Priority | Completion Level 
------------------------------|-------|-----------------|----------------------|------------------
SYSTEM RESET                  | 001   | 1               | 1                    | 0
IMU RESET                     | 002   | 1               | 1                    | 0
QUERY SOH                     | 003   | 2               | 1                    | 0
ENTER SH MODE                 | 004   | 1               | 1                    | 0
EXIT SH MODE                  | 005   | 1               | 1                    | 0
QUERY MODE                    | 006   | 3               | 2                    | 0
QUERY FREE MEMORY             | 007   | 3               | 3                    | 0
QUERY FREE FILESYSTEM STORAGE | 008   | 3               | 4                    | 0
QUERY FILESYSTEM CONTENTS     | 009   | 3               | 4                    | 0
DELETE FILE                   | 010   | 4               | 4                    | 0
DOWNLINK FILE CONTENTS        | 011   | 2               | 4                    | 0
QUERY UPTIME                  | 012   | 3               | 5                    | 0
QUERY SYSTEM TIME             | 013   | 3               | 5                    | 0
SET SYSTEM TIME               | 014   | 2               | 5                    | 0
QUERY TASKLIST                | 101   | 3               | 2                    | 0
SCHEDULE TASK                 | 102   | 2               | 2                    | 0
END TASK                      | 103   | 2               | 2                    | 0
QUERY LOGS                    | 104   | 4               | 5                    | 0
LOG                           | 105   | 4               | 5                    | 0
END LOG                       | 106   | 4               | 5                    | 0
QUERY MAGNETIC FIELD DATA     | 201   | 2               | 1                    | 0
QUERY SUN SENSOR DATA         | 202   | 2               | 1                    | 0
QUERY RATE DATA               | 203   | 2               | 1                    | 0
QUERY ATTITUDE                | 204   | 2               | 1                    | 0
QUERY SYSTEM TEMPERATURE      | 205   | 2               | 1                    | 0
DOWNLINK SENSOR DATA          | 206   | 2               | 2                    | 0
MOMENTUM WHEEL RESET          | 301   | 1               | 3                    | 0
QUERY MOMENTUM WHEEL SPEED    | 302   | 2               | 3                    | 0
MAGNETIC DEVICE RESET         | 303   | 1               | 3                    | 0
QUERY MAGNETIC DEVICE POWER   | 304   | 2               | 3                    | 0
DETUMBLE                      | 401   | 1               | 1                    | 0
ORIENT TO NADIR               | 402   | 1               | 1                    | 0
TERMINATE ATTITUDE COMMAND    | 403   | 1               | 1                    | 0

Notes:
* In the system task queue, task priority will be arbitrated by the task precedence value assorted with each assigned task.
* Completion level is measured on a scale from 0 to 3. 
	* 0: not started.
	* 1: in development.
	* 2: in testing.
	* 3: completed.