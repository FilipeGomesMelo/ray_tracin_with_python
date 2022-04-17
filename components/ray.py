from components import Vector3, Point

class Ray:
    """A half-line with an Point as its Origin and a normalized Vector3 as its direction"""
    def __init__(self, origin: Point, direction: Vector3) -> None:
        self.origin = origin
        self.direction = direction.normalize()
    
    def __str__(self) -> str:
        return f'(Origin: {self.origin}, Direction: {self.direction})'