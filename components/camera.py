from __future__ import annotations
from components import Point, Vector3, Object3D, Ray

class Camera(Object3D):
    """3D camera class used for scenes"""
    def __init__(self, 
            v_res: int, h_res: int, pixel_size: float, focal_distance: float, 
            eye: Point, look_at: Point, up: Vector3 = Vector3(0, 1, 0)) -> None:
        self.v_res = v_res
        self.h_res = h_res
        self.pixel_size = pixel_size
        self.focal_distance = focal_distance
        self.eye = eye
        self.look_at = look_at
        self.up = up

    def intersects(self, ray: Ray) -> tuple[float, Vector3] | tuple[None, None]:
        return None, None

    def _get_normal(self) -> Vector3:
        return None

    def transform(self, matrix: list[list[float]]) -> Object3D:
        new_eye = self.eye.transform(matrix)
        new_up = (self.up + self.eye).transform(matrix) - new_eye
        return Camera(self.v_res, self.h_res, self.pixel_size, self.focal_distance, new_eye, self.look_at, new_up)