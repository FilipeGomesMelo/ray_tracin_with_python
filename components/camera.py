from components import Point, Vector3

class Camera:
    """3D camera class used for scenes"""
    def __init__(self, 
            v_res: int, h_res: int, square_size: float, focal_distance: float, 
            eye: Point, look_at: Vector3, up: Vector3 = Vector3(0, 1, 0)
        ) -> None:
        self.v_res = v_res
        self.h_res = h_res
        self.square_size = square_size
        self.focal_distance = focal_distance
        self.eye = eye
        self.look_at = look_at
        self.up = up