from myColorSensor import my_color_sensor, my_gyro_sensor
from PID import PID
import sys, time, os, threading 
from brickpi3 import *
# from winsound import  Beep
   
class WroRobot(BrickPi3):

    def __init__(self):
        BrickPi3.__init__(self)
        self.set_led(0)
        self.gyro_correction = 0
        self.left_motor_port = self.PORT_B
        self.right_motor_port = self.PORT_C
        self.gyro_sensor = my_gyro_sensor(port = self.PORT_1, BP=self)
        self.touch_sensor_port = self.PORT_4
        self.set_sensor_type(self.touch_sensor_port, self.SENSOR_TYPE.EV3_TOUCH)
        # self.start_log()
        self.left_color_sensor = my_color_sensor(self.PORT_3, BP=self)
        self.right_color_sensor = my_color_sensor(self.PORT_2, BP=self)
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
                self.gyro_sensor.reset()
            except SensorError as se:
                print(se)
            except Exception as e:
                print("Nem Sensorhiba:", e)
            else:
                break
            finally:
                time.sleep(0.5)

        print("beep beep")
        self.set_led(100)
        
        self.log(f"aku: {self.get_voltage_battery()}")
        self.wait_for_button_press()

    def align_to_black(self, speed=150, black_threshold = None):
        self.set_motor_dps(self.left_motor_port, -speed)
        self.set_motor_dps(self.right_motor_port, -speed)
        is_right_running = 3
        is_left_running = 3
        while (is_right_running or is_left_running):
            if (is_left_running and self.left_color_sensor.is_black_reflection(black_threshold)):
                is_left_running -= 1

            if (is_right_running and self.right_color_sensor.is_black_reflection(black_threshold)):
                is_right_running -= 1

            if (not is_left_running): self.set_motor_dps(self.left_motor_port, 0)
            if (not is_right_running): self.set_motor_dps(self.right_motor_port, 0)
        self.log(f"fekete: {self.left_color_sensor.get_reflection()}")
        self.log(f"fekete: {self.right_color_sensor.get_reflection()}")

    def align_to_white(self, speed=150, white_threshold = None):
        self.set_motor_dps(self.left_motor_port, -speed)
        self.set_motor_dps(self.right_motor_port, -speed)
        is_right_running = 3
        is_left_running = 3
        while (is_right_running or is_left_running):
            if (is_left_running and self.left_color_sensor.is_white_reflection(white_threshold)):
                self.set_motor_dps(self.left_motor_port, 0)
                is_left_running -= 1

            if (is_right_running and self.right_color_sensor.is_white_reflection(white_threshold)):
                is_right_running -= 1

            if (not is_left_running): self.set_motor_dps(self.left_motor_port, 0)
            if (not is_right_running): self.set_motor_dps(self.right_motor_port, 0)
        self.log(f"fehér: {self.left_color_sensor.get_reflection()}")
        self.log(f"fehér: {self.right_color_sensor.get_reflection()}")

    def align_to_wall(self, time_to_go = 1.5, speed = 350): 
        self.set_motor_dps(self.left_motor_port, speed)
        self.set_motor_dps(self.right_motor_port, speed) 
        now_time = time.time()
        while (time.time() - now_time < time_to_go):
            time.sleep(0.02)
        self.set_motor_dps(self.left_motor_port, 0)
        self.set_motor_dps(self.right_motor_port, 0) 

    def turn_one_wheel_gyro(self, port, angle, speed=500, slow=True):
        for _ in range(3):
            if port is self.left_motor_port: self.turn_one_left_gyro(angle, speed, slow)
            if port is self.right_motor_port: self.turn_one_right_gyro(angle, speed, slow)

    def turn_one_left_gyro(self, angle, speed, slow):
        start_angle = self.gyro_sensor.angle
        if (start_angle > angle):
            self.set_motor_dps(self.left_motor_port, -speed)
            angle_now = self.gyro_sensor.angle
            while (angle_now > angle):
                if (slow and abs(angle - angle_now) < 15):
                    self.set_motor_dps(self.left_motor_port, -speed/5)
                    slow = False
                angle_now = self.gyro_sensor.angle
        else: 
            self.set_motor_dps(self.left_motor_port, speed)
            angle_now = self.gyro_sensor.angle
            while (angle_now < angle): 
                if (slow and abs(angle_now - angle) < 15):
                    # self.log(f"slow {angle_now} {angle}")
                    self.set_motor_dps(self.left_motor_port, speed/5)
                    slow = False
                angle_now = self.gyro_sensor.angle
                # print("Current angle: ", angle_now, angle, speed)
        self.set_motor_dps(self.left_motor_port, 0)

    def turn_one_right_gyro(self, angle, speed, slow):
        self.log("Turning with right_motor")
        start_angle = self.gyro_sensor.angle
        if (start_angle > angle):
            self.set_motor_dps(self.right_motor_port, speed)
            angle_now = self.gyro_sensor.angle
            while (angle_now > angle):
                if (slow and abs(angle - angle_now) < 15):
                    self.set_motor_dps(self.right_motor_port, speed/5)
                    slow = False
                angle_now = self.gyro_sensor.angle
        else: 
            self.log(f"turning right {speed}")
            self.set_motor_dps(self.right_motor_port, -speed)
            angle_now = self.gyro_sensor.angle
            while (angle_now < angle): 
                if (slow and abs(angle_now - angle) < 15):
                    speed /= 5
                    self.set_motor_dps(self.right_motor_port, -speed)
                    slow = False
                angle_now = self.gyro_sensor.angle
                print(f"Current angle: {angle_now}, {angle}, {speed}")
        self.set_motor_dps(self.right_motor_port, 0)

    def turn_with_gyro(self, angle, speed=500, slow=True):
        for _ in range(3):
            start_angle = self.gyro_sensor.angle
            angle_now = 0
            if (start_angle > angle):
                self.set_motor_dps(self.left_motor_port, -speed)
                self.set_motor_dps(self.right_motor_port, speed)
                angle_now = self.gyro_sensor.angle
                while (angle_now > angle):
                    if (slow and abs(angle - angle_now) < 15):
                        self.set_motor_dps(self.left_motor_port, -speed/5)
                        self.set_motor_dps(self.right_motor_port, speed/5)
                        slow = False
                    angle_now = self.gyro_sensor.angle
            else: 
                # print("turning right")
                self.set_motor_dps(self.left_motor_port, speed)
                self.set_motor_dps(self.right_motor_port, -speed)
                angle_now = self.gyro_sensor.angle
                while (angle_now < angle): 
                    if (slow and abs(angle_now - angle) < 15):
                        self.set_motor_dps(self.left_motor_port, speed/5)
                        self.set_motor_dps(self.right_motor_port, -speed/5)
                        slow = False
                    angle_now = self.gyro_sensor.angle
            self.set_motor_dps(self.left_motor_port, 0)
            self.set_motor_dps(self.right_motor_port, 0)
            self.log(f"{angle}: {angle_now}")

    def forward_with_gyro_to_black(self, speed, angle, sensor):
        wf = lambda robot : not sensor.is_black_reflection()
        self.forward_with_gyro(speed, angle, wf, True)            
    
    def forward_with_gyro_to_white(self, speed, angle, sensor):
        wf = lambda robot : not sensor.is_white_reflection()
        self.forward_with_gyro(speed, angle, wf, True)            
   
    def forward_cm_with_gyro(self, distance, angle, speed=500, stop = None, is_PID = False):
        print(speed, distance)   
        degrees = distance * (360 / 17.6) * -1
        self.forward_angle_wit_gyro(speed, degrees, angle, stop, is_PID)

    def forward_angle_wit_gyro(self, speed, degrees, angle, stop = None, is_PID = True): 
        self.offset_motor_encoder(self.left_motor_port, self.get_motor_encoder(self.left_motor_port))
        self.offset_motor_encoder(self.right_motor_port, self.get_motor_encoder(self.right_motor_port))
        if speed * degrees > 0:
            wf = lambda robot : robot.get_motor_encoder(robot.left_motor_port) < abs(degrees)
            self.forward_with_gyro(abs(speed), angle, wf, stop, is_PID)
        else:
            wf = lambda robot : robot.get_motor_encoder(robot.left_motor_port) > -abs(degrees)
            self.forward_with_gyro(-abs(speed), angle, wf, stop, is_PID)

    def forward_with_gyro(self, speed, angle, while_func, stop = True, is_PID = True):
        is_PID = False
        sign = speed / abs(speed)
        time_step=0.05
        left_speed = 300 * sign
        right_speed = 300 * sign
        diff_speed = 0
        while while_func(self):
            now_gyro_angle = self.gyro_sensor.angle
            # print("left_speed: ", left_speed, ", right_speed: ", right_speed, ", speed: ", speed, ", diff_speed: ", diff_speed, ", now_gyro_angle: ", now_gyro_angle, ", forw gyro", sep="")

            self.set_motor_dps(self.left_motor_port, left_speed)
            self.set_motor_dps(self.right_motor_port, right_speed)
            diff_speed = 0
            #print("gyro: {0}, left speed: {1}, right speed: {2}".format(self.gyro_sensor.angle, left_speed, right_speed), file=sys.stderr)
            if is_PID: 
                my_PID = PID(25, 10, 5, angle, time_step)
                diff_speed = my_PID.compute(now_gyro_angle)
            else:
                diff_speed = (angle - (now_gyro_angle + self.gyro_correction)) *25
            
            if speed > 0:
                if right_speed < speed or left_speed < speed:
                    left_speed += 15
                    right_speed += 15
                

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
            time.sleep(time_step)
        # if stop:
        self.set_motor_dps(self.left_motor_port, 0)
        self.set_motor_dps(self.right_motor_port, 0)

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

    def calibrate(self):
        self.left_color_sensor.calibrate(self.button_pressed)
        time.sleep(1)
        self.right_color_sensor.calibrate(self.button_pressed)