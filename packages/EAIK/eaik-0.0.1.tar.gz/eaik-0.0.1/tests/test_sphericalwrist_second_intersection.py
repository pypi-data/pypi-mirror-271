import unittest
import numpy as np

import eaik.utils.spherical_wrist_checks as sphwCheck


class Test_sphericalwrist_second_intersection(unittest.TestCase):
    """Tests the capabilities of checking second axis intersection"""

    def setUp(self) -> None:
        self.translation_list = np.linspace(-50.0, 50.0, num=15)
        self.rotation_list = np.linspace(0.0, np.pi, num=10, endpoint=False)[1:]  # exclude parallel cases (0,np.pi)

    def test_first_parallel_last(self):
        """Tests spherical wrist, where first and last axis are the same"""
        for r_val in self.rotation_list:
            for t_val in self.translation_list:
                ##
                # Orthogonal intermediate axis
                ##
                # First axis equals last; Last axis Translated in x_0-dir (-y_1-dir) by t_val
                # Second axis is translated by t_val in y_0-dir ->  intersection in (0,0,0)
                xyz_1 = np.array([0, t_val, 0])
                rpy_1 = np.array([0, 0, np.pi / 2])
                xyz_2 = np.array([-t_val, t_val, 0])
                rpy_2 = np.array([r_val, 0, -np.pi / 2])
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))
                if not np.isclose(t_val, 0):  # xyz_2 offset needed
                    rpy_2[1] = 1e-4  # Last axis off center
                    self.assertFalse(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

                # First axis equals last; Last axis Translated in x_0-dir (-z_1-dir) by t_val
                # Second axis is translated by t_val in z_0-dir -> intersection in (0,0,0)
                xyz_1 = np.array([0, 0, t_val])
                rpy_1 = np.array([0, np.pi / 2, 0])
                xyz_2 = np.array([t_val, 0, t_val])
                rpy_2 = np.array([r_val, -np.pi / 2, 0])
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))
                xyz_1[1] = 1e-4  # Second and last axis off center
                self.assertFalse(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

                ##
                # Non-Orthogonal intermediate axis
                ##
                # Second axis facing 45° from (0,0,0) to (1,1,1) -> intersection at (0,0,0) w.r.t. axis_0
                # Third axis exactly on first axis
                arctan_sqrt_2 = np.arctan(np.sqrt(2))
                xyz_1 = np.array([t_val, t_val, t_val])
                rpy_1 = np.array([0, -((np.pi / 2) - arctan_sqrt_2), np.pi / 4])  # new Axis
                xyz_2 = np.array([-np.sqrt(3) * t_val, 0, 0])
                rpy_2 = np.array([0, 0.42053434, -0.88607712])  # Inverse rotation values calculated by hand
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))
                xyz_2[1] = 1e-4  # Last axis off center
                self.assertFalse(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

                # Second axis facing 45° from (tval,0,0) to (tval+1,1,1) -> intersection at (tval,0,0) w.r.t. axis_0
                # Third axis exactly on first axis
                arctan_sqrt_2 = np.arctan(np.sqrt(2))
                xyz_1 = np.array([t_val + 1, 1, 1])
                rpy_1 = np.array([0, -((np.pi / 2) - arctan_sqrt_2), np.pi / 4])  # new Axis
                xyz_2 = np.array([-np.sqrt(3), 0, 0])
                rpy_2 = np.array([0, 0.42053434, -0.88607712])  # Inverse rotation values calculated by hand
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))
                rpy_1[1] += 1e-3  # Second axis off center
                self.assertFalse(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

                # Second axis facing 45° from (0,tval,tval) to (1,tval+1,tval+1)
                # Third axis exactly on first axis -> intersection at (-tval,0,0) w.r.t. axis_0
                arctan_sqrt_2 = np.arctan(np.sqrt(2))
                xyz_1 = np.array([1, t_val + 1, t_val + 1])
                rpy_1 = np.array([0, -((np.pi / 2) - arctan_sqrt_2), np.pi / 4])  # new Axis
                xyz_2 = np.array([-np.sqrt(3) * (t_val + 1), 0, 0])
                rpy_2 = np.array([0, 0.42053434, -0.88607712])  # Inverse rotation values calculated by hand
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))
                xyz_2[2] += 1e-4  # Last axis off center
                self.assertFalse(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

    def test_second_parallel_last(self):
        """Tests spherical wrist, where second and last axis are parallel"""
        # Three orthogonal axes intersecting at (t_val, 0, 0) w.r.t. axis 0
        # first axis aligns with (1, 0, 0), second with (0,1,0), third with (0,0,1)
        for r_val in self.rotation_list:
            for t_val in self.translation_list:
                # Last axis with z-offset w.r.t. second axis -> not inherently redundant
                if not np.isclose(t_val, 0):
                    xyz_1 = np.array([t_val, t_val, 0])
                    rpy_1 = np.array([0, 0, r_val])
                    xyz_2 = np.array([-t_val, 0, t_val])
                    rpy_2 = np.array([r_val, 0, 0])
                    self.assertFalse(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

                # Last axis directly on second axis -> inherently redundant
                xyz_1 = np.array([0, 0, 0])
                rpy_1 = np.array([0, 0, r_val])
                xyz_2 = np.array([-t_val, 0, 0])
                rpy_2 = np.array([r_val, np.pi, 0])
                with self.assertRaises(Exception):
                    sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2)

    def test_all_orthogonal_wrist(self):
        """Tests check for 3-orthogonal axes forming a spherical wrist"""
        for r_val in self.rotation_list:
            for t_val in self.translation_list:
                # Three orthogonal axes intersecting at (t_val, 0, 0) w.r.t. axis 0
                # first axis aligns with (1, 0, 0), second with (0,1,0), third with (0,0,1)
                xyz_1 = np.array([t_val, t_val, 0])
                rpy_1 = np.array([0, 0, np.pi / 2])
                xyz_2 = np.array([-t_val, 0, t_val])
                rpy_2 = np.array([r_val, -np.pi / 2, 0])
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))
                xyz_1[2] += 1e-3  # Second and last axis off center
                self.assertFalse(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

                # Three orthogonal axes intersecting at (t_val, 0, 0) w.r.t. axis 0
                # first axis aligns with (1, 0, 0), second with (0,0,1), third with (0,1,0)
                xyz_1 = np.array([t_val, 0, 0])
                rpy_1 = np.array([0, -np.pi / 2, 0])
                xyz_2 = np.array([0, 0, 0])
                rpy_2 = np.array([r_val, 0, np.pi / 2])
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

    def test_two_orthogonal_wrist(self):
        """Tests check for 2-orthogonal axes forming a spherical wrist"""
        for r_val in self.rotation_list:
            for t_val in self.translation_list:
                if (np.isclose(r_val, np.pi / 2)):
                    r_val -= 1e5  # This makes our third axis non redundant for the following code
                ##
                # Orthogonal second axis
                ##
                # First axis orthogonal to second; Intersection in (t_val,0,0)
                # Second axis is translated by t_val in y_0-dir and x_0-dir
                # Third axis has its center in the intersection point and is yawed by r_val
                # (r_val=/=np.pi/2 -> non redundant to second axis)
                xyz_1 = np.array([t_val, t_val, 0])
                rpy_1 = np.array([r_val, 0, np.pi / 2])
                xyz_2 = np.array([-t_val, 0, 0])
                rpy_2 = np.array([r_val, 0, -np.pi / 2 + r_val])
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

                # First axis orthogonal to second; Intersection in (t_val,0,0)
                # Second axis is translated by t_val in z_0-dir and x_0-dir
                # Third axis has its center in the intersection point and is pitched and yawed by r_val
                xyz_1 = np.array([t_val, 0, t_val])
                rpy_1 = np.array([r_val, np.pi / 2, 0])
                xyz_2 = np.array([t_val, 0, 0])
                rpy_2 = np.array([r_val, -np.pi / 2 + r_val, r_val])
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

                ##
                # Orthogonal third axis
                ##
                # Second axis facing 45° from (0,0,0) to (1,1,1) -> intersection at (0,0,0) w.r.t. axis_0
                # Third axis orthogonal to first axis (aligned with (0,1,0))
                arctan_sqrt_2 = np.arctan(np.sqrt(2))
                xyz_1 = np.array([t_val, t_val, t_val])
                rpy_1 = np.array([0, -((np.pi / 2) - arctan_sqrt_2), np.pi / 4])  # new Axis
                xyz_2 = np.array([-np.sqrt(3) * t_val, 0, 0])
                rpy_2 = np.array([0, 0.42053434, -0.88607712 + np.pi / 2])  # Inverse rotation values calculated by hand
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

                # Second axis facing 45° from (0,tval,tval) to (-1,tval+1,tval+1)
                # Third axis orthogonal to first axis (aligned with (0,0,1)) -> intersection at (tval,0,0) w.r.t. axis_0
                arctan_sqrt_2 = np.arctan(np.sqrt(2))
                xyz_1 = np.array([1, t_val + 1, t_val + 1])
                rpy_1 = np.array([0, -((np.pi / 2) - arctan_sqrt_2), 3 * np.pi / 4])  # new Axis
                xyz_2 = np.array([-np.sqrt(3) * (t_val + 1), 0, 0])
                rpy_2 = np.array([0.78539816, 0.61547971, -2.0943951])  # Inverse rotation values calculated by hand
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

    def test_no_orthogonal_wrist(self):
        """Tests check for 3 non-orthogonal axes forming a spherical wrist"""
        for r_val in self.rotation_list:
            for t_val in self.translation_list:
                # Second axis facing 45° from (0,0,0) to (1,1,1)
                # Third axis facing 45° from (0,0,0) to (1,1,0) -> intersection at (0,0,0) w.r.t. axis_0
                arctan_sqrt_2 = np.arctan(np.sqrt(2))
                xyz_1 = np.array([t_val, t_val, t_val])
                rpy_1 = np.array([0, -((np.pi / 2) - arctan_sqrt_2), np.pi / 4])  # new Axis
                xyz_2 = np.array([-np.sqrt(3) * t_val, 0, 0])
                rpy_2 = np.array([0, 0.42053434, -0.88607712 + np.pi / 4])  # Inverse rotation values calculated by hand
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))
                xyz_2[0] += 1e-4  # Last axis off center
                self.assertFalse(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))

                # Second axis facing 45° from (0,tval,tval) to (-1,tval+1,tval+1)
                # Third axis facing 36° from (0,0,0) -> intersection at (0,0,0) w.r.t. axis_0
                arctan_sqrt_2 = np.arctan(np.sqrt(2))
                xyz_1 = np.array([1, t_val + 1, t_val + 1])
                rpy_1 = np.array([0, -((np.pi / 2) - arctan_sqrt_2), 3 * np.pi / 4])  # new Axis
                xyz_2 = np.array([-np.sqrt(3) * (t_val + 1), 0, 0])
                rpy_2 = np.array([0, 0.42053434, -0.88607712 + np.pi / 5])  # Inverse rotation values calculated by hand
                self.assertTrue(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))
                xyz_1[2] += 1e-4  # Second and last axis off center
                self.assertFalse(sphwCheck.check_second_intersection_axis(xyz_1, rpy_1, xyz_2, rpy_2))


if __name__ == '__main__':
    unittest.main()
