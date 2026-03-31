from myColorSensor import my_color_sensor, my_gyro_sensor
import sys, time, os, threading 
from brickpi3 import *
   
class WroRobot(BrickPi3):

    def __init__(self):
        BrickPi3.__init__(self)
        self.gyro_correction = 0
        self.reset_all()
        self.left_motor_port = self.PORT_B
        self.right_motor_port = self.PORT_C
        self.gyro_sensor = my_gyro_sensor(port = self.PORT_1, BP=self)
        self.touch_sensor_port = self.PORT_4
        self.set_sensor_type(self.touch_sensor_port, self.SENSOR_TYPE.EV3_TOUCH)
        self.start_log()

    def __del__(self):
        self.reset_all()
    
    def wait_for_button_press(self):
        value = 0
        while not value:
            try:
                value = self.button_pressed()
            except SensorError:
                pass

    def button_pressed(self):
        return self.get_sensor(self.touch_sensor_port)

    def starting(self):
        while True:
            try:
                time.sleep(.02)
                print(self.gyro_sensor.angle)
            except SensorError as se:
                print(se)
            except Exception as e:
                print("Nem Sensorhiba:", e)
            else:
                break
            finally:
                time.sleep(0.5)

        print("beep beep")
        print(self.get_voltage_battery())
        self.wait_for_button_press()

    def forward_cm(self, speed, distance, stop=True):
        degrees = distance * (360 / 17.6)
        self.forward_angle(speed, degrees, stop)

    def forward_angle(self, speed, degrees, wait=True):
        
        self.set_motor_limits(self.left_motor_port, 100, speed)
        self.set_motor_limits(self.right_motor_port, 100, speed)
        self.set_motor_position_relative(self.left_motor_port, -degrees)
        self.set_motor_position_relative(self.right_motor_port, -degrees)
        time.sleep(0.5)
        if wait:
            while self.get_motor_status(self.left_motor_port)[3] != 0:
                time.sleep(0.01)

    def align_to_black(self, speed, black_threshold = None):
        self.set_motor_power(self.left_motor_port, speed)
        self.set_motor_power(self.right_motor_port, speed)
        is_right_running = True
        is_left_running = True
        while (is_right_running or is_left_running):
            if (self.left_color_sensor.is_black_reflection(black_threshold)):
                self.set_motor_power(self.left_motor_port, 0)

            if (self.right_color_sensor.is_black_reflection(black_threshold)):
                self.set_motor_power(self.right_motor_port, 0)

    def align_to_white(self, speed, white_threshold = None):
        self.set_motor_power(self.left_motor_port, speed)
        self.set_motor_power(self.right_motor_port, speed)
        is_right_running = True
        is_left_running = True
        while (is_right_running or is_left_running):
            if (self.left_color_sensor.is_white_reflection(white_threshold)):
                self.set_motor_power(self.left_motor_port, 0)

            if (self.right_color_sensor.is_white_reflection(white_threshold)):
                self.set_motor_power(self.right_motor_port, 0)


    # def turn(self, angle, speed=None, left_speed=None, right_speed=None):  # pozitív angle -> jobbra
    #     angle=angle*1
    #     if speed != None:
    #         degrees = 270 * (angle / 90)
    #         self.log(degrees)
    #         self.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=abs(speed), stop_action=Motor.STOP_ACTION_HOLD)
    #         self.right_motor.run_to_rel_pos(position_sp=-degrees, speed_sp=abs(speed), stop_action=Motor.STOP_ACTION_HOLD)
    #     elif left_speed != None:
    #         degrees = 580 * (angle / 90)
    #         self.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=abs(left_speed), stop_action=Motor.STOP_ACTION_HOLD)
    #     elif right_speed != None:
    #         degrees = 580 * (angle / 90)
    #         self.right_motor.run_to_rel_pos(position_sp=-degrees, speed_sp=abs(right_speed), stop_action=Motor.STOP_ACTION_HOLD)
    #     self.left_motor.wait_until_not_moving()
    #     self.right_motor.wait_until_not_moving()
    #     time.sleep(0.3)

    # def turn_with_gyro(self, speed, deegres):

    def turn_with_gyro(self, angle, speed = 800, slow = True):
        if (self.gyro_sensor.angle > angle):
            self.set_motor_dps(self.left_motor_port, -speed)
            self.set_motor_dps(self.right_motor_port, speed)
            while (self.gyro_sensor.angle > angle): 
                print(self.gyro_sensor.angle, angle)
                time.sleep(0.2)
        else: 
            print("turning right")
            self.set_motor_dps(self.left_motor_port, speed)
            self.set_motor_dps(self.right_motor_port, -speed)
            angle_now = self.gyro_sensor.angle
            while (angle_now < angle): 
                angle_now = self.gyro_sensor.angle
                print(angle_now, angle)
                time.sleep(1)

    def forward_with_gyro_to_black(self, speed, angle, sensor):
        wf = lambda robot : not sensor.is_black_reflection()
        self.forward_with_gyro(speed, angle, wf, True)            
    
    def forward_with_gyro_to_white(self, speed, angle, sensor):
        wf = lambda robot : not sensor.is_white_reflection()
        self.forward_with_gyro(speed, angle, wf, True)            
   
    def forward_cm_with_gyro(self, speed, distance, angle, stop = None):
        degrees = distance * (360 / 17.6) *-1
        self.forward_angle_wit_gyro(speed, degrees, angle, stop)

    def forward_angle_wit_gyro(self, speed, degrees, angle, stop = None):    
        self.offset_motor_encoder(self.left_motor_port, self.get_motor_encoder(self.left_motor_port))
        self.offset_motor_encoder(self.right_motor_port, self.get_motor_encoder(self.right_motor_port))
        if speed * degrees > 0:
            wf = lambda robot : robot.get_motor_encoder(robot.left_motor_port) < abs(degrees)
            self.forward_with_gyro(abs(speed), angle, wf, stop)
        else:
            wf = lambda robot : robot.get_motor_encoder(robot.left_motor_port) > -abs(degrees)
            self.forward_with_gyro(-abs(speed), angle, wf, stop)


    def forward_with_gyro(self, speed, angle, while_func, stop = True):
        sign = speed / abs(speed)

        left_speed = 50 * sign
        right_speed = 50 * sign
        diff_speed = 0
        now_gyro_angle = self.gyro_sensor.angle
        while while_func(self):
            print(left_speed, right_speed, speed, diff_speed, now_gyro_angle)
            self.set_motor_power(self.left_motor_port, left_speed)
            self.set_motor_power(self.right_motor_port, right_speed)
            #print("gyro: {0}, left speed: {1}, right speed: {2}".format(self.gyro_sensor.angle, left_speed, right_speed), file=sys.stderr)
            
            if speed > 0:
                if right_speed < speed or left_speed < speed:
                    left_speed += 15
                    right_speed += 15
                
                diff_speed = (angle - (now_gyro_angle + self.gyro_correction)) * 25

                if diff_speed < 0:
                    if right_speed >= speed:
                        right_speed = speed
                        left_speed = speed - abs(diff_speed)
                    else:
                        right_speed = left_speed + abs(diff_speed)
                elif diff_speed > 0:
                    if left_speed >= speed:
                        left_speed = speed
                        right_speed = speed - abs(diff_speed)
                    else:
                        left_speed = right_speed + abs(diff_speed)
                elif left_speed != right_speed:
                    if left_speed > speed or right_speed > speed:
                        left_speed = speed
                        right_speed = speed
                    else:
                        left_speed = max(left_speed, right_speed)
                        right_speed = left_speed
            else:
                if right_speed > speed or left_speed > speed:
                    left_speed -= 15
                    right_speed -= 15
                
                diff_speed = (angle - self.gyro_sensor.angle) * 25
                

                if diff_speed > 0:
                    if right_speed <= speed:
                        right_speed = speed
                        left_speed = speed + abs(diff_speed)
                    else:
                        right_speed = left_speed - abs(diff_speed)
                elif diff_speed < 0:
                    if left_speed <= speed:
                        left_speed = speed
                        right_speed = speed + abs(diff_speed)
                    else:
                        left_speed = right_speed - abs(diff_speed)
                elif left_speed != right_speed:
                    if left_speed < speed or right_speed < speed:
                        left_speed = speed
                        right_speed = speed
                    else:
                        left_speed = min(left_speed, right_speed)
                        right_speed = left_speed
            time.sleep(0.05)

    def start_log(self):
        try:
            os.mkdir("./log")
        except:
            pass

        log_files = os.listdir("./log")
        i = 1
        if len(log_files) > 0:
            log_files.sort()
            i = int(log_files[-1][4:7]) + 1

        self.log_file_name = "./log/log_{0:03d}.txt".format(i)
        self.displayed_events = []
        with open(self.log_file_name, "w+") as f:
            pass
        print("Log file created: {0}".format(self.log_file_name), file=sys.stderr)        

    def log(self, text, logtext=""):
        with open(self.log_file_name, "a") as f:
            if logtext == "":
                f.write("{0}\n".format(text))
                print("{0}".format(text), file=sys.stderr)
            else:
                f.write("{0}\n".format(logtext))
                print("{0}".format( logtext), file=sys.stderr)

        # if len(self.displayedEvents) == 4:
        #     self.displayedEvents.pop(0)

        # self.displayedEvents.append(str(text)[:13])
        # self.display.clear()
        # for i, event in enumerate(self.displayedEvents):
        #     self.display.draw.text((0,i*30), event, font=fonts.load('luBS24'))
        # self.display.update()    