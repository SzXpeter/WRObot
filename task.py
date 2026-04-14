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
        self.left_servo = 23
        self.right_servo = 22
        self.lift_motor_port = robot.PORT_A
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_servo, GPIO.OUT)
        GPIO.setup(self.right_servo, GPIO.OUT)
        self.left_pwm=GPIO.PWM(self.left_servo, 50)
        self.right_pwm=GPIO.PWM(self.right_servo, 50)
        self.left_pwm.start(0)     
        self.right_pwm.start(0)  
        self.robot.reset_motor_encoder(self.lift_motor_port)


    def __del__(self):
        self.left_pwm.stop()
        self.right_pwm.stop()
        GPIO.cleanup()
        self.robot.reset_all()

    def lift(self, degrees=270, speed=800):
        self.robot.set_motor_limits(self.lift_motor_port, 100, speed)
        self.robot.set_motor_position(self.lift_motor_port, degrees)
    
    def set_grabber(self, angle, hold=False):
        if angle < 15:
            angle = 15
        elif angle > 60:
            angle = 60
  
        cycle = -angle / 36 + 4.6  
        # time.sleep(0.5)
        GPIO.output(self.left_servo, True)
        GPIO.output(self.right_servo, True)
        self.left_pwm.ChangeDutyCycle(cycle)
        self.right_pwm.ChangeDutyCycle(cycle)

        time.sleep(0.3)
        if not hold:
            GPIO.output(self.left_servo, False)
            GPIO.output(self.right_servo, False)


    def gyro_test(self):
        try:
            while True:
                try:
                    if not self.robot.button_pressed():
                        break
                    print(self.robot.gyro_sensor.angle)
                except brickpi3.SensorError as error:
                    print(error)
                time.sleep(.2)
        except KeyboardInterrupt:
            pass
        
    def gyro_forw_test(self):
        self.robot.forward_cm_with_gyro(600, 75, 0)
    
    def turn_gyro_test(self):
        for i in range(1, 9):
            self.robot.turn_with_gyro(angle=90*i, speed=720)
            time.sleep(0.5)
            print(self.robot.gyro_sensor.angle, self.robot.get_sensor(self.robot.gyro_sensor.port)[1])

    def align_white_test(self):
        self.robot.align_to_white(speed=200)
        
    def gyro_one_wheel_test(self):
        for i in range(1, 3):
            self.robot.turn_one_wheel_gyro(self.robot.right_motor_port, 90*i)
            time.sleep(0.5)
            self.robot.turn_one_wheel_gyro(self.robot.right_motor_port, -90*i)
            time.sleep(0.5)
        
    def test_wall_align(self):
        self.robot.align_to_wall(time_to_go=3)

    def do_glettelo(self): # laposkenő
        self.set_grabber(0)
        self.robot.forward_cm_with_gyro(speed=500, distance=25, angle=-15)

        self.robot.forward_cm_with_gyro(speed=500, distance=40, angle=0)
        self.set_grabber(60)
        self.robot.forward_cm_with_gyro(speed=500, distance=-26, angle=0)
        self.set_grabber(0)
        self.robot.forward_cm_with_gyro(speed=500, distance=-10, angle=0)
        self.robot.forward_cm_with_gyro(speed=500, distance=-15, angle=-30)
        self.set_grabber(60)
        self.robot.turn_with_gyro(0)
        self.robot.forward_cm_with_gyro(speed=500, distance=72, angle=0)
        self.lift()
        self.robot.forward_cm_with_gyro(speed=500, distance=22, angle=-35)
        self.robot.forward_cm_with_gyro(speed=500, distance=8, angle=0)
        self.robot.turn_one_wheel_gyro(self.robot.right_motor_port, angle = 45, slow=False)
        self.robot.turn_one_wheel_gyro(self.robot.left_motor_port, angle = 0)
        self.robot.wait_for_button_press()
        self.robot.forward_cm_with_gyro(speed=500, distance=42, angle=0)

        self.robot.turn_one_wheel_gyro(self.robot.right_motor_port, 180, slow=False)
        time.sleep(0.2)
        self.robot.forward_cm_with_gyro(speed=500, distance=-15, angle=210)
        self.robot.turn_one_wheel_gyro(self.robot.left_motor_port, angle=270)
        self.robot.forward_cm_with_gyro(speed=500, distance=36, angle=270)
        self.robot.wait_for_button_press()
        self.robot.align_to_black(speed=100)
        self.robot.turn_with_gyro(angle=180, speed=500)
        self.robot.forward_cm_with_gyro(speed=500, distance=-8, angle=180)
        self.robot.wait_for_button_press()
        self.robot.align_to_black(speed=-100)
        self.robot.forward_cm_with_gyro(speed=500, distance=-10, angle=180)
        self.robot.turn_with_gyro(speed=500, angle=90)
        self.robot.forward_cm_with_gyro(speed=500, distance=15, angle=90)
        self.robot.turn_one_wheel_gyro(self.robot.right_motor_port, angle=180, speed=500)

    def test1(self):
        self.set_grabber(0)
        self.robot.forward_cm_with_gyro(600, 80, 0, is_PID=False)
        self.robot.forward_cm_with_gyro(600, -5, 0, is_PID=False)
        self.robot.wait_for_button_press()
        self.set_grabber(60)
        self.robot.wait_for_button_press()
        self.lift(degrees=200)

    def grab_test_1(self):
        self.set_grabber(15)
        self.robot.wait_for_button_press()
        self.set_grabber(60, hold=True)
        # self.robot.wait_for_button_press()
        # self.set_grabber(30)
        
        self.robot.wait_for_button_press()
        self.lift(degrees=200)
        
