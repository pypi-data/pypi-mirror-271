import numpy as np
import svg.path
import re
import math

def polar_to_cartesian(r,theta):
    return r * math.cos(math.radians(theta)),r * math.sin(math.radians(theta))

def getsvgrectfunc(path,n=100):
    pp = svg.path.parse_path(path)
    points = [pp.point(pos) for pos in np.linspace(0, 1, n)]
    xx,yy = [],[]
    for z in points:
        pattern = r'-?\d+\.*\d*'

        matches = re.findall(pattern, str(z))
        x, y = polar_to_cartesian(float(matches[0]),float(matches[1]))
        print(x,y)
        xx.append(math.ceil(x))
        yy.append(math.ceil(y))
    
    return min(xx),min(yy),max(xx),max(yy)

from svg.path import parse_path

def calculate_path_bbox(svg_path_data):
    path = parse_path(svg_path_data)
    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')
    for segment in path:
        if segment.start.real < min_x:
            min_x = segment.start.real
        if segment.start.imag < min_y:
            min_y = segment.start.imag
        if segment.start.real > max_x:
            max_x = segment.start.real
        if segment.start.imag > max_y:
            max_y = segment.start.imag

        if hasattr(segment, 'end'):
            if segment.end.real < min_x:
                min_x = segment.end.real
            if segment.end.imag < min_y:
                min_y = segment.end.imag
            if segment.end.real > max_x:
                max_x = segment.end.real
            if segment.end.imag > max_y:
                max_y = segment.end.imag
    width = max_x - min_x
    height = max_y - min_y
    
    return min_x,min_y,max_x,max_y
    return {"x": min_x, "y": min_y, "width": width, "height": height}


def mergePath(pathList:list[str]) -> str:
    path = ""
    for i in pathList:
        path += i + " "

    return path