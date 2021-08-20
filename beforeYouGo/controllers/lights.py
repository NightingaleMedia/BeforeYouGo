import time
from rpi_ws281x import *
import argparse
from threading import Thread

def threaded(fn):
    def wrapper(*args, **kwargs):
        print('theading the func...')
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


class Lights():
    def __init__(self):
        print('Initializing lights...')
        # LED strip configuration:
        LED_COUNT      = 144      # Number of LED pixels.
        #LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
        LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self._BREATH_MAX = 255;
        self._BREATH_MIN = 1
        self._breathing = False;
        self._fade_time = 0.2

    def init(self):
        self._breathing = True;
        self.breathe();

    # """Wipe color across display a pixel at a time."""
    def colorWipe(self, color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def show(self, brightness = 255):
        self.strip.setBrightness(brightness)
        self.strip.show()

    @threaded
    def breathe(self):
        self._breathing = True;
        for i in range(self.strip.numPixels()):
           self.strip.setPixelColor(i, Color(255, 255, 255, 255))
        i = self._BREATH_MIN
        direction = "up"
        running = True
        while running:
            # if it is below 255 go up
            if(i < self._BREATH_MAX and direction == "up"):
                i = i * 1.03
               
            # if it at 255 go down
            if(i > self._BREATH_MAX or direction == "down"):
                direction = "down"
                if(i > 255):
                    i = 255;
                i = int(i)
                i = i / 1.1
              
            if(i < self._BREATH_MIN and direction == "down"):
                direction = "up"
            self.show(int(i))
            time.sleep(0.02)
            if(not self._breathing):
                running = False
    @threaded
    def fadeWhite(self, desired_brightness = 255, fade_time = 0.1):
        self.clear()
        initial_brightness = self.strip.getBrightness();
        self.show(initial_brightness)
        if(initial_brightness > desired_brightness):
            # Fade Down
            print('fade down')
            while desired_brightness <= self.strip.getBrightness():
                initial_brightness -= 3;
                self.show(initial_brightness)
                time.sleep(fade_time)
        
        if(initial_brightness < desired_brightness):
            #Fade Up
            print('fade up')
            while desired_brightness >= self.strip.getBrightness():
                initial_brightness += 3;
                self.show(initial_brightness)
                time.sleep(fade_time)

    def fillWhite(self, brightness = 255):
        self.clear();
        print('fill white')
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(255,255,255,255))
        self.show(brightness)

    def clear(self):
        self._breathing = False;
    # Main program logic follows:

