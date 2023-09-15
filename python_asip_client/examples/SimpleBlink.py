__author__ = 'Gianluca Barbon'

"""
blink an LED

LED_PIN constant should be set to match board running ASIP
Note that Pico LED pin is 25, PicoW LED pin cannot be be set from ASIP

Run this from a parent directory of python_asip_client
"""

import sys
import time
import os # for kbhit
from python_asip_client.boards.kbhit import KBHit
from python_asip_client.boards.serial_board import SerialBoard

LED_PIN = 25 # set this to the LED pin for the board running ASIP (13 for Uno, 25 for Pico)
# fixme: update ASIP on microcontroller to treat pin -2 as LED_BUILTIN 

# A simple board with just the I/O services.
# The main method does a standard blink test.
class SimpleBlink(SerialBoard):

    def main(self):
        if os.name == 'nt':
            kb = KBHit()  # needed for windows to handle keyboard interrupt
            sys.stdout.write('Hit ESC to exit\n')
        try:
            time.sleep(0.5)
            self.asip.set_pin_mode(LED_PIN, self.asip.OUTPUT)
            time.sleep(0.5)
        except Exception as e:
            sys.stdout.write("Exception caught while setting pin mode: {}\n".format(e))
            self.abort()
            sys.exit(1)

        while True:        
            if os.name == 'nt':
                if kb.kbhit():
                    c = kb.getch()
                    if ord(c) == 27:  # ESC
                        kb.set_normal_term()
                        break
            try:
                self.asip.digital_write(LED_PIN, self.asip.HIGH)
                time.sleep(1.25)
                self.asip.digital_write(LED_PIN, self.asip.LOW)
                time.sleep(1.25)
            except (KeyboardInterrupt, Exception) as e:
                sys.stdout.write("Caught exception in main loop: {}\n".format(e))
                self.abort()
                sys.exit()
        self.abort()


# test SimpleBlink
if __name__ == "__main__":
    SimpleBlink().main()
    sys.stdout.write("Quitting!\n")
    sys.exit(0)