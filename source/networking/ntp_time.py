import ntptime
import time
from ..utils.logger import log


def adjust_own_time():
    log("getting time ...")
    ntptime.settime()
    log("current utc time is " + str(time.localtime()))
