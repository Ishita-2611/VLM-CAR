from commands.command_listener import listen_for_command
from car_control.car import Car
import time

def main():
    print("Car Control System Initialized")
    car = Car()  # Initialize car object

    try:
        while True:
            command = listen_for_command()  # Get command from input/VLM
            print(f"Received command: {command}")

            if command == 'forward' or command == 'f':
                car.move_forward()
            elif command == 'left':
                car.turn_left()
            elif command == 'right':
                car.turn_right()
            elif command == 'stop':
                car.stop()
            else:
                print("Unknown command. Please try again.")
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Shutting down car control system.")
        car.cleanup()

if __name__ == "__main__":
    main()
