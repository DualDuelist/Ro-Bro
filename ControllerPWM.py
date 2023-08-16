import RPi.GPIO as GPIO
import sys
import time
import tty
import termios
import speech_recognition as sr


# Set GPIO mode and pins for motor control
GPIO.setmode(GPIO.BCM)

# Motor A (Left Motor)
motor_a_enable_pin = 18
motor_a_input1_pin = 23
motor_a_input2_pin = 24

# Motor B (Right Motor)
motor_b_enable_pin = 19
motor_b_input1_pin = 5
motor_b_input2_pin = 6

# PWM frequency (Hz)
pwm_frequency = 100

# Motor A and B PWM variables (declared as global)
motor_a_pwm = None
motor_b_pwm = None

# Motor Initialization
def setup_motors():
    global motor_a_pwm, motor_b_pwm  # Declare them as global
    GPIO.setup(motor_a_enable_pin, GPIO.OUT)
    GPIO.setup(motor_a_input1_pin, GPIO.OUT)
    GPIO.setup(motor_a_input2_pin, GPIO.OUT)
    
    GPIO.setup(motor_b_enable_pin, GPIO.OUT)
    GPIO.setup(motor_b_input1_pin, GPIO.OUT)
    GPIO.setup(motor_b_input2_pin, GPIO.OUT)
    
    motor_a_pwm = GPIO.PWM(motor_a_enable_pin, pwm_frequency)
    motor_b_pwm = GPIO.PWM(motor_b_enable_pin, pwm_frequency)
    
    motor_a_pwm.start(0)
    motor_b_pwm.start(0)
    
def forward(speed):
    GPIO.output(motor_a_input1_pin, GPIO.HIGH)
    GPIO.output(motor_a_input2_pin, GPIO.LOW)
    GPIO.output(motor_b_input1_pin, GPIO.HIGH)
    GPIO.output(motor_b_input2_pin, GPIO.LOW)
    
    motor_a_pwm.ChangeDutyCycle(speed)
    motor_b_pwm.ChangeDutyCycle(speed)

def backward(speed):
    GPIO.output(motor_a_input1_pin, GPIO.LOW)
    GPIO.output(motor_a_input2_pin, GPIO.HIGH)
    GPIO.output(motor_b_input1_pin, GPIO.LOW)
    GPIO.output(motor_b_input2_pin, GPIO.HIGH)
    
    motor_a_pwm.ChangeDutyCycle(speed)
    motor_b_pwm.ChangeDutyCycle(speed)

def left(speed):
    GPIO.output(motor_a_input1_pin, GPIO.LOW)
    GPIO.output(motor_a_input2_pin, GPIO.HIGH)
    GPIO.output(motor_b_input1_pin, GPIO.HIGH)
    GPIO.output(motor_b_input2_pin, GPIO.LOW)
    
    motor_a_pwm.ChangeDutyCycle(speed)
    motor_b_pwm.ChangeDutyCycle(speed)

def right(speed):
    GPIO.output(motor_a_input1_pin, GPIO.HIGH)
    GPIO.output(motor_a_input2_pin, GPIO.LOW)
    GPIO.output(motor_b_input1_pin, GPIO.LOW)
    GPIO.output(motor_b_input2_pin, GPIO.HIGH)
    
    motor_a_pwm.ChangeDutyCycle(speed)
    motor_b_pwm.ChangeDutyCycle(speed)

def stop_motors():
    GPIO.output(motor_a_input1_pin, GPIO.LOW)
    GPIO.output(motor_a_input2_pin, GPIO.LOW)
    GPIO.output(motor_b_input1_pin, GPIO.LOW)
    GPIO.output(motor_b_input2_pin, GPIO.LOW)
    
    motor_a_pwm.ChangeDutyCycle(0)
    motor_b_pwm.ChangeDutyCycle(0)

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

# Voice command recognition
def get_voice_command():
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio).lower()
            print("You said:" + command)
            return command
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand your command.")
        except sr.RequestError:
            print("Sorry, there was an error connecting to the speech recognition service.")

# Main function
if __name__ == "__main__":
    try:
        # Initialize motors
        setup_motors()

        print("Use WASD keys or voice commands to control the robot. Press 'q' to quit.")
        print("W: Move Forward    S: Move Backward")
        print("A: Turn Left       D: Turn Right")
        print("V: Enable Voice Commands")
        print("Q: Stop Motors and Quit")

        while True:
            char = getch()

            if char.lower() == 'w':
                forward(speed=100)
            elif char.lower() == 's':
                backward(speed=100)
            elif char.lower() == 'a':
                left(speed=100)
            elif char.lower() == 'd':
                right(speed=100)
            elif char.lower() == 'q':
                stop_motors()
                break
            elif char.lower() == 'v':
                command = get_voice_command()
                if "forward" in command:
                    forward(speed=50)
                    print("Moving", command)
                elif "backward" in command:
                    backward(speed=30)
                    print("Moving", command)
                elif "left" in command:
                    left(speed=40)
                    print("Moving", command)
                elif "right" in command:
                    right(speed=40)
                    print("Moving", command)
                elif "stop" in command:
                    stop_motors()
                    print("Stopping!")
                else:
                    print("Sorry, I didn't recognize that command.")
                print("Returning to Keyboard Commands!")

        # Clean up GPIO
        GPIO.cleanup()

    except KeyboardInterrupt:
        # Clean up GPIO on Ctrl+C exit
        stop_motors()
        GPIO.cleanup()
