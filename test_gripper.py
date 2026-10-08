from dobot_sdk import DobotRobot
import time

ROBOT_IP = "192.168.5.1"


def print_gripper_state(robot, label="Gripper state"):
    """Print both gripper control outputs in a consistent, useful format."""
    print(f"{label}:")
    print("  DO1:", robot.io.GetDO(1))
    print("  DO2:", robot.io.GetDO(2))


with DobotRobot(ROBOT_IP) as robot:

    print("Connected")

    # Take control of the robot
    print("\nRequesting control...")
    print(robot.robot_control.RequestControl())

    # Stop any previous queued operation
    print("\nStopping previous operation...")
    print(robot.robot_control.Stop())

    # Clear any error
    print("\nClearing errors...")
    print(robot.robot_control.ClearError())

    # Enable robot
    print("\nEnabling robot...")
    print(robot.robot_control.EnableRobot())

    time.sleep(1)

    # =========================================================
    # OPEN GRIPPER
    # DO1 ON  = OPEN
    # DO2 OFF
    # =========================================================

    print("\n==============================")
    print("        OPEN GRIPPER")
    print("==============================")

    print("DO2 OFF:")
    (robot.io.DOInstant(2, 0))

    time.sleep(0.1)

    print("DO1 ON:")
    print(robot.io.DOInstant(1, 1))

    time.sleep(1)

    print_gripper_state(robot)

    input("\nGripper should now be OPEN. Press ENTER to CLOSE...")

    # =========================================================
    # CLOSE GRIPPER
    #
    # IMPORTANT:
    # DO1 MUST be OFF first.
    # Then DO2 ON.
    # =========================================================

    print("\n==============================")
    print("        CLOSE GRIPPER")
    print("==============================")

    print("Step 1: DO1 OFF")
    robot.io.DOInstant(1, 0)
    time.sleep(0.2)

    print("Step 2: DO2 ON")
    robot.io.DOInstant(2, 1)

    time.sleep(1)

    print("DO1 state:", robot.io.GetDO(1))
    print("DO2 state:", robot.io.GetDO(2))

    input("\nGripper should now be CLOSED. Press ENTER to OPEN...")

    # =========================================================
    # OPEN AGAIN
    #
    # DO2 OFF first.
    # Then DO1 ON.
    # =========================================================

    print("\n==============================")
    print("        OPEN GRIPPER AGAIN")
    print("==============================")

    print("Step 1: DO2 OFF")
    robot.io.DOInstant(2, 0)

    time.sleep(0.2)

    print("Step 2: DO1 ON")
    robot.io.DOInstant(1, 1)

    time.sleep(1)

    print("DO1 state:", robot.io.GetDO(1))
    print("DO2 state:", robot.io.GetDO(2))

    # =========================================================
    # FINISH
    # =========================================================

    print("\nDisabling robot...")
    print(robot.robot_control.DisableRobot())

print("\nFinished.")