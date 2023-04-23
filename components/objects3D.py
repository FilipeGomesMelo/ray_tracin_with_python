from __future__ import annotations
from abc import abstractmethod
from components import Material, Vector3, Point, Ray, LinearTransformationsMixin
import math

class Object3D(LinearTransformationsMixin):
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


class BezierCurve:
    def __init__(self, control_points: list[Point]):
        self.control_points = control_points

    def __call__(self, t: float) -> Point:
        n = len(self.control_points) - 1
        point = Vector3()
        for i in range(n + 1):
            binomial = math.comb(n, i)
            basis = binomial * (1 - t) ** (n - i) * t ** i
            point += basis * self.control_points[i]
        return point


class RevolutionSurface(Object3D):
    def __init__(self, control_points: list[Point], resolution: int, point: Point, vector: Vector3, material: Material):
        super().__init__(material)
        self.bezier_curve = BezierCurve(control_points)
        self.point = point
        self.vector = vector
        self.triangle_mesh = self.generate_mesh(resolution)

    def evaluate_point(self, u, v):
        """Evaluate a point on the revolution surface at (u, v)"""
        point_on_curve = self.bezier_curve(u)

        # Rotate the point around the line
        theta = math.degrees(2 * math.pi * v)
        point_on_curve.rotate(self.point, self.vector, theta)

        return point_on_curve.rotate(self.point, self.vector, theta)

    def generate_mesh(self, resolution):
        """Generate a triangle mesh for the revolution surface"""
        vertices = []
        indices = []

        # Generate the vertices and normals
        for i in range(resolution):
            u = i / (resolution - 1)
            for j in range(resolution):
                v = j / (resolution - 1)
                point = self.evaluate_point(u, v)
                vertices.append(point)

        # Generate the indices for the triangle mesh
        for i in range(resolution - 1):
            for j in range(resolution - 1):
                a = i * resolution + j
                b = i * resolution + j + 1
                c = (i + 1) * resolution + j + 1
                d = (i + 1) * resolution + j
                indices.extend([[a, b, c], [a, c, d]])

        return TriangleMesh(vertices, indices, self.material)

    def intersects(self, ray: Ray) -> "tuple[float, Vector3] | tuple[None, None]":
        return self.triangle_mesh.intersects(ray)

    def _get_normal(self, triangle: Triangle) -> Vector3:
        return self.triangle_mesh._get_normal(triangle)