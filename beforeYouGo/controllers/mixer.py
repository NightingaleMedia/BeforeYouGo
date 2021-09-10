import pygame
import time
import json
import random
import os
# Opening JSON file
f = open('../data/manifest.json')
DIRECTORY = json.load(f)


DIAL_KEYS = {
    10: "../data/DTMF/DTMF-0.wav",
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

        self.main_channel = self.mixer.Channel(0)
        self.main_channel.set_volume(0.2)
    
        self.voice_channel = self.mixer.Channel(1)
        self.voice_channel.set_volume(0.9)
        
        self.dial_channel = self.mixer.Channel(2)
        self.dial_channel.set_volume(0.2)
        self.DIAL_TONE = None;
        self.audio_list = {}
        self.key_list = {}
        self.current_file = None
        self.playing = False
        self._loading = False

    def init(self):
        print('Initializing mixer...')
        self.DIAL_TONE = self.mixer.Sound('../data/DTMF/dial_tone.wav')
        for file in DIAL_KEYS.keys():
            self.key_list[file] = self.mixer.Sound(DIAL_KEYS[file])
            print("loading dial tone: %s" % file)
        # for item in DIRECTORY:
        #     self.audio_list[item] = []
        #     for file in DIRECTORY[item]['files']:
        #         if(file == '.DS_Store'):
        #             print('skip')
        #         else:
        #             path = str('../data/' + DIRECTORY[item]['name'] + "/" + file)
        #             print('loading %s ...' % path)
        #             audio_file = self.mixer.Sound(path)
        #             self.audio_list[item].append(audio_file)


    def get_loading(self):
        return self._loading;

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
            self.main_channel.play(self.DIAL_TONE, -1, fade_ms=100)

    def dial(self, number):
        if(not self.playing):
            self.dial_channel.play(self.key_list[number])
            time.sleep(0.25)
            self.dial_channel.stop()
    
    def load_file(self, path_to_file):
            print('loading file: %s' % path_to_file)
            self._loading = True;
            self.current_file = self.mixer.Sound(path_to_file)
            self._loading = False;
             
    def play_file(self, number, callback = None):
        # get a random file from the list of files
        category = number
        if(category == 10):
            category = "0"
        print('category: %s' % category)
        folderName = DIRECTORY[str(category)]['name'] 
        print("folder name: "+ folderName)

        folderFileArray = DIRECTORY[str(category)]['files']

        randomNumber = random.randint(0, len(folderFileArray))

        winnerFile =  '../data/' + folderName + '/' + str(folderFileArray[randomNumber])
        
        print("winner: " + winnerFile)

        self.load_file(winnerFile)

        while(self.get_loading()):
            print('loading...')
            time.sleep(0.2)

        # If something else is playing, stop it
        if(self.main_channel.get_busy()):
            self.stop_main()
        
        # start the playing loop

        self.playing = True;
        self.voice_channel.play(self.current_file)   
        while(self.get_voice_playing()):
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
    def kill(self):
        self.stop();
        self.mixer.quit();