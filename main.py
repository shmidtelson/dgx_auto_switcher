#!/usr/bin/env python3.7
import re
import os
import subprocess


class ChangeAudioInput():
    prevStatus = None
    channelNumber = None
    is_connected = None
    def __init__(self):
        self.getChannelNumber()
        while True:
            self.is_connected = self.getStatus()
            if self.is_connected != self.prevStatus or self.prevStatus == None:
                self.changeHeadphones()
                self.show_notify()
                self.prevStatus = self.is_connected

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
        status = '1' if self.is_connected else '0'
        os.popen(f"amixer -c {self.channelNumber} cset name='Analog Output Playback Enum' {status}")

    def show_notify(self):
        if self.is_connected:
            subprocess.call(['notify-send', 'Headphones connected'])
        else:
            subprocess.call(['notify-send', 'Headphones disconnected'])

if __name__ == '__main__':
    ChangeAudioInput()

