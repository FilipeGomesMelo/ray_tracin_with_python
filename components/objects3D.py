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
    
    def intersects(self, ray: Ray) -> "float | None":
        """Checks if a ray intersects the Object3D.
        Returns distance to the closest intersection if the ray does intersect, returns None if it does not"""
        pass

    def normal(self, surface_point: Point) -> Vector3:
        """Returns the normal of the Object3D surface in a given point"""
        pass

class Sphere(Object3D):
    """3D sphere shape, has center, radius and material"""
    def __init__(self, center: Point, radius: float, material: Material) -> None:
        super().__init__(material)
        self.center = center
        self.radius = radius
    
    def __str__(self) -> str:
        return f'''-Sphere:
        \tCenter: {self.center}
        \tRadius: {self.radius}'''

    def intersects(self, ray: Ray) -> "float | None":
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
                return distance
            distance = (-b + math.sqrt(discriminant)) / 2
            if distance > 0.001:
                return distance
        return None
    
    def normal(self, surface_point: Point) -> Vector3:
        """Returns surface normal to the point on the sphere's surface"""
        return (surface_point-self.center).normalize()


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
        self._normal = normal.normalize()
    
    def __str__(self) -> str:
        return f'''-Plane:
        \ point: {self.point}
        \ normal: {self._normal}'''


    def intersects(self, ray: Ray) -> "float | None":
        """Checks if a ray intersects the plane. Returns distance to intersection if the ray does intersect, returns None if it does not"""
        if abs(self._normal ^ ray.direction) >= 0.001:
            distance = (self._normal ^ (self.point - ray.origin))/(self._normal ^ ray.direction)
            if distance > 0.001:
                return distance
                
        return None
    
    # surface_point is only here so we can interact with the plane the same way we would with a sphere
    def normal(self, surface_point: Point=None) -> Vector3:
        """Returns surface normal, same normal for any surface_point"""
        return self._normal