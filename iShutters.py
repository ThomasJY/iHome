#!/usr/bin/env python3
########################################################################
# Filename    : iShutters.py
# Description : 
# Version     : 0.1
# Author      : Yu, Bo
# Creation    : 2021/03/16
########################################################################
# Log:
# 2021/04/08 [feat] keyboard control will change the state as well. 
# 2021/04/05 [feat] Finished basic keyboard control function.
# 2021/04/01 [prep] Trying to add keyboard control without blocking the automation. The keyboard lib 
# requires root therefore the script has to run under su. Re-installed pytz and suntime libs 
# under the su as needed.
# 2021/03/16 [feat] Finished the basic function.
########################################################################
# TO DO:
# 2. Implement WiFi module to realize IoT.
# 1. (Optional) add fucntion(s) to allow the user to change the shutter state from 0 to 100, matching 
# the cycle number of the stepping motor.
########################################################################

import SteppingMotor as sm
import time
import pytz
from datetime import date, timedelta, datetime
from suntime import Sun
import keyboard

sun = Sun(34.004230, -117.369540)

state = False   # closed
state = True   # opened


class Shutters:
    def __init__(self, state):
        self.today = date.today()
        self.sr = sun.get_local_sunrise_time()
        self.ss = sun.get_local_sunset_time()
        self.state = state

    def time_update(self):
        self.today = date.today()
        print("Today is", self.today)
        self.sr = sun.get_local_sunrise_time()
        self.ss = sun.get_local_sunset_time() + timedelta(days=1)
        print("Sunrise at", self.sr.strftime('%H:%M'))
        print("Sunset at", self.ss.strftime('%H:%M'))

    def close(self):
        sm.moveSteps(0,3,2048)
        self.state = False
    
    def open(self):
        sm.moveSteps(1,3,2048)
        self.state = True

    def state_update(self, now):
        # if now < self.sr or now > self.ss:
        #     print(now, "Night")
        #     if self.state:
        #         print("Now closing the shutters.")
        #         sm.close()
        #         self.state = False
        # else:
        #     print(now.strftime('%H:%M'), "Daytime")
        #     if not self.state:
        #         print("Now opening the shutters")
        #         sm.open()
        #         self.state = True
        # state = "opened" if self.state else "closed"
        # print("Shutters are", state)

        if self.sr < now < self.sr + timedelta(minutes=2):
            if not self.state:
                print("Sunrise! Now opening the shutters")
                self.open()
        elif self.ss < now < self.ss + timedelta(minutes=2):
            if self.state:
                print("Sunset! Now closing the shutters.")
                self.close()
        print(now.strftime('%H:%M'))
        state = "opened" if self.state else "closed"
        print("Shutters are", state)


def automation():
    yesterday = date.today() - timedelta(days=1)
    while True:
        today = date.today()
        if today != yesterday:              # update the date per day
            my_shutters.time_update()
            yesterday = today

        now = datetime.now(pytz.utc).astimezone(pytz.timezone('America/Los_Angeles'))
        my_shutters.state_update(now)       # update the shutters' state based on current time
        time.sleep(60)                      # check per min

        
if __name__ == "__main__":
    # init the stepper motor
    sm.setup()

    # init the shutters and keyboard
    my_shutters = Shutters(False)
    keyboard.add_hotkey("up arrow", lambda: my_shutters.open())
    keyboard.add_hotkey("down arrow", lambda: my_shutters.close())

    try:
        automation()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        sm.destroy()

    
    
            
        
        


