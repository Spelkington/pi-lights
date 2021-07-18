FPS             = 60
""" Frames per second for the program. """

PROJECT_NAME    = "spelkington-vis"
""" Project name for configuration """

PROJECT_VERSION = 1.0
""" Project version. """

AUDIO_INPUT_DEVICE_INDEX = 0

AUDIO_MIN_FREQ      = 200
""" Minimum frequency bound for audio analysis """

AUDIO_MAX_FREQ      = 12000
""" Maximum frequency bound for audio analysis """

AUDIO_MIN_VOL       = 1e-7
""" Maximum volume bound for audio analysis """

AUDIO_SAMPLE_RATE   = 44100
""" Sample rate for audio. """

AUDIO_FFT_BIN_N     = 24
""" Bins for the Fast-Fourier Transform categorization """

AUDIO_FRAME_HIST    = 5
""" Audio frames stored for analysis. """

# LED Strip Configuration

LED_COUNT       = 357
""" Number of LEDs in the light strip. """

LED_GPIO_PIN    = 18
""" Connected GPIO pin for the strip. """

LED_FREQ_HZ     = 800000
""" LED Frequency - usually 800kHz """

LED_DMA         = 10
""" DMA for the strip """

LED_BRIGHTNESS  = 255
""" Brightness value for the LEDs. """

LED_INV_LOGIC   = False
""" Whether a logic inverter is connected to the data pin for the strip. """

LED_CHANNEL     = 0
""" Channel for the LEDs. """
