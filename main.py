#!/usr/bin/env python3
from time import sleep
from wroRobot import WroRobot
from task import Task
import sys, time

robot = WroRobot()
task = Task(robot)

leallit = False
# leallit = True

# robot.calibrate()
# sys.exit()

if leallit: 
    print("ÖSSZES MOTOR LEÁLL!!!!!ÖSSZES MOTOR LEÁLL!!!!!ÖSSZES MOTOR LEÁLL!!!!!ÖSSZES MOTOR LEÁLL!!!!!ÖSSZES MOTOR LEÁLL!!!!!")
    robot.reset_all()
    sys.exit()

try:
    now_time = time.time()
    robot.starting()
    sleep(1)
    task.gyro_test()
    task.do_glettelo()

    robot.log(f"Task completed in {time.time() - now_time} seconds")



except KeyboardInterrupt as e:
    print("Keyboard: " + str(e))
    robot.reset_all()

except Exception as e:
    print(e)
    robot.reset_all()

