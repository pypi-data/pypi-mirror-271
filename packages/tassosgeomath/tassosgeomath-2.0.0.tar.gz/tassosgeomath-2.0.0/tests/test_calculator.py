import unittest
from tassosgeomath.calculator import Geometry


class TestCalculator(unittest.TestCase):
    def test_calculate_square_area(self):
        self.assertEqual(Geometry.calculate_square_area(5), 25)

    def test_calculate_triangle_area(self):
        self.assertEqual(Geometry.calculate_triangle_area(base=10, height=5), 25)

    def test_calculate_trapezoid_area(self):
        self.assertEqual(Geometry.calculate_trapezoid_area(base1=10, base2=5, height=5), 37.5)
