from logic import Drone, Vec3

def main():
    abobus = Drone(pos = (1, 3, 7))
    print(abobus.pos.distance_to(Vec3(5, 2, 3)), abobus.pos.length())

if __name__ == "__main__":
    main()
