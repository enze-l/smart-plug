import ntptime
import time


def adjust_own_time():
    print("getting time ...")
    ntptime.settime()
    print("current utc time is " + str(time.localtime()))
