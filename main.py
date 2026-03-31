#!/usr/bin/env python3
from time import sleep
from wroRobot import WroRobot
from task import Task
import sys, time

robot = WroRobot()
task = Task(robot)

leallit = False
# leallit = True

if leallit: 
    print("ÖSSZES MOTOR LEÁLL!!!!!ÖSSZES MOTOR LEÁLL!!!!!ÖSSZES MOTOR LEÁLL!!!!!ÖSSZES MOTOR LEÁLL!!!!!ÖSSZES MOTOR LEÁLL!!!!!")
    robot.reset_all()
    sys.exit()

try:
    print(time.time())
    robot.starting()
    sleep(0.5)
    robot.starting()
    sleep(1)
    task.gyro_test()
    task.turn_gyro_test()
    # n = 1000
    # while n: 
    #     print(robot.gyro_sensor.angle)
    #     n -= 1
    #     time.sleep(0.01)

except KeyboardInterrupt as e:
    print("Keyboard: " + str(e))
    robot.reset_all()
except Exception as e:
    print(e)
    robot.reset_all()



# task.lift()
# task.set_grabber(0)
# sleep(.5)
# task.lift(0)
# task.set_grabber(60)

sleep(1)
