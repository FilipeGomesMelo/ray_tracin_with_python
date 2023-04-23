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

    def kron_product(self, other: Vector3) -> Vector3:
        """Returns the Kronecker product between self Vector and another Vector3"""
        assert isinstance(other, Vector3) or issubclass(other, Vector3)
        return self.__class__((self.x * other.x), (self.y * other.y), (self.z * other.z))
    
    def dot_product(self, other: Vector3) -> float:
        """Returns the dot product between self Vector and another Vector3"""
        assert isinstance(other, Vector3) or issubclass(other, Vector3)
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)
    
    def cross_product(self, other: Vector3) -> Vector3:
        """Returns the cross product between self Vector and another Vector3"""
        assert isinstance(other, Vector3) or issubclass(other, Vector3)
        return self.__class__(
            self.y*other.z - self.z*other.y,
            self.z*other.x - self.x*other.z,
            self.x*other.y - self.y*other.x
        )
    
    def magnitude(self) -> float:
        """Returns the magnitude of the Vector"""
        return math.sqrt(self.dot_product(self))
    
    def normalize(self) -> Vector3:
        """Returns the normalized Vector"""
        return self / self.magnitude()
    
    def __add__(self, other: Vector3) -> Vector3:
        """Returns the sum of the two Vectors"""
        assert isinstance(other, Vector3) or issubclass(other, Vector3)
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: Vector3) -> Vector3:
        """Returns the subtraction of the two Vectors"""
        assert isinstance(other, Vector3) or issubclass(other, Vector3)
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __neg__(self):
        """Returns the inverse of the vector"""
        return self.__class__(-self.x, -self.y, -self.z)

    def __xor__(self, other: Vector3) -> float:
        """Returns the dot product between the two vectors"""
        assert isinstance(other, Vector3) or issubclass(other, Vector3)
        return self.dot_product(other)
    
    def __mul__(self, other: float) -> Vector3:
        """Multiplication with scalar value"""
        assert not isinstance(other, Vector3) or issubclass(other, Vector3)
        return self.__class__(self.x * other, self.y * other, self.z * other)
    
    def __rmul__(self, other: float) -> Vector3:
        """Multiplication with scalar value"""
        return self.__mul__(other)
    
    def __eq__(self, other: Vector3) -> bool:
        """Equality between two vectors"""
        assert isinstance(other, Vector3) or issubclass(other, Vector3)
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __truediv__(self, other: float) -> Vector3:
        """Division by scalar value"""
        assert not isinstance(other, Vector3) or issubclass(other, Vector3)
        return self.__class__(self.x / (other or 1), self.y / (other or 1), self.z / (other or 1))
    
    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def __floordiv__(self, other: float) -> Vector3:
        """Division by scalar value"""
        assert not isinstance(other, Vector3) or issubclass(other, Vector3)
        return self.__class__(self.x // (other or 1), self.y // (other or 1), self.z // (other or 1))

    def transform(self, matrix):
        """Transform this vector by a 3x3 or 4x4 matrix."""
        assert isinstance(matrix, list) \
            and (len(matrix) == 3 or len(matrix) == 4) \
            and all(len(row) == 3 or len(row) == 4 for row in matrix), "Invalid matrix"
        if len(matrix) == 3:
            for row in matrix:
                row.append(0)
            matrix.append([0,0,0,1])

        x, y, z = self.x, self.y, self.z
        w = 1.0
        matrix = matrix[0] + matrix[1] + matrix[2] + matrix[3]
        new_x = x * matrix[0] + y * matrix[1] + z * matrix[2] + w * matrix[3]
        new_y = x * matrix[4] + y * matrix[5] + z * matrix[6] + w * matrix[7]
        new_z = x * matrix[8] + y * matrix[9] + z * matrix[10] + w * matrix[11]
        return Vector3(new_x, new_y, new_z)

class Color(Vector3):
    """Stores colors as RGB triplets, based of Vector3"""
    @classmethod
    def from_hex(cls, hex="#000000") -> Color:
        """Creates Color from hexcode"""
        x = int(hex[1:3], 16) / 255.0
        y = int(hex[3:5], 16) / 255.0
        z = int(hex[5:], 16) / 255.0
        return cls(x, y, z)
    
    @classmethod
    def from_RGB(cls, r=0, g=0, b=0) -> Color:
        """Creates Color from RGB"""
        return cls(r / 255, g / 255, b / 255)
    
    def to_RGB(self) -> Color:
        """Returns tuple in 255 RGB form with normalization"""
        return (self*255)//max(*self, 1)

class Point(Vector3):
    """Point stores coordinates of a point in 3D space, based on Vector"""
    pass