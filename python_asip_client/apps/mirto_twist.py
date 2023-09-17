#!/usr/bin/env python

# mirto_twist.py

import math

from python_asip_client.mirto_robot import MirtoRobot
from python_asip_client.mirto_robot_services import SerialMirtoRobot


WHEEL_DIAMETER= .064
WHEEL_CIRCUMFERENCE=WHEEL_DIAMETER * math.pi
WHEEL_TRACK=.162
TRACK_CIRCUMFERENCE=WHEEL_TRACK * math.pi
GEAR_REDUCTION=34
PPR=12 # note each pulse triggers 4 interrupts
ENCODER_TICKS_PER_WHEEL_REV=GEAR_REDUCTION * PPR * 4 



    
class MirtoTwist:
    def __init__(self):
        self.robot_board=SerialMirtoRobot()
        self.robot=MirtoRobot(self.robot_board.get_services())
        self.abort=self.robot_board.abort        
        
    def twist(self, linear_x, angular_z, duration):
        if linear_x == 0 and angular_z == 0:
            print("stop motors")
            self.robot.stop_motors()
        else:    
            left_wheel_velocity=linear_x - (angular_z * WHEEL_TRACK)/2
            right_wheel_velocity=linear_x + (angular_z * WHEEL_TRACK)/2
            # todo add code to check if velocity is within robot's capability 
            left_rpm=(left_wheel_velocity * 60) / WHEEL_CIRCUMFERENCE
            right_rpm=(right_wheel_velocity * 60) / WHEEL_CIRCUMFERENCE   
            duration=int(duration * 1000) # ASIP expects milliseconds
            self.robot.set_motors_rpm(left_rpm, right_rpm, duration)
            print("twist msg: linear={}, angular={}, left rpm={}, right rpm={}".format(linear_x, angular_z, left_rpm, right_rpm))

    def get_encoder_counts(self):
        return self.robot.get_encoders(False) # return list of ints
        
    def get_ir_sensors(self):
        return self.robot.get_all_ir_values() # returns list of ints
  
    def get_bump_sensors(self):
        return [self.robot.is_bump_pressed(0), self.robot.is_bump_pressed(1)] # returns list of bools