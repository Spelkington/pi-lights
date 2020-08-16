import numpy as np
import time
import pyaudio
from . import config as cfg

class PiMusic:

    def __init__(self):

        self.pa = pyaudio.PyAudio()

        self.framesPerBuffer = int(cfg.AUDIO_SAMPLE_RATE / cfg.FPS)

        self.stream = self.pa.open(format      = pyaudio.paInt16,
                        channels    = 1,
                        rate        = cfg.AUDIO_SAMPLE_RATE,
                        input       = True,
                        frames_per_buffer = self.framesPerBuffer,
                        input_device_index = cfg.AUDIO_INPUT_DEVICE_INDEX
        )

        self.overflows = 0
        self.prevOvfTime = time.time()

        return

    def printDevices(self):
        print('\n'.join([y['name'] for y in [self.pa.get_device_info_by_index(x)
                                   for x in range(self.pa.get_device_count())]]))
        return

    def update(self):

        try:
            data = np.fromstring(self.stream.read(self.framesPerBuffer,
                                                  exception_on_overflow = False), 
                                 dtype = np.int16
            )

            data = data.astype(np.float32)
            self.stream.read(self.stream.get_read_available(),
                             exception_on_overflow = False
            )

            self.__analyzeAudio(data)
        
        except IOError:
            self.overflows += 1
            if time.time() > self.prevOvfTime + 1:
                self.prevOvfTime = time.time()
                print(f'Audio buffer has overflowed {overflows} times')

        return

    def __analyzeAudio(self, data):

        print(max(data))

        pass

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
        
