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
    # while True:
    #     for reg in range(0x41, 0x48):
    #         robot.set_sensor_type(
    #             robot.PORT_1,
    #             robot.SENSOR_TYPE.I2C,
    #             [robot.SENSOR_I2C_SETTINGS.SAME, 50, 0, 0x02, [reg], 2]
    #         )
    #         time.sleep(0.1)
    #         print(hex(reg), robot.get_sensor(robot.PORT_1))
    #     sleep(.3)
    # robot.set_sensor_type(robot.PORT_1, robot.SENSOR_TYPE.I2C, [robot.SENSOR_I2C_SETTINGS.SAME, 50, 0, 0x02, [0x42], 2])
    # while True:
    #     sleep(.02)
    #     print(robot.gyro_sensor.angle)
        # resultx42 = robot.get_sensor(robot.PORT_1)
        # robot.set_sensor_type(robot.PORT_1, robot.SENSOR_TYPE.I2C, [robot.SENSOR_I2C_SETTINGS.SAME, 50, 0, 0x02, [0x44], 2])
        # sleep(.02)
        # resultx44 = robot.get_sensor(robot.PORT_1)
        # print("0x42 raw: " + str(resultx42[0]) + ", " + str(resultx42[1]) + " formatted: " + str((resultx42[0] * 2 + resultx42[1])))
        # print("0x44 raw: " + str(resultx44[0]) + ", " + str(resultx44[1]) + " formatted: " + str((resultx44[0] << 8 | resultx44[1]) / 10.0))
    # robot.starting()

    # sleep(0.5)
    robot.starting(command=task.lift)
    task.gyro_test()
    now_time = time.time()
    task.do_glettelo()
    task.align_to_lines()
    task.do_kanal()
    task.cubes1()
    robot.log(f"cubes1 {time.time() - now_time} seconds")
    task.cubes2()
    robot.log(f"Task completed in {time.time() - now_time} seconds")
    # task.cubes3()
    robot.log(f"Task+ completed in {time.time() - now_time} seconds")


except KeyboardInterrupt as e:
    print("Keyboard" + str(e))
    robot.reset_all()

except Exception as e:
    print(e)
    task.set_grabber(0)
    task.set_grabber(80)
    robot.reset_all()

