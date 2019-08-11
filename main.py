#!/usr/bin/env python3.7
import re
import os
import subprocess


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
                self.show_notify()
                self.prevStatus = self.is_connected

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

    def show_notify(self):
        msg = 'Headphones connected' if self.is_connected else'Headphones disconnected'
        self._notify(msg)

    @staticmethod
    def _notify(text):
        subprocess.call(['notify-send', text])

if __name__ == '__main__':
    ChangeAudioInput()

