class Palette:

    def __init__(self, packet, length = 256):
        self.__colorArray = generatePalette(packet, length)

    def __getitem__ (self, key):
        """
        Retrieves a colorf colors, from the data of the LightStrip.
        """

        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return [self[i] for i in range(start, stop, step)]

        elif isinstance(key, int):
            return self.__colorArray[key]

        elif isinstance(key, tuple):
            raise NotImplementedError('Tuple as index')

        else:
            raise TypeError('Invalid Argument Type: {}'.format(type(key)))

    def __len__(self):
        return len(self.__colorArray)

def generatePalette(packet, length):

    # Check packet validity - all entries should have 3 values
    for i, c in enumerate(packet):

        if type(c) == str:
            # determine if string is in the colormap dictionary
            if not c in COLOR_MAP.keys():
                raise ValueError("Color shortcut wasn't available!")
            packet[i] = COLOR_MAP[c]

        elif type(c) == int:
            
            if int(c) > 16**6:
                raise ValueError("Hexadecimal color entry was out of range")

            r = (0xFF0000 & c) >> 16
            g = (0x00FF00 & c) >> 8
            b = (0x0000FF & c) >> 0

            packet[i] = (r, g, b)

        if len(packet[i]) != 3:
            raise ValueError("Color packet malformed!")

    paletteIndices = [int(i * ((length - 1) / (len(packet) - 1))) for i in range(len(packet))]

    result = []
    for i in range(len(packet) - 1):
        leftColor = packet[i]
        rightColor = packet[i + 1]
        numEntries = (paletteIndices[i + 1] -
                     paletteIndices[i])

        interpSet = linInterp(leftColor, rightColor, numEntries)

        for c in interpSet:
            result.append(c)

    result.append((packet[len(packet) - 1]))

    return result

def linInterp(leftColor, rightColor, entries):

    channels = [None, None, None]

    for c in range(3):
        l = leftColor[c]
        r = rightColor[c]
        channels[c] = [l + ((r - l) / entries) * x for x in range(entries)]

    result = []
    for i in range(entries):
        result.append((
            int(channels[0][i]),
            int(channels[1][i]),
            int(channels[2][i])
            )
        )

    return result