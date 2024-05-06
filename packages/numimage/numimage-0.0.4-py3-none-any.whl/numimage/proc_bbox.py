


from tqdm import tqdm
import os
import numpy as np
from PIL import Image
import torch



import cv2
import time
import copy
from ultralytics.engine.results import Results
import shutil


def bboxes_intersection_baseMin(bboxes_a, bboxes_b):
    
    if bboxes_a.shape[1] != 4 or bboxes_b.shape[1] != 4:
        raise IndexError

    tl = torch.max(bboxes_a[:, None, :2], bboxes_b[None, :, :2]) 
    br = torch.min(bboxes_a[:, None, 2:], bboxes_b[None, :, 2:])  
    area_a = torch.prod(bboxes_a[:, 2:] - bboxes_a[:, :2], 1) 
    area_b = torch.prod(bboxes_b[:, 2:] - bboxes_b[:, :2], 1)  

    is_overlapped = (tl < br).type(tl.dtype).prod(dim=2)  
    area_overlap = torch.prod(br-tl, 2) * is_overlapped  
    min_area = torch.minimum(area_a[:, None], area_b[None, :])  
    overlap_ratio = area_overlap/min_area

    return overlap_ratio, area_overlap


def objectBoxes(image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if image is None or 0 == image.size:
        return None, None

    if image.ndim != 2:
        return None, None

    num, labels, stats, centroids = cv2.connectedComponentsWithStats(image)
    stats = stats[1:]
    if len(stats) == 0:
        return None, None

    xywh = stats[:, :4].copy()
    xyxy = xywh.copy()
    xyxy[:, 2] += xyxy[:, 0]
    xyxy[:, 3] += xyxy[:, 1]
    return xyxy, xywh


def filterBoxes(exist_xywh: list, xyxys: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    exist_xyxy = np.array(exist_xywh).reshape((1, 4))
    exist_xyxy[:, 2] += exist_xyxy[:, 0]
    exist_xyxy[:, 3] += exist_xyxy[:, 1]
    areas = (xyxys[:, 2] - xyxys[:, 0]) * (xyxys[:, 3] - xyxys[:, 1])
    ratio, area = bboxes_intersection_baseMin(
        torch.tensor(exist_xyxy), torch.tensor(xyxys))
    area = area[0].numpy()
    ratio = area / areas
    xyxy = xyxys[ratio < 0.5]
    xywh = xyxy.copy()
    xywh[:, 2] -= xywh[:, 0]
    xywh[:, 3] -= xywh[:, 1]
    return xyxy, xywh


def clusterBoxes(xyxys: np.ndarray, outs: list[np.ndarray] = None) -> list:
    xyxys = xyxys.copy()
    whs = xyxys[:, :2].copy()
    whs = xyxys[:, 2:] - whs
    med = np.median(whs, axis=0)
    haf = (med / 2).astype(np.int32)
    xyxys[:, :2] -= haf
    xyxys[:, 2:] += haf
    ratio, area = bboxes_intersection_baseMin(
        torch.tensor(xyxys), torch.tensor(xyxys))
    area = area.numpy()
    mask = area > 0
    ready = np.full(len(xyxys), False, dtype=bool)
    clus = dict[int, list[int]]()
    for ind in range(len(xyxys)):
        if ready[ind]:
            continue
        ready[ind] = True
        clus[ind] = [ind,]
        a_que = []
        idxs = list(np.where(mask[ind, :])[0])
        for idx in idxs:
            if ready[idx]:
                continue
            a_que.append(idx)
        while len(a_que):
            sub = a_que.pop()
            if ready[sub]:
                continue
            idxs = list(np.where(mask[sub, :])[0])
            for idx in idxs:
                if ready[idx]:
                    continue
                a_que.append(idx)
            ready[sub] = True
            clus[ind].append(sub)
    new_xyxys = []
    for clu in clus.values():
        a_clu = xyxys[clu]
        new_xyxys.append(np.concatenate(
            [a_clu[:, :2].min(axis=0)+haf, a_clu[:, 2:].max(axis=0)-haf]))
    new_xyxys = np.stack(new_xyxys, axis=0)
    new_xywhs = new_xyxys.copy()
    new_xywhs[:, 2] -= new_xywhs[:, 0]
    new_xywhs[:, 3] -= new_xywhs[:, 1]
    if isinstance(outs, list):
        outs.clear()
        outs.append(np.array(new_xyxys))
        outs.append(np.array(new_xywhs))
    xywhs = sorted(new_xywhs, reverse=True, key=lambda x: x[2]*x[3])
    return list(xywhs[0])





