import RPi.GPIO as GPIO

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    
    # Define your GPIO pins
    left_motor_forward = 17
    left_motor_backward = 18
    right_motor_forward = 22
    right_motor_backward = 23
    
    # Setup pins
    motor_pins = [left_motor_forward, left_motor_backward, right_motor_forward, right_motor_backward]
    for pin in motor_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    return left_motor_forward, left_motor_backward, right_motor_forward, right_motor_backward
