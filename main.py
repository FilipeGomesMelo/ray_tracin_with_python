import argparse

from engine import RenderEngine
from vectors import Vector3, Color, Point
from scene import Scene
from objects3D import Sphere, Plane
from light import Light
from material import ChequeredMaterial, Material

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("imageout", help="Path to output the rendered image")
    args = parser.parse_args()

    WIDTH = 1280
    HEIGHT = 720
    CAMERA = Vector3(0, -0.35, -1)
    OBJECTS = [    
        # Floor Plane
        Plane(Point(0, 0.5, 0), Vector3(0, 1, 0), ChequeredMaterial(
                color1=Color.fromHex("#420500"),
                color2=Color.fromHex("#E6B87D"),
                ambient=0.2,
                reflection=0.2,
            )
        ),
        
        # Blue ball
        Sphere(Point(0.75, -0.1, 1), 0.6, Material(Color.fromHex("#0000FF"))),
        # Pink ball
        Sphere(Point(-0.75, -0.1, 2.25), 0.6, Material(Color.fromHex("#803980"))),
        # Chequered ball
        Sphere(Point(0, -0.5, 5.0), 1.0, ChequeredMaterial(
                color1=Color.fromHex("#420500"),
                color2=Color.fromHex("#E6B87D"),
                ambient=0.2,
                reflection=0.2,
                specular=0.2
            )
        )
    ]
    LIGHTS = [
        Light(Point(1.5, -0.5, -10), Color.fromHex("#FF0000")),
        Light(Point(-0.5, -10.5, 0), Color.fromHex("#00FF00"))
    ]
    scene = Scene(CAMERA, OBJECTS, LIGHTS, WIDTH, HEIGHT, bg_color=Color.fromHex("#87CEEB"))
    engine = RenderEngine()
    image = engine.render(scene, True)

    with open(args.imageout, 'w') as img_file:
        image.write_ppm(img_file)
    

if __name__ == "__main__":
    main()