from components import Color, Point

class Material:
    """Material has color and properties that define how light interacts with it"""
    
    def __init__(self, color=Color.fromHex('#FFFFFF'), ambient=0.05, diffuse=1.0, specular=1.0, reflection=0.5) -> None:
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
    
    def color_at(self, postion: Point) -> Color:
        """Returns the color of the material in a given point in space"""
        return self.color

class ChequeredMaterial(Material):
    """Material with chess board pattern using two colors"""

    def __init__(
        self, color1=Color.fromHex('#FFFFFF'), color2=Color.fromHex('#000000'),
        ambient=0.05, diffuse=1, specular=1, reflection=0.5
    ) -> None:
        self.color1 = color1
        self.color2 = color2
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
    
    def color_at(self, position: Point) -> Color:
        """Returns the color of the material in a given point in space"""
        if int((position.y + 5.0) * 3.0) % 2:
            if int((position.x + 5.0) * 3.0) % 2 == int((position.z + 5.0) * 3.0) % 2:
                return self.color1
            else:
                return self.color2
        else:
            if int((position.x + 5.0) * 3.0) % 2 == int((position.z + 5.0) * 3.0) % 2:
                return self.color2
            else:
                return self.color1