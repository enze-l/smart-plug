import ntptime


def adjust_own_time():
    print("getting time ...")
    succeeded = False
    while not succeeded:
        try:
            ntptime.settime()
            succeeded = True
        except OSError:
            print("NTP server couldn't be reached. Trying again ...")
    print("current time has been set")
