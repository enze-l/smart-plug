import ntptime
import time


def adjust_own_time():
    succeeded = False
    while not succeeded:
        try:
            print("getting time ...")
            ntptime.settime()
            succeeded = True
            print("current utc time is " + str(time.localtime()))
        except OSError:
            print("Failed to connect to network server. Trying again in 1 second ...")
            time.sleep(1)

