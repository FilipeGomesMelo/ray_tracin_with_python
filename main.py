import argparse
from camera import Camera

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

    CAM_WIDTH = 640
    CAM_HEIGHT = 480
    CAM_SQUARE_SIZE = 0.1
    CAM_FOCAL_DISTANCE = 100
    CAM_EYE = Point(-20, -300, 100)
    CAM_LOOK_AT = Vector3(0, 0, 100)
    CAM_UP = Vector3(0, 0, 1)
    CAMERA = Camera(CAM_HEIGHT, CAM_WIDTH, CAM_SQUARE_SIZE, CAM_FOCAL_DISTANCE, CAM_EYE, CAM_LOOK_AT, CAM_UP)
    OBJECTS = [    
        Sphere(Point(8., -8., 100), 30., Material(Color.fromHex("#00FFFF"))),
        Sphere(Point(25., -25., 100), 8., Material(Color.fromHex("#000000"))),
        Sphere(Point(-10., 10., 100), 50., Material(Color.fromHex("#FFFFFF")))
    ]
    LIGHTS = [
        Light(CAM_EYE-CAM_LOOK_AT.normalize(), Color.fromHex('#FFFFFF'))
    ]
    scene = Scene(CAMERA, OBJECTS, LIGHTS, bg_color=Color.fromHex("#191970"))
    engine = RenderEngine()
    image = engine.render(scene, True)

    with open(args.imageout, 'w') as img_file:
        image.write_ppm(img_file)
    

if __name__ == "__main__":
    main()