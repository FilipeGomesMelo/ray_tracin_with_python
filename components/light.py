from components import Color, Point

class Light:
    """Point light source of a certain color"""

    def __init__(self, position: Point, color=Color.fromHex('#FFFFFF')) -> None:
        self.position = position
        self.color = color
    
    def __str__(self) -> str:
        return f'(Position: {self.position}, Color: {self.color})'