import unittest
import numpy as np
import numpy.testing as np_test

import eaik.utils.spherical_wrist_checks as sphwCheck


class Test_axis_convention_trafo(unittest.TestCase):
    """Tests the capabilities transforming different joint-axis conventions to each other"""

    def test_simple_transformations(self):
        """Test simple transformations between coordinate frame bases"""
        old_axis = np.array([1, 0, 0])
        # No change at all
        xyz, rpy, basis = sphwCheck.transformToNewAxisConvention(np.eye(4), old_axis, old_axis, np.eye(3))
        np_test.assert_array_almost_equal(xyz, np.array([0, 0, 0]))
        np_test.assert_array_almost_equal(rpy, np.array([0, 0, 0]))
        np_test.assert_array_almost_equal(basis, np.eye(3))

        # Yaw by 90°:
        old_axis = np.array([1, 0, 0])
        new_axis = np.array([0, 1, 0])
        xyz, rpy, basis = sphwCheck.transformToNewAxisConvention(np.eye(4), old_axis, new_axis, np.eye(3))
        np_test.assert_array_almost_equal(xyz, np.array([0, 0, 0]))
        np_test.assert_array_almost_equal(rpy, np.array([0, 0, np.pi / 2]))
        np_test.assert_array_almost_equal(basis, np.array([[0, -1, 0],
                                                           [1, 0, 0],
                                                           [0, 0, 1]]))
        # Pitch by -90°:
        old_axis = np.array([1, 0, 0])
        new_axis = np.array([0, 0, 1])
        xyz, rpy, basis = sphwCheck.transformToNewAxisConvention(np.eye(4), old_axis, new_axis, np.eye(3))
        np_test.assert_array_almost_equal(xyz, np.array([0, 0, 0]))
        np_test.assert_array_almost_equal(rpy, np.array([0, -np.pi / 2, 0]))
        np_test.assert_array_almost_equal(basis, np.array([[0, 0, -1],
                                                           [0, 1, 0],
                                                           [1, 0, 0]]))

    def test_consecutive_parent_basis_transformations(self):
        """Test transformations with prior parent basis change"""
        old_axis = np.array([1, 0, 0])
        # Only parent basis differs
        parent_basis_x_to_y = np.array([[0, -1, 0],
                                        [1, 0, 0],
                                        [0, 0, 1]])
        xyz, rpy, basis = sphwCheck.transformToNewAxisConvention(np.eye(4), old_axis, old_axis, parent_basis_x_to_y)
        np_test.assert_array_almost_equal(xyz, np.array([0, 0, 0]))
        np_test.assert_array_almost_equal(rpy, np.array([0, 0, -np.pi / 2]))
        np_test.assert_array_almost_equal(basis, np.eye(3))

        # Own axis and parent axis differ
        old_axis = np.array([1, 0, 0])
        new_axis = np.array([0, 0, 1])
        parent_basis_x_to_y = np.array([[0, -1, 0],
                                        [1, 0, 0],
                                        [0, 0, 1]])
        xyz, rpy, basis = sphwCheck.transformToNewAxisConvention(np.eye(4), old_axis, new_axis, parent_basis_x_to_y)
        np_test.assert_array_almost_equal(xyz, np.array([0, 0, 0]))
        np_test.assert_array_almost_equal(rpy, np.array([-np.pi / 2, -np.pi / 2, 0]))
        np_test.assert_array_almost_equal(basis, np.array([[0, 0, -1],
                                                           [0, 1, 0],
                                                           [1, 0, 0]]))

    def test_axis_trafo_with_rot_trans(self):
        """Test axis ransformations including rotations and translation between frames"""
        # Only translation (Own axis change has no effect on xyz! As it is w.r.t. previous frame)
        old_axis = np.array([1, 0, 0])
        new_axis = np.array([0, 0, 1])
        parent_basis_x_to_y = np.eye(3)
        trafo = np.array([[1, 0, 0, 3.14],
                          [0, 1, 0, 69],
                          [0, 0, 1, 42],
                          [0, 0, 0, 1]])
        xyz, rpy, basis = sphwCheck.transformToNewAxisConvention(trafo, old_axis, new_axis, parent_basis_x_to_y)
        np_test.assert_array_almost_equal(xyz, np.array([3.14, 69, 42]))
        np_test.assert_array_almost_equal(rpy, np.array([0, -np.pi / 2, 0]))
        np_test.assert_array_almost_equal(basis, np.array([[0, 0, -1],
                                                           [0, 1, 0],
                                                           [1, 0, 0]]))

        # Translation & Rotation without parent-basis change
        old_axis = np.array([1, 0, 0])
        new_axis = np.array([0, 0, 1])
        parent_basis_x_to_y = np.eye(3)
        trafo = np.array([[0, 1, 0, 3.14],   # Yaw -90°
                          [-1, 0, 0, 69],
                          [0, 0, 1, 42],
                          [0, 0, 0, 1]])
        xyz, rpy, basis = sphwCheck.transformToNewAxisConvention(trafo, old_axis, new_axis, parent_basis_x_to_y)
        np_test.assert_array_almost_equal(xyz, np.array([3.14, 69, 42]))
        np_test.assert_array_almost_equal(rpy, np.array([-np.pi / 2, -np.pi / 2, 0]))
        np_test.assert_array_almost_equal(basis, np.array([[0, 0, -1],
                                                           [0, 1, 0],
                                                           [1, 0, 0]]))

        # Translation & Rotation with parent-basis change
        old_axis = np.array([1, 0, 0])
        new_axis = np.array([0, 0, 1])
        parent_basis_x_to_y = np.array([[0, -1, 0],
                                        [1, 0, 0],
                                        [0, 0, 1]])
        trafo = np.array([[0, 1, 0, 3.14],   # Yaw -90°
                          [-1, 0, 0, 69],
                          [0, 0, 1, 42],
                          [0, 0, 0, 1]])
        xyz, rpy, basis = sphwCheck.transformToNewAxisConvention(trafo, old_axis, new_axis, parent_basis_x_to_y)
        np_test.assert_array_almost_equal(xyz, np.array([69, -3.14, 42]))
        np_test.assert_array_almost_equal(rpy, np.array([np.pi, np.pi / 2, 0]))
        np_test.assert_array_almost_equal(basis, np.array([[0, 0, -1],
                                                           [0, 1, 0],
                                                           [1, 0, 0]]))


if __name__ == '__main__':
    unittest.main()
