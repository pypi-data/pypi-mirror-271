
import numpy as np
import cv2
from typing import Iterable
from scipy import stats
import base64
import requests

def findMaskBox(mask: np.ndarray, expand: int | list[int] = None):
   
    if mask is None or 0 == mask.size:
        return None, None

    if mask.ndim < 1 or 3 < mask.ndim:
        print("维度错误!", "[{}]".format(mask.ndim))
        return None, None

    def start_1d_stop(line: np.ndarray):
        start = None
        for index, value in enumerate(line):
            if value:
                start = index
                break
        stop = None
        for index, value in enumerate(line[::-1]):
            if value:
                stop = index
                break
        if start is not None and stop is not None:
            return start, len(line) if 0 == stop else len(line) - stop
        return 0, len(line)

    is_1dim = False
    if 1 == mask.ndim:
        mask = mask.reshape((1,) + mask.shape)
        is_1dim = True

    if 3 == mask.ndim:
        mask = np.max(mask, -1)

    x1, x2 = start_1d_stop(np.max(mask, 0))
    y1, y2 = start_1d_stop(np.max(mask, 1))
    bbox = [x1, y1, x2, y2]

    bbox2 = bbox.copy()
    if isinstance(expand, (int, float, list, tuple)):
        if isinstance(expand, (int, float)):
            expand = [int(expand)]
        elif isinstance(expand, (list, tuple)):
            expand = [int(val) for val in expand]
        expand = (expand * 4)[:4]
        limit = (mask.shape[1], mask.shape[0]) * 2
        sign = (-1, -1, 1, 1)
        for ind in range(4):
            bbox2[ind] += sign[ind] * expand[ind]
            bbox2[ind] = max(0, bbox2[ind])
            bbox2[ind] = min(bbox2[ind], limit[ind])

    if is_1dim:
        return bbox[::2], bbox2[::2]

    return bbox, bbox2


def findContentBox1(image: np.ndarray, expand: int | list[int] = None):
    
    if image is None:
        return None, None

    # cv2.imshow('image', image)

    if 2 == image.ndim:
        grey = image
    elif 3 == image.shape[-1]:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        grey = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

    # cv2.imshow('grey', grey)
    # cv2.waitKey()

    bbox = [0, 0, 0, 0]
    dx = [1, 0]
    dy = [0, 1]
    size = [grey.shape[1], grey.shape[0]]
    for dim in range(2):
        rdc = cv2.reduce(
            np.abs(cv2.Sobel(grey, cv2.CV_16S,
                   dx[dim], dy[dim])), dim, cv2.REDUCE_MAX
        )
        contours, hierarchy = cv2.findContours(
            rdc.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if len(contours) == 0:
            bbox[dim + 0], bbox[dim + 2] = 0, size[dim]
            continue
        rects = np.array([cv2.boundingRect(cont) for cont in contours])
        bboxs = np.array(
            [[rect[dim + 0], rect[dim + 0] + rect[dim + 2]] for rect in rects]
        )
        loc1, loc2 = np.min(bboxs[:, 0], axis=0), np.max(bboxs[:, 1], axis=0)
        bbox[dim + 0], bbox[dim + 2] = loc1, loc2

    bbox2 = bbox.copy()
    if isinstance(expand, (int, float, list, tuple)):
        if isinstance(expand, (int, float)):
            expand = [int(expand)]
        elif isinstance(expand, (list, tuple)):
            expand = [int(val) for val in expand]
        expand = (expand * 4)[:4]
        limit = (image.shape[1], image.shape[0]) * 2
        sign = (-1, -1, 1, 1)
        for ind in range(4):
            bbox2[ind] += sign[ind] * expand[ind]
            bbox2[ind] = max(0, bbox2[ind])
            bbox2[ind] = min(bbox2[ind], limit[ind])

    return bbox, bbox2


def findContentBox2(image: np.ndarray, expand: int | list[int] = None):
    
    if image is None:
        return None, None


    if 2 == image.ndim:
        grey = image
    elif 3 == image.shape[-1]:
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        grey = image[:,:,-1]
       
    def start_1d_stop(line: np.ndarray):
        start = None
        for index, value in enumerate(line):
            if value:
                start = index
                break
        stop = None
        for index, value in enumerate(line[::-1]):
            if value:
                stop = index
                break
        if start is not None and stop is not None:
            return start, len(line) if 0 == stop else len(line) - stop
        return 0, len(line)

    bbox = [0, 0, 0, 0]
    dx = [1, 0]
    dy = [0, 1]
    for dim in range(2):
        sbl = cv2.Sobel(grey, cv2.CV_16S, dx[dim], dy[dim])
        sbl_abs = np.abs(sbl).astype(np.uint16)
        bin = cv2.threshold(sbl_abs, 120, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        rdc = 0 < cv2.reduce(bin, dim, cv2.REDUCE_MAX).squeeze()
        bin2 = cv2.threshold(sbl_abs, sbl_abs.mean(), 255, cv2.THRESH_BINARY)[1]
        rdc2 = 0 < cv2.reduce(bin2, dim, cv2.REDUCE_MAX).squeeze()
        loc1, loc2 = start_1d_stop(rdc|rdc2)
        bbox[dim + 0], bbox[dim + 2] = loc1, loc2

    bbox2 = bbox.copy()
    if isinstance(expand, (int, float, list, tuple)):
        if isinstance(expand, (int, float)):
            expand = [int(expand)]
        elif isinstance(expand, (list, tuple)):
            expand = [int(val) for val in expand]
        expand = (expand * 4)[:4]
        limit = (image.shape[1], image.shape[0]) * 2
        sign = (-1, -1, 1, 1)
        for ind in range(4):
            bbox2[ind] += sign[ind] * expand[ind]
            bbox2[ind] = max(0, bbox2[ind])
            bbox2[ind] = min(bbox2[ind], limit[ind])

    return bbox, bbox2


def dropBlankBorder(image: np.ndarray, expand: int | list[int] = None):
    # if image.ndim == 3 and image.shape[2] == 4:
    #     _, bbox = findMaskBox(image, expand)
    # else:
    _, bbox = findContentBox2(image, expand)
    print(image.shape,bbox)
    return image[bbox[1]:bbox[3], bbox[0]:bbox[2]]


def calcMajorInThickBorder(image: np.ndarray, margin: int = 5, calc_mean: str = "mode", calc_std: str = "no"):
    
    if image is None or 0 == image.size:
        return None, None

    if image.shape[0] < margin or image.shape[1] < margin:
        return None, None

    bars = [
        image[:margin, :],
        image[-margin:, :],
        image[:, :margin],
        image[:, -margin:],
    ]
    shape = image.shape if 3 == image.ndim else image.shape + (1,)
    lines = [bar.reshape((-1, shape[-1])) for bar in bars]
    one_bar = np.concatenate(lines, axis=0)

    mean_value = None
    if "mean" == calc_mean:
        mean_value = np.mean(one_bar, axis=0)
    elif "median" == calc_mean:
        mean_value = np.median(one_bar, axis=0)
    else:
        if image.dtype in (np.int8, np.uint8, np.int16, np.uint16, np.int32, np.uint32, np.int64, np.uint64) \
                and (image.ndim == 2 or 1 == shape[-1]):
            mean_value = stats.mode(one_bar, axis=None, keepdims=False).mode
        else:
            print("mode 仅支持单通道整型像素图像，将改用 median。")
            mean_value = np.median(one_bar, axis=0)

    std_value = None
    if "std" == calc_std:
        std_value = np.std(one_bar, axis=0)
    elif "max" == calc_std:
        std_value = np.max(one_bar, axis=0)
    elif "min" == calc_std:
        std_value = np.min(one_bar, axis=0)

    return mean_value, std_value


def expandBorder(
    image: np.ndarray,
    expands: int | list | None = None,
    scale_up: float | list | None = None,
    value: list | str = "median",
    **kwargs
):
   

    if image.ndim not in (2, 3):
        print("输入数组形状不正确! image.shape:=", image.shape)
        return None

    image_height, image_width, image_nChannels = (
        image.shape if image.ndim == 3 else image.shape + (1,)
    )

    if expands is not None:
        if not isinstance(expands, Iterable):
            expands = [expands]
        expands = (list(expands) * 4)[:4]

    if scale_up is not None:
        if not isinstance(scale_up, Iterable):
            scale_up = [scale_up]
        scale_up = (list(scale_up) * 2)[:2]

    border = [5, 5, 5, 5]
    if expands is not None and len(expands) != 0:
        border = [val if val > 0 else 0 for val in expands]
    elif scale_up is not None and len(scale_up) != 0:
        new_height, new_width = int(image_height * scale_up[0]), int(
            image_width * scale_up[1]
        )
        dif_height, dif_width = new_height - image_height, new_width - image_width
        dif_height = dif_height if dif_height > 0 else 0
        dif_width = dif_width if dif_width > 0 else 0
        top, left = dif_height // 2, dif_width // 2
        border = [top, dif_height - top, left, dif_width - left]

    if isinstance(value, str):
        margin: int = kwargs["margin"] if "margin" in kwargs else 5
        if "corner" in value:
            bars = [
                image[:margin, :margin],
                image[:margin, -margin:],
                image[-margin:, :margin],
                image[-margin:, -margin:],
            ]
        else:
            bars = [
                image[:margin, :],
                image[-margin:, :],
                image[:, :margin],
                image[:, -margin:],
            ]
        lines = [bar.reshape((-1, image_nChannels)) for bar in bars]
        if "median" in value:
            value = np.median(np.vstack(lines), axis=0)
        else:
            value = np.mean(np.vstack(lines), axis=0)

    return cv2.copyMakeBorder(
        image,
        border[0],
        border[1],
        border[2],
        border[3],
        cv2.BORDER_CONSTANT,
        value=value,
    )


def segmentBackground(image: np.ndarray, is_all_in_one: bool,
                      kmeans_K: int = 6, kmeans_max_iter: int = 10, kmeans_epsilon: float = 0.1, kmeans_attempts: int = 3,
                      border_thickness: int = 5, border_buffer: int = 1, min_object_size: int = 3) -> np.ndarray:

    if image is None:
        print('空图片!')
        return None

    if 3 == image.ndim and 4 == image.shape[-1]:
        print('已有透明通道!')
        return None

    if min(image.shape[:2]) < 3*border_thickness:
        print('图像过小!')
        return None

    image_height, image_width, image_channels = (
        image.shape if 3 == image.ndim else image.shape + (1,))
    kmeans_flags = cv2.KMEANS_RANDOM_CENTERS
    kmeans_criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS,
                       kmeans_max_iter, kmeans_epsilon)
    _, label_map, color_centers = cv2.kmeans(
        image.reshape([-1, image_channels]).astype(np.float32),
        kmeans_K, None, kmeans_criteria, kmeans_attempts, kmeans_flags)
    label_map = label_map.reshape([image_height, image_width])

    WHITE_COLOR_THRESH = 240
    white_valids = np.all(color_centers > WHITE_COLOR_THRESH, 1)
    white_labels = np.arange(kmeans_K)[white_valids]
    # numpy.vectorize 太慢了，怀疑没并行
    # white_varify = np.vectorize(lambda x: x in white_labels)

    label_bars = [label_map[:border_thickness, :-border_thickness],
                  label_map[-border_thickness:, border_thickness:],
                  label_map[border_thickness:, :border_thickness],
                  label_map[:-border_thickness, -border_thickness:]]

    is_white_background = False
    background_mask = None
    white_include_number = 0
    min_object_size += (min_object_size+1) % 2
    open_kernel = np.ones([min_object_size, min_object_size])
    for label_bar in label_bars:
        # numpy.vectorize 太慢了，怀疑没并行
        # background_mask = white_varify(label_bar).astype(np.uint8)
        background_mask = np.full_like(label_bar, False, bool)
        for white_label in white_labels:
            background_mask |= label_bar == white_label
        background_mask = background_mask.astype(np.uint8)
        if np.any(cv2.morphologyEx(background_mask, cv2.MORPH_OPEN, open_kernel)):
            white_include_number += 1
        if 2 < white_include_number:
            is_white_background = True
            break

    if is_white_background:
        # numpy.vectorize 太慢了，怀疑没并行
        # background_mask = white_varify(label_map).astype(np.uint8)
        background_mask = np.full_like(label_map, False, bool)
        for white_label in white_labels:
            background_mask |= label_map == white_label
    else:
        background_ID = np.argmax(np.bincount(
            np.concatenate([label_bar.reshape(-1) for label_bar in label_bars])))
        background_mask = label_map == background_ID

    if is_all_in_one:
        return 0 < cv2.dilate(background_mask.astype(np.uint8), np.ones((3, 3), dtype=np.uint8))
        return background_mask

    region_count, region_label, region_stats, region_centroids = cv2.connectedComponentsWithStats(
        background_mask.astype(np.uint8))
    if region_count < 2:
        print('区域过少!')
        return None

    XYXYs = [(box[0], box[1], box[0]+box[2], box[1]+box[3])
             for box in region_stats[1:, :-1]]
    limit = (border_buffer, border_buffer, image_width -
             border_buffer, image_height-border_buffer)

    def border_varify(
        x): return x[0] <= limit[0] or x[1] <= limit[1] or limit[2] <= x[2] or limit[3] <= x[3]
    region_indices = np.arange(1, region_count)[
        list(map(border_varify, XYXYs))]
    # numpy.vectorize 太慢了，怀疑没并行
    # background_filter = np.vectorize(lambda x: x in region_indices)
    # filtered_background_mask = background_filter(region_label)
    filtered_background_mask = np.full_like(region_label, False, bool)
    for region_index in region_indices:
        filtered_background_mask |= region_label == region_index

    return 0 < cv2.dilate(filtered_background_mask.astype(np.uint8), np.ones((3, 3), dtype=np.uint8))
    return filtered_background_mask


# 去除背景
def removebackground(img: np.ndarray):
    
    if img.ndim == 3 and img.shape[2] == 4 and np.min(img[:,:,3]) < 128:
        return np.concatenate([img[:,:,:3], np.where(img[:,:,3:] < 128, 0, 255).astype(img.dtype)], axis=2)
    
    content = img[:,:,:3]
    filtered_background_mask = segmentBackground(image=content, is_all_in_one=True)
    alpha = np.where(filtered_background_mask, 0, 255).astype(img.dtype)

    image = np.zeros((content.shape[0], content.shape[1], 4), dtype=np.uint8)
    image[:, :, 0:3] = content
    image[:, :, -1] = alpha

    return image


def resizeByHeightOrWidth(
    image: np.ndarray, height_or_width: int, is_base_height: bool
):
   
    if image is None:
        return None

    if height_or_width < 1:
        return image

    base_length = image.shape[0] if is_base_height else image.shape[1]
    multiplier = height_or_width / base_length

    return cv2.resize(image, None, fx=multiplier, fy=multiplier)


def resizeByShortestOrLongest(
    image: np.ndarray, height_or_width: int, is_base_short: bool
):
   
    if image is None:
        return None

    if height_or_width < 1:
        return image

    base_height = np.array([[True, False], [False, True]])
    is_width_greater = image.shape[1] > image.shape[0]

    return resizeByHeightOrWidth(
        image, height_or_width, base_height[int(
            is_base_short), int(is_width_greater)]
    )


def resizeToUniformSize(
    image: np.ndarray, new_size: int | float, size_type: str = "area"
):
    
    if image is None:
        return None

    if new_size < 1:
        return image

    size_type = size_type.lower()
    if size_type in [
        "area",
        "npixels",
        "height*width",
        "h*w",
        "sum",
        "amount",
        "total",
    ]:
        factor = np.sqrt(new_size / (image.shape[0] * image.shape[1]))
        return cv2.resize(image, None, fx=factor, fy=factor)
    elif size_type in ["height", "h"]:
        return resizeByHeightOrWidth(image, int(new_size), True)
    elif size_type in ["width", "w"]:
        return resizeByHeightOrWidth(image, int(new_size), False)
    elif size_type in ["shortest", "smallest", "min", "minimum", "lowest"]:
        return resizeByShortestOrLongest(image, int(new_size), True)
    elif size_type in ["longest", "largest", "max", "maximum", "highest"]:
        return resizeByShortestOrLongest(image, int(new_size), False)
    else:
        # print('参数错误', 'size_type:=', size_type, '  不缩放')
        return image


def splitPixelKMeans(
    image: np.ndarray,
    K: int = 6,
    max_iter: int = 10,
    epsilon: float = 0.1,
    attempts: int = 3,
    flags: int = cv2.KMEANS_RANDOM_CENTERS,
) -> tuple[np.ndarray, np.ndarray]:
    
    image_height, image_width, image_channels = (
        image.shape if 3 == image.ndim else image.shape + (1,)
    )
    image_one_line = image.reshape([-1, image_channels]).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_MAX_ITER +
                cv2.TERM_CRITERIA_EPS, max_iter, epsilon)
    if cv2.KMEANS_USE_INITIAL_LABELS == flags:
        flags = cv2.KMEANS_RANDOM_CENTERS
    _, best_labels, centers = cv2.kmeans(
        image_one_line, K, None, criteria, attempts, flags
    )
    label = best_labels.reshape([image_height, image_width])
    return label, centers


def splitElementKMeans(
    vector: np.ndarray,
    K: int = 6,
    max_iter: int = 10,
    epsilon: float = 0.1,
    attempts: int = 3,
    flags: int = cv2.KMEANS_RANDOM_CENTERS,
) -> tuple[np.ndarray, np.ndarray]:
    
    if vector is None or vector.ndim < 1:
        print("vector 参数错误", vector if vector is None else vector.shape)
    nChannels = 1 if 1 == vector.ndim else vector.shape[-1]
    vector_one_line = vector.reshape([-1, nChannels]).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_MAX_ITER +
                cv2.TERM_CRITERIA_EPS, max_iter, epsilon)
    if cv2.KMEANS_USE_INITIAL_LABELS == flags:
        flags = cv2.KMEANS_RANDOM_CENTERS
    _, best_labels, centers = cv2.kmeans(
        vector_one_line, K, None, criteria, attempts, flags
    )
    label = best_labels.reshape(
        vector.shape if 1 == vector.ndim else vector.shape[:-1])
    return label, centers


def findClosestPoint(
    search_set: np.ndarray, target_point: np.ndarray, distance_type: str = "Euclidean"
):
    set_shape = search_set.shape
    pt_shape = target_point.shape
    if len(set_shape) != 2 or len(pt_shape) != 1 or set_shape[-1] != pt_shape[0]:
        print("形状不匹配！")
        return None, None

    min_distance = 1e8
    min_index = None
    distance_type = distance_type.lower()
    if "city" in distance_type or "block" in distance_type:
        for index, point in enumerate(search_set):
            distance = np.abs(point - target_point).sum()
            if min_distance > distance:
                min_distance = distance
                min_index = index
    elif "max" in distance_type:
        for index, point in enumerate(search_set):
            distance = np.abs(point - target_point).max()
            if min_distance > distance:
                min_distance = distance
                min_index = index
    else:
        for index, point in enumerate(search_set):
            distance = np.sqrt(np.sum(np.power(point - target_point, 2)))
            if min_distance > distance:
                min_distance = distance
                min_index = index

    return min_index, min_distance


def IOU_x1x2(
    bar1_x1: int | float,
    bar1_x2: int | float,
    bar2_x1: int | float,
    bar2_x2: int | float,
    return_intersection: bool = False,
):
    x1 = max(bar1_x1, bar2_x1)
    x2 = min(bar1_x2, bar2_x2)
    intersection = max(0, x2 - x1)
    x1 = min(bar1_x1, bar2_x1)
    x2 = max(bar1_x2, bar2_x2)
    union_set = x2 - x1
    iou = intersection / union_set
    if return_intersection:
        return iou, intersection
    else:
        return iou


def IOU_xLen(
    bar1_x: int | float,
    bar1_len: int | float,
    bar2_x: int | float,
    bar2_len: int | float,
    return_intersection: bool = False,
):
    return IOU_x1x2(
        bar1_x, bar1_x + bar1_len, bar2_x, bar2_x + bar2_len, return_intersection
    )


def IOU_x1y1x2y2(
    box1_x1: int | float,
    box1_y1: int | float,
    box1_x2: int | float,
    box1_y2: int | float,
    box2_x1: int | float,
    box2_y1: int | float,
    box2_x2: int | float,
    box2_y2: int | float,
    return_intersection: bool = False,
):
    _, intersection_x = IOU_x1x2(box1_x1, box1_x2, box2_x1, box2_x2, True)
    _, intersection_y = IOU_x1x2(box1_y1, box1_y2, box2_y1, box2_y2, True)
    intersect_area = intersection_x * intersection_y
    union_set_area = (
        (box1_x2 - box1_x1) * (box1_y2 - box1_y1)
        + (box2_x2 - box2_x1) * (box2_y2 - box2_y1)
        - intersect_area
    )
    iou = intersect_area / union_set_area
    if return_intersection:
        return iou, intersect_area
    else:
        return iou


def IOU_x_y_w_h(
    box1_x: int | float,
    box1_y: int | float,
    box1_w: int | float,
    box1_h: int | float,
    box2_x: int | float,
    box2_y: int | float,
    box2_w: int | float,
    box2_h: int | float,
    return_intersection: bool = False,
):
    return IOU_x1y1x2y2(
        box1_x,
        box1_y,
        box1_x + box1_w,
        box1_y + box1_h,
        box2_x,
        box2_y,
        box2_x + box2_w,
        box2_y + box2_h,
        return_intersection,
    )


def clusterColourOneShot(image: np.ndarray, order_minimum: int, mask: np.ndarray = None, once_again: bool = True,
                         use_edge_mask: bool = True, edge_ksize: int = 3, edge_thresh: float = 20,
                         kmeans_K: int = 12, kmeans_max_iter: int = 10, kmeans_epsilon: float = 0.1, kmeans_attempts: int = 3,
                         output_label: list[np.ndarray] = None, output_mask: list[np.ndarray] = None, output_palette: list[np.ndarray] = None):

    if image is None:
        print("空图片!")
        return 0, None, None

    if mask is None:
        # mask 是 None，尝试设置 mask，失败也没关系
        if 3 == image.ndim and 4 == image.shape[-1]:
            mask = image[:, :, -1] > 0
            image = image[:, :, :-1]
    else:
        # mask 非 None 时，需要判断 image 和 mask 的大小是否匹配
        if mask.shape != image.shape[:2]:
            print('image 和 mask 大小不匹配!')
            return 0, None, None
        if 2 < mask.ndim and 1 < mask.shape[-1]:
            print('mask 应该为单通道!')
            return 0, None, None
        if bool != mask.dtype:
            mask = mask > 0

    if use_edge_mask:
        edge_thresh1 = edge_thresh
        edge_thresh2 = 2*edge_thresh1
        edge = cv2.Canny(image, edge_thresh1, edge_thresh2,
                         apertureSize=edge_ksize)
        edge_mask = edge < 100
        if mask is None:
            mask = edge_mask
        else:
            mask &= edge_mask

    if isinstance(output_mask, list):
        output_mask.clear()
        output_mask.append(mask)

    is_output_label = False
    if isinstance(output_label, list):
        output_label.clear()
        is_output_label = True

    # 统计各颜色数目
    kmeans_flags = cv2.KMEANS_RANDOM_CENTERS
    if mask is None:
        label_map, color_centers = splitPixelKMeans(
            image, kmeans_K, kmeans_max_iter, kmeans_epsilon, kmeans_attempts, kmeans_flags)
        if is_output_label and not once_again:
            output_label.append(label_map)
    else:
        label_map, color_centers = splitElementKMeans(
            image[mask], kmeans_K, kmeans_max_iter, kmeans_epsilon, kmeans_attempts, kmeans_flags)
        if is_output_label and not once_again:
            label = np.full_like(mask, np.iinfo(
                label_map.dtype).max, label_map.dtype)
            label[mask] = label_map
            output_label.append(label)

    amounts = np.bincount(label_map.reshape(-1))
    orders = np.array([len(str(val)) for val in amounts])
    valid_number = 0
    while valid_number < 1 and 0 <= order_minimum:
        valid_array = order_minimum <= orders
        valid_number: int = np.sum(valid_array)
        valid_colours = color_centers[valid_array]
        valid_amounts = amounts[valid_array]
        order_minimum -= 1
    if valid_number < 0:
        return 0, None, None

    if once_again:
        kmeans_K = valid_number
        kmeans_flags = cv2.KMEANS_PP_CENTERS
        if mask is None:
            label_map, color_centers = splitPixelKMeans(
                image, kmeans_K, kmeans_max_iter, kmeans_epsilon, kmeans_attempts, kmeans_flags)
            if is_output_label:
                output_label.append(label_map)
        else:
            label_map, color_centers = splitElementKMeans(
                image[mask], kmeans_K, kmeans_max_iter, kmeans_epsilon, kmeans_attempts, kmeans_flags)
            if is_output_label:
                label = np.full_like(mask, np.iinfo(
                    label_map.dtype).max, label_map.dtype)
                label[mask] = label_map
                output_label.append(label)
        valid_colours = color_centers
        valid_amounts = np.bincount(label_map.reshape(-1))

    sorted_index = np.argsort(valid_amounts)[::-1]
    valid_colours = valid_colours[sorted_index]
    valid_amounts = valid_amounts[sorted_index]

    if isinstance(output_palette, list):
        nChannels = 1 if image.ndim < 3 else image.shape[-1]
        bar_size = 20
        bar_num = 6
        img_size = bar_num * bar_size
        max_column_num = 10
        row_num = valid_number // max_column_num + \
            int(bool(valid_number % max_column_num))
        col_num = valid_number if valid_number < max_column_num else max_column_num
        supplement = row_num * col_num - valid_number
        img_row_blocks = []
        for row in range(row_num):
            if row + 1 == row_num and 0 < supplement:
                white = np.full([bar_size, bar_size, nChannels], 200, np.uint8)
                mosaic = np.full(
                    [img_size, img_size, nChannels], 100, np.uint8)
                for i0 in range(bar_num):
                    for i1 in range(bar_num):
                        if (i0+i1) % 2:
                            mosaic[i0*bar_size:(i0+1)*bar_size,
                                   i1*bar_size:(i1+1)*bar_size] = white
                img_row_blocks.append(np.concatenate([np.full([img_size, img_size, nChannels], color_value, np.uint8)
                                      for color_value in valid_colours[row*col_num:valid_number]] + [mosaic]*supplement, 1))
            else:
                img_row_blocks.append(np.concatenate([np.full([img_size, img_size, nChannels], color_value, np.uint8)
                                                      for color_value in valid_colours[row*col_num:(row+1)*col_num]], 1))
        output_palette.clear()
        output_palette.append(np.concatenate(img_row_blocks, 0))

    return valid_number, valid_colours, valid_amounts

def opencv2base64(image:np.ndarray):
    data = cv2.imencode('.png', image)[1]
    image_bytes = data.tobytes()
    img_data = base64.b64encode(image_bytes).decode('utf8')
    result = "data:image/png;base64," + str(img_data)
    return result

def requestImage(imgeUrl:str):
    image_np = np.frombuffer(requests.get(imgeUrl, timeout=30).content, dtype=np.uint8)
    logo = cv2.imdecode(image_np, cv2.IMREAD_UNCHANGED)
    if logo.dtype != np.uint8:
        logo = cv2.normalize(logo, None, 0, 255,cv2.NORM_MINMAX, cv2.CV_8U)
    return logo


def resizeImage(image:np.ndarray,maxSize:int=None,fx:float=1,fy:float=1):
    if maxSize !=None:
        if max(image.shape[0], image.shape[1]) > maxSize:
            if image.shape[0] >= image.shape[1]:
                image = cv2.resize(image, dsize=(int(maxSize * image.shape[1] / image.shape[0]), maxSize))
            else:
                image = cv2.resize(image, dsize=(maxSize, int(maxSize * image.shape[0] / image.shape[1])))
    else:
        image = cv2.resize(image, dsize=None,fx=fx,fy=fy)
    
    return image
