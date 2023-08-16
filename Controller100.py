import RPi.GPIO as GPIO
import time
import sys
import tty
import termios

# Set GPIO mode and pins for motor control
GPIO.setmode(GPIO.BCM)

# Motor A (Left Motor)
motor_a_input1_pin = 23
motor_a_input2_pin = 24

# Motor B (Right Motor)
motor_b_input1_pin = 5
motor_b_input2_pin = 6

# Motor Initialization
def setup_motors():
    GPIO.setup(motor_a_input1_pin, GPIO.OUT)
    GPIO.setup(motor_a_input2_pin, GPIO.OUT)
    GPIO.setup(motor_b_input1_pin, GPIO.OUT)
    GPIO.setup(motor_b_input2_pin, GPIO.OUT)

def forward():
    GPIO.output(motor_a_input1_pin, GPIO.HIGH)
    GPIO.output(motor_a_input2_pin, GPIO.LOW)
    GPIO.output(motor_b_input1_pin, GPIO.HIGH)
    GPIO.output(motor_b_input2_pin, GPIO.LOW)

def backward():
    GPIO.output(motor_a_input1_pin, GPIO.LOW)
    GPIO.output(motor_a_input2_pin, GPIO.HIGH)
    GPIO.output(motor_b_input1_pin, GPIO.LOW)
    GPIO.output(motor_b_input2_pin, GPIO.HIGH)

def left():
    GPIO.output(motor_a_input1_pin, GPIO.LOW)
    GPIO.output(motor_a_input2_pin, GPIO.HIGH)
    GPIO.output(motor_b_input1_pin, GPIO.HIGH)
    GPIO.output(motor_b_input2_pin, GPIO.LOW)

def right():
    GPIO.output(motor_a_input1_pin, GPIO.HIGH)
    GPIO.output(motor_a_input2_pin, GPIO.LOW)
    GPIO.output(motor_b_input1_pin, GPIO.LOW)
    GPIO.output(motor_b_input2_pin, GPIO.HIGH)

def stop_motors():
    GPIO.output(motor_a_input1_pin, GPIO.LOW)
    GPIO.output(motor_a_input2_pin, GPIO.LOW)
    GPIO.output(motor_b_input1_pin, GPIO.LOW)
    GPIO.output(motor_b_input2_pin, GPIO.LOW)

# Get the character from terminal without pressing Enter (for WASD control)
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Main function
if __name__ == "__main__":
    try:
        # Initialize motors
        setup_motors()

        print("Use WASD keys to control the robot. Press 'q' to quit.")
        print("W: Move forward    S: Move backward")
        print("A: Turn left       D: Turn right")
        print("Q: Stop motors and quit")

        while True:
            char = getch()

            if char.lower() == 'w':
                forward()
            elif char.lower() == 's':
                backward()
            elif char.lower() == 'a':
                left()
            elif char.lower() == 'd':
                right()
            elif char.lower() == 'q':
                stop_motors()
                break

        # Clean up GPIO
        GPIO.cleanup()

    except KeyboardInterrupt:
        # Clean up GPIO on Ctrl+C exit
        stop_motors()
        GPIO.cleanup()
