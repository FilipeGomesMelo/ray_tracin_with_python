from __future__ import annotations
from io import TextIOWrapper

from components import Color

class Image:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.pixels: list[list[Color]] = [[Color() for _ in range(width)] for _ in range(height)]
    
    def set_pixel(self, x: int, y: int, color: Color) -> None:
        """Sets color of pixel on column x and roll y as color, x=0 and y=0 it the top left of the image"""
        self.pixels[y][x] = color

    def write_ppm(self, img_file: TextIOWrapper) -> None:
        """Writes image on a ppm file"""
        # Header of file
        img_file.write("P3 {} {}\n255\n".format(self.width, self.height))

        # Writes each pixel
        for row in self.pixels:
            for color in row:
                img_file.write(
                    '{} {} {} '.format(
                        *color.to_RGB()
                    )
                )
            img_file.write('\n')