from math import sqrt
from components import Vector3, Color, Point, Ray, Object3D, Image, Scene

class RenderEngine:
    """Renders 3D objects into a 2D image using ray tracing"""

    MAX_DEPTH = 5
    MIN_DISPLACE = 0.001

    def render(self, scene: Scene, show_progess: bool = False) -> Image:
        width = scene.width
        height = scene.height
        
        camera = scene.camera
        pixel_size = camera.pixel_size
        cam_focal_distance = camera.focal_distance
        cam_focus = camera.eye
        cam_look_at = camera.look_at
        up = camera.up

        w = (cam_focus - cam_look_at).normalize()
        u = (up.crossProduct(w)).normalize()
        v = w.crossProduct(u)

        z_vector = cam_focus - cam_focal_distance * w
        y_vector = (height / 2) * v
        x_vector = (width / 2 ) * u
        image_center = z_vector + pixel_size * (y_vector - x_vector)

        pixels = Image(width, height)

        for y in range(0, height):
            for x in range(0, width):
                position = image_center + pixel_size * (x * u - y * v)
                ray_direction = (position - cam_focus).normalize()
                ray = Ray(cam_focus, ray_direction)
                pixels.set_pixel(x, y, self.rayTrace(ray, scene))
            if show_progess:
                print(f"{(y / height) * 100:.2f}%", end='\r')
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
            material_hit = object_hit.material
            # Checks if object is reflective
            if material_hit.reflection > 0:
                # Note to self: we might want to do this as a object3D method that returns
                # the reflected ray or None if the ray does not reflect
                new_ray_pos = hit_pos + hit_normal * self.MIN_DISPLACE
                new_ray_dir = ray.direction - 2 * ray.direction.dotProduct(hit_normal) * hit_normal
                new_ray = Ray(new_ray_pos, new_ray_dir)
                # Attenuating the reflected color by reflection coefficient
                color += self.rayTrace(new_ray, scene, depth+1) * material_hit.reflection
            # Checks if object is not opaque
            if material_hit.refraction > 0:
                # Note to self: we might want to do this as a object3D method that returns
                # the refracted ray or None if the ray does not refract

                normal = hit_normal
                omega = -ray.direction
                relative_refraction = material_hit.refraction
                # Checks if ray is leaving the object, is so, invert normal and coefficient (air coefficient is 1)
                if normal ^ omega < 0:
                    relative_refraction = 1/material_hit.refraction
                    normal = -hit_normal

                # delta for the refraction formula
                delta = 1 - (1/(relative_refraction**2)) * (1 - (normal ^ omega)**2)

                # if delta is less than 0, total refraction occurs and we have no new ray
                if delta >= 0:
                    inverse_refraction = 1 / relative_refraction

                    # generating the new ray
                    new_ray_dir = - inverse_refraction * omega - (sqrt(delta) - inverse_refraction * (normal ^ omega)) * normal
                    new_ray_pos = hit_pos - normal * self.MIN_DISPLACE
                    new_ray = Ray(new_ray_pos, new_ray_dir)
                    # Attenuating the ray color by transmission coefficient
                    color += self.rayTrace(new_ray, scene, depth+1) * material_hit.transmission
                
        return color
    
    def find_nearest(self, ray: Ray, scene: Scene) -> "tuple[float | None, Object3D | None]":
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
    
    def color_at(self, object_hit: Object3D, hit_pos: Point, normal: Vector3, scene: Scene) -> Color:
        material = object_hit.material
        obj_color = material.color_at(hit_pos)
        color = material.ambient * (obj_color.kronProduct(Color.fromHex("#FFFFFF")))
        phong_coefficient = material.phong
        
        # Calculating lights
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)
            distance_hit, object_hit = self.find_nearest(to_light, scene)

            if object_hit != None and 0 < distance_hit < to_light.direction ^ (light.position - hit_pos):
                continue

            # Diffuse shading (lambert)
            color += (
                (obj_color.kronProduct(light.color))
                * material.diffuse 
                * max(normal ^ to_light.direction, 0)
            )
            # Specular shading (Blinn-Phong)
            half_vector = 2 * (normal ^ to_light.direction) * normal - to_light.direction
            color += (
                light.color
                * material.specular
                * max(normal ^ half_vector, 0) ** phong_coefficient
            )

        return color
        