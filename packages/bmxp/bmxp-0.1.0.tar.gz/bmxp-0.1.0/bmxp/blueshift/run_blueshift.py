from blueshift import DriftCorrection
import time

dc = DriftCorrection(
    "DCinput2-10k.csv",
    "DCinfo2.csv",
)

print("calculating")
t0 = time.time()
dc.calculate_cvs()
print("done")
print(time.time() - t0)
