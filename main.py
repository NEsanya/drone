from logic import Drone, Position

def main():
    abobus = Drone("Abobus")
    abobus.go(Position(1, 2, 3))
    print(abobus)

if __name__ == "__main__":
    main()
