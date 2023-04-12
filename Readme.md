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
Below is a list of commands that will be issued to the ADCS externally via a UART connection. If a value is returned, it will be made accessible to the outside caller.

### System commands
* SYSTEM RESET: resets the controller. 
	* Arguments: none.
	* Returns: none.
* IMU RESET: resets the BNO-055 Absolute Orientation Sensor.
	* Arguments: none.
	* Returns: none.
* SET IMU POWER: sets the IMU to full power regular operation or suspended power usage.
	* Arguments: mode (true for full power, false for suspended).
	* Returns: none.
* QUERY SYSTEM OPERATIONAL HEALTH (SOH): checks all power levels and hardware states for normal operation.
	* Arguments: safe mode entry/exit flag (set to true if the system should automatically enter/exit safe hold mode depending on health check results).
	* Returns: notifies sender of health check result and if the system mode has been changed. 
* SET SAFE HOLD (SH) MODE: places the system into or out of safe hold mode.
	* Arguments: mode (true for safe hold mode, false for regular mode).
	* Returns: notification of successful mode transition.
* QUERY MODE: queries the system mode.
	* Arguments: none.
	* Returns: the system mode.
* QUERY FREE MEMORY: checks the amount of free memory on system.
	* Arguments: none.
	* Returns: bytes of free memory.
* QUERY FREE FILESYSTEM STORAGE: checks the amount of free storage available on the controller's filesystem.
	* Arguments: none.
	* Returns: bytes of free filesystem storage.
* QUERY TWO-LINE ELEMENT (TLE): queries the currently loaded TLE for orbit simulation/propagation.
	* Arguments: none.
	* Returns: a string containing the currently loaded TLE.
* SET TWO-LINE ELEMENT (TLE): overwrites the currently loaded TLE for orbit simulation/propagation.
	* Arguments: a string containing the new TLE.
	* Returns: none.
* QUERY SYSTEM TIME: queries the system's GMT time.
	* Arguments: none.
	* Returns: the system's GMT time.
* SET SYSTEM TIME: sets the system GMT time.
	* Arguments: year, month, day, hour, minute, second.
	* Returns: notification of success or failure.
* QUERY UPTIME: queries the system uptime.
	* Arguments: none.
	* Returns: the system uptime in seconds.

### Tasking and logging commands
* QUERY SYSTEM LOG: lists the contents of the system log.
	* Arguments: log level (a number corresponding to the highest level of log item to be listed).
	* Returns: a list of system log items.
* CLEAR SYSTEM LOG: erases the current contents of the system log.
	* Arguments: save flag (set to auto-save log contents before erasure), the destination file name, log level.
	* Returns: none.
* SET MAX LOG ENTRIES: sets the maximum number of system log entries before the system log is automatically cleared.
	* Arguments: max log entries.
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
* QUERY SUN VECTOR: obtains a vector to the sun in body coordinates.
	* Arguments: none.
	* Returns: 3 floats, denoting a vector to the sun in body coordinates.
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
* MOMENTUM WHEEL SPINUP: spins up the momentum wheel.
	* Arguments: none.
	* Returns: none.
* MOMENTUM WHEEL SPINDOWN: spins down the momentum wheel.
	* Arguments: none.
	* Returns: none.
* MOMENTUM WHEEL RESET: resets the CubeADCS momentum wheel.
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

## Table of Command Priorities and Statuses

Command                       | Index | Arguments            | Returns       | Task Precedence | Development Priority | Completion Level 
------------------------------|-------|----------------------|---------------|-----------------|----------------------|-------------------
SYSTEM RESET                  | 000   | none                 | none          | 1               | 1                    | 0
IMU RESET                     | 001   | none                 | none          | 1               | 1                    | 2
SET IMU POWER                 | 002   | 1 bool               | none          | 2               | 1                    | 1
QUERY SOH                     | 003   | 1 int                | 1 int         | 2               | 1                    | 0
SET SH MODE                   | 004   | 1 bool               | none          | 1               | 1                    | 0
QUERY MODE                    | 005   | none                 | 1 int         | 3               | 2                    | 0
QUERY FREE MEMORY             | 006   | none                 | 1 int         | 3               | 3                    | 1
QUERY FREE FILESYSTEM STORAGE | 007   | none                 | 1 int         | 3               | 4                    | 0
QUERY TLE                     | 008   | none                 | 1 string      | 3               | 1                    | 1
SET TLE                       | 009   | 1 string             | none          | 2               | 1                    | 1
QUERY SYSTEM TIME             | 010   | none                 | 1 string      | 3               | 1                    | 0
SET SYSTEM TIME               | 011   | 2 int                | 1 int         | 2               | 1                    | 0
QUERY UPTIME                  | 012   | none                 | 1 int         | 3               | 5                    | 0
QUERY SYSTEM LOG              | 100   | 1 int                | 1 string      | 4               | 2                    | 0
CLEAR SYSTEM LOG              | 101   | 1 string, 2 int      | none          | 3               | 2                    | 0
SET MAX LOG ENTRIES           | 102   | 1 int                | none          | 4               | 2                    | 0
QUERY MAGNETIC FIELD DATA     | 200   | none                 | 3 float       | 2               | 1                    | 2
QUERY RATE DATA               | 201   | none                 | 3 float       | 2               | 1                    | 2
QUERY SUN SENSOR DATA         | 202   | none                 | n float       | 2               | 1                    | 2
QUERY SUN VECTOR              | 203   | none                 | 3 float       | 2               | 1                    | 2
QUERY ATTITUDE                | 204   | 1 int                | 3 or 4 float  | 2               | 1                    | 0
QUERY SYSTEM TEMPERATURE      | 205   | none                 | 1 float       | 2               | 1                    | 1
CALIBRATE GYROSCOPE           | 206   | none                 | 1 int         | 4               | 5                    | 2
CALIBRATE MAGNETOMETER        | 207   | none                 | 1 int         | 4               | 5                    | 2
CALIBRATE SENSOR SYSTEM       | 208   | none                 | 1 int         | 4               | 5                    | 2
DOWNLINK SENSOR DATA          | 209   | 1 int                | none          | 2               | 2                    | 0
MOMENTUM WHEEL SPINUP         | 300   | none                 | none          | 1               | 1                    | 0
MOMENTUM WHEEL SPINDOWN       | 301   | none                 | none          | 1               | 2                    | 0
QUERY MOMENTUM WHEEL SPEED    | 302   | none                 | 1 float       | 2               | 3                    | 0
MAGNETIC DEVICE RESET         | 304   | none                 | none          | 1               | 3                    | 2
QUERY MAGNETIC DEVICE POWER   | 305   | none                 | 3 float       | 2               | 3                    | 0
DETUMBLE                      | 400   | 1 or 2 float, 1 int  | none          | 1               | 1                    | 1
ORIENT TO NADIR               | 401   | 2 or 3 float, 1 int  | none          | 1               | 1                    | 0
TERMINATE ATTITUDE COMMAND    | 402   | none                 | 1 int         | 1               | 1                    | 1

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
The ADCS continuously runs a "master process" which is responsible for arbitrating between other lesser processes, communicating with outside hardware, and monitoring the system for abnormalities or pre-defined conditions. 

High-level task management, communications, scheduling, and system configuration commands will be made available in the following libraries:
* MASTER_PROCESS - contains the functions and bindings for running the master process.
* PLD_INTERFACE - contains the functions and bindings for communicating with the NASB payload interface device.

Global variables, to include device and communications protocol objects, state variables, and filenames will be contained in the following library:
* CFG

The master process will call and manage the user-accessible commands via the following library:
* CMD_INDEX - contains a custom class for commands and fully indexes them and enables execution by that index.

The user-accessible commands to the ADCS will be implemented in the following libraries, and will be called by CMD_INDEX.
* CMDS_0 - contains the supporting functions and classes for executing commands with indices 0XX.
* CMDS_1 - contains the supporting functions and classes for executing commands with indices 1XX.
* CMDS_2 - contains the supporting functions and classes for executing commands with indices 2XX.
* CMDS_3 - contains the supporting functions and classes for executing commands with indices 3XX.
* CMDS_4 - contains the supporting functions and classes for executing commands with indices 4XX.

Device drivers will be contained in the following libraries. The user-accessible command implementation libraries will access these functions and routines.
* BNO055 - contains supporting functions and classes for interfacing the Adafruit BNO055 IMU.
* HBRIDGE - contains supporting functions and classes for interfacing the magnetic devices' h-bridge drivers.
* SUNSENSOR - contains supporting funtions and classes for interfacing the system's coarse sun sensors through analog input.
* CUBEWHEEL - contains the I2C interface, supporting functions, and classes for interfacing with the CubeSpace CubeWheel.

The following non-executable files will be standard on the system:
* STARTUP.txt - contains the default state the system will inherit when powered on.
* LOG.txt - contains the system log.
* *N_cal_profile.txt* - where *N* is an integer, 0-9. These files contain previously saved calibration profiles for the BNO055.

### Standardization 
In general, the following conventions and naming schemes apply to all libraries and software, and should be adhered to for future additions and edits.
* Library names should be fully capitalized
* User-accessible command libraries should be prefixed with CMDS\_, followed by the numerical series of commands the library implements.
* Device driver libraries should be concisely named after the device it implements.
	* Device drivers should declare a class denoting an object for the device. A global instance of this class should be initialized in CFG, and then be accessed as such in external command and process libraries.
* Non-executable files should have a .txt filetype.
* Inheritance - types declared in a class which inherits from a pre-written class will contain a \_T suffix.
* Global variables - global variables will consist of all capital letters. Global variables should be declared in the CFG library.
	* Variables corresponding to a communication protocol will contain the prefix P\_.
	* Variables corresponding to a physical device will contain the prefix D\_.
	* Variables corresponding to a file name will contain the prefix F\_.
	* Variables corresponding to state will not contain any suffixes.
* In general, library access should follow a hierarchical order. MASTER_PROCESS should call routines from the CMDS_X libraries, which in turn call routines from the device driver libraries. This need not always be the case, and should be deviated from when clarity and programmitcal straightforwardness require.

### Testing
Each command will be tested using an ordered sequence:
* Debugging and simulation--the command will be validated for programming correctness and tested against using simulated inputs with known, expected outcomes.
* Hardware mockup--the command will be run connected to all relevant hardware and validated for correct behavior.
* Full scale testing--the command will be run with hardware and software fully integrated and validated for correct behavior.

