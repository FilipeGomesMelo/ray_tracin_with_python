from components import Point, Vector3

class Camera:
    """3D camera class used for scenes"""
    def __init__(self, 
            v_res: int, h_res: int, pixel_size: float, focal_distance: float, 
            eye: Point, look_at: Point, up: Vector3 = Vector3(0, 1, 0)
        ) -> None:
        self.v_res = v_res
        self.h_res = h_res
        self.pixel_size = pixel_size
        self.focal_distance = focal_distance
        self.eye = eye
        self.look_at = look_at
        self.up = up