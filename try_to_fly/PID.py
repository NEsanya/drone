import json
import time

calculate_cos_clock_delay = 0.1 # в секундах
dt = 0.1 # в секундах
# hor_kp, hor_ki, hor_kd = 0.3, 0.5, 0.08
z_kp, z_ki, z_kd = 20.0, 5.0, 3.0
hor_kp, hor_ki, hor_kd = 0.4, 0.0, 0.03

calculate_cos_clock = time.time()
pid_clock = time.time()
prev_cos = 0
prev_direction = 0
yaw_right, yaw_left = 0, 0
prev_pos = [0, 0, 0]
motorSpeed = [0 for _ in range(8)]

err_x, err_y = 0, 0
integral_x, prevErr_x = 0, 0
integral_y, prevErr_y = 0, 0

err_z = 0
integral_z, prevErr_z = 0, 0

def constrain(x, a, b):
    if x < a:
        return a
    if x > b:
        return b
    return x

def computePID_X(input, setpoint, kp, ki, kd, dt, minOut, maxOut):
    global err_x, integral_x, prevErr_x
    err_x = setpoint - input
    integral_x = constrain(integral_x + err_x * dt * ki, minOut, maxOut)
    D = (err_x - prevErr_x) / dt
    prevErr_x = err_x
    return constrain(err_x * kp + integral_x + D * kd, minOut, maxOut)

def computePID_Y(input, setpoint, kp, ki, kd, dt, minOut, maxOut):
    global err_y, integral_y, prevErr_y
    err_y = setpoint - input
    integral_y = constrain(integral_y + err_y * dt * ki, minOut, maxOut)
    D = (err_y - prevErr_y) / dt
    prevErr_y = err_y
    return constrain(err_y * kp + integral_y + D * kd, minOut, maxOut)

def computePID_Z(input, setpoint, kp, ki, kd, dt, minOut, maxOut):
    global err_z, integral_z, prevErr_z
    err_z = setpoint - input
    integral_z = constrain(integral_z + err_z * dt * ki, minOut, maxOut)
    D = (err_z - prevErr_z) / dt
    prevErr_z = err_z
    return constrain(err_z * kp + integral_z + D * kd, minOut, maxOut)

def get_clock(timer):
    """Возвращает время в секундах"""
    return time.time() - timer

def calculate_engine(data):
    global pid_clock, dt, motorSpeed

    axis_x, axis_y = data["droneAxisRotation"]["x"], data["droneAxisRotation"]["z"]
    target_axis_x, target_axis_y = data["targetAxisRotation"]["x"], data["targetAxisRotation"]["z"]
    current_z, target_z = data["droneVector"]["y"], data["targetVector"]["y"]

    if get_clock(pid_clock) > dt:
        xSpeed = computePID_X(axis_x, target_axis_x, hor_kp, hor_ki, hor_kd, dt, -15, 15)
        ySpeed = computePID_Y(axis_y, target_axis_y, hor_kp, hor_ki, hor_kd, dt, -15, 15)
        speed = computePID_Z(current_z, target_z, z_kp, z_ki, z_kd, dt, 0, 60)

        motorSpeed[0] = speed + xSpeed
        motorSpeed[1] = speed + xSpeed
        motorSpeed[2] = speed + ySpeed
        motorSpeed[3] = speed + ySpeed
        motorSpeed[4] = speed - xSpeed
        motorSpeed[5] = speed - xSpeed
        motorSpeed[6] = speed - ySpeed
        motorSpeed[7] = speed - ySpeed

        pid_clock = time.time()

    return motorSpeed


def get_data(str_data: str):
    data = json.loads(str_data)["dronesData"][0]
    return data, data["droneVector"], data["lidarInfo"]


def concat_engine(engines, data, t, drop=False):
    result = {"drones": [{
        "id": data["id"],
        "engines": {
            "fr": engines[0],
            "fl": engines[1],
            "br": engines[5],
            "bl": engines[4],
            "rf": engines[7],
            "rb": engines[6],
            "lf": engines[2],
            "lb": engines[3],
        },
        "dropExtinguisher": drop
    }], "returnTimer": 1000*t}
    return json.dumps(result)


def axis_move(target_data, t, drop=False):
    engines = calculate_engine(target_data)
    return concat_engine(engines, target_data, t, drop)


def move(type, data, angle, height, t, drop=False):
    """
    type - один из 4 вариантов: r - вправо, l - влево, f - вперед, b - назад
    str_data - данные о дроне
    angle - угол наклона в соответствующее направление. положительная величина
    height - высота, на которой летит дрон
    """
    target_data = {}
    target_axis = {}
    target_data["id"] = data["id"]
    target_data["droneVector"] = data["droneVector"]
    target_data["droneAxisRotation"] = data["droneAxisRotation"]
    target_data["targetVector"] = {"y": height}

    if type == "r":
        target_axis = {"x": 0, "y": 0, "z": angle}
    elif type == "l":
        target_axis = {"x": 0, "y": 0, "z": -angle}
    elif type == "f":
        target_axis = {"x": -angle, "y": 0, "z": 0}
    elif type == "b":
        target_axis = {"x": angle, "y": 0, "z": 0}

    target_data["targetAxisRotation"] = target_axis
    return axis_move(target_data, t, drop)

def equal(a, b):
    return abs(a - b) < 1
