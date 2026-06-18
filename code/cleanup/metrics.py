import numpy as np
import os
with open(f'../points/LHSpointsNEW.txt', 'r') as f:
    LHSlines = [[float(i) for i in line.strip().split(' ')] for line in f if line]
with open(f'../new_metrics/overall_metrics_trial1.txt', 'w') as o0:
    with open(f'../new_metrics/overall_metrics_trial2.txt', 'w') as o1:
        with open(f'../new_metrics/overall_metrics_trial3.txt', 'w') as o2:
            with open(f'../new_metrics/overall_metrics_trial4.txt', 'w') as o3:
                with open(f'../new_metrics/overall_metrics_trial5.txt', 'w') as o4:
                    with open(f'../new_metrics/specfc_metrics.txt', 'w') as w:
                        for idix in range(100):
                            if not os.path.isfile(f"../new extracted order/{idix}_0.txt"):
                                print(f"File does not exist; {idix}")
                                continue
                            w.write(f"\n#{idix}:\n")
                            runOrder = []; runBinder = []; runSuscep = []
                            for runix in range(5):
                                with open(f'../new extracted order/{idix}_{runix}.txt', 'r') as f:
                                    lines = [float(line.strip()) for line in f if line.strip()]
                                meanOrder = sum(lines)/len(lines)
                                n = len(lines)
                                m2 = sum(i**2 for i in lines)/n
                                m4 = sum(i**4 for i in lines)/n
                                suscep = m2 - meanOrder**2
                                binderCum = 1 - (m4 / (3 * (m2**2)))
                                # w.write(f"   ##{runix} - order: {round(meanOrder, 3)}, binder: {round(binderCum, 3)}\n")
                                [o0, o1, o2, o3, o4][runix].write(f"{', '.join(str(q) for q in LHSlines[idix])}, {meanOrder}, {binderCum}, {suscep:.20f}\n")
                            # w.write(f"   Final - Mean Order: {round(meanMeanOrder, 3)}, Mean Binder: {round(meanBinder, 3)}\n")