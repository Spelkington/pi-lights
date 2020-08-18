def generatePalette(packet):

    # Check packet validity - all entries should have 3 values
    for c in packet:
        if len(c) != 3:
            raise ValueError("Color packet malformed!")

    paletteIndices = [int(i * ((256 - 1) / (len(packet) - 1))) for i in range(len(packet))]

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

COLOR_BLACK     = (0,0,0)
COLOR_RED 	= (255, 0, 0)
COLOR_ORANGE 	= (255, 165, 0)
COLOR_YELLOW 	= (255, 255, 0)
COLOR_GREEN   	= (0, 128, 0)
COLOR_BLUE	= (0, 0, 255)
COLOR_PURPLE	= (75, 0, 130)
COLOR_INDIGO	= (238, 130, 238)

TEST = generatePalette((
        (0, 0, 32),
        (0, 0, 64),
        (0, 32, 128),
        (32, 64, 192),
        (64, 96, 220)
))

TEST_TWO = generatePalette((
    (0, 0, 32),
    (32, 0, 64),
    (64, 0, 96),
    (96, 0, 128),
    (32, 32, 160),
    (0, 96, 192)
))

RAINBOW = generatePalette((
    COLOR_BLACK,
    COLOR_RED,
    COLOR_ORANGE,
    COLOR_YELLOW,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_PURPLE,
    COLOR_INDIGO
))

OCEAN = generatePalette((
    (0, 0, 0),
    COLOR_PURPLE,
    COLOR_GREEN,
    (6,66,115),
    (118,182,196),
    (127,205,255),
    (29,162,216),
    (222,243,246)
))

FOREST = generatePalette((
    (0,0,0),
    (60, 30, 10),
    (10, 30, 10),
    (30, 50, 15),
    (50, 80, 50),
    (50, 140, 70)
))
