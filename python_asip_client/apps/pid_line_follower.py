import math
import sys
import time


class PidLineFollower:
    def __init__(self):
        self.howTo = "AsipMirtoPIDFollower usage:\n"
        + "You can invoke AsipMirtoPIDFollower with default parameter without providing \n"
        + "arguments on the command line. Otherwise, you need to provide exactly 7 arguments:\n"
        + " 1. power: this is an integer number between 0 and 100. Default 75\n"
        + " 2. maxDelta: this is an integer providing the maximum correction value (0-100), default 75\n"
        + " 3. Proportional correction constant: this is a double, default 0.05\n"
        + " 4. Derivative correction constant: this is a double, default 1.6\n"
        + " 5. Integral correction constant: this is a double, default 0.0001\n"
        + " 6. Frequence of updates: this is an integer, default 30 (ms)\n"
        + " 7. Cut-off IR value: this is the value under which we define black. Default 40.\n"

        self.cut_off_ir = 40
        self.PWR = 50
        self.freq = 35
        self.max_delta = self.PWR

        self.Kp = 0.050
        self.Kd = 1.6
        self.Ki = 0.0001

        self.cur_error = 2000
        self.prev_error = 2000

    def set_cut_off_ir(self, cut_off_ir):
        self.cut_off_ir = cut_off_ir

    def set_PWR(self, pwr):
        self.PWR = pwr

    def set_freq(self, freq):
        self.freq = freq

    def set_max_delta(self, max_delta):
        self.max_delta = max_delta

    def set_Kp(self, kp):
        self.Kp = kp

    def set_Kd(self, kd):
        self.Kd = kd

    def set_Ki(self, ki):
        self.Ki = ki

    def cut_ir(self, ir_value):
        """

        :param ir_value:
        :return:
        """
        if ir_value < self.cur_error:
            return 0
        else:
            return ir_value

    def compute_error(self, ir_left, ir_middle, ir_right, previous):
        if (ir_left + ir_right + ir_middle) == 0:
            return previous
        else:
            return (ir_middle * 2000 + ir_right * 4000) / (ir_left + ir_middle + ir_right)

    def navigate(self, robot):
        try:
            sys.stdout.write("Starting PID follower\n")
            time_now = time.time()
            old_time = 0
            proportional = 0
            integral = 0
            derivative = 0
            correction = 0

            while True:
                time_now = time.time()

                if (time_now - old_time) > self.freq:

                    left_ir = self.cut_ir(robot.get_ir(2))
                    middle_ir = self.cut_ir(robot.get_ir(1))
                    right_ir = self.cut_ir(robot.get_ir(0))

                    if left_ir == 0 and middle_ir == 0 and right_ir == 0:
                        self.cur_error = self.prev_error
                    else:
                        self.cur_error = self.compute_error(left_ir, middle_ir, right_ir, self.prev_error)

                proportional = self.cur_error - 2000
                if proportional == 0:
                    integral = 0
                else:
                    integral = proportional
                derivative = proportional - (self.prev_error - 2000)
                self.prev_error = self.cur_error
                correction = math.floor(self.Kp * proportional + self.Ki * integral + self.Kd * derivative)
                delta = correction

                if delta > self.max_delta:
                    delta = self.max_delta
                elif delta < -self.max_delta:
                    delta = -self.max_delta

                print("IR: " + left_ir + " " + middle_ir + " " + right_ir)
                print("Delta: " + delta)

                if delta < 0:
                    robot.set_motors(2.55 * self.PWR + delta, 2.55 * -self.PWR)
                else
                    robot.set_motors(2.55 * self.PWR, -self.PWR - delta * 2.55)
                old_time = time_now

            time.sleep(10)

        except Exception as error:
            sys.stdout.write("Error in PID follower: {}\n".format(error))

    def main(self, argv=None):
        try:
            if argv == None:  # in python first argument is always filename
                # No command line parameters provided
                self.set_PWR(50)
                self.set_max_delta(50)

                self.set_Kp(0.015)
                self.set_Kd(0)
                self.set_Ki(0)

                self.set_freq(50)
                self.set_cut_off_ir(50)

                self.navigate()

            elif len(argv) == 7:
                # the order is: power, maxDelta, Kp, Kd, Ki, freq, cutoffIR
                try:
                    self.set_PWR(argv[1])
                    self.set_max_delta(argv[2])

                    self.set_Kp(argv[3])
                    self.set_Kd(argv[4])
                    self.set_Ki(argv[5])

                    self.set_freq(argv[6])
                    self.set_cut_off_ir(argv[7])
                except Exception as e:
                    sys.stdout.write("Error parsing command line parameters! The correct syntax is: ")
                    sys.stdout.write("Exception caught is: {}\n".format(e))

                self.navigate()

            else:
                sys.stdout.write("Error parsing command line parameters! The correct syntax is: ")






