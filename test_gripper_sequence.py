from dobot_sdk import DobotRobot
import time

ROBOT_IP = "192.168.5.1"

with DobotRobot(ROBOT_IP) as robot:

    print("Connected")

    robot.robot_control.RequestControl()
    robot.robot_control.ClearError()
    robot.robot_control.EnableRobot(load=0.5)

    # -------------------------
    # OPEN
    # -------------------------
    print("\n--- OPEN ---")

    # DO2 OFF first
    robot.io.ToolDO(2, 0)

    # DO1 ON = open
    robot.io.ToolDO(1, 1)

    time.sleep(5)

    print("DO1:", robot.io.GetDO(1))
    print("DO2:", robot.io.GetDO(2))

    input("\nPress ENTER to CLOSE...")

    # -------------------------
    # CLOSE
    # -------------------------
    print("\n--- CLOSE ---")





    # DO1 MUST be OFF first
    robot.io.ToolDO(1, 0)

    time.sleep(0.05)

    # DO2 ON = close
    robot.io.ToolDO(2, 1)

    time.sleep(1)

    print("DO1:", robot.io.GetDO(1))
    print("DO2:", robot.io.GetDO(2))

    input("\nPress ENTER to OPEN again...")

    # -------------------------
    # OPEN AGAIN
    # -------------------------
    print("\n--- OPEN AGAIN ---")

    # DO2 OFF first
    robot.io.ToolDO(2, 0)

    time.sleep(0.1)

    # DO1 ON = open
    robot.io.ToolDO(1, 1)

    time.sleep(1)

    print("DO1:", robot.io.GetDO(1))
    print("DO2:", robot.io.GetDO(2))

    robot.robot_control.DisableRobot()

print("\nFinished.")