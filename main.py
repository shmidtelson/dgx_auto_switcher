#!/usr/bin/env python3.7
import re
import os
import subprocess


class ChangeAudioInput():
    headphones_connected = None
    channelNumber = None

    def __init__(self):
        self.getChannelNumber()
        while True:
            is_connected = self.getStatus()
            if is_connected != self.headphones_connected:
                self.changeHeadphones()
                self.show_notify()
                self.headphones_connected = is_connected

    def getChannelNumber(self):
        pattern = "(\d) \[DGX"
        devices = os.popen('cat /proc/asound/cards').read()
        search = re.findall(pattern, devices)
        assert 1 == len(search)
        self.channelNumber = re.findall(pattern, devices)[0]

    def getStatus(self):
        bytes = os.popen(f'cat /proc/asound/card{self.channelNumber}/oxygen').read()
        search = re.findall("a0: (.*)", bytes)
        splited = search[0].split()[6]
        if splited in ['68', 'e8']:
            return True
        if splited in ['78', 'f8']:
            return False

    def changeHeadphones(self):
        status = '0' if self.headphones_connected else '1'
        os.popen(f"amixer -c {self.channelNumber} cset name='Analog Output Playback Enum' {status}")

    def show_notify(self):
        if not self.headphones_connected:
            subprocess.call(['notify-send', 'Headphones connected'])
        else:
            subprocess.call(['notify-send', 'Headphones disconnected'])

if __name__ == '__main__':
    ChangeAudioInput()

