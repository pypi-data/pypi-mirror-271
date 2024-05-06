
import cv2
import numpy as np
from typing import Iterable


def scalePointSet(point_set: np.ndarray, rectangle: np.ndarray,
                  scale_abs:  list | tuple | np.ndarray | None = None,
                  scale_rel:  list | tuple | np.ndarray | None = None):

    rect_x, rect_y, rect_w, rect_h = rectangle
    cent_x, cent_y = rect_x+rect_w*0.5, rect_y+rect_h*0.5
    fix_abs = 1
    if scale_abs is not None:
        if not isinstance(scale_abs, Iterable):
            scale_abs = [scale_abs]
        scale_abs = scale_abs*4
        scale_abs = scale_abs[:4]
        new_w = rect_w + scale_abs[0]*2
        new_h = rect_h + scale_abs[1]*2
        fx = new_w / rect_w
        fy = new_h / rect_h
    elif scale_rel is not None:
        if not isinstance(scale_rel, Iterable):
            scale_rel = [scale_rel]
        scale_rel = scale_rel*4
        scale_rel = scale_rel[:4]
        fx = 1.0 + scale_rel[0]
        fy = 1.0 + scale_rel[1]
    else:
        new_w = rect_w - fix_abs*2
        new_h = rect_h - fix_abs*2
        fx = new_w / rect_w
        fy = new_h / rect_h
    m_to_00 = np.array([
        [1, 0, -cent_x],
        [0, 1, -cent_y],
        [0, 0, 1]
    ], dtype=np.float64)
    m_to_ori = np.array([
        [1, 0, cent_x],
        [0, 1, cent_y],
        [0, 0, 1]
    ], dtype=np.float64)
    m_scale = np.array([
        [fx, 0, 0],
        [0, fy, 0],
        [0, 0, 1]
    ], dtype=np.float64)
    m = np.matmul(m_scale, m_to_00)
    m = np.matmul(m_to_ori, m)[:2]
    return cv2.transform(point_set, m)

