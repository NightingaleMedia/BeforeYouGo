import pygame
import time
from threading import Thread
from runner import Logger
def threaded(fn):
    def wrapper(*args, **kwargs):
        print('theading the func...')
        Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

DIRECTORY = {
"DIAL": "../data/dial_tone.wav",
1 : '../data/track1.wav',
2 : '../data/track2.wav',
3 : '../data/track3.wav',
4 : '../data/track4.wav',
5 : '../data/track5.wav',
6 : '../data/track6.wav',
7 : '../data/track7.wav',
8 : '../data/track8.wav',
9 : '../data/track9.wav',
0 : '../data/track9.wav'

}

DIAL_KEYS = {
    0: "../data/DTMF/DTMF-0.wav",
    1: "../data/DTMF/DTMF-1.wav",
    2: "../data/DTMF/DTMF-2.wav",
    3: "../data/DTMF/DTMF-3.wav",
    4: "../data/DTMF/DTMF-4.wav",
    5: "../data/DTMF/DTMF-5.wav",
    6: "../data/DTMF/DTMF-6.wav",
    7: "../data/DTMF/DTMF-7.wav",
    8: "../data/DTMF/DTMF-8.wav",
    9: "../data/DTMF/DTMF-9.wav",
    10: "../data/DTMF/DTMF-0.wav",
    11: "../data/DTMF/DTMF-pound.wav",
}

class Mixer:
    def __init__(self):
        self.mixer = pygame.mixer
        self.mixer.init()

        self.logger = Logger("mixer")
        self.main_channel = self.mixer.Channel(0)
        self.main_channel.set_volume(0.2)

        self.voice_channel = self.mixer.Channel(1)
        self.voice_channel.set_volume(0.5)
        
        self.dial_channel = self.mixer.Channel(2)
        self.dial_channel.set_volume(0.4)
  
        self.audio_list = {}
        self.key_list = {}
        self.currentFile = None
        self.playing = False
     

    def init(self):
        print('Initializing mixer...')
        for file in DIRECTORY.keys():
                self.audio_list[file] = self.mixer.Sound(DIRECTORY[file])
                print("loading: %s" % file)
        for file in DIAL_KEYS.keys():
                self.key_list[file] = self.mixer.Sound(DIAL_KEYS[file])
                print("loading: %s" % file)

    def get_voice_playing(self):
        if(self.voice_channel.get_busy()):
            self.playing = True;
        else:
            self.playing = False
        return(self.playing)
    
    def set_voice_playing(self, value):
        if(value == False and self.voice_channel.get_busy()):
            self.playing = False;
        if(value == True and not self.voice_channel.get_busy()):
            self.playing = True

    def handle_pickup(self):
        if(self.get_voice_playing()):
            return
        else:
            self.main_channel.play(self.audio_list['DIAL'], -1, fade_ms=100)

    def dial(self, number):
        if(not self.playing):
            self.dial_channel.play(self.key_list[number])
            time.sleep(0.25)
            self.dial_channel.stop()

    def play_file(self, number, callback = None):
      
        print('play file... %s' % number)
        self.logger.log('Playing file: %s', number)
        # If something else is playing, stop it
        if(self.main_channel.get_busy()):
            self.stop_main()
        # start the playing loop
        self.playing = True;
        self.voice_channel.play(self.audio_list[number])   
        while(self.get_voice_playing()):
            print('busy playing...')
            time.sleep(1)
        print('callback...')
        self.get_voice_playing()
        time.sleep(0.2)
        callback()
      
    def stop_main(self):
        self.main_channel.stop()
    def stop(self):
        self.main_channel.stop()
        self.voice_channel.stop()
        self.dial_channel.stop()