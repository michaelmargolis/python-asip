from python_asip_client.services.asip_service import AsipService
import sys


class LCDService(AsipService):
    DEBUG = False
    _serviceID = 'L'

    __TAG_LCD_WRITE = 'W'
    __TAG_LCD_CLEAR = 'C'

    asip = None # The service should be attached to a client

    def __init__(self, id, asipclient):
        AsipService.__init__(self)
        self.asip = asipclient

    # *** Standard getters and setters ***

    def get_service_id(self):
        return self._serviceID

    def set_service_id(self,id):
        self._serviceID = id

    # receives an instance of AsipClient as parameter
    def set_client(self, client):
        self.asip = client

    def get_client(self):
        return self.asip

    def process_response(self, message):
        # Do nothing
        pass

    def set_lcd_message(self, message, line):
        if line < 0:  # note asip firmware checks line does not exceed physical LCD
            sys.stdout.write("ERROR: invalid line number ({})".format(line))
            return
        if self.DEBUG:
            sys.stdout.write("DEBUG: Writing: {} to line {} on the LCD\n".format(message,line))

        self.asip.get_asip_writer().write("{},{},{},{}\n".format(
            self._serviceID, self.__TAG_LCD_WRITE, str(line), message))

    def clear_lcd(self):
        if self.DEBUG:
            sys.stdout.write("DEBUG: Clearing the LCD")
        self.asip.get_asip_writer().write("{},{}\n".format(
            self._serviceID, self.__TAG_LCD_CLEAR))