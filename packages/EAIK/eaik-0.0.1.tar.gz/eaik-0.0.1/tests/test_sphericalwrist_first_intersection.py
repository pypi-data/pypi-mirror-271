import unittest
import numpy as np
import numpy.testing as np_test

import eaik.utils.spherical_wrist_checks as sphwCheck


class Test_sphericalwrist_first_intersection(unittest.TestCase):
    """Tests the capabilities of checking and calculating first axis intersection"""

    def setUp(self) -> None:
        self.translation_list = np.linspace(-50.0, 50.0, num=20)
        self.rotation_list = np.linspace(0.0, np.pi, num=10, endpoint=False)[1:]  # exclude parallel cases (0,np.pi)

    def test_first_intersection_y_orthogonality(self):
        """Tests check and calculation of intersection points for axes orthogonal to Y-axis"""
        for t_val in self.translation_list:
            for r_val in self.rotation_list:
                # Test y-orthogonality (x-axis translated)
                xyz = np.array([1 + t_val, 1, 0])
                rpy = np.array([r_val, 0, np.pi / 4])
                intersec = sphwCheck.calculate_intersection(xyz, rpy)  # should intersect at (t_val,0,0)
                np_test.assert_array_almost_equal(intersec, np.array([t_val, 0, 0]))
                rpy[2] = r_val  # Test for different yaw angles != 0,np.pi
                self.assertTrue(sphwCheck.check_first_intersection_axis(xyz, rpy))

                # Test y-orthogonality (y-axis translated)
                xyz = np.array([1, 1 + t_val, 0])
                rpy = np.array([r_val, 0, np.pi / 4])
                intersec = sphwCheck.calculate_intersection(xyz, rpy)  # should intersect at (-t_val,0,0)
                np_test.assert_array_almost_equal(intersec, np.array([-t_val, 0, 0]))
                rpy[2] = r_val  # Test for different yaw angles != 0,np.pi
                self.assertTrue(sphwCheck.check_first_intersection_axis(xyz, rpy))

                # Test y-orthogonality (z-axis translated)
                xyz = np.array([1, 1, t_val])
                rpy = np.array([r_val, 0, np.pi / 4])
                if not np.isclose(t_val, 0):
                    with self.assertRaises(Exception):  # should not intersect
                        intersec = sphwCheck.calculate_intersection(xyz, rpy)
                    rpy[2] = r_val  # Test for different yaw angles != 0,np.pi
                    self.assertFalse(sphwCheck.check_first_intersection_axis(xyz, rpy))

    def test_first_intersection_z_orthogonality(self):
        """Tests check and calculation of intersection points for axes orthogonal to Z-axis"""
        for t_val in self.translation_list:
            for r_val in self.rotation_list:
                # Test z-orthogonality (x-axis translated)
                xyz = np.array([1 + t_val, 0, 1])
                rpy = np.array([r_val, -np.pi / 4, 0])
                intersec = sphwCheck.calculate_intersection(xyz, rpy)  # should intersect at (t_val,0,0)
                np_test.assert_array_almost_equal(intersec, np.array([t_val, 0, 0]))
                rpy[1] = r_val  # Test for different pitch angles != 0,np.pi
                self.assertTrue(sphwCheck.check_first_intersection_axis(xyz, rpy))

                # Test z-orthogonality (z-axis translated)
                xyz = np.array([1, 0, 1 + t_val])
                rpy = np.array([r_val, -np.pi / 4, 0])
                intersec = sphwCheck.calculate_intersection(xyz, rpy)  # should intersect at (-t_val,0,0)
                np_test.assert_array_almost_equal(intersec, np.array([-t_val, 0, 0]))
                rpy[1] = r_val  # Test for different pitch angles != 0,np.pi
                self.assertTrue(sphwCheck.check_first_intersection_axis(xyz, rpy))

                # Test z-orthogonality (y-axis translated)
                xyz = np.array([1, t_val, 1])
                rpy = np.array([r_val, -np.pi / 4, 0])
                if not np.isclose(t_val, 0):
                    with self.assertRaises(Exception):  # should not intersect
                        intersec = sphwCheck.calculate_intersection(xyz, rpy)  # should not intersect
                    rpy[1] = r_val  # Test for different pitch angles != 0,np.pi
                    self.assertFalse(sphwCheck.check_first_intersection_axis(xyz, rpy))

    def test_first_intersection_yz_orthogonality(self):
        """Tests check and calculation of intersection points for axes orthogonal to Y,Z-axes"""
        for t_val in self.translation_list:
            for r_val in self.rotation_list:
                # Test yz-orthogonality (x-axis translated)
                xyz = np.array([1 + t_val, 1, 0])
                rpy = np.array([r_val, 0, np.pi / 2])
                intersec = sphwCheck.calculate_intersection(xyz, rpy)  # should intersect at (1+t_val,0,0)
                np_test.assert_array_almost_equal(intersec, np.array([1 + t_val, 0, 0]))
                self.assertTrue(sphwCheck.check_first_intersection_axis(xyz, rpy))

                # Test yz-orthogonality (y-axis translated)
                xyz = np.array([1, 1 + t_val, 0])
                rpy = np.array([r_val, 0, np.pi / 2])
                intersec = sphwCheck.calculate_intersection(xyz, rpy)  # should intersect at (1,0,0)
                np_test.assert_array_almost_equal(intersec, np.array([1, 0, 0]))
                self.assertTrue(sphwCheck.check_first_intersection_axis(xyz, rpy))

                # Test yz-orthogonality (z-axis translated)
                xyz = np.array([1, 1, t_val])
                rpy = np.array([r_val, 0, np.pi / 2])
                if not np.isclose(t_val, 0):
                    with self.assertRaises(Exception):  # should not intersect
                        intersec = sphwCheck.calculate_intersection(xyz, rpy)
                    self.assertFalse(sphwCheck.check_first_intersection_axis(xyz, rpy))

    def test_first_intersection_parallel(self):
        """Tests check and calculation of intersection points for parallel cases"""
        # Test x-orthogonality (Parallel case)
        for t_val in self.translation_list:
            for r_val in self.rotation_list:
                rpy = np.array([r_val, 0, 0])
                xyz = np.array([t_val, 0, 0])
                with self.assertRaises(Exception):
                    sphwCheck.calculate_intersection(xyz, rpy)
                self.assertTrue(sphwCheck.check_first_intersection_axis(xyz, rpy))

                if not np.isclose(t_val, 0):
                    xyz = np.array([0, t_val, 0])
                    with self.assertRaises(Exception):
                        sphwCheck.calculate_intersection(xyz, rpy)
                    self.assertFalse(sphwCheck.check_first_intersection_axis(xyz, rpy))

                    xyz = np.array([0, 0, t_val])
                    with self.assertRaises(Exception):
                        sphwCheck.calculate_intersection(xyz, rpy)
                    self.assertFalse(sphwCheck.check_first_intersection_axis(xyz, rpy))


if __name__ == '__main__':
    unittest.main()
