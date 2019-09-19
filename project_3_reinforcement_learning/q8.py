import os
import numpy as np
import subprocess

epsilonRange = [0.98]
lrRange = [0.86]
stepSize = 0.02
# epsilonRange = np.arange(0.8, 1, stepSize)
# lrRange = np.arange(0.8, 1, stepSize)
for epsilon in epsilonRange:
    for lr in lrRange:
    # for lr in np.arange(epsilon, 0.93, stepSize):
        print("Running +++++++++++++++++++++++++++++++++++++++++++")
        print("epsilon = ", epsilon)
        print("lr = ", lr)
        process = subprocess.Popen(["python", "gridworld.py", "-a", "q", "-k",
            "50", "-n", "0", "-g", "BridgeGrid", "-e", str(epsilon), "-l",
            str(lr), "-q", "-w", "100"])
        try:
            process.wait(timeout=1)
        except:
            process.kill()
#os.system("python gridworld.py -a q -k 50 -n 0 -g BridgeGrid -e 0.695 -l 0.071 -q")
