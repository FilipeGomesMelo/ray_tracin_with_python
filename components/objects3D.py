from __future__ import annotations
from abc import abstractmethod
from components import Material, Vector3, Point, Ray
import math

class Object3D:
    """Abstract class for 3D objects used in the Rendering Engine
    
    Requirements:

    - Material attribute

    - intersects method
    
    - normal method

    """
    def __init__(self, material: Material) -> None:
        self.material = material
    
    @abstractmethod
    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        """Checks if a ray intersects the Object3D.
        Returns distance to the closest intersection if the ray does intersect, returns None if it does not"""
        pass

    @abstractmethod
    def _get_normal(self) -> Vector3:
        """Returns the normal of the Object3D surface in a given point"""
        pass

    @abstractmethod
    def transform(self, matrix: list[list[float]]) -> Object3D:
        """Returns the tranformed object using a 3x3 or 4x4 matrix"""
        pass

    def translate(self, vector: Vector3) -> Object3D:
        """Returns the object tranlated by a vector"""
        translation_matrix = [
            [1, 0, 0, vector.x],
            [0, 1, 0, vector.y],
            [0, 0, 1, vector.z],
            [0, 0, 0, 1],
        ]
        return self.transform(translation_matrix)

    def rotate(self, vector: Vector3, angle: float, point: Point = Point(0, 0, 0)) -> Object3D:
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

    def scale(self, vector: Vector3) -> Object3D:
        distotion_matrix = [
            [vector.x, 0, 0, 0],
            [0, vector.y, 0, 0],
            [0, 0, vector.z, 0],
            [0, 0, 0, 1]
        ]
        return self.transform(distotion_matrix)

    def reflect(self, point: Point, normal: Vector3) -> Object3D:
        d = -(normal ^ point)
        normal = normal
        reflection_matrix = [
            [1 - 2 * normal.x ** 2, 0 - 2 * normal.x * normal.y, 0 - 2 * normal.x * normal.z, -2 * d * normal.x],
            [- 2 * normal.x * normal.y, 1 - 2 * normal.y **2, 0 - 2 * normal.y * normal.z, -2 * d * normal.y],
            [0 - 2 * normal.x * normal.z, 0 - 2 * normal.z * normal.y, 1 - 2 * normal.z ** 2, -2 * d * normal.z],
            [0, 0, 0, 1]
        ]
        return self.transform(reflection_matrix)

class Sphere(Object3D):
    """3D sphere shape, has center, radius and material"""
    def __init__(self, center: Point, radius: float, material: Material) -> None:
        super().__init__(material)
        self.center = center
        self.radius = radius
    
    def __str__(self) -> str:
        return '-Sphere:' \
        f'\tCenter: {self.center}' \
        f'\tRadius: {self.radius}'

    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        """Checks if a ray intersects the sphere.
        Returns distance to intersection if the ray does intersect, returns None if it does not"""
        sphere_to_ray = ray.origin - self.center
        
        # a = 1
        b = 2 * (ray.direction ^ sphere_to_ray)
        c = (sphere_to_ray ^ sphere_to_ray) - self.radius ** 2
        discriminant = (b**2) - (4*c)

        if discriminant >= 0:
            distance = (-b - math.sqrt(discriminant)) / 2
            if distance > 0.001:
                hit_point = ray.origin + ray.direction * distance
                return distance, self._get_normal(hit_point)
            distance = (-b + math.sqrt(discriminant)) / 2
            if distance > 0.001:
                hit_point = ray.origin + ray.direction * distance
                return distance, self._get_normal(hit_point)
        return None, None
    
    def _get_normal(self, surface_point: Point) -> Vector3:
        """Returns surface normal to the point on the sphere's surface"""
        return (surface_point-self.center).normalize()

    def transform(self, matrix: list[list[float]]) -> Object3D:
        new_center = self.center.transform(matrix)
        return Sphere(new_center, self.radius, self.material)


class Plane(Object3D):
    """3D plane shape, has point that belongs to the plane and a normal vector"""
    def __init__(self, point: Point, normal: Vector3, material: Material) -> None:
        """
        Point is any point belonging to the plane
        normal is a Vector3 with the direction of the plane's normal
        Material defines how it interacts with light
        """
        super().__init__(material)
        self.point = point
        self.normal = normal.normalize()
    
    def __str__(self) -> str:
        return f'-Plane:' \
        f'\t point: {self.point}' \
        f'\t normal: {self.normal}'

    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        """Checks if a ray intersects the plane. Returns distance to intersection if the ray does intersect, returns None if it does not"""
        if abs(self.normal ^ ray.direction) >= 0.001:
            distance = (self.normal ^ (self.point - ray.origin))/(self.normal ^ ray.direction)
            if distance > 0.001:
                return distance, self._get_normal()
                
        return None, None
    
    # surface_point is only here so we can interact with the plane the same way we would with a sphere
    def _get_normal(self) -> Vector3:
        """Returns surface normal, same normal for any surface_point"""
        return self.normal

    def transform(self, matrix: list[list[float]]) -> Object3D:
        new_point = self.point.transform(matrix)
        new_normal = (self.normal + self.point).transform(matrix) - new_point
        return Plane(new_point, new_normal, self.material)

class Triangle(Object3D):
    """3D triangle shape, defined by tree points"""
    def __init__(self, vertex_0: Point, vertex_1: Point, vertex_2: Point, material: Material) -> None:
        """
        Point is any point belonging to the plane
        normal is a Vector3 with the direction of the plane's normal
        Material defines how it interacts with light
        """
        super().__init__(material)
        self.vertex_0 = vertex_0
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2
        edge1 = self.vertex_1 - self.vertex_0
        edge2 = self.vertex_2 - self.vertex_0
        self.normal = edge1.cross_product(edge2).normalize()
    
    def __str__(self) -> str:
        return '-Triangle:' \
        f'\t vertex_0: {self.vertex_0}' \
        f'\t vertex_1: {self.vertex_1}' \
        f'\t vertex_2: {self.vertex_2}'


    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        """Checks if a ray intersects the triangle. Returns distance to intersection if the ray does intersect, returns None if it does not"""
        EPSILON = 0.001
        edge1 = self.vertex_1 - self.vertex_0
        edge2 = self.vertex_2 - self.vertex_0
        h = ray.direction.cross_product(edge2)
        a = edge1.dot_product(h)
        if -EPSILON < a < EPSILON:
            return None, None
        f = 1/a
        s = ray.origin - self.vertex_0
        u = f * s.dot_product(h)
        if u < 0.0 or u > 1.0:
            return None, None
        q = s.cross_product(edge1)
        v = f * ray.direction.dot_product(q)
        if v < 0.0 or u + v > 1.0:
            return None, None
        t = f * edge2.dot_product(q)
        if (t > EPSILON):
            return t, self._get_normal()
                
        return None, None
    
    def _get_normal(self) -> Vector3:
        """Returns surface normal, same normal for any surface_point"""
        return self.normal

    def transform(self, matrix: list[list[float]]) -> Object3D:
        new_vertex_0 = self.vertex_0.transform(matrix)
        new_vertex_1 = self.vertex_1.transform(matrix)
        new_vertex_2 = self.vertex_2.transform(matrix)
        return Triangle(new_vertex_0, new_vertex_1, new_vertex_2, self.material)

class TriangleMesh(Object3D):
    def __init__(self, list_vertices: list[Point], list_triangles: list[tuple[int, int, int]], material: Material) -> None:
        super().__init__(material)
        self.list_vertices = list_vertices
        self.list_triangles = list_triangles

    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        distance_min = None
        hit_normal = None
        for triangle_data in self.list_triangles:
            vertecies = (
                self.list_vertices[triangle_data[0]],
                self.list_vertices[triangle_data[1]],
                self.list_vertices[triangle_data[2]]
            )
            triangle = Triangle(*vertecies, self.material)
            distance, normal = triangle.intersects(ray)
            if distance is not None and (distance_min is None or distance < distance_min):
                distance_min = distance
                hit_normal = normal

        return distance_min, hit_normal

    def _get_normal(self, triangle: Triangle) -> Vector3:
        return triangle._get_normal()

    def transform(self, matrix: list[list[float]]) -> Object3D:
        new_verticies = []
        for vertex in self.list_vertices:
            new_vertex = Vector3(*vertex).transform(matrix)
            new_verticies.append(new_vertex)
        return TriangleMesh(new_verticies, self.list_triangles, self.material)