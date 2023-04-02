from components import (Vector3, Color, Point, Sphere, Plane, Triangle,
    Light, ChequeredMaterial, Material, Scene, Camera, Object3D, TriangleMesh)
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
        "ambient_light": tuple(infos.get("ambient_light", (255, 255, 255))),
        "lights": infos.get("lights", []),
        "max_depth": infos.get("max_depth", 5)
    }

def identify_object(object_opt: dict) -> "Object3D | None":
    new_object = None
    
    ambient: float = object_opt.get("ka", 0.05)
    diffuse: float = object_opt.get("kd", 1)
    specular: float = object_opt.get("ks", 1)
    phong: float =  object_opt.get("exp", 50)
    reflection: float = object_opt.get("kr", 0.5)
    transmission: float = object_opt.get("kt", 0)
    index_of_refraction: float = object_opt.get("index_of_refraction", 1)

    color = Color.from_RGB(*object_opt["color"])
    material = Material(color, ambient, diffuse, 
                        specular, reflection, phong, 
                        transmission, index_of_refraction)

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
    elif "triangle" in object_opt:
        triangle_options = object_opt["triangle"]
        vertex_0 = Point(*triangle_options[0])
        vertex_1 = Point(*triangle_options[1])
        vertex_2 = Point(*triangle_options[2])
        new_object = Triangle(vertex_0, vertex_1, vertex_2, material)
    elif "triangle_mesh" in object_opt:
        triangle_mesh_options = object_opt["triangle_mesh"]
        vertices = [Point(a, b, c) for a, b, c in triangle_mesh_options["verteces"]]
        triangles = [(a - 1, b - 1, c - 1) for a, b, c in triangle_mesh_options["triangle_indexes"]]
        new_object = TriangleMesh(vertices, triangles, material)
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

    CAM_FOCAL_DISTANCE = infos["cam_focal_distance"]
    CAM_LOOK_AT = Point(*infos["cam_look_at"])
    BG_COLOR = Color.from_RGB(*infos["bg_color"])
    CAM_SQUARE_SIZE = infos["cam_square_size"]
    CAM_EYE = Point(*infos["cam_eye"])
    CAM_UP = Vector3(*infos["cam_up"])

    CAMERA = Camera(CAM_HEIGHT, CAM_WIDTH, CAM_SQUARE_SIZE, 
            CAM_FOCAL_DISTANCE, CAM_EYE, CAM_LOOK_AT, CAM_UP)
    OBJECTS = [identify_object(object_opt) for object_opt in infos["objects"]]
    
    AMBIENT_COLOR = Color.from_RGB(*infos["ambient_light"])

    LIGHTS = [
        Light(Point(*light["position"]), Color.from_RGB(*light["intensity"])) 
        for light in infos.get("lights", [])
    ]

    if len(LIGHTS) == 0:
        LIGHTS.append(Light(CAM_EYE, Color.from_hex("#FFFFFF")))
    MAX_DEPTH = infos.get("max_depth", 5)
    return Scene(CAMERA, OBJECTS, LIGHTS, AMBIENT_COLOR, bg_color = BG_COLOR, max_depth=MAX_DEPTH)