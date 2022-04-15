from __future__ import annotations
import math

class Vector3:
    def __init__(self, x=.0, y=.0, z=.0) -> None:
        """Simple 3D Vector Class with basic operations"""
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'
    
    def dotProduct(self, other: Vector3) -> float:
        """Returns the dot product between self Vector and another Vector3D"""
        assert isinstance(other, Vector3)
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
    
    def magnitude(self) -> float:
        """Returns the magnitude of the Vector"""
        return math.sqrt(self.dotProduct(self))
    
    def normalize(self) -> Vector3:
        """Returns the normalized Vector"""
        return self / self.magnitude()
    
    def __add__(self, other: Vector3) -> Vector3:
        """Returns the sum of the two Vectors"""
        assert isinstance(other, Vector3)
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: Vector3) -> Vector3:
        """Returns the subtraction of the two Vectors"""
        assert isinstance(other, Vector3)
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __neg__(self):
        """Returns the inverse of the vector"""
        return Vector3(-self.x, -self.y, -self.z)

    def __xor__(self, other: Vector3) -> float:
        """Returns the dot product between the two vectors"""
        assert isinstance(other, Vector3)
        return self.dotProduct(other)
    
    def __mul__(self, other: float) -> Vector3:
        """Multiplication with scalar value"""
        assert not isinstance(other, Vector3)
        return Vector3(self.x * other, self.y * other, self.z * other)
    
    def __rmul__(self, other: float) -> Vector3:
        """Multiplication with scalar value"""
        return self.__mul__(other)
    
    def __eq__(self, other: Vector3) -> bool:
        """Equality between two vectors"""
        assert isinstance(other, Vector3)
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __truediv__(self, other: float) -> Vector3:
        """Division by scalar value"""
        assert not isinstance(other, Vector3)
        return Vector3(self.x / other, self.y / other, self.z / other)

class Color(Vector3):
    """Stores colors as RGB triplets, based of Vector3"""
    @classmethod
    def fromHex(cls, hex="#000000") -> Color:
        x = int(hex[1:3], 16) / 255.0
        y = int(hex[3:5], 16) / 255.0
        z = int(hex[5:], 16) / 255.0
        return cls(x, y, z)

class Point(Vector3):
    """Point stores coordinates of a point in 3D space, based on Vector"""
    pass