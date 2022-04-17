from utils import build_scene, load_from_json
from engine import RenderEngine
import argparse

def generate_3d_image():
    """
    Receives two arguments:
    - The path to the json file containing the scene information.
    - The path to the output image file.
    Writes the image specified on json to the output file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonpath", help="Path to config file to be loaded")
    parser.add_argument("imageout", help="Path to output the rendered image")
    args = parser.parse_args()

    infos_path = args.jsonpath
    image_path = args.imageout

    infos = load_from_json(infos_path)
    scene = build_scene(infos)

    engine = RenderEngine()
    image = engine.render(scene, True)

    with open(image_path, 'w') as img_file:
        image.write_ppm(img_file)

if __name__ == "__main__":
    generate_3d_image()