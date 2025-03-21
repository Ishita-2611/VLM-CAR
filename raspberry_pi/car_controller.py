import RPi.GPIO as GPIO
import time
from utils import setup_gpio

class CarController:
    def __init__(self):
        # Setup GPIO pins for motor driver
        self.left_motor_forward, self.left_motor_backward, self.right_motor_forward, self.right_motor_backward = setup_gpio()

    def stop(self):
        print("Stopping car.")
        GPIO.output(self.left_motor_forward, GPIO.LOW)
        GPIO.output(self.left_motor_backward, GPIO.LOW)
        GPIO.output(self.right_motor_forward, GPIO.LOW)
        GPIO.output(self.right_motor_backward, GPIO.LOW)

    def move_forward(self):
        print("Moving forward.")
        GPIO.output(self.left_motor_forward, GPIO.HIGH)
        GPIO.output(self.left_motor_backward, GPIO.LOW)
        GPIO.output(self.right_motor_forward, GPIO.HIGH)
        GPIO.output(self.right_motor_backward, GPIO.LOW)

    def turn_left(self):
        print("Turning left.")
        GPIO.output(self.left_motor_forward, GPIO.LOW)
        GPIO.output(self.left_motor_backward, GPIO.LOW)
        GPIO.output(self.right_motor_forward, GPIO.HIGH)
        GPIO.output(self.right_motor_backward, GPIO.LOW)

    def turn_right(self):
        print("Turning right.")
        GPIO.output(self.left_motor_forward, GPIO.HIGH)
        GPIO.output(self.left_motor_backward, GPIO.LOW)
        GPIO.output(self.right_motor_forward, GPIO.LOW)
        GPIO.output(self.right_motor_backward, GPIO.LOW)

    def execute(self, command):
        if command == "forward" or command == "f":
            self.move_forward()
        elif command == "left":
            self.turn_left()
        elif command == "right":
            self.turn_right()
        elif command == "stop":
            self.stop()
        else:
            print(f"Unknown command: {command}")
            self.stop()
