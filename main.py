#!/usr/bin/env python3
import re
import os
import time


class ChangeAudioInput():
    HEADPHONES_FRONT_DISCONNECTED = '0'
    HEADPHONES_FRONT_CONNECTED = '1'
    HEADPHONES_MULTICHANNEL = '2'

    pathToDGXCard = '/proc/asound/DGX'
    channelNumber = None
    currentHeadphonesStatus = None

    def start(self):
        self.loop()

    def loop(self):
        # We wait symlink
        while not os.path.islink(self.pathToDGXCard):
            time.sleep(2)

        self.getChannelNumber()

        time.sleep(20)

        while True:
            status = self.getStatus()

            if self.currentHeadphonesStatus is None:
                self.changeHeadphones(status)

            if self.currentHeadphonesStatus != status:
                self.changeHeadphones(status)

            time.sleep(1)

    def getChannelNumber(self):
        self.channelNumber = re.findall("card(\d+)", os.popen(f"ls -ld {self.pathToDGXCard}").read())[0]

    def getStatus(self):
        cardBytes = os.popen(f'cat /proc/asound/card{self.channelNumber}/oxygen').read()
        search = re.findall("a0: (.*)", cardBytes)
        splitted = search[0].split()[6]

        if splitted in ['68', 'e8']:
            return self.HEADPHONES_FRONT_CONNECTED

        if splitted in ['78', 'f8']:
            return self.HEADPHONES_FRONT_DISCONNECTED

        return self.HEADPHONES_MULTICHANNEL

    def changeHeadphones(self, status):
        os.popen(f"amixer -c {self.channelNumber} cset name='Analog Output Playback Enum' {status}")

        self.currentHeadphonesStatus = status


if __name__ == '__main__':
    try:
        ChangeAudioInput().start()
    except KeyboardInterrupt:
        print('Exited by user')
