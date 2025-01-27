import sys
sys.path.insert(1, '../src')
import numpy as np
import unittest
import json
from point_target import PointTarget


class TestPointTarget(unittest.TestCase):
    def setUp(self):
        fp = open('metrics.json')
        self.point_target = []
        self.point_target.append(PointTarget('../data/0.npy'))
        self.point_target.append(PointTarget('../data/1.npy'))
        self.point_target.append(PointTarget('../data/2.npy'))
        self.check = json.load(fp)
        self.accuracy = 0.005
        fp.close()

    def test_azimuth_irw0(self):
        self.assertAlmostEqual(self.point_target[0].azimuth_irw(), self.check['0']['azimuth_irw'],
                               delta=self.accuracy * np.abs(self.check['0']['azimuth_irw']))

    def test_azimuth_pslr_db0(self):
        self.assertAlmostEqual(self.point_target[0].azimuth_pslr_db(), self.check['0']['azimuth_pslr_db'],
                               delta=self.accuracy * np.abs(self.check['0']['azimuth_pslr_db']))

    def test_azimuth_islr_db0(self):
        self.assertAlmostEqual(self.point_target[0].azimuth_islr_db(), self.check['0']['azimuth_islr_db'],
                               delta=self.accuracy * np.abs(self.check['0']['azimuth_islr_db']))

    def test_range_irw0(self):
        self.assertAlmostEqual(self.point_target[0].range_irw(), self.check['0']['range_irw'],
                               delta=self.accuracy * np.abs(self.check['0']['range_irw']))

    def test_range_pslr_db0(self):
        self.assertAlmostEqual(self.point_target[0].range_pslr_db(), self.check['0']['range_pslr_db'],
                               delta=self.accuracy * np.abs(self.check['0']['range_pslr_db']))

    def test_range_islr_db0(self):
        self.assertAlmostEqual(self.point_target[0].range_islr_db(), self.check['0']['range_islr_db'],
                               delta=self.accuracy * np.abs(self.check['0']['range_islr_db']))

#######################################################################################################################

    def test_azimuth_irw1(self):
        self.assertAlmostEqual(self.point_target[1].azimuth_irw(), self.check['1']['azimuth_irw'],
                               delta=self.accuracy * np.abs(self.check['1']['azimuth_irw']))

    def test_azimuth_pslr_db1(self):
        self.assertAlmostEqual(self.point_target[1].azimuth_pslr_db(), self.check['1']['azimuth_pslr_db'],
                               delta=self.accuracy * np.abs(self.check['1']['azimuth_pslr_db']))

    def test_azimuth_islr_db1(self):
        self.assertAlmostEqual(self.point_target[1].azimuth_islr_db(), self.check['1']['azimuth_islr_db'],
                               delta=self.accuracy * np.abs(self.check['1']['azimuth_islr_db']))

    def test_range_irw1(self):
        self.assertAlmostEqual(self.point_target[1].range_irw(), self.check['1']['range_irw'],
                               delta=self.accuracy * np.abs(self.check['1']['range_irw']))

    def test_range_pslr_db1(self):
        self.assertAlmostEqual(self.point_target[1].range_pslr_db(), self.check['1']['range_pslr_db'],
                               delta=self.accuracy * np.abs(self.check['1']['range_pslr_db']))

    def test_range_islr_db1(self):
        self.assertAlmostEqual(self.point_target[1].range_islr_db(), self.check['1']['range_islr_db'],
                               delta=self.accuracy * np.abs(self.check['1']['range_islr_db']))

########################################################################################################################

    def test_azimuth_irw2(self):
        self.assertAlmostEqual(self.point_target[2].azimuth_irw(), self.check['2']['azimuth_irw'],
                               delta=self.accuracy * np.abs(self.check['2']['azimuth_irw']))

    def test_azimuth_pslr_db2(self):
        self.assertAlmostEqual(self.point_target[2].azimuth_pslr_db(), self.check['2']['azimuth_pslr_db'],
                               delta=self.accuracy * np.abs(self.check['2']['azimuth_pslr_db']))

    def test_azimuth_islr_db2(self):
        self.assertAlmostEqual(self.point_target[2].azimuth_islr_db(), self.check['2']['azimuth_islr_db'],
                               delta=self.accuracy * np.abs(self.check['2']['azimuth_islr_db']))

    def test_range_irw2(self):
        self.assertAlmostEqual(self.point_target[2].range_irw(), self.check['2']['range_irw'],
                               delta=self.accuracy * np.abs(self.check['2']['range_irw']))

    def test_range_pslr_db2(self):
        self.assertAlmostEqual(self.point_target[2].range_pslr_db(), self.check['2']['range_pslr_db'],
                               delta=self.accuracy * np.abs(self.check['2']['range_pslr_db']))

    def test_range_islr_db2(self):
        self.assertAlmostEqual(self.point_target[2].range_islr_db(), self.check['2']['range_islr_db'],
                               delta=self.accuracy * np.abs(self.check['2']['range_islr_db']))


if __name__ == '__main__':
    unittest.main()
