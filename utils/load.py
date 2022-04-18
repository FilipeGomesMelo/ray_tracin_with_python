from components import (Vector3, Color, Point, Sphere, Plane, 
    Light, ChequeredMaterial, Material, Scene, Camera, Object3D)
import json

def load_from_json(file_path: str) -> dict:
    """
    Loads a json file and returns a dictionary of its contents.
    """

    with open(file_path) as file:
        infos = json.load(file)
    
    return {
        "cam_width": infos["h_res"],
        "cam_height": infos["v_res"],
        "cam_square_size": infos["square_side"],
        "cam_focal_distance": infos["dist"],
        "cam_eye": tuple(infos["eye"]),
        "cam_look_at": tuple(infos["look_at"]),
        "cam_up": tuple(infos["up"]),
        "bg_color": tuple(infos["background_color"]),
        "objects": infos["objects"],
    }

def identify_object(object_opt: dict, mat_ambient: float = 1,
                    mat_diffuse: float = 1, mat_specular: float = 1, 
                    mat_reflection: float = 0) -> Object3D:
    new_object = None
    color = Color.fromRGB(*object_opt["color"])
    material = Material(color, mat_ambient, mat_diffuse, 
                        mat_specular, mat_reflection)
    if "sphere" in object_opt:
        sphere_options = object_opt["sphere"]
        center = sphere_options["center"]
        radius = sphere_options["radius"]
        new_object = Sphere(Point(*center), radius, material)
    elif "plane" in object_opt:
        plane_options = object_opt["plane"]
        sample = plane_options["sample"]
        normal = plane_options["normal"]
        new_object = Plane(Point(*sample), Vector3(*normal), material)
    return new_object

def build_scene(infos: dict) -> Scene:
    """
    Builds a scene instantiating the Camera, objects and lights
    from the information of a dictionary.
    """
    CAM_WIDTH = infos["cam_width"]
    CAM_HEIGHT = infos["cam_height"]

    # If height is not specified, it`s possible:
    # aspect_ratio = width / height
    # height = width / aspect_ratio

    BG_COLOR = Color.fromRGB(*infos["bg_color"])
    CAM_SQUARE_SIZE = infos["cam_square_size"]
    CAM_FOCAL_DISTANCE = infos["cam_focal_distance"]
    CAM_LOOK_AT = Vector3(*infos["cam_look_at"])
    CAM_EYE = Point(*infos["cam_eye"])
    CAM_UP = Vector3(*infos["cam_up"])

    CAMERA = Camera(CAM_HEIGHT, CAM_WIDTH, CAM_SQUARE_SIZE, 
            CAM_FOCAL_DISTANCE, CAM_EYE, CAM_LOOK_AT, CAM_UP)
    OBJECTS = [identify_object(object_opt) for object_opt in infos["objects"]]
    LIGHTS = [Light(CAM_EYE-(CAM_LOOK_AT.normalize())*100, Color.fromHex('#FFFFFF'))]
    return Scene(CAMERA, OBJECTS, LIGHTS, bg_color = BG_COLOR)