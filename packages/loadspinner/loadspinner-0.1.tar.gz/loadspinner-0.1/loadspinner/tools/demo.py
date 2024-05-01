import loadspinner
import time, random

for i in loadspinner.all_spinners:
    print("%d) %s" % (list(loadspinner.all_spinners).index(i), i))

spinnerType = int(input("Select spinner: "))
spinnerType = str(list(loadspinner.all_spinners)[spinnerType])

spinner = loadspinner.Spinner(spinnerType)
print("Process is running, wait until complete ", end="")
spinner.start()
time.sleep(random.randint(5, 10))
spinner.stop("Process has been completed", clearline=True, newline=True)
