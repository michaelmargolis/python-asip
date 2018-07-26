from python_asip_client.boards.tcp_board import TCPBoard
from python_asip_client.services.bump_service import BumpService
from python_asip_client.services.ir_service import IRService
from python_asip_client.services.motor_service import MotorService
import sys
import time


class TCPMirtoRobot(TCPBoard):

    def __init__(self, ip, tcp_port=9999):
        TCPBoard.__init__(self, ip, tcp_port)

        # Creating instances of services
        self._motors = [MotorService(0, self.asip), MotorService(1, self.asip)]  # init 2 motors (wheels)
        self._irs = [IRService(0, self.asip), IRService(1, self.asip), IRService(2, self.asip)]  # init 3 IR sensors
        self._bumps = [BumpService(0, self.asip), BumpService(1, self.asip)]  # init 2 bump sensors
        sys.stdout.write("DEBUG: instances of services created\n")

        # Setting reporting interval of sensors
        reporting_interval = 25
        self._motors[0].enable_encoder()
        self._motors[1].enable_encoder()
        self._irs[0].set_reporting_interval(reporting_interval)
        self._irs[1].set_reporting_interval(reporting_interval)
        self._irs[2].set_reporting_interval(reporting_interval)
        self._bumps[0].set_reporting_interval(reporting_interval)
        self._bumps[1].set_reporting_interval(reporting_interval)
        sys.stdout.write("DEBUG: reporting interval set to {}\n".format(reporting_interval))

        #  Adding services
        self.get_asip_client().add_service(self._motors[0].get_service_id(), self._motors)
        # self.get_asip_client().add_service(self._encoders[0].get_service_id(), self._encoders)
        self.get_asip_client().add_service(self._irs[0].get_service_id(), self._irs)
        self.get_asip_client().add_service(self._bumps[0].get_service_id(), self._bumps)
        sys.stdout.write("DEBUG: services added\n")

    # Setting the two motors speed
    def set_motors(self, s0, s1):
        self._motors[0].set_motor(s0)
        self._motors[1].set_motor(s1)
        sys.stdout.write("DEBUG: setting motors to {}, {}\n".format(s0, s1))

    # Stopping the two motors
    def stop_motors(self):
        self._motors[0].stop_motor()
        self._motors[1].stop_motor()

    # Retrieving data from IR sensor, -1 if sensor number is wrong
    def get_ir(self, sensor):
        return self._irs[sensor].get_ir() if sensor in [0, 1, 2] else -1

    # Retrieving count value from encoder sensor, -1 if sensor number is wrong
    def get_count(self, sensor):
        return self._motors[sensor].get_count() if sensor in [0, 1] else -1

    # Retrieving count value from bump sensor, -1 if sensor number is wrong
    def is_pressed(self, sensor):
        return self._bumps[sensor].is_pressed() if sensor in [0, 1] else -1

    # method for testing
    def test(self):
        sys.stdout.write("Start test for tcp\n")
        try:
            sys.stdout.write("IR: {}, {}, {}\n".format(self.get_ir(0), self.get_ir(1), self.get_ir(2)))
            sys.stdout.write("Encoders: {}, {}\n".format(self.get_count(0), self.get_count(1)))
            sys.stdout.write("Bumpers: {}, {}\n".format(self.is_pressed(0), self.is_pressed(1)))
            sys.stdout.write("Setting motors to 100, 0\n")
            self.set_motors(100, 0)
            time.sleep(1.5)
            sys.stdout.write("Stopping motors\n")
            self.stop_motors()
            time.sleep(0.5)
            sys.stdout.write("Setting motors to 0, -250\n")
            self.set_motors(0, -250)
            time.sleep(1.5)
            sys.stdout.write("Stopping motors\n")
            self.stop_motors()
            time.sleep(0.5)
        except Exception as e:
            sys.stdout.write("Exception: caught {} in testing mirto robot\n".format(e))


# Method for testing is called
if __name__ == "__main__":
    ip_address = "10.14.122.61"
    TCPMirtoRobot(ip_address).test()
