from objects3D import Object3D
from vectors import Vector3, Color, Point
from ray import Ray
from image import Image
from scene import Scene

class RenderEngine:
    """Renders 3D objects into a 2D image using ray tracing"""

    MAX_DEPTH = 5
    MIN_DISPLACE = 0.001

    def render(self, scene: Scene, show_progess: bool = False) -> Image:
        width = scene.width
        height = scene.height
        aspect_ratio = width / height
        
        x0 = -1.
        x1 = 1.
        x_step = (x1 - x0) / (width - 1)

        y0 = -1. / aspect_ratio
        y1 = 1. / aspect_ratio
        y_step = (y1 - y0) / (height - 1)

        camera = scene.camera
        pixels = Image(width, height)

        for i in range(height):
            y = y0 + i * y_step
            for j in range(width):
                x = x0 + j * x_step
                ray = Ray(camera, Point(x, y) - camera)
                pixels.set_pixel(j, i, self.rayTrace(ray, scene))
            if show_progess:
                print(f"{(i/height) * 100:.2f}%", end='\r')
        return pixels
    
    def rayTrace(self, ray: Ray, scene: Scene, depth=0) -> Color:
        """Traces the ray and finds the color for it"""
        color = Color()
        
        # Finding the nearest object hit by the ray in the scene
        distance_hit, object_hit = self.find_nearest(ray, scene)
        if object_hit is None:
            return scene.bg_color
        
        hit_pos = ray.origin + ray.direction * distance_hit
        hit_normal = object_hit.normal(hit_pos)
        color += self.color_at(object_hit, hit_pos, hit_normal, scene)
        if depth < self.MAX_DEPTH:
            new_ray_pos = hit_pos + hit_normal * self.MIN_DISPLACE
            new_ray_dir = ray.direction - 2 * ray.direction.dotProduct(hit_normal) * hit_normal
            new_ray = Ray(new_ray_pos, new_ray_dir)
            # Attenuating the reflected color by reflection coefficient
            color += self.rayTrace(new_ray, scene, depth+1) * object_hit.material.reflection
        return color
    
    def find_nearest(self, ray: Ray, scene: Scene) -> tuple[float | None, Object3D | None]:
        """Finds the nearest point of intersection of a ray with any object in a scene
        Returns a tuple of distance to the hit point and the object that was hit
        """
        distance_min = None
        object_hit = None
        for obj in scene.objects:
            distance = obj.intersects(ray)
            if distance is not None and (object_hit is None or distance < distance_min):
                distance_min = distance
                object_hit = obj

        return (distance_min, object_hit)
    
    def color_at(self, object_hit, hit_pos: Point, normal: Vector3, scene: Scene) -> Color:
        material = object_hit.material
        obj_color = material.color_at(hit_pos)
        to_cam = scene.camera - hit_pos
        color = material.ambient * Color.fromHex("#000000")
        specular_k = 50
        
        # Calculating lights
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)

            # Diffuse shading (lambert)
            color += (
                obj_color 
                * material.diffuse 
                * max(normal.dotProduct(to_light.direction), 0)
            )
            # Specular shading (Blinn-Phong)
            half_vector = (to_light.direction + to_cam).normalize()
            color += (
                light.color
                * material.specular
                * max(normal.dotProduct(half_vector), 0) ** specular_k
            )

        return color
        