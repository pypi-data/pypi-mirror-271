all_spinners = {
    "classic": {
        "frames": [
            "   ",
            ".  ",
            ".. ",
            "...",
        ],
        "interval": 1/4,
    },
    "spinner": {
        "frames": ["|", "/", "\u2013", "\\"],
        "interval": 0.5/4,
    },
    "balloon": {
        "frames": [" ", ".", "o", "O", "*", " "],
        "interval": 1.5/6,
    },
    "blinkingHeart": {
        "frames": ["\u2661", "\u2665"],
        "interval": 0.5,
    },
    "blinkingCircle": {
        "frames": ["\u25CB", "\u25CF"],
        "interval": 0.5,
    },
    "blinkingSquare": {
        "frames": ["\u25A0", "\u25A1"],
        "interval": 0.5,
    },
    "loadingCircle": {
        "frames": ["\u25D4", "\u25D1", "\u25D5", "\u25CF"],
        "interval": 1/3,
    },
    "spinningArrow": {
        "frames": [
            "\u2190",
            "\u2196",
            "\u2191",
            "\u2197",
            "\u2192",
            "\u2198",
            "\u2193",
            "\u2199"
        ],
        "interval": 1/8,
    },
    "breathing": {
        "frames": [
            "\u258f",
            "\u258e",
            "\u258d",
            "\u258c",
            "\u258b",
            "\u258a",
            "\u2589",
            "\u2588",
        ],
        "interval": 1.5/16,
    },
    "digit": {
        "frames": [],
        "interval": 1/4,
    },
    "circleDigit": {
        "frames": [],
        "interval": 1/4,
    },
    "arc": {
        "frames": ["\u25DC", "\u25DD", "\u25DE", "\u25DF"],
        "interval": 1/8,
    },
    "triangleCorners": {
        "frames": ["\u25E4", "\u25E5", "\u25E2", "\u25E3"],
        "interval": 1/5,
    },
    "star": {
        "frames": [" ", "\u2729", "\u2730", "\u272D", "\u272E", "\u272F"],
        "interval": 1/6,
    },
    "building": {
        "frames": [" ", "\u2596", "\u2584", "\u2599", "\u2588"],
        "interval": 1/4,
    }
}

for _ in [i for i in reversed(all_spinners["breathing"]["frames"])]:
    all_spinners["breathing"]["frames"].append(_)

# https://en.wikipedia.org/wiki/List_of_Unicode_characters#Enclosed_Alphanumerics
for i in range(8, 28):
    if i <= 9:
        currentChar = bytes("\\u" + "248" + str(i), "utf-8").decode("unicode-escape")
    elif i in range(10, 15+1):
        currentChar = bytes("\\u" + "248" + chr(55 + i), "utf-8").decode("unicode-escape")
    else:
        _char = str(i - 16) if i <= 25 else chr(i + 39)
        currentChar = bytes("\\u" + "249" + _char, "utf-8").decode("unicode-escape")
    all_spinners["digit"]["frames"].append(currentChar)

for i in range(16):
    _char = chr(55+i) if i > 9 else str(i)
    currentChar = bytes("\\u" + "246" + _char, "utf-8").decode("unicode-escape")
    all_spinners["circleDigit"]["frames"].append(currentChar)
    if i == 15:
        for i2 in range(4):
            currentChar = bytes("\\u" + "247" + str(i2), "utf-8").decode("unicode-escape")
            all_spinners["circleDigit"]["frames"].append(currentChar)

def generateBounceSpinner(character: str, walls: tuple = (" ", " ")):
    frames = [
        f"{walls[0]}    {walls[1]}",
        f"{walls[0]}{character}   {walls[1]}",
        f"{walls[0]}{character*2}  {walls[1]}",
        f"{walls[0]} {character*2} {walls[1]}",
        f"{walls[0]}  {character*2}{walls[1]}",
        f"{walls[0]}   {character}{walls[1]}",
        f"{walls[0]}    {walls[1]}",
        f"{walls[0]}   {character}{walls[1]}",
        f"{walls[0]}  {character*2}{walls[1]}",
        f"{walls[0]} {character*2} {walls[1]}",
        f"{walls[0]}{character*2}  {walls[1]}",
        f"{walls[0]}{character}   {walls[1]}",
        f"{walls[0]}    {walls[1]}",
    ]
    return frames

def generateSingleCharacterBounceSpinner(character: str, walls: tuple = ("|", "|")):
    frames = []
    for i in range(7):
        currentFrame = f"{walls[0]}{' '*i}{character}"
        currentFrame += " " * abs(i-6)
        currentFrame += walls[1]
        frames.append(currentFrame)
    _frames = reversed(frames)
    for _ in _frames:
        frames.append(_)
    return frames


all_spinners["bouncingCircles"] = {
    "frames": generateBounceSpinner("\u25CF", ("(", ")")),
    "interval": 1.5/10,
}
all_spinners["bouncingBars"] = {
    "frames": generateBounceSpinner("=", ("[", "]")),
    "interval": 1.5/10,
}
all_spinners["bouncingHearts"] = {
    "frames": generateBounceSpinner("\u2665", ("|", "|")),
    "interval": 1.5/10,
}
all_spinners["bouncingCircle"] = {
    "frames": generateSingleCharacterBounceSpinner("\u25cf", ("(",")")),
    "interval": 3/50,
}
all_spinners["bouncingBar"] = {
    "frames": generateSingleCharacterBounceSpinner("=", ("[", "]")),
    "interval": 3/50,
}
all_spinners["bouncingHeart"] = {
    "frames": generateSingleCharacterBounceSpinner("\u2665", ("|", "|")),
    "interval": 3/50,
}
