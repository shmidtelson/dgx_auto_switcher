#!/usr/bin/env python3.7
import re
import os
import subprocess
import time

class ChangeAudioInput():
    prevStatus = None
    channelNumber = None
    is_connected = None

    def __init__(self):
        self.get_channel_number()
        while True:
            self.is_connected = self.get_status()
            if self.is_connected != self.prevStatus or self.prevStatus is None:
                self.change_headphones()
                self.prevStatus = self.is_connected
            time.sleep(1)

    def get_channel_number(self):
        pattern = "(\d) \[DGX"
        devices = os.popen('cat /proc/asound/cards').read()
        search = re.findall(pattern, devices)
        assert 1 == len(search)
        self.channelNumber = re.findall(pattern, devices)[0]

    def get_status(self):
        card_bytes = os.popen(f'cat /proc/asound/card{self.channelNumber}/oxygen').read()
        search = re.findall("a0: (.*)", card_bytes)
        splitted = search[0].split()[6]
        if splitted in ['68', 'e8']:
            return True
        if splitted in ['78', 'f8']:
            return False

    def change_headphones(self):
        status = '1' if self.is_connected else '0'
        os.popen(f"amixer -c {self.channelNumber} cset name='Analog Output Playback Enum' {status}")

if __name__ == '__main__':
    ChangeAudioInput()


