# Dobot-Nova-5-Automated-16-Point-Pick-and-Place
A Python-based robotic automation project for the Dobot Nova 5 implementing a 16-point pick-and-place process using a Zimmer parallel gripper.
The robot operates over a 4 × 4 grid of 16 pickup locations, approaches each part through a predefined hover position, picks the part, transfers it to a designated blue-bin location, releases it, and returns to the working area before continuing with the next part.

Robot: Dobot Nova 5
Control: Python SDK
Operating mode: TCP mode
End effector: Zimmer parallel gripper
Application: Automated pick-and-place
Pickup locations: 16
Layout: 4 × 4 grid
Overview: 
The system is designed for a repeatable and structured pick-and-place workflow:
Start
  │
  ▼
Move to board center
  │
  ▼
Wait
  │
  ▼
Open gripper
  │
  ▼
Move to hover position
  │
  ▼
Move down to pickup position
  │
  ▼
Close gripper
  │
  ▼
Return to hover position
  │
  ▼
Return to board center
  │
  ▼
Move to bin hover position
  │
  ▼
Move down to bin drop position
  │
  ▼
Release part
  │
  ▼
Return to bin hover
  │
  ▼
Return to board center
  │
  ▼
Move to next pickup point




Pick up Grid:-

P1   P2   P3   P4

P5   P6   P7   P8

P9   P10  P11  P12

P13  P14  P15  P16
The nominal distance between adjacent pickup locations is approximately 50 mm horizontally and vertically.

The diagonal distance between adjacent diagonal locations is approximately 70.7 mm for a 50 mm × 50 mm grid.

The actual robot coordinates are calibrated for the physical setup and are stored in the robot program.


Motion Sequence

For each pickup point, the robot performs the following sequence:

Move to the board-center position.
Move to the hover position above the selected part.
Pause briefly.
Move down to the pickup position.
Close the gripper.
Pause to allow the gripper to securely hold the part.
Move back to the hover position.
Pause.
Move to the center position.
Move to the bin hover position.
Pause.
Slowly move down to the bin drop position.
Open the gripper to release the part.
Pause.
Move back to the bin hover position.
Return to the board center.
Continue with the next pickup location.

The process continues until all 16 parts have been transferred.

The project uses a Zimmer parallel gripper with a finger attachment.

The gripper is controlled through the robot's digital outputs.

The configured output states are:

Gripper state	DO1	DO2
Open	ON	OFF
Closed	OFF	ON

The exact output configuration depends on the installed gripper and robot wiring.

Timing

The motion sequence includes deliberate pauses between operations.

These pauses allow time for:

Robot motion stabilization
Gripper actuation
Part gripping
Part release
Transition between process stages

The exact timing values are defined in the robot program and can be adjusted according to the hardware and application requirements.

Requirements
Hardware
Dobot Nova 5
Zimmer parallel gripper
Appropriate gripper finger attachment
Robot controller
Network connection to the robot
Software
Python 3
Dobot Nova 5 SDK/API
Appropriate robot communication configuration

The exact SDK version should match the robot controller/software environment used by the project.


Installation

Clone the repository:

git clone <repository-url>
cd Dobot-Nova5-Pick-and-Place

Install/configure the required Dobot SDK according to the SDK documentation for your robot and software environment.

Configure the robot connection and verify that the robot is reachable before running the program.

Usage

Run the pick-and-place program using Python:

python pick_and_place.py

Before operating the robot:

Verify the robot and TCP configuration.
Verify the gripper configuration.
Verify the digital output configuration.
Verify all calibrated coordinates.
Verify the pickup and bin positions.
Confirm that the robot workspace is clear.
Test the sequence under controlled conditions.


Safety

This project is intended for robotics research, development, testing, and experimental automation.

Always verify the robot's safety configuration and operating environment before running automated motion.

Particular attention should be given to:

Robot workspace clearance
TCP/tool configuration
Payload configuration
Gripper operation
Digital output configuration
Pickup coordinates
Hover coordinates
Bin coordinates
Robot speed and acceleration
Emergency-stop functionality

The software should not be considered a replacement for the robot manufacturer's safety systems.

Calibration

The pickup coordinates are specific to the physical setup.

Changing any of the following may require recalibration:

Robot position
Plate position
Plate orientation
Pickup grid
Tool attachment
Gripper fingers
TCP configuration
Bin position
Robot base/reference frame

The supplied coordinates should therefore be treated as calibrated experiment parameters, not universal Nova 5 coordinates.

Future Improvements

Possible extensions include:

Automatic coordinate generation for different grid sizes
Configurable pickup patterns
Adjustable motion speeds
Automatic cycle counting
Experiment logging
Real-time monitoring
Simulation mode
Automatic error recovery
Collision detection and process monitoring
Integration with external sensors
Automated performance analysis
Disclaimer

This project is provided for educational, research, and experimental purposes.

Robot coordinates, motion parameters, gripper settings, and timing values are specific to the author's experimental setup. They should be verified before use on another robot or hardware configuration.

The user is responsible for ensuring safe robot operation and validating all motion parameters before running the program.
