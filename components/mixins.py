from abc import abstractmethod
import math

class LinearTransformationsMixin:
    @abstractmethod
    def transform(self, matrix: list[list[float]]) -> any:
        """Returns the tranformed object using a 3x3 or 4x4 matrix"""
        pass

    def translate(self, vector) -> any:
        """Returns the object tranlated by a vector"""
        translation_matrix = [
            [1, 0, 0, vector.x],
            [0, 1, 0, vector.y],
            [0, 0, 1, vector.z],
            [0, 0, 0, 1],
        ]
        return self.transform(translation_matrix)

    def rotate(self, point, vector, angle: float) -> any:
        """Return the object after being rotated by angle(degrees) around the axis defined by a point and a vector clockwise"""
        # Convert angle from degrees to radians
        angle = math.radians(angle)
        
        # Normalize the axis vector
        axis = vector.normalize()
        
        # Calculate the rotation matrix
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        ux = axis.x
        uy = axis.y
        uz = axis.z
        rot_matrix = [
            [cos_a + ux**2*(1-cos_a), ux*uy*(1-cos_a) - uz*sin_a, ux*uz*(1-cos_a) + uy*sin_a, 0],
            [uy*ux*(1-cos_a) + uz*sin_a, cos_a + uy**2*(1-cos_a), uy*uz*(1-cos_a) - ux*sin_a, 0],
            [uz*ux*(1-cos_a) - uy*sin_a, uz*uy*(1-cos_a) + ux*sin_a, cos_a + uz**2*(1-cos_a), 0],
            [0, 0, 0, 1]]

        to_origin_matrix = [
            [1, 0, 0, -point.x],
            [0, 1, 0, -point.y],
            [0, 0, 1, -point.z], 
            [0, 0, 0, 1]]

        back_from_origin_matrix = [
            [1, 0, 0, point.x],
            [0, 1, 0, point.y],
            [0, 0, 1, point.z], 
            [0, 0, 0, 1]]

        def matrix_multiply(A, B):
            m = len(A)
            n = len(B[0])
            product = []
            for i in range(m):
                row = []
                for j in range(n):
                    element = 0
                    for k in range(len(B)):
                        element += A[i][k] * B[k][j]
                    row.append(element)
                product.append(row)
            return product

        final_matrix = matrix_multiply(back_from_origin_matrix, matrix_multiply(rot_matrix, to_origin_matrix))

        return self.transform(final_matrix)

    def scale(self, vector) -> any:
        distotion_matrix = [
            [vector.x, 0, 0, 0],
            [0, vector.y, 0, 0],
            [0, 0, vector.z, 0],
            [0, 0, 0, 1]
        ]
        return self.transform(distotion_matrix)

    def reflect(self, point, normal) -> any:
        d = -(normal ^ point)
        normal = normal
        reflection_matrix = [
            [1 - 2 * normal.x ** 2, 0 - 2 * normal.x * normal.y, 0 - 2 * normal.x * normal.z, -2 * d * normal.x],
            [- 2 * normal.x * normal.y, 1 - 2 * normal.y **2, 0 - 2 * normal.y * normal.z, -2 * d * normal.y],
            [0 - 2 * normal.x * normal.z, 0 - 2 * normal.z * normal.y, 1 - 2 * normal.z ** 2, -2 * d * normal.z],
            [0, 0, 0, 1]
        ]
        return self.transform(reflection_matrix)