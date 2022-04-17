from __future__ import annotations
from components import Camera, Light, Object3D, Color


class Scene:
    """All the information needed to render a image with the ray tracing engine
    Has a camera, a list of objects, a width and a height
    """
    def __init__(
            self, camera: Camera, objects: list[Object3D], lights: Light[Light], bg_color: Color=Color()
        ) -> None:
        self.camera = camera
        self.objects = objects
        self.lights = lights
        self.width = camera.h_res
        self.height = camera.v_res
        self.bg_color = bg_color