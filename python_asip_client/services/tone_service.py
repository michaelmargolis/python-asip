from python_asip_client.services.asip_service import AsipService
import sys


class ToneService(AsipService):
    DEBUG = False
    _serviceID = 'T'

    __TAG_TONE_PLAY = 'P'  # play tone of given frequency and duration

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

    def play(self, frequency, duration): # f in Hz, duration in ms
        if self.DEBUG:
            sys.stdout.write("DEBUG: Playing tone {} Hz for {} ms\n".format(frequency,duration))

        self.asip.get_asip_writer().write("{},{},{},{}\n".format(
            self._serviceID, self.__TAG_TONE_PLAY, frequency, duration))
