from __future__ import annotations

from light import Light
from objects3D import Object3D
from vectors import Color, Vector3


class Scene:
    """All the information needed to render a image with the ray tracing engine
    Has a camera, a list of objects, a width and a height
    """
    def __init__(
            self, camera: Vector3, objects: list[Object3D], lights: Light[Light], 
            width: float, height: float, bg_color: Color=Color()
        ) -> None:
        self.camera = camera
        self.objects = objects
        self.lights = lights
        self.width = width
        self.height = height
        self.bg_color = bg_color