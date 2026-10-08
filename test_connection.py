from dobot_api import DobotApiDashboard

ROBOT_IP = "192.168.5.1"

dashboard = DobotApiDashboard(ROBOT_IP, 29999)

print("Dashboard connected")

result1 = dashboard.ClearError()
print("ClearError:", result1)

result2 = dashboard.Continue()
print("Continue:", result2)

print("Done")