from components import Vector3, Color, Point, Ray, Object3D, Image, Scene

class RenderEngine:
    """Renders 3D objects into a 2D image using ray tracing"""

    MAX_DEPTH = 5
    MIN_DISPLACE = 0.001

    def render(self, scene: Scene, show_progess: bool = False) -> Image:
        width = scene.width
        height = scene.height
        aspect_ratio = width / height
        
        camera = scene.camera
        pixel_size = camera.square_size
        cam_focal_distance = camera.focal_distance
        cam_focus = camera.eye
        cam_look_at = camera.look_at
        up = camera.up

        w = (cam_focus - cam_look_at).normalize()
        u = (up.crossProduct(w)).normalize()

        v = w.crossProduct(u)

        Q_origin = cam_focus - cam_focal_distance*w + pixel_size*(((height)/2)*v-((width)/2)*u)

        pixels = Image(width, height)

        for i in range(0, height):
            for j in range(0, width):
                Q_current = Q_origin + pixel_size * (j * u - i * v)
                ray = Ray(cam_focus, (Q_current-cam_focus).normalize())
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
        to_cam = scene.camera.eye - hit_pos
        color = material.ambient * (obj_color.kronProduct(Color.fromHex("#FFFFFF")))
        specular_k = 50
        
        # Calculating lights
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)
            distance_hit, object_hit = self.find_nearest(to_light, scene)

            if object_hit != None and 0 < distance_hit < (light.position - hit_pos).magnitude():
                continue

            # Diffuse shading (lambert)
            color += (
                (obj_color.kronProduct(light.color))
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
        