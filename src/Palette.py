def generatePalette(packet):

    # Check packet validity - all entries should have 3 values
    for i, c in enumerate(packet):

        if type(c) == str:
            # determine if string is in the colormap dictionary
            if not c in COLOR_MAP.keys():
                raise ValueError("Color shortcut wasn't available!")
            packet[i] = COLOR_MAP[c]

        elif type(c) == int:
            
            if int(c) > 16**6:
                raise ValueError("Hexadecimal color entry was out of range");


            r = (0xFF0000 & c) >> 16
            g = (0x00FF00 & c) >> 8
            b = (0x0000FF & c) >> 0

            packet[i] = (r, g, b)

        if len(packet[i]) != 3:
            raise ValueError("Color packet malformed!")

    paletteIndices = [int(i * ((1024 - 1) / (len(packet) - 1))) for i in range(len(packet))]

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

    channels = [None for x in range(3)]
    
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

COLOR_MAP = {
    "black":    (0,   0,   0  ),
    "red":      (255, 0,   0  ),
    "orange":   (255, 165, 0  ),
    "yellow":   (255, 255, 0  ),
    "green":    (0,   128, 0  ),
    "blue":     (0,   0,   255),
    "purple":   (75,  0,   130),
    "indigo":   (238, 130, 238),
}

DEFAULT_PALETTE = generatePalette([
    (0, 0, 0),
    (0, 0, 0)
])