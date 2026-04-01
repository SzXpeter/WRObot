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

    def lift(self, degrees=0, speed=300):
        self.robot.reset_motor_encoder(self.lift_motor_port)
        self.robot.set_motor_limits(self.lift_motor_port, 100, speed)
        if degrees > 0:
            self.robot.set_motor_dps(self.lift_motor_port, speed)

            while (degrees-self.robot.get_motor_encoder(self.lift_motor_port) > 5):
                # self.robot.set_motor_dps(self.lift_motor_port, speed)
                time.sleep(0.02)
                # print(degrees, self.robot.get_motor_encoder(self.lift_motor_port))
        else:  
            self.robot.set_motor_dps(self.lift_motor_port, -speed)

            while (degrees-self.robot.get_motor_encoder(self.lift_motor_port) <= -5):
                # self.robot.set_motor_dps(self.lift_motor_port, -speed)
                time.sleep(0.02)
                # print(degrees, self.robot.get_motor_encoder(self.lift_motor_port))
        self.robot.set_motor_dps(self.lift_motor_port, 0)    
    
    def set_grabber(self, angle, hold=False):
        if angle < 0:
            angle = 0
        elif angle > 80:
            angle = 80
  
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
        # self.lift(30)
        self.set_grabber(0)
        self.robot.forward_cm_with_gyro(distance=25, angle=-15, stop=False)

        self.robot.forward_cm_with_gyro(distance=40, angle=0)
        self.set_grabber(80)
        self.robot.forward_cm_with_gyro(distance=-26, angle=0, stop=False)
        self.set_grabber(0)
        # self.robot.forward_cm_with_gyro(distance=-10, angle=0)

        # 1. eszköz letéve

        self.robot.forward_cm_with_gyro(distance=-15, angle=-30)
        self.set_grabber(80)
        self.robot.turn_with_gyro(0)
        self.robot.forward_cm_with_gyro(distance=62, angle=0, stop=False)
        self.lift(degrees=200)
        self.robot.forward_cm_with_gyro(distance=27.5, angle=-38, stop=False)
        self.robot.forward_cm_with_gyro(distance=8, angle=0)
        self.robot.turn_one_wheel_gyro(self.robot.right_motor_port, angle = 53, slow=False, speed=500)
        self.robot.turn_one_wheel_gyro(self.robot.left_motor_port, angle = 0, speed=500)
        # self.robot.wait_for_button_press()
        self.robot.forward_cm_with_gyro(distance=44, angle=0)

        self.robot.turn_one_wheel_gyro(self.robot.right_motor_port, 200, slow=False)
        time.sleep(0.2)

        # 2. eszköz letéve

        self.robot.forward_cm_with_gyro(distance=-17, angle=210)
        self.robot.turn_one_wheel_gyro(self.robot.left_motor_port, angle=270)
        self.robot.forward_cm_with_gyro(distance=38, angle=270, stop=False)
        # self.robot.wait_for_button_press()



    def align_to_lines(self):
        self.robot.align_to_black()
        # self.robot.gyro_sensor.reset_with_angle(270)
        self.robot.turn_with_gyro(angle=180)
        self.robot.turn_with_gyro(angle=180)
        self.robot.forward_cm_with_gyro(distance=-5, angle=180, stop=False)

        # self.robot.wait_for_button_press()

        self.robot.align_to_black(speed=-100)

        # self.robot.gyro_sensor.reset_with_angle(180)

    def do_kanal(self):
        # self.robot.align_to_black(speed=-100)
        # self.robot.gyro_sensor.reset_with_angle(180)
        self.robot.forward_cm_with_gyro(distance=10, angle=200, stop=False)
        # self.robot.wait_for_button_press()
        self.robot.forward_cm_with_gyro(distance=50, angle=177, stop=False)
        # self.robot.wait_for_button_press()
        self.robot.forward_cm_with_gyro(distance=20, angle=160, stop=False)
        # self.robot.wait_for_button_press()
        self.robot.forward_cm_with_gyro(distance=45, angle=177, stop=False)
        # self.robot.wait_for_button_press()
        self.robot.forward_cm_with_gyro(distance=35, angle=170, stop=False)
        # self.robot.wait_for_button_press()
        self.robot.forward_cm_with_gyro(distance=20, angle=180, stop=False)
        # self.robot.wait_for_button_press()
        self.robot.forward_cm_with_gyro(distance=15, angle=200)
        time.sleep(0.3)
        self.robot.forward_cm_with_gyro(distance=-18.5, angle=185, speed=500)

        self.robot.turn_with_gyro(angle=90, speed=500)
        # self.robot.wait_for_button_press()
        time.sleep(0.2)


    def cubes1(self):
        self.robot.align_to_black(speed=100)
        self.robot.forward_cm_with_gyro(distance=15, angle=90)
        # self.robot.wait_for_button_press()
        self.robot.align_to_black()
        # self.robot.wait_for_button_press()
        self.robot.turn_with_gyro(angle=184)

        self.robot.forward_cm_with_gyro(distance=3, angle=182, stop=False, speed=200)
        self.set_grabber(0)
        self.lift(degrees=-195)
        time.sleep(0.2)
        self.robot.align_to_black()
        time.sleep(0.5)
        # self.robot.forward_cm_with_gyro(distance=1.5, angle=180, speed=300)
        self.set_grabber(60, hold=True)
        self.robot.forward_cm_with_gyro(distance=2, angle=180, speed=300)
        self.set_grabber(0, hold=True)
        self.robot.forward_cm_with_gyro(distance=3.75, angle=180, speed=300)
        self.set_grabber(60, hold=True)

        # self.robot.wait_for_button_press()

        self.robot.forward_cm_with_gyro(distance=-3, angle=182, stop=False, speed=300)
        self.robot.align_to_white(speed=-150)
        
        # self.robot.wait_for_button_press()
        self.robot.forward_cm_with_gyro(distance=-3, angle=181, stop=False, speed=300)
        self.robot.align_to_black(speed=-150)

