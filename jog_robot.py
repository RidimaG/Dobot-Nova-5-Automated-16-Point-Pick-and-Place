import tkinter as tk
from dobot_sdk import DobotRobot, CoordinateType

ROBOT_IP = "192.168.5.1"

robot = DobotRobot(ROBOT_IP)
robot.Connect()

robot.robot_control.RequestControl()
robot.robot_control.Stop()
robot.robot_control.ClearError()
robot.robot_control.EnableRobot()
robot.robot_control.SpeedFactor(10)


def start_jog(axis):
    robot.motion.MoveJog(axis, CoordinateType.CARTESIAN)


def stop_jog(event=None):
    robot.motion.MoveJog()


def get_pose():
    pose = robot.robot_control.GetPose()
    print("\nCURRENT POSE:")
    print(pose)
    return pose


def save_point(name):
    pose = get_pose()

    with open("points.txt", "a") as f:
        f.write(f"{name}: {pose}\n")

    status_label.config(text=f"{name} saved")


def close_program():
    robot.motion.MoveJog()
    robot.robot_control.DisableRobot()
    robot.close()
    window.destroy()


window = tk.Tk()
window.title("Nova 5 - Jog & Point Recorder")
window.geometry("500x600")

tk.Label(
    window,
    text="NOVA 5 JOG CONTROL",
    font=("Arial", 18, "bold")
).pack(pady=10)

tk.Label(
    window,
    text="Hold a button to jog. Release to stop.\nSpeed factor: 10%",
    font=("Arial", 11)
).pack(pady=5)


# -------------------------
# Jog buttons
# -------------------------

frame = tk.Frame(window)
frame.pack(pady=15)


def make_jog_button(parent, text, axis, row, column):
    button = tk.Button(
        parent,
        text=text,
        width=10,
        height=2,
        font=("Arial", 12)
    )

    button.grid(row=row, column=column, padx=5, pady=5)

    button.bind("<ButtonPress-1>", lambda event: start_jog(axis))
    button.bind("<ButtonRelease-1>", stop_jog)

    return button


make_jog_button(frame, "X +", "X+", 0, 2)
make_jog_button(frame, "X -", "X-", 0, 0)

make_jog_button(frame, "Y +", "Y+", 1, 2)
make_jog_button(frame, "Y -", "Y-", 1, 0)

make_jog_button(frame, "Z +", "Z+", 2, 2)
make_jog_button(frame, "Z -", "Z-", 2, 0)


# -------------------------
# Current position
# -------------------------

tk.Button(
    window,
    text="READ CURRENT POSE",
    width=25,
    height=2,
    command=get_pose
).pack(pady=10)


# -------------------------
# Save points
# -------------------------

save_frame = tk.Frame(window)
save_frame.pack(pady=10)

tk.Button(
    save_frame,
    text="SAVE P1",
    width=15,
    height=2,
    command=lambda: save_point("P1")
).grid(row=0, column=0, padx=5)

tk.Button(
    save_frame,
    text="SAVE P16",
    width=15,
    height=2,
    command=lambda: save_point("P16")
).grid(row=0, column=1, padx=5)

tk.Button(
    save_frame,
    text="SAVE BIN",
    width=15,
    height=2,
    command=lambda: save_point("BIN")
).grid(row=1, column=0, columnspan=2, pady=8)


status_label = tk.Label(
    window,
    text="Robot enabled - ready",
    font=("Arial", 11)
)

status_label.pack(pady=10)


tk.Button(
    window,
    text="EXIT / DISABLE ROBOT",
    width=25,
    height=2,
    command=close_program
).pack(pady=20)


window.protocol("WM_DELETE_WINDOW", close_program)

window.mainloop()