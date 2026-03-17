# #!/usr/bin/env python3
from wroRobot import WroRobot
import time
import sys
from threading import Thread
import RPi.GPIO as GPIO
import brickpi3

class Task:
    def __init__(self, robot: WroRobot):
        self.robot = robot
        self.left_servo = 18
        self.right_servo = 17
        self.lift_motor_port = robot.BP.PORT_A
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_servo, GPIO.OUT)
        GPIO.setup(self.right_servo, GPIO.OUT)

    def lift(self, degrees=720, speed=800):
        self.robot.BP.set_motor_limits(self.lift_motor_port, 100, speed)
        self.robot.BP.set_motor_position_relative(self.lift_motor_port, degrees)

    
    def set_grabber(self, angle):
        if angle < 0:
            angle = 0
        elif angle > 60:
            angle = 60

        left_pwm=GPIO.PWM(self.left_servo, 50)
        left_pwm.start(0)
        right_pwm=GPIO.PWM(self.right_servo, 50)
        right_pwm.start(0)

        cycle = -angle / 36 + 4.6
        GPIO.output(self.left_servo, True)
        GPIO.output(self.right_servo, True)
        left_pwm.ChangeDutyCycle(cycle)
        right_pwm.ChangeDutyCycle(cycle)

        time.sleep(.25)
        GPIO.output(self.left_servo, False)
        GPIO.output(self.right_servo, False)
        left_pwm.ChangeDutyCycle(cycle)
        right_pwm.ChangeDutyCycle(cycle)

        left_pwm.stop()
        right_pwm.stop()


    def gyro_test(self):
        try: 
            while True:
                try:
                    if self.robot.button_pressed():
                        self.robot.gyro_sensor.reset()
                    print(self.robot.gyro_sensor.angle)
                except brickpi3.SensorError as error:
                    print(error)
                time.sleep(.2)
        except KeyboardInterrupt:
            pass
        self.robot.BP.reset_all()
        time.sleep(1)
        
    