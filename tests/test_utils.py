#!/usr/bin/env python

# """Tests for `utils` package."""

# import os
# import unittest

# from nclpy import utils


# class TestUtils(unittest.TestCase):
#     """Tests for `utils` package."""

#     def setUp(self):
#         """Set up test fixtures, if any."""
#         print("setUp")
#         self.in_shp = os.path.abspath("examples/data/countries.shp")

#     def tearDown(self):
#         """Tear down test fixtures, if any."""
#         print("tearDown\n")

#     def test_random_string(self):
#         print("test_random_string")
#         self.assertEqual(len(utils.random_string(3)), 3)

#     def test_add(self):
#         print("test_add")
#         self.assertEqual(utils.add(-1, 1), 0)
#         self.assertEqual(utils.add(-1, -1), -2)
#         self.assertEqual(utils.add(10, 5), 15)

#     def test_subtract(self):
#         print("test_subtract")
#         self.assertEqual(utils.subtract(10, 5), 5)
#         self.assertEqual(utils.subtract(-1, 1), -2)
#         self.assertEqual(utils.subtract(-1, -1), 0)

#     def test_multiply(self):
#         print("test_multiply")
#         self.assertEqual(utils.multiply(10, 5), 50)
#         self.assertEqual(utils.multiply(-1, 1), -1)
#         self.assertEqual(utils.multiply(-1, -1), 1)

#     def test_divide(self):
#         print("test_divide")
#         self.assertEqual(utils.divide(10, 5), 2)
#         self.assertEqual(utils.divide(-1, 1), -1)
#         self.assertEqual(utils.divide(-1, -1), 1)
#         self.assertEqual(utils.divide(5, 2), 2.5)

#         with self.assertRaises(ValueError):
#             utils.divide(10, 0)


# if __name__ == '__main__':
#     unittest.main()