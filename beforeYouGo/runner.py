import time
from datetime import datetime
from gpio_config  import keypad
from controllers import mixer, lights
from tabulate import tabulate
from threading import Thread


def get_date():
        dateTimeObj = datetime.now()
        date =  str(dateTimeObj.month) + '/' + str(dateTimeObj.day) + "/" + str(dateTimeObj.year)
        year = str(dateTimeObj.hour) + ':' + str(dateTimeObj.minute) + ':'+ str(dateTimeObj.second) + '.' + str(dateTimeObj.microsecond)
        return dict({"date": date, "year": year})

class State:

# while phone is up lights on
# while phone is playing lights mid white
# while audio is playing, input is disabled
    def __init__(self):
        self.input = None
        self.listening = False

        self.mixer = mixer.Mixer()
        self.lights = lights.Lights()

        self.mixer.init()
        self.lights.init()

    def handlePickup(self):
        if(not self.listening):
            self.logState('handle pickup')
            self.listening = True
            self.mixer.handle_pickup()
            self.lights.fillWhite()
            print('--------\nPICKUP\n--------')

    def handleHangup(self):  
        if(self.listening):
            self.logState('handle hangup')
            self.listening = False
            self.input = None
            print('--------\nHANGUP\n--------')
            self.mixer.stop();
            self.lights.init()

    def setInput(self, value):
        if(not self.mixer.get_voice_playing()):
            self.input = value
        self.mixer.dial(value)
        print('setting input: %s' % self.input)


    def handle_play_state(self):        
        self.listening = False;
         # if something if audio is not playing
        if(not self.mixer.get_voice_playing()):
            self.logState('handle play state')
            self.lights.fadeWhite(10)
            self.mixer.play_file(self.input, self.handlePickup)
        else:
            print('Audio is playing...')
            
    # executed when input is "#" 
    def handleCue(self):
        self.logState('handle cue')
        if(range(10).__contains__(self.input) and self.listening):
            print('trying to play the audio %s...' % self.input)
            self.handle_play_state()
        else:
            print('no audio selected or it is not listening \n--------')

    def handleInput(self, input): 
        DIRECTORY = {
            11 : self.handleCue,
            12 : self.handlePickup,
            13 : self.handleHangup,
        }

        if(input and range(10).__contains__(input)) :
            if(self.listening):
                self.setInput(input)
            else:
                print('Not listening, please pickup the phone...')
        else:
            DIRECTORY[input]()
       
        
    def logState(self, from_meth = "unknown"):
        date = get_date()
        data = [["From",      from_meth,           ""],
                ["Input",     self.input,          date['date']],
                ["Listening", self.listening,      date['year']],
                ["Mixer Ply", self.mixer.playing,   ""],
                ["__________",'__________',         "__________"]] 
        return print ("\n\n" + tabulate(data, headers=["State", "Value", "Time"]) + "\n\n")
        
    



# polling
def __main__():
    kp = keypad.Keypad();

    state = State()
    # main game loop
    while True:
        # game logic here based on the state object
        if(kp.isTriggered()): # basically if the phone is up
            state.handlePickup()
            result = kp.getKey()
            if(result):
                print(result)
                try:
                    state.handleInput(int(result))
                except:
                    print('an error occured...' )
            
        else:
            state.handleHangup()
        time.sleep(0.02)

__main__()
