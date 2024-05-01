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
    "blinking_heart": {
        "frames": ["\u2661", "\u2665"],
        "interval": 0.5,
    },
    "blinking_circle": {
        "frames": ["\u25CB", "\u25CF"],
        "interval": 0.5,
    },
    "loading_circle": {
        "frames": ["\u25D4", "\u25D1", "\u25D5", "\u25CF"],
        "interval": 1/3,
    },
}

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

all_spinners["bouncing_ball"] = {
    "frames": generateBounceSpinner("\u25CF", ("(", ")")),
    "interval": 1.5/10,
}
all_spinners["bouncing_bar"] = {
    "frames": generateBounceSpinner("=", ("[", "]")),
    "interval": 1.5/10,
}
all_spinners["bouncing_heart"] = {
    "frames": generateBounceSpinner("\u2665", ("|", "|")),
    "interval": 1.5/10,
}
