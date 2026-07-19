import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False
    
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
    
class Vector(Point):
    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y

        return Vector(new_x, new_y)

print("--- Task 5 ---")
print("Point class:")
point1 = Point(1, 2)
point2 = Point(3, 5)
point3 = Point(1, 2)
print("Equality (Not Equal): ", point1 == point2)
print("Equality (Equal): ", point1 == point3)
print("String Representation: ", str(point1))
print("Distance from (1, 2) to (3, 5): ", point1.distance(point2))
print("\nVector class:")
vector1 = Vector(4, 1)
vector2 = Vector(7, 2)
print("Addition of [4, 1] and [7, 2]: ", vector1 + vector2)