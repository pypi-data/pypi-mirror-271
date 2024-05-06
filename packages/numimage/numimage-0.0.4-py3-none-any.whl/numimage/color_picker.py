
from proc_color import pickColor, rgb2cymk, rgb2hsv,RGB_to_Hex
import numpy as np

def pick_color(input: dict, output: dict) -> bool:
    """
    output:[
        {
            "rgb":list
            "cmyk":list
            "hsv":list
            "hex":str
        },
        {
            "rgb":list
            "cmyk":list
            "hsv":list
            "hex":str
        },
        {
            "rgb":list
            "cmyk":list
            "hsv":list
            "hex":str
        }
    ]
    
    """
    use_material_pack: bool = input['use_material_pack']
    images: list[np.ndarray] = input['images']
    image: np.ndarray = images[0]


    colors_bgr = pickColor(image)["colors"]
    all_colors = list()
    for i in range(0, colors_bgr.shape[0]):
        singlecolor = dict()
        color = colors_bgr[i].tolist()
        color[0], color[2] = color[2], color[0]

        singlecolor["rgb"] = color
        singlecolor["hex"] = RGB_to_Hex(color)
        R, G, B = color[0] / 255, color[1] / 255, color[2] / 255
        C, Y, M, K = rgb2cymk(R, G, B)
        H, S, V = rgb2hsv(R, G, B)

        singlecolor["cmyk"] = [C,M,Y,K]
        singlecolor["hsv"]=[H,S,V]

        all_colors.append(singlecolor)
    

    output.clear()
    output['colors'] = all_colors


    return True