from point_target import *


p1 = PointTarget('src/0.npy')
p2 = PointTargetScale('src/0.npy', 17)
print(p1.azimuth_irw())
print(p2.azimuth_irw())