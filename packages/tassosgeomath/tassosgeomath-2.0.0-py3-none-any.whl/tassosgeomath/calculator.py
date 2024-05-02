class Geometry:

    @staticmethod
    def calculate_square_area(side):
        return side ** 2

    @staticmethod
    def calculate_triangle_area(base, height):
        return 0.5 * base * height

    @staticmethod
    def calculate_trapezoid_area(base1, base2, height):
        return 0.5 * (base1 + base2) * height