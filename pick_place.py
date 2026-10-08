import re
import time
from typing import Sequence

from dobot_sdk import CoordinateType, DobotRobot


ROBOT_IP = "192.168.6.3"

GRID_SIZE = 4
MOVE_SPEED = 20
PICK_DOWN_SPEED = 20
BIN_DOWN_SPEED = 15
HOVER_OFFSET = 50.0

START_END_WAIT = 2.0
PICK_HOVER_WAIT = 0.2
GRIP_WAIT = 0.2
AFTER_PICK_HOVER_WAIT = 0.3
MIDDLE_WAIT = 0.4
BIN_HOVER_WAIT = 0.4
DROP_WAIT = 0.3
AFTER_BIN_HOVER_WAIT = 0.3

# The supplied pick points differ slightly in Z; use P1's height for all 16.
P1_X = 454.8277
P1_Y = -341.9963
PICK_Z = 142.7265
P16_X = 303.6355
P16_Y = -483.5364

RX = 179.1656
RY = 2.1845
RZ = 152.8763

X_STEP = (P16_X - P1_X) / (GRID_SIZE - 1)
Y_STEP = (P16_Y - P1_Y) / (GRID_SIZE - 1)

MIDDLE = [375.8829, -406.0047, 314.3064, RX, RY, RZ]
BIN_HOVER = [551.7789, -40.8397, 314.3064, RX, RY, RZ]
BIN_DROP = [556.3259, -42.4800, 248.2365, RX, RY, RZ]

# Per the existing working gripper test: ToolDO(1) opens and ToolDO(2) closes.
OPEN_DO = 1
CLOSE_DO = 2


Pose = list[float]


def wait_for_queued_command(
    robot: DobotRobot,
    response: str,
    timeout: float = 120.0,
) -> None:
    """Wait until a queued robot command has completed or time out."""
    match = re.match(r"\s*(-?\d+),\s*\{(\d+)\}", response)
    if match is None:
        raise RuntimeError(f"Unexpected robot response: {response}")

    error_id = int(match.group(1))
    command_id = int(match.group(2))
    if error_id != 0:
        raise RuntimeError(f"Robot rejected command: {response}")

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        status = robot.GetStatus()
        if (
            status is not None
            and status.current_command_id >= command_id
            and not status.is_moving()
        ):
            return
        time.sleep(0.01)

    raise TimeoutError(f"Timed out waiting for robot command {command_id}")


def move_j(robot: DobotRobot, pose: Sequence[float]) -> None:
    """Queue a Cartesian joint-interpolated move and wait for completion."""
    response = robot.motion.MovJ(
        pose,
        CoordinateType.CARTESIAN,
        v=MOVE_SPEED,
    )
    wait_for_queued_command(robot, response)


def move_l(robot: DobotRobot, pose: Sequence[float], speed: int) -> None:
    """Queue a Cartesian linear move at the requested TCP speed."""
    response = robot.motion.MovL(
        pose,
        CoordinateType.CARTESIAN,
        speed=speed,
    )
    wait_for_queued_command(robot, response)


def tool_do(robot: DobotRobot, index: int, state: int) -> None:
    """Set a tool output and wait for its queued state change."""
    response = robot.io.ToolDO(index, state)
    wait_for_queued_command(robot, response)


def gripper_open(robot: DobotRobot, wait: float = GRIP_WAIT) -> None:
    """Open the gripper using the verified output order."""
    tool_do(robot, CLOSE_DO, 0)
    time.sleep(0.1)
    tool_do(robot, OPEN_DO, 1)
    time.sleep(wait)


def gripper_close(robot: DobotRobot) -> None:
    """Close the gripper using the verified output order."""
    tool_do(robot, OPEN_DO, 0)
    time.sleep(0.05)
    tool_do(robot, CLOSE_DO, 1)
    time.sleep(GRIP_WAIT)


def get_pick_point(row: int, column: int) -> Pose:
    """Calculate a pick pose by interpolating between P1 and P16."""
    return [
        P1_X + column * X_STEP,
        P1_Y + row * Y_STEP,
        PICK_Z,
        RX,
        RY,
        RZ,
    ]


def get_hover_point(row: int, column: int) -> Pose:
    """Return the matching pick pose raised by the hover offset."""
    point = get_pick_point(row, column)
    point[2] += HOVER_OFFSET
    return point


def pick_and_place(robot: DobotRobot, row: int, column: int) -> None:
    """Pick one grid position and place its part in the bin."""
    pick_point = get_pick_point(row, column)
    hover_point = get_hover_point(row, column)

    print(f"Picking point {row * GRID_SIZE + column + 1}")

    move_j(robot, hover_point)
    time.sleep(PICK_HOVER_WAIT)

    move_l(robot, pick_point, PICK_DOWN_SPEED)
    gripper_close(robot)

    move_l(robot, hover_point, PICK_DOWN_SPEED)
    time.sleep(AFTER_PICK_HOVER_WAIT)

    move_j(robot, MIDDLE)
    time.sleep(MIDDLE_WAIT)

    move_j(robot, BIN_HOVER)
    time.sleep(BIN_HOVER_WAIT)

    move_l(robot, BIN_DROP, BIN_DOWN_SPEED)
    gripper_open(robot, wait=DROP_WAIT)

    move_l(robot, BIN_HOVER, BIN_DOWN_SPEED)
    time.sleep(AFTER_BIN_HOVER_WAIT)

    move_j(robot, MIDDLE)
    time.sleep(MIDDLE_WAIT)


def main() -> None:
    """Connect to the robot and process all 16 board positions."""
    with DobotRobot(ROBOT_IP) as robot:
        print("Connected")

        robot.robot_control.RequestControl()
        robot.robot_control.ClearError()
        robot.robot_control.EnableRobot(load=0.5)
        time.sleep(1.0)
        robot.StartFeedbackMonitor()

        gripper_open(robot)
        move_j(robot, MIDDLE)
        time.sleep(START_END_WAIT)

        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                pick_and_place(robot, row, column)

        # The last pick-and-place cycle already returns to MIDDLE.
        time.sleep(START_END_WAIT)
        robot.robot_control.DisableRobot()
        print("Finished")


if __name__ == "__main__":
    main()