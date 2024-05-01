"""A CLI based loading spinner."""

from ._spinners import all_spinners
from time import sleep
from time import time as getEpoch
import multiprocessing

__all__ = [
    "Spinner",
]

__version__ = "0.1"
__description__ = "a CLI based loading spinner."
__author__ = "xyzpw"
__license__ = "MIT"

class Spinner:
    def __init__(self, spinner_type: str = "classic"):
        self.spinner_type = spinner_type
        self.frames = all_spinners[spinner_type]["frames"]
        self.interval = all_spinners[spinner_type]["interval"]
        self._process = None
    def _createProcess(self, alive_time=None): # Not intended for user use
        frameIndex = 0
        creationTime = getEpoch()
        newSpaceSize = 0
        for f in self.frames:
            if len(f) > newSpaceSize:
                newSpaceSize = len(f)
        print("\x1b[%sC" % newSpaceSize, end="")
        while True:
            if frameIndex == len(self.frames):
                frameIndex = 0
            currentFrame = self.frames[frameIndex]
            frameLength = len(str(currentFrame))
            print(f"\x1b[{frameLength}D{currentFrame}", end="", flush=True)
            if alive_time != None:
                if getEpoch() - creationTime >= alive_time:
                    break
            sleep(self.interval)
            frameIndex += 1
    def start(self, alive_time: int | float = None):
        """Initiates the spinner animation which will be displayed.

        :param alive_time: how long the spinner will be active before stopping (optional)"""
        self._process = multiprocessing.Process(target=self._createProcess, daemon=True, args=[alive_time])
        self._process.start()
    def stop(self, message: str = None, clearline: bool = None, newline: bool = None):
        """Terminates the spinner process.

        :param message:   optional message upon completion
        :param clearline: clears the entire line which the spinner was on
        :param newline:   prints a newline upon spinner completion"""
        self._process.terminate()
        if clearline:
            print("\x1b[2K\r", end="")
        if message != None:
            print(message, end="")
        if newline:
            print("\n", end="")
