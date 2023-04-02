from utils import build_scene, load_from_json
from components.image import Image
from engine import RenderEngine
import argparse

def generate_3d_image(json_path: str = "", image_out: str = "out.ppm", 
                      return_image: bool = False) -> Image:
    """
    Receives two arguments:
    - The path to the json file containing the scene information.
    - The path to the output image file.
    Writes the image specified on json to the output file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonpath", default = json_path, nargs='?',
                const=1, help="Path to config file to be loaded")
    parser.add_argument("imageout", default = image_out, nargs='?',
                const=1, help="Path to output the rendered image")
    args = parser.parse_args()

    infos_path = args.jsonpath
    image_path = args.imageout

    if infos_path == "":
        print("No json file specified. Run with -h for help.")
        return

    infos = load_from_json(infos_path)
    scene = build_scene(infos)

    engine = RenderEngine()
    image = engine.render(scene, True, 0)
    if return_image: return image

    with open(image_path, 'w') as img_file:
        image.write_ppm(img_file)

if __name__ == "__main__":
    generate_3d_image()