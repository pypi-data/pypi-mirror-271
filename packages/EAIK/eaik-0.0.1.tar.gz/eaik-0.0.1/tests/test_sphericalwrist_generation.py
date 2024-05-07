import unittest
import numpy as np
import random

import eaik.utils.generate_spherical_wrist as sphwGen
import eaik.utils.spherical_wrist_checks as sphwCheck


class Test_sphericalwrist_generation(unittest.TestCase):
    """Tests the capabilities of generating spherical wrists"""

    def setUp(self) -> None:
        self.number_wrists = 1000
        np.random.seed(0)
        random.seed(3141592654)

    def test_spherical_wrist_generation(self):
        """Test generates variety of spherical wrists and checks their axes intersection"""
        for i in range(self.number_wrists):
            xyz_1, rpy_1 = sphwGen.generate_first_intersection_axis()
            xyz_2, rpy_2 = sphwGen.generate_second_intersection_axis(xyz_1, rpy_1)

            self.assertTrue(sphwCheck.check_first_intersection_axis(xyz_1, rpy_1))
            self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))


if __name__ == '__main__':
    unittest.main()
