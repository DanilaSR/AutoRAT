from point_target import *
import matplotlib.pyplot as plt


def error(signal, size):

    for i in range(size - 1):
        signal[i] = 100 * np.abs((signal[i + 1] - signal[i]) / signal[i])

    signal[size - 1] = signal[size - 2]

    return signal


range_irw = []
azimuth_irw = []

range_pslr = []
azimuth_pslr = []

range_islr = []
azimuth_islr = []

scale = np.linspace(5, 30, dtype="int64")

scale2k0 = np.array([2*i for i in range(3, 20)])
scale2k1 = np.array([2*i + 1 for i in range(3, 20)])

scale = scale2k0

for i in scale:
    p1 = PointTargetScale('src/0.npy', i)
    range_irw.append(p1.range_irw())
    azimuth_irw.append(p1.azimuth_irw())

    range_pslr.append(p1.range_pslr_db())
    azimuth_pslr.append(p1.azimuth_pslr_db())

    range_islr.append(p1.range_islr_db())
    azimuth_islr.append(p1.azimuth_islr_db())

range_irw = error(range_irw, scale.size)
azimuth_irw = error(azimuth_irw, scale.size)
range_pslr = error(range_pslr, scale.size)
azimuth_pslr = error(azimuth_pslr, scale.size)
range_islr = error(range_islr, scale.size)
azimuth_islr = error(azimuth_islr, scale.size)

plt.figure(figsize=(12, 18))

plt.subplot(321)
plt.title('range_irw')
plt.plot(scale, range_irw)
plt.ylabel('%')


plt.subplot(322)
plt.title('azimuth_irw')
plt.plot(scale,  azimuth_irw)
plt.ylabel('%')

plt.subplot(323)
plt.title('range_pslr')
plt.plot(scale, range_pslr)
plt.ylabel('%')

plt.subplot(324)
plt.title('azimuth_pslr')
plt.plot(scale, azimuth_pslr)
plt.ylabel('%')

plt.subplot(325)
plt.title('range_islr')
plt.plot(scale, range_islr)
plt.ylabel('%')

plt.subplot(326)
plt.title('azimuth_islr')
plt.plot(scale, azimuth_islr)
plt.ylabel('%')

plt.suptitle("Чётный Scale")

plt.show()

