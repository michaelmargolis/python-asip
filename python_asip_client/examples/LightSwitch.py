__author__ = 'Gianluca Barbon'

from python_asip_client.boards.serial_board import SerialBoard
import sys
import time

"""
A simple board with just the I/O services on a fixed port.
The main method simulates a light switch.

LED and swtich constant should be set to match board running ASIP
Note that Mirto Pico LED pin is 25, switch is on pin 12(PicoW LED pin cannot be be set from ASIP)

Run this from a parent directory of python_asip_client folder

"""
class LightSwitch(SerialBoard):

    def __init__(self):
        SerialBoard.__init__(self)
        self.buttonPin = 12  # the number for the pushbutton pin on the Arduino
        self.ledPin = 25     # the number for the LED pin on the Arduino
        self.buttonState = self.asip.LOW
        self.oldstate = self.asip.LOW

        self.init_conn()

    # init_conn initializes the pin
    def init_conn(self):
        try:
            time.sleep(0.5)
            self.asip.set_pin_mode(self.ledPin, self.asip.OUTPUT)
            time.sleep(0.5)
            self.asip.set_pin_mode(self.buttonPin, self.asip.INPUT_PULLUP)
        except Exception as e:
            sys.stdout.write("Exception caught while setting pin mode: {}\n".format(e))
            self.abort()
            sys.exit(1)

    def main(self):
        while True:
            try:
                # check the value of the pin
                self.buttonState = self.asip.digital_read(self.buttonPin)

                # check if the value is changed with respect to previous iteration
                if self.buttonState != self.oldstate:
                    if self.buttonState == 0:  # turn on LED when pull-up switch goes LOW
                        self.asip.digital_write(self.ledPin, self.asip.HIGH)
                    else:
                        self.asip.digital_write(self.ledPin, self.asip.LOW)
                self.oldstate = self.buttonState
                time.sleep(0.005)  # Needed for thread scheduling/concurrency

            except (KeyboardInterrupt, Exception) as e:
                sys.stdout.write("Caught exception in main loop: {}\n".format(e))
                break
        self.abort()
    
# test LightSwitch
if __name__ == "__main__":
    LightSwitch().main()