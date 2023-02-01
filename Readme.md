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
	* Arguments: the file to be transmitted, and the number of lines from the bottom of the file to be transmitted.
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
* QUERY SYSTEM LOG: lists the contents of the system log.
	* Arguments: log level (a number corresponding to the highest level of log item to be listed).
	* Returns: a list of system log items.
* SAVE SYSTEM LOG: saves the current contents of the system log to the destination file.
	* Arguments: the destination file name, log level (a number corresponding to the highest level of log item to be saved).
	* Returns: notification of success or failure.
* CLEAR SYSTEM LOG: erases the current contents of the system log.
	* Arguments: save flag (set to auto-save log contents before erasure), the destination file name, log level.
	* Returns: none.
* SET MAX LOG ENTRIES: sets the maximum number of system log entries before the system log is automatically cleared.
	* Arguments: max log entries.
	* Returns: none.
* QUERY TASKLIST: lists the contents of the system task queue.
	* Arguments: maximum priority level (a number corresponding to the highest priority category of tasks to be listed).
	* Returns: a list of tasks in the system task queue.
* SCHEDULE TASK: adds a task to the system task queue.
	* Arguments: command to be executed (any command other than SCHEDULE TASK can be selected), recurrence interval (time in seconds between recurring executions; passed as 0 for no recurrence), delay until start (time in seconds to delay the task's first execution by), all properly formatted arguments to the command being executed.
	* Returns: none.
* END TASK: terminates a specified task by deleting it from the system task queue.
	* Arguments: the task to be terminated.
	* Returns: none.
* QUERY RECORD: queries the active recording commands.
	* Arguments: none.
	* Returns: a list of active recording commands.
* RECORD: recurringly records the output of a command to a specified file destination.
	* Arguments: command to be recorded (any command beginning with QUERY may be selected), destination file name, maximum log entries, recurrence interval (time in seconds between recurring executions; passed as 0 for no recurrence), delay until start (time in seconds to delay the task's first execution by). 
	* Returns: none.
* END RECORD: terminates the specified recording command.
	* Arguments: the record to be terminated.
	* Returns: none.

### Sensor commands
* QUERY MAGNETIC FIELD DATA: obtains magnetic field information from the ADCS.
	* Arguments: none.
	* Returns: the magnetometer measurements of the magnetic field strength about each spacecraft axis (3 values).
* QUERY RATE DATA: obtains attitude rate data from the ADCS.
	* Arguments: none.
	* Returns: the gyroscope measurements of the attitude rate about each spacecraft axis (3 values).
* QUERY SUN SENSOR DATA: obtains sun sensor readings from the ADCS.
	* Arguments: none.
	* Returns: the readings from each coarse sun sensor attached to the spacecraft (n values).
* QUERY ATTITUDE: obtains synthesized spacecraft attitude information from ADCS.
	* Arguments: coordinate system (LVLH, ECI), representation (quaternion, euler angle).
	* Returns: a representation of the satellite's attitude (3 (euler angle) or 4 (quaternion) values).
* QUERY SYSTEM TEMPERATURE: obtains controller temperature in degrees Celcius.
	* Arguments: none.
	* Returns: the controller's temperature in degrees Celcius.
* CALIBRATE GYROSCOPE: initiates an ongoing attempt to calibrate the BNO055's onboard gyroscope.
	* Arguments: none.
	* Returns: none.
* CALIBRATE MAGNETOMETER: initiates an ongoing attempt to calibrate the BNO055's onboard magentometer.
	* Arguments: none.
	* Returns: none.
* CALIBRATE SENSOR SYSTEM: initiates an ongoing attempt to calibrate the BNO055 system.
	* Arguments: none.
	* Returns: none.
* DOWNLINK SENSOR DATA: sends the result of a sensor command to the Payload Interface Board for downlink.
	* Arguments: the sensor command to be downlinked (any of the sensor commands beginning with QUERY may be selected).
	* Returns: none.

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

Command                       | Index | Arguments            | Returns       | Task Precedence | Development Priority | Completion Level 
------------------------------|-------|----------------------|---------------|-----------------|----------------------|-------------------
SYSTEM RESET                  | 001   | none                 | none          | 1               | 1                    | 0
IMU RESET                     | 002   | none                 | none          | 1               | 3                    | 1
IMU SUSPEND                   | 003   | none                 | none          | 2               | 1                    | 1
IMU UN-SUSPEND                | 004   | none                 | none          | 2               | 1                    | 1
QUERY SOH                     | 005   | 1 int                | 1 int         | 2               | 1                    | 0
ENTER SH MODE                 | 006   | 1 float              | 1 int         | 1               | 1                    | 0
EXIT SH MODE                  | 007   | 1 int                | 1 int         | 1               | 1                    | 0
QUERY MODE                    | 008   | none                 | 1 int         | 3               | 2                    | 0
QUERY FREE MEMORY             | 009   | none                 | 1 int         | 3               | 3                    | 0
QUERY FREE FILESYSTEM STORAGE | 010   | none                 | 1 int         | 3               | 4                    | 0
QUERY FILESYSTEM CONTENTS     | 011   | 1 string             | 1 string      | 3               | 4                    | 0
DELETE FILE                   | 012   | 1 string             | 1 int         | 4               | 4                    | 0
DOWNLINK FILE CONTENTS        | 013   | 1 string, 1 int      | none          | 2               | 4                    | 0
QUERY UPTIME                  | 014   | none                 | 1 int         | 3               | 5                    | 0
QUERY SYSTEM TIME             | 015   | none                 | 1 string      | 3               | 5                    | 0
SET SYSTEM TIME               | 016   | 2 int                | 1 int         | 2               | 5                    | 0
QUERY SYSTEM LOG              | 101   | 1 int                | 1 string      | 4               | 2                    | 0
SAVE SYSTEM LOG               | 102   | 1 string, 1 int      | 1 int         | 4               | 2                    | 0
CLEAR SYSTEM LOG              | 103   | 1 string, 2 int      | none          | 3               | 2                    | 0
SET MAX LOG ENTRIES           | 104   | 1 int                | none          | 4               | 2                    | 0
QUERY TASKLIST                | 105   | 1 int                | 1 string      | 3               | 2                    | 0
SCHEDULE TASK                 | 106   | 1 int, 2 float, args | none          | 2               | 2                    | 0
END TASK                      | 107   | 1 int                | none          | 2               | 2                    | 0
QUERY RECORDS                 | 108   | none                 | 1 string      | 4               | 5                    | 0
RECORD                        | 109   | 1 int, 2 float, 1 str| none          | 4               | 5                    | 0
END RECORD                    | 110   | 1 int                | none          | 4               | 5                    | 0
QUERY MAGNETIC FIELD DATA     | 201   | none                 | 3 float       | 2               | 1                    | 1
QUERY RATE DATA               | 202   | none                 | 3 float       | 2               | 1                    | 1
QUERY SUN SENSOR DATA         | 203   | none                 | n float       | 2               | 1                    | 0
QUERY ATTITUDE                | 204   | 1 int                | 3 or 4 float  | 2               | 1                    | 0
QUERY SYSTEM TEMPERATURE      | 205   | none                 | 1 float       | 2               | 1                    | 1
CALIBRATE GYROSCOPE           | 206   | none                 | 1 int         | 4               | 5                    | 1
CALIBRATE MAGNETOMETER        | 207   | none                 | 1 int         | 4               | 5                    | 1
CALIBRATE SENSOR SYSTEM       | 208   | none                 | 1 int         | 4               | 5                    | 1
DOWNLINK SENSOR DATA          | 209   | 1 int                | none          | 2               | 2                    | 0
MOMENTUM WHEEL RESET          | 301   | none                 | none          | 1               | 3                    | 0
QUERY MOMENTUM WHEEL SPEED    | 302   | none                 | 1 float       | 2               | 3                    | 0
MAGNETIC DEVICE RESET         | 303   | none                 | none          | 1               | 3                    | 0
QUERY MAGNETIC DEVICE POWER   | 304   | none                 | 3 float       | 2               | 3                    | 0
DETUMBLE                      | 401   | 1 or 2 float, 1 int  | none          | 1               | 1                    | 0
ORIENT TO NADIR               | 402   | 2 or 3 float, 1 int  | none          | 1               | 1                    | 0
TERMINATE ATTITUDE COMMAND    | 403   | none                 | 1 int         | 1               | 1                    | 0

Notes:
1. Development priority is rated 1 (highest) to 5 (lowest).
2. In the system task queue, task priority will be arbitrated by the task precedence value assorted with each assigned task (1 highest).
3. Completion level is measured on a scale from 0 to 3. 
	* 0: not started.
	* 1: in development.
	* 2: in testing.
	* 3: completed.
4. String arguments will be limited to no greater than 31 characters (plus null terminator)

## Development Roadmap
### Architecture and organization
The ADCS continuously run a "master process" which is responsible for arbitrating between other lesser processes, communicating with outside hardware, and monitoring the system for abnormalities or pre-defined conditions. 

The system will call routines implemented in the following library files:
* MASTER_PROCESS - contains the functions and bindings for running the master process.
* PLD_INTERFACE - contains the functions and bindings for communicating with the NASB payload interface device.
* CMDS_0 - contains the supporting functions and classes for executing commands with indices 0XX.
* CMDS_1 - contains the supporting functions and classes for executing commands with indices 1XX.
* CMDS_2 - contains the supporting functions and classes for executing commands with indices 2XX.
* CMDS_3 - contains the supporting functions and classes for executing commands with indices 3XX.
* CMDS_4 - contains the supporting functions and classes for executing commands with indices 4XX.
* CMDS_4_MATH - contains functions for performing high-speed computations in support of ADCS_COMMANDS_4. This library will likely be written in C or C++, then compiled to a Python library.

MASTER_PROCESS will be prototyped before any CMDS_*N* libraries can be constructed. The progress on these is as follows:

MASTER PROCESS | PLD_INTERFACE | CMDS_0 | CMDS_1 | CMDS_2 | CMDS_3 | CMDS_4 | CMDS_4_MATH 
---------------|---------------|--------|--------|--------|--------|--------|-------------
indev          | -             | -      | -      | indev  | -      | -      | -

Supporting hardware driver libraries will be labeled as the device name in all capital letters.

The following non-executable files will be standard on the system:
* STARTUP.txt - contains the default state the system will inherit when powered on.
* LOG.txt - contains the system log.
* *N_cal_profile.txt* - where *N* is an integer, 0-9. These files contain previously saved calibration profiles for the BNO055.
* *N_record.txt* - where *N* is an integer, 0-9. These files contain saved records as requested by the user or system.

### Testing
Each command will be tested using an ordered sequence:
* Debugging and simulation--the command will be validated for programming correctness and tested against using simulated inputs with known, expected outcomes.
* Hardware mockup--the command will be run connected to all relevant hardware and validated for correct behavior.
* Full scale testing--the command will be run with hardware and software fully integrated and validated for correct behavior.

### Naming schemes
* Inheritance - types declared in a class which inherits from a pre-written class will contain a \_T suffix.
* Global variables - global variables will consist of all capital letters.
	* Variables corresponding to a communication protocol will contain the suffix P\_.
	* Variables corresponding to a physical device will contain the suffix D\_.
	* Variables corresponding to a file name will contain the suffix F\_.
	* Variables corresponding to state will not contain any suffixes.
