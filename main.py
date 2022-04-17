from components import (Vector3, Color, Point, Sphere, Plane, 
            Light, ChequeredMaterial, Material, Scene, Camera)
from engine import RenderEngine
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("imageout", help="Path to output the rendered image")
    args = parser.parse_args()


    # Eye Test case
    CAM_WIDTH = 640
    CAM_HEIGHT = 480
    CAM_SQUARE_SIZE = 0.1
    CAM_FOCAL_DISTANCE = 100
    CAM_EYE = Point(-20, -300, 100)
    CAM_LOOK_AT = Vector3(0, 0, 100)
    CAM_UP = Vector3(0, 0, 1)
    CAMERA = Camera(CAM_HEIGHT, CAM_WIDTH, CAM_SQUARE_SIZE, CAM_FOCAL_DISTANCE, CAM_EYE, CAM_LOOK_AT, CAM_UP)
    OBJECTS = [
        # Blue Sphere 
        Sphere(Point(8., -8., 100), 30., Material(Color.fromHex("#00FFFF"), 0.2)),
        # Black Sphere
        Sphere(Point(25., -25., 100), 8., Material(Color.fromHex("#000000"), 0.2)),
        # Withe Sphere
        Sphere(Point(-10., 10., 100), 50., Material(Color.fromHex("#FFFFFF"), 0.2))
    ]
    LIGHTS = [
        Light(CAM_EYE-(CAM_LOOK_AT.normalize())*100, Color.fromHex('#FFFFFF'))
    ]
    scene = Scene(CAMERA, OBJECTS, LIGHTS, bg_color=Color.fromHex("#191970"))

    # CAM_WIDTH = 1920
    # CAM_HEIGHT = 1080
    # CAM_SQUARE_SIZE = 0.02
    # CAM_FOCAL_DISTANCE = 40
    # CAM_EYE = Point(0, -1, -3)
    # CAM_LOOK_AT = Vector3(0, 20, 100)
    # CAM_UP = Vector3(0, -1, 0)
    # CAMERA = Camera(CAM_HEIGHT, CAM_WIDTH, CAM_SQUARE_SIZE, CAM_FOCAL_DISTANCE, CAM_EYE, CAM_LOOK_AT, CAM_UP)
    # OBJECTS = [
    #     # Floor Plane
    #     Plane(Point(0, 0.5, 0), Vector3(0, 1, 0), ChequeredMaterial(
    #             color1=Color.fromHex("#420500"),
    #             color2=Color.fromHex("#E6B87D"),
    #             ambient=0.2,
    #             reflection=0.2,
    #         )
    #     ),

    #     # Blue ball
    #     Sphere(Point(0.75, -0.1, 1), 0.6, Material(Color.fromHex("#0000FF"))),
    #     # Pink ball
    #     Sphere(Point(-0.75, -0.1, 2.25), 0.6, Material(Color.fromHex("#803980"))),
    #     # Chequered ball
    #     Sphere(Point(0, -0.5, 5.0), 1.0, ChequeredMaterial(
    #             color1=Color.fromHex("#420500"),
    #             color2=Color.fromHex("#E6B87D"),
    #             ambient=0.2,
    #             reflection=0.2,
    #             specular=0.2
    #         )
    #     )
    # ]
    # LIGHTS = [
    #     Light(Point(5, -5, -20), Color.fromHex("#eb4034")),
    #     Light(Point(-5, -10.5, -15), Color.fromHex("#34eb3d"))
    # ]
    # scene = Scene(CAMERA, OBJECTS, LIGHTS, bg_color=Color.fromHex("#87CEEB"))
    
    engine = RenderEngine()
    image = engine.render(scene, True)

    with open(args.imageout, 'w') as img_file:
        image.write_ppm(img_file)
    

if __name__ == "__main__":
    main()