from rpi_ws281x import *
import math
from . import config as cfg

class LightStrip():
    """ 
    A convenient wrapper class for the NeoPixel LED strip object. Provides
    additional functionality and the wonderful conveniences of working in 
    Python.

    author: Spencer Elkington
    date:   August 2020
    email:  spelkington@gmail.com
    """


    def __init__ (self, numPixels,
                  gpio_pin      = cfg.LED_GPIO_PIN,
                  freq_hz       = cfg.LED_FREQ_HZ,
                  dma           = cfg.LED_DMA,
                  brightness    = cfg.LED_BRIGHTNESS,
                  invert_logic  = cfg.LED_INV_LOGIC,
                  channel       = cfg.LED_CHANNEL):
        """
        Creates a new LightStrip object to represent an LED strip
        attached to the Pi.

        :param numPixels:    An integer value representing the number of pixels attached to
                            the LED strip.
        :param freq_hz:      The frequency of the lights on the strip. Default is 800kHz,
                            which is the most common value.
        :param dma:          DMA. Not really sure what this is, but 10 sure does seem to work.
        :param brightness:   The max brightness value for the LEDs on the strip. Default is 255.
        :param invert_logic: Set to true if a logic inverter is used between the Pi and the data
                            wire of the LED lights. Defaults to false.
        :param channel:      Channel for the LED lights. Defaults to 0.

        """
        
        # Instantiate the light strip using the given parameters
        self.strip = Adafruit_NeoPixel(
                                        numPixels,
                                        gpio_pin,
                                        freq_hz,
                                        dma,
                                        invert_logic,
                                        brightness,
                                        channel
                                      )

        # Save the length of the strip internally
        self.length = numPixels

        # Set everything we need for the internals of the light.
        self.__setup()

        # Allocate the memory for the strip.
        self.strip.begin()

        return


    def setChannelFunction(self, function, channel):
        """
        Sets the channel function for the given channel.

        :param function: A function in the form of func(int) = int[]
        :channel: A valid channel to load the function into.
        """

        # Before loading, attempt to run the function with a single
        # integer input, and then index the output. Throw an exception if
        # this operation was not possible.
        try:
            output = function(10)
            output[0]
        except Exception as e:
            print(e)
            raise TypeError("Channel function was not accepted. Channel functions must take one integer as a parameter and output an integer array.")

        self.channelFunctions[channel] = function

        return

    def setPalette(self, palette):
        """
        Takes in a 256-length tuple of RGB tuples and sets it as the palette for LightStrip
        palette steps.
        """

        if len(palette) != 256 or len(palette[1]) != 3:
            raise ValueError("Palette was malformed!")

        self.palette = palette

        return

    def setStepMode(self, mode):
        """
        Shift the current step mode between RGB and Palette mode.
        """

        if not mode in [self.MODE_RGB,
                        self.MODE_PALETTE]:
            raise ValueError("Mode was not a valid step mode")

        self.__CURRENT_MODE = mode

        return

    def __setup (self):
        """
        Sets up the LightStrip with self values and default channel functions for visualization.
        """

        # Set up enumerations for channel values
        self.CH_RED   = 0
        self.CH_GREEN = 1
        self.CH_BLUE  = 2
        self.CH_BRIGHTNESS = 3
        self.CH_PALETTE    = 4
        self.NUM_CHANNELS  = 5
        
        # Set up enumerations for modes
        self.MODE_RGB = 10
        self.MODE_PALETTE = 11

        # Begin the strip in RGB mode.
        self.setStepMode(self.MODE_RGB)

        # Set the state of the strip to 0.
        self.state = 0

        # Loads the default functions into each of the 3 color channels.
        self.channelFunctions = [None for _ in range(self.NUM_CHANNELS)]

        # Set the default RGB channel functions to slow-pulsing blue light
        self.setChannelFunction(self.__getConstantChannelFunction(), self.CH_RED)
        self.setChannelFunction(self.__getConstantChannelFunction(), self.CH_GREEN)
        self.setChannelFunction(self.__getPulseChannelFunction(),    self.CH_BLUE)

        # Set the default brightness and pulse channel functions to 
        self.setChannelFunction(self.__getConstantChannelFunction(), self.CH_BRIGHTNESS)
        self.setChannelFunction(self.__getPulseChannelFunction(),    self.CH_PALETTE)     

        return


    def step(self):

        self.state += 1
        
        if   self.__CURRENT_MODE == self.MODE_RGB:
            self.__stepRGB()
        elif self.__CURRENT_MODE == self.MODE_PALETTE:
            self.__stepPalette()
        else:
            raise ValueError("The current LightStrip mode is invalid!")

    def __stepRGB(self):

        # Run each color function and store the resulting array
        channels = [self.channelFunctions[i](self.state) for i in range(3)]
        count = min([len(s) for s in channels])

        for i in range(count):
            color = [channels[c][i] for c in range(3)]
            self[i] = color

        return

    def __stepPalette(self):

        values = self.channelFunctions[self.CH_PALETTE](self.state)
        count = min(len(self), len(values))

        for i in range(count):

            paletteIndex = int(max(0, min(255, values[i])))
                
            color = self.palette[paletteIndex]
            self[i] = color

        return

    def __getConstantChannelFunction (self):
        """
        Creates a null color function with all channel indices set to 0.
        """

        # Create a new zero-brightness color function
        def colorFunc(t):
            return [10 for i in range(len(self))]

        return colorFunc
        
    def __getPulseChannelFunction (self):
        """
        Creates a default color function where the channel slow-pulses as a sin wave
        """
        
        # Create a new function that will set every value to the value of a sin function
        def colorFunc(t):
            value = 128 * math.sin(t / 50) + 96
            return [value for i in range(len(self))]

        return colorFunc

    def __len__ (self):
        """
        Retrieves the length of the LightStrip in pixels.
        """
        return self.length


    def show (self):
        """
        Pushes display changes to the physical LED strip.
        """
        self.strip.show()
        return


    def __getNEOColorTuple(self, color):
        """
        Converts a NeoPixel Color object (stored as a 32-bit integer) into
        a tuple of RGB values.

        :param color:   A NeoPixel color object (32-bit integer)
        :return:        A 3-number tuple with the (R, G, B) values of the
                        input color
        """

        # Because NeoPixel stores their color values as a single integer, we
        # need to bitshift in order to get them out. These operations:
        #   First, mask the bits that we don't need to 0
        #   Second, bitshift the number until the color value is in the LSBs
        r = (color & 0xff0000) >> 16
        g = (color & 0x00ff00) >> 8
        b = (color & 0x000044) >> 0

        return (r, g, b)


    def __Color(self, colorTuple):
        """
        Converts an RGB tuple to a NeoPixel color object. Clamps any values outside of [0, 255]
        into range.

        :param colorTuple:  An (R, G, B) tuple with any values.
        :return:            The valid NeoPixel color object representing the input tuple.
        """

        # To sanitize the input color, we use the max-min method to clamp numbers between
        # values of 0 and 255, inclusive.
        return Color(
                int(max(0, min(255, colorTuple[0]))),
                int(max(0, min(255, colorTuple[1]))),
                int(max(0, min(255, colorTuple[2])))
               )


    def fill(self, color):
        """
        Fills the entire strip with a single color.

        :param color:   An (R, G, B) color tuple.
        """
        color = self.__Color(color)
        for i in range(len(self)):
            self.strip.setPixelColor(i, color)

        return


    def clear(self):
        """
        Clears the entire strip by filling all pixels with (0, 0, 0)
        """

        self.fill((0, 0, 0))
        return


    def __getitem__ (self, key):
        """
        Retrieves an color, or set of colors, from the data of the LightStrip.

        :param key: the specified index or indices to be retrieved.
        :return: a color or set of colors from the LightStrip.
        """

        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return [self[i] for i in range(start, stop, step)]

        elif isinstance(key, int):
            return self.__getNEOColorTuple(self.strip.getPixelColor(key))

        elif isinstance(key, tuple):
            raise NotImplementedError('Tuple as index')

        else:
            raise TypeError('Invalid Argument Type: {}'.format(type(key)))

        return


    def __setitem__ (self, key, color):
        """
        Sets the value at an index or a range of indices to an (R, G, B) color tuple.

        :param key: an index or range of indices to set
        :param color:   an (R, G, B) color value
        """

        color = self.__Color(color)

        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            for i in range(start, stop, step):
                self.strip.setPixelColor(i, color)

        elif isinstance(key, int):
            self.strip.setPixelColor(key, color)

        elif isinstance(key, tuple):
            raise NotImplementedError('Tuple as index')

        else:
            raise TypeError('Invalid Argument Type: {}'.format(type(key)))

        return

    def setBrightness(self, val):
        self.strip.setBrightness(val)
        return
