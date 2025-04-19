import time

from PID import move, get_data, equal
from connection.SocketConnection import SocketConnection


connection = SocketConnection()
H = 8  # высота, на которой летит дрон
T = 0.1  # время, через которое симулятор пришлет новый пакет данных
ANGLE = 3  # угол наклона дрона
drone_position = {"x": 0, "y": 0, "z": 0}
lidars = {"f": 0, "fr": 0, "r": 0, "br": 0, "b": 0, "bl": 0, "l": 0, "fl": 0, "up": 0, "d": 0}


def check_lidars(directions):
    """Проверка лидаров. True - если можно лететь в заданном направлении дальне, False - если рядом преграда"""
    if 0 < lidars[directions[0]] < 5:
        return False
    for direction in directions[1:]:
        if 0 < lidars[direction] < 2:
            return False
    return True


def get_direction1(drone_z, fire_z):
    """Направление по оси Z. f - forward - вперед, b - backward - назад
    Возвращается кортеж из 3 элементов: еще добавляются боковые направления"""
    direction = "b"
    if drone_z - fire_z > 0:
        return "f"
    return direction, direction + "r", direction + "l"


def get_direction2(drone_x, fire_x):
    """Направление по оси X. r - right - вправо, l - left - влево
    Возвращается кортеж из 3 элементов: еще добавляются боковые направления"""
    direction = "l"
    if drone_x - fire_x > 0:
        return "r"
    return direction, "f" + direction, "b" + direction


def step(direction):
    """Функция делает один шаг. Принимает, анализирует и отправляет данные на симулятор"""
    global drone_position, lidars

    data, drone_position, lidars = get_data(connection.receive_data())
    new_data = move(direction, data, ANGLE, H, T)
    connection.send_data(new_data)
    time.sleep(T)


def go(directions, fire, coord):
    """Летим по направлению пока лидары не встречают преград"""
    global drone_position, lidars

    while not equal(drone_position[coord], fire) and check_lidars(directions):
        step(directions[0])


def run_to_point(fire_x, fire_z):
    global drone_position, lidars

    directions2 = get_direction2(drone_position["x"], fire_x)
    step(directions2[0])

    while not try_run_to_point(fire_x, fire_z):
        continue


def try_run_to_point(fire_x, fire_z):
    """Функция выравнивает координату дрона с огнем по X или по Z"""
    global drone_position, lidars

    directions2 = get_direction2(drone_position["x"], fire_x)
    print("Выравниваю X...")
    go(directions2, fire_x, "x")

    if not equal(drone_position["x"], fire_x):
        directions1 = get_direction1(drone_position["z"], fire_z)
        print("С X проблемы, пытаюсь повернуть...")
        while not check_lidars(directions2):
            step(directions1[0])
        print("Поворачиваю и выравниваю X...")
        go(directions2, fire_x, "x")
        return False
    elif equal(drone_position["z"], fire_z):
        return True
    else:
        stop()

    print("Выравниваю Z...")
    directions1 = get_direction1(drone_position["z"], fire_z)
    go(directions1, fire_z, "z")

    if not equal(drone_position["z"], fire_z):
        print("С Z проблемы, пытаюсь повернуть...")
        directions2 = get_direction2(drone_position["x"], fire_x)
        while lidars[directions1[0]] > 0:
            step(directions2[0])
        print("Поворачиваю и выравниваю Z...")
        go(directions1[0], fire_z, "z")
        return False
    if not equal(drone_position["x"], fire_x):
        return False
    return True


def stop():
    """Остановка дрона на 10 итераций (примерно 1с)"""
    for i in range(10):
        data, _, _ = get_data(connection.receive_data())
        new_data = move("f", data, 0, H, T)
        connection.send_data(new_data)
        time.sleep(T)


def down():
    """Полет вниз"""
    for i in range(10):
        data, _, _ = get_data(connection.receive_data())
        new_data = move("f", data, 0, 5, T)
        connection.send_data(new_data)
        time.sleep(T)


def drop_water():
    """Сброс огнетушителя"""
    data, _, _ = get_data(connection.receive_data())
    new_data = move("f", data, 0, H, T, drop=True)
    connection.send_data(new_data)
    time.sleep(T)