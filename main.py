import re
import os
import subprocess


class ChangeAudioInput():
    headphones_connected = None
    channelNumber = 1

    def __init__(self):
        while True:
            boolean = self.getStatus()
            print(boolean)
            if boolean != self.headphones_connected:
                self.getChannelNumber()
                self.changeHeadphones()
                self.headphones_connected = boolean

    def getChannelNumber(self):
        pattern = "(\d) \[DGX"
        devices = os.popen('cat /proc/asound/cards').read()
        search = re.findall(pattern, devices)
        assert 1 == len(search)
        self.channelNumber = re.findall(pattern, devices)[0]

    def getStatus(self):
        bytes = os.popen('cat /proc/asound/card0/oxygen').read()
        search = re.findall("a0: (.*)", bytes)
        splited = search[0].split()[6]
        print(splited)
        if splited in ['68', 'e8']:
            return True
        if splited in ['78', 'f8']:
            return False

    def changeHeadphones(self):
        status = '0' if self.headphones_connected else '1'
        os.system(f"amixer -c {self.channelNumber} cset name='Analog Output Playback Enum' {status}")
        subprocess.call(['notify-send', 'Наушники подключены'])

a = ChangeAudioInput()

