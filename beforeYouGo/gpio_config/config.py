import RPi.GPIO as GPIO



#inputs are reversed from o1 - o4
    # 1 : 0001
    # 2 : 0010
    # 3 : 0011
    # 4 : 0100
    # 5 : 0101
    # 6 : 0110
    # 7 : 0111
    # 8 : 1000
    # 9 : 1001
    # 0 : 1010
    # # : 1100

obj = { 
    "1000": "1",
    "0100": "2",
    "1100": "3",
    "0010": "4",
    "1010": "5",
    "0110": "6",
    "1110": "7",
    "0001": "8",
    "1001": "9",
    "0101": "0",
    #interpret the star as 11
    "0011": "11",
    # * 12 is 1101
    # "1101" : "12",
    # C is initiate
    "1111" : "12",
    # D might be hangup
    "0000" : "13"
}

# when the stq is on then query what button is being pressed

class Inputs():
    def __init__(self, inputs, trigger_pin):
        self.input_array = inputs
        self.TRIGGER = trigger_pin

        GPIO.setmode(GPIO.BOARD)
        for item in self.input_array:
            print('setting up input %d' % item)
            GPIO.setup(item, GPIO.IN)
        # ======= TRIGGER PIN =======
        #   STQ = 21 = 40
        GPIO.setup(self.TRIGGER, GPIO.IN)
        print('Ready to go boss....')
       # GPIO.add_event_detect(self.TRIGGER, GPIO.RISING)

    #basically a poll
    def get_number(self):
        if(GPIO.input(self.TRIGGER)):
            #wait for release
            GPIO.wait_for_edge(self.TRIGGER, GPIO.FALLING)
            init_array = []
            for item in self.input_array:
                if GPIO.input(item):
                    init_array.append("1")
                else:
                    init_array.append("0")

            result = "".join(init_array)
            try:
                print("number pressed: %s \n" % obj[result] )
                return int(obj[result])
            except:
                print("invalid entry: %s" % result)
                return False
    
               