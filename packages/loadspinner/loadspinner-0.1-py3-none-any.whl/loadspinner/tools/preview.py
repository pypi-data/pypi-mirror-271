import loadspinner
from time import sleep

allSpinners = list(loadspinner.all_spinners)

for spinner in allSpinners:
    print(spinner, "", end="")
    usrSpinner = loadspinner.Spinner(spinner)
    usrSpinner.start()
    sleep(2.5)
    usrSpinner.stop(newline=True)
