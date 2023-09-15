import math
import sys
import time
import traceback

from python_asip_client.mirto_robot import MirtoRobot
from python_asip_client.mirto_robot_services import SerialMirtoRobot
from python_asip_client.mirto_robot_services import TCPMirtoRobot

class MirtoTest:
    def __init__(self):
        self.robot = None

    def init_robot(self, hostname=None):
        if hostname is None:
            self.robot_board = SerialMirtoRobot()
        else:
            self.robot_board = TCPMirtoRobot(hostname, 9999)
        self.robot = MirtoRobot( self.robot_board.get_services())
        self.abort = self.robot_board.abort
        
        self.prev_encoder_counts = None
   
    def test_tones(self):
        print("testing Tones")
        self.robot.clear_lcd()
        self.robot.set_lcd_message("Testing Tones", 0) 
        tones = [262,294,330,349,392,440,494]
        score = [0,0,4,4,5,5,4,3,3,2,2,1,1,0]
        for note in score:
            self.robot.play_tone(tones[note], 200)
            time.sleep(.3)  
    
    def test_neopixels(self):
        print("testing neopixel")
        self.robot.set_lcd_message("Testing Neopixels", 0) 
        rgb = [(255,0,0),( 0,255,0), ( 0,0,255), ( 16,16,16)]
        for idx, color in enumerate(rgb):
            self.robot.set_pixel_color(0, *color)  # set pixel 0
            time.sleep(1)
        
    def test_ir(self):
        print("testing IR, press both bump switches to end test")
        self.robot.clear_lcd()
        self.robot.set_lcd_message("IR Sensor Test", 0) 
        while( not self.robot.is_bump_pressed(0) or not self.robot.is_bump_pressed(1)):
            self.robot.set_lcd_message("Right   {}   ".format(self.robot.get_ir(2)), 1)
            self.robot.set_lcd_message("Mid     {}   ".format(self.robot.get_ir(1)), 2)
            self.robot.set_lcd_message("Left    {}   ".format(self.robot.get_ir(0)), 3)           
            time.sleep(.1)
    
    def test_distance(self):
        print("testing Distance, press both bump switches to end test")
        self.robot.clear_lcd()
        self.robot.set_lcd_message("Distance Sensor Test", 0) 
        while( not self.robot.is_bump_pressed(0) or not self.robot.is_bump_pressed(1)):
            self.robot.set_lcd_message("Distance = {}   ".format(self.robot.get_sensor_distance()), 1)
            time.sleep(.1)
            print(self.robot.get_sensor_distance())
            
    def test_motors(self):    
        print("testing Motors") 
        self.robot.reset_count()        
        self.robot.clear_lcd()
        # press both bumpers to end this test
        self.robot.set_lcd_message("Motor Test", 0)
        self.robot.set_lcd_message("Rotate CW 90 deg", 1)
        self.robot.rotate_robot_angle(45, 90) # cw
        self.show_encoder_counts(4)   
        self.robot.set_lcd_message("Rotate CCW 90 deg", 1)
        self.robot.rotate_robot_angle(45, -90 ) # ccw
        self.show_encoder_counts(4)

    def show_encoder_counts(self, timeout):
        start_time = time.monotonic()
        start_counts = self.robot.get_encoders(False)
        while  time.monotonic() - start_time < timeout:
            encoder_counts = self.robot.get_encoders(False)
            self.robot.set_lcd_message("  L Enc {}".format( encoder_counts[0]), 2)
            self.robot.set_lcd_message("  R Enc {}".format( encoder_counts[1]), 3)
            #if start_counts != encoder_counts and self.robot.is_any_motor_moving() == False:
            #    break
            time.sleep(.25)    
     

    
    def test_main(self):
        print("\nstarting test")
        try:
            self.robot.clear_lcd()
            self.robot.set_lcd_message("Starting Tests", 0)
            time.sleep(.5)
            self.test_tones()
            self.test_neopixels()
            self.test_ir()
            # self.test_distance()
            self.test_motors() 
            self.robot.clear_lcd()
            self.robot.set_lcd_message("Tests completed", 0)
            
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self.abort()
            sys.exit()


if __name__ == '__main__':
    test = MirtoTest()
    test.init_robot()
    test.test_main()
    test.abort()
