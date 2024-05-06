
import cv2
import numpy as np
import numba as nb
from numpy import linalg as la
import os
import collections.abc
from shapely import geometry
from joblib import Parallel, delayed
import multiprocessing
from scipy import stats
from datetime import datetime
from typing import Iterable
from scipy import stats
import time
import itertools
from proc_image import calcMajorInThickBorder, segmentBackground, findMaskBox, expandBorder, findContentBox2
from proc_points import scalePointSet
from proc_color import hex2rgb, overlap_color

def fenceMap(image: np.ndarray, *, return_extend: str = None, powers: Iterable = [2]):
    """构建围栏图。

    参数:
        - image (np.ndarray): 图片。
        - return_extend (str, optional): 返回额外的结果图，可选【binary、label、label-with-fence】，默认无。
        - powers (Iterable, optional): 额外的颜色变换，幂指数。默认 2.

    返回:
        dict: 'fence'围栏图，'binary'多重二值图，'label'标签图
    """
    if image is None or 0 == image.size:
        return None

    if image.ndim < 2 or 3 < image.ndim:
        return None

    if image.dtype != np.uint8:
        return None

    if image.ndim == 2:
        image = image.reshape(image.shape+(1,))

    if powers:
        tweaks = [image]
        for power in powers:
            pow_vals = [power, 1/power]
            for pow_val in pow_vals:
                lut = np.linspace(0, 1, 256)
                np.power(lut, pow_val, out=lut)
                np.multiply(lut, 255, out=lut)
                lut = lut.astype(np.uint8)
                if 4 == image.shape[-1]:
                    tweaks.append(cv2.LUT(image[:, :, :3], lut))
                else:
                    tweaks.append(cv2.LUT(image, lut))
        image = np.concatenate(tweaks, axis=2)

    contours = []
    binaries = []
    for ch in range(image.shape[-1]):
        bin = np.greater(image[:, :, ch], 127).astype(np.uint8)
        np.multiply(bin, 255, out=bin)
        val = calcMajorInThickBorder(bin)[0]
        if 0 < val:
            np.bitwise_not(bin, out=bin)
        cont = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
        if len(cont) == 0:
            cv2.threshold(image[:, :, ch], 127, 255,
                          cv2.THRESH_BINARY+cv2.THRESH_OTSU, dst=bin)
            val = calcMajorInThickBorder(bin)[0]
            if 0 < val:
                np.bitwise_not(bin, out=bin)
            cont = cv2.findContours(
                bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
        contours.extend(cont)
        if return_extend:
            binaries.append(bin)
    if len(contours) == 0:
        extend = {'fence': np.zeros(image.shape[:2], dtype=np.uint8)}
        if return_extend:
            return_extend = return_extend.lower()
            if 'binary' in return_extend:
                extend['binary'] = np.stack(binaries, axis=2)
            if 'label' in return_extend:
                extend['label'] = np.zeros_like(
                    extend['fence'], dtype=np.uint8)

    fence = np.zeros(image.shape[:2], dtype=np.uint8)
    some = np.concatenate(contours, axis=0).squeeze(axis=1)
    fence[(some[:, 1], some[:, 0])] = 255

    extend = {'fence': fence}
    if return_extend:
        return_extend = return_extend.lower()
        if 'binary' in return_extend:
            extend['binary'] = np.stack(binaries, axis=2)
        if 'label' in return_extend:
            dtype = np.uint32
            label = np.zeros_like(fence, dtype=dtype)
            temp1 = np.zeros_like(label, dtype=dtype)
            temp2 = np.zeros_like(label, dtype=dtype)
            for index in range(len(binaries)):
                np.greater(binaries[index], 127, out=temp1)
                np.multiply(temp1, 2**index, out=temp2)
                label += temp2
            if 'label-with-fence' in return_extend or 'label with fence' in return_extend:
                label[0 < fence] = np.iinfo(dtype).max
            extend['label'] = label

    return extend




def slideCurve(x: int | float, min=0.0, max=1.0, shift=-2000, scale=0.001) -> float:
    return (max - min) / (1.0 + np.exp((x+shift)*scale)) + min


def slideThresh(x: int | float, min=0.0, max=1.0, shift=-2000, scale=0.001) -> float:
    return x * slideCurve(x=x, min=min, max=max, shift=shift, scale=scale)


def reverseLogo(input: dict, output: dict) -> bool:
    # 以下是输入参数提取
    use_material_pack: bool = input['use_material_pack']
    # image 与 images 一般不同时存在
    images: list[np.ndarray] = input['images']
    image: np.ndarray = images[0]

    expands = input["expands"]
    coloring_logo = input["logoColor"]
    coloring_bg = input["bgColor"]
    reverse_bg_color = input["reverse_bg_color"]
    reverse_logo_color = input["reverse_logo_color"]
    out_coordinate = input["out_coordinate"]
    output["images"] = [whiteningLogo(image=image, expands=expands,
                  coloring_logo=coloring_logo, coloring_bg=coloring_bg,
                  reverse_logo_color=reverse_logo_color, reverse_bg_color= reverse_bg_color,
                  out_coordinate=out_coordinate)]
    return True


def invertColors_v1(layer_dict: dict, alg_dict: dict, param_list: list[dict], queue: list[list]) -> str:
    if len(queue) == 0:
        return 'no input image'
    
    last_result = queue[-1]
    
    if len(last_result) < 2:
        return 'no enough data from previous result'
    
    if not isinstance(last_result[1], np.ndarray):
        return 'error type from previous result'
    
    image: np.ndarray = last_result[1]
    
    if image.ndim == 3:
        mono = image[:,:,-1]
    else:
        mono = image
        
    if len(param_list) < 1:
        return 'no enough parameters'
    
    param_color = param_list[0]
    
    for the_name in ('param_en_name', 'param_input_type', 'option_list', 'option'):
        if the_name not in param_color:
            return f'no key name "{the_name}"'
    
    if 'color' != param_color['param_en_name']:
        return 'need parameter "color"'
    
    if 'multiBox' != param_color['param_input_type']:
        return 'illegal type, require two-stage box'
    
    color_str = None
    if 'manual' in param_color['option']:
        for option in param_color['option_list']:
            if 'manual' != option['en']:
                continue
            color_str = option['children']['value']
            break
    if color_str is None:
        if 'color' in alg_dict:
            color_str = alg_dict['color']
        elif 'color' in layer_dict:
            color_str = layer_dict['color']
        else:
            return 'no color specified'     
        
    if 'overlap' == param_color['option']:
        color = list(hex2rgb(overlap_color(color_str)))
    else:
        color = list(hex2rgb(color_str))
    image = np.concatenate([np.full(image.shape[:2]+(3,), fill_value=color, dtype=np.uint8), mono.reshape(mono.shape+(1,))], axis=2)
    
    queue.append(['image', image])
    
    return ''


def whiteningLogo(image: np.ndarray, expands: list[int] = None,
                  coloring_logo: str = None, coloring_bg: str = None,
                  reverse_logo_color: bool = True, reverse_bg_color: bool = True,
                  out_coordinate: list[int] = None):
    KMEANS_K = 6
    KMEANS_MAX_ITER = 10
    KMEANS_EPSILON = 0.1
    KMEANS_ATTEMPTS = 3

    DEGENERATE_RANGE = 32

    BAND_KERNEL_SIZE = 5
    BAND_RATIO_THRESH = 0.98

    FILTER_WIDTH = 4
    FILTER_HEIGHT = FILTER_WIDTH
    FILTER_AREA = FILTER_WIDTH*FILTER_HEIGHT
    FILTER_A_DIV_L = 1.5

    HIER_NEXT = 0
    HIER_PREV = 1
    HIER_CHILD = 2
    HIER_PARENT = 3

    EQU_THRESH_SINGLE = 0.95
    EQU_THRESH_MERGE = 0.95

    MIN_SIZE_TO_SCALE = 2

    raw_input_image = image
    if image is None or 0 == image.size:
        print('反白算法，入口检查，空图片!')
        return None

    tst = datetime.now()
    # 计算前景掩码 foreground，同时将 image 的透明通道去除
    raw_has_alpha = False
    if 3 == image.ndim and 4 == image.shape[-1]:
        foreground_mask = 127 < image[:, :, -1]
        image = image[:, :, :-1]
        raw_has_alpha = True
    else:
        background_mask = segmentBackground(image, is_all_in_one=False,
                                            kmeans_K=KMEANS_K, kmeans_max_iter=KMEANS_MAX_ITER, kmeans_epsilon=KMEANS_EPSILON, kmeans_attempts=KMEANS_ATTEMPTS,
                                            border_thickness=5, border_buffer=1, min_object_size=3)
        foreground_mask = ~background_mask
        raw_has_alpha = False
    print('去背景', datetime.now() - tst)
    tst = datetime.now()

    # 先把周围空白区去掉，加下速
    bbox, bbox_ex = findMaskBox(foreground_mask)
    image = image[bbox_ex[1]:bbox_ex[3], bbox_ex[0]:bbox_ex[2]]
    foreground_mask = foreground_mask[bbox_ex[1]:bbox_ex[3],
                                      bbox_ex[0]:bbox_ex[2]]
    bounding_box = [bbox[0] - bbox_ex[0], bbox[1] - bbox_ex[1],
                    bbox[2] - bbox_ex[0], bbox[3] - bbox_ex[1]]
    if expands is None or sum(expands) == 0:
        top_left_xy = [-bbox_ex[0], -bbox_ex[1]]
    else:
        exps = (expands*2)[:2]
        top_left_xy = [-bbox_ex[0]+exps[0], -bbox_ex[1]+exps[1]]
    if isinstance(out_coordinate, list):
        out_coordinate.clear()
        out_coordinate.extend(top_left_xy)
    print('去空白', datetime.now() - tst)
    tst = datetime.now()

    # 构建围栏图
    # lut = np.array(
    #     [rank//DEGENERATE_RANGE*DEGENERATE_RANGE for rank in range(256)], dtype=np.uint8)
    # descended_image = cv2.LUT(image, lut)
    if raw_has_alpha:
        return_fence = fenceMap(
            np.concatenate([image, foreground_mask.astype(
                np.uint8).reshape(foreground_mask.shape+(1,))*255], axis=2),
            return_extend='label')
    else:
        return_fence = fenceMap(
            image,
            return_extend='label')
    region_fence_map = return_fence['fence']
    color_label_map = return_fence['label']
    # cv2.namedWindow('fence', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('fence', region_fence_map)
    print('色块围栏图', datetime.now() - tst)
    tst = datetime.now()

    go_to_directly_binary = False
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(
        grey, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (BAND_KERNEL_SIZE, BAND_KERNEL_SIZE))
    dilated = cv2.dilate(binary, kernel)
    eroded = cv2.erode(binary, kernel)
    band_bin = cv2.bitwise_xor(dilated, eroded)
    band_bool = np.greater(band_bin, 127)
    total_num = np.sum(region_fence_map)/255
    outer_num_thresh = slideThresh(min(binary.shape[:2]))
    pow_vals = (-1.0, 2.0, 0.5)
    for times, pow_val in enumerate(pow_vals, start=1):
        if 1 < times:
            lut = np.linspace(0, 1, 256)
            np.power(lut, pow_val, out=lut)
            np.multiply(lut, 255, out=lut)
            lut = lut.astype(np.uint8)
            cv2.threshold(cv2.LUT(grey, lut), 127, 255,
                          cv2.THRESH_BINARY, dst=binary)
            cv2.dilate(binary, kernel, dst=dilated)
            cv2.erode(binary, kernel, dst=eroded)
            cv2.bitwise_xor(dilated, eroded, dst=band_bin)
            np.greater(band_bin, 127, out=band_bool)
        inner_num = np.sum(region_fence_map[band_bool])/255
        band_ratio = inner_num/total_num
        outer_num = total_num - inner_num
        print(BAND_RATIO_THRESH, band_ratio)
        print(outer_num, outer_num_thresh)
        # cv2.namedWindow(f'binary {times}', cv2.WINDOW_KEEPRATIO)
        # cv2.imshow(f'binary {times}', binary)
        print(f'直接二值化尝试，times {times}/{len(pow_vals)}', datetime.now() - tst)
        tst = datetime.now()
        if BAND_RATIO_THRESH < band_ratio or outer_num < outer_num_thresh:
            go_to_directly_binary = True
            break

    if go_to_directly_binary:
        val = calcMajorInThickBorder(binary)[0]
        if 0 < val:
            np.bitwise_not(binary, out=binary)
        bg_color = np.array([0, 0, 0, 0], np.float32)
        if isinstance(coloring_bg, str) and len(coloring_bg):
            color_str = ''.join(filter(str.isalnum, coloring_bg))
            if len(color_str) == 6:
                color = [int(color_str[:2], 16),
                         int(color_str[2:4], 16),
                         int(color_str[4:], 16)]
                if reverse_bg_color:
                    color = color[::-1]
                bg_color = np.append(np.array(color).astype(np.float32), 0)
        fg_color = None
        if isinstance(coloring_logo, str) and len(coloring_logo):
            color_str = ''.join(filter(str.isalnum, coloring_logo))
            if len(color_str) == 6:
                color = [int(color_str[:2], 16),
                         int(color_str[2:4], 16),
                         int(color_str[4:], 16)]
                if reverse_logo_color:
                    color = color[::-1]
                fg_color = np.append(np.array(color).astype(np.float32), 255)
        if fg_color is None:
            the_white = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGRA)
        else:
            the_white = np.full(binary.shape+(4,), fg_color, np.uint8)
        the_color = np.full_like(the_white, bg_color, np.uint8)
        the_light = cv2.add(cv2.bitwise_and(the_white, the_white, mask=binary),
                            cv2.bitwise_and(the_color, the_color, mask=~binary))

        print('生成效果图', datetime.now() - tst)
        tst = datetime.now()

        if expands is None or sum(expands) == 0:
            return the_light
        else:
            return expandBorder(the_light, expands, value=[float(val) for val in bg_color])

    # 基于围栏图查找所有轮廓，同时获取包含关系树
    labels_contours, labels_hierarchy = cv2.findContours(
        region_fence_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if 0 == len(labels_contours):
        print('反白算法，空内容')
        return None
    labels_hierarchy = labels_hierarchy[0]
    # cv2.namedWindow('contour', cv2.WINDOW_KEEPRATIO)
    # for index in range(len(contours_label)):
    #     contour_to_show = region_fence_map.copy()
    #     cv2.drawContours(contour_to_show, contours_label, index, 125, 1)
    #     cv2.imshow('contour', contour_to_show)
    #     print('index:', index, 'hierarchy:', hierarchy_label[index])
    #     cv2.waitKey()
    print('查找轮廓', datetime.now() - tst)
    tst = datetime.now()

    # 面积
    areas = np.array([cv2.contourArea(contour) for contour in labels_contours])
    # 周长
    lengths = np.array([cv2.arcLength(contour, True)
                       for contour in labels_contours])
    # 外接正矩形
    rectangles = np.array([cv2.boundingRect(contour)
                          for contour in labels_contours])
    # [print(index, rectangles[index], areas[index], lengths[index])
    #  for index in range(len(areas))]
    print('面积、周长、外接矩形', datetime.now() - tst)
    tst = datetime.now()

    # 去除掉小轮廓，并更新相关数据
    filter_mask = np.full(len(labels_contours), fill_value=True, dtype=bool)
    for index in range(len(labels_contours)):
        if areas[index] < FILTER_AREA and (rectangles[index][2] < FILTER_WIDTH or rectangles[index][3] < FILTER_HEIGHT):
            filter_mask[index] = False
            continue
        # if areas[index] / lengths[index] < FILTER_A_DIV_L:
        #     filter_mask[index] = False
        #     continue
    labels_contours = [labels_contours[index]
                       for index in range(len(labels_contours)) if filter_mask[index]]
    map_back = list(np.where(filter_mask)[0])
    map_foreword = dict([(the_old, the_new)
                        for the_new, the_old in enumerate(map_back)])
    new_hierarchy = labels_hierarchy[filter_mask]
    for new_index in range(len(new_hierarchy)):
        for sub_index in range(4):
            old_index = new_hierarchy[new_index][sub_index]
            while -1 != old_index and not filter_mask[old_index]:
                if HIER_CHILD == sub_index:
                    old_index = labels_hierarchy[old_index][HIER_NEXT]
                else:
                    old_index = labels_hierarchy[old_index][sub_index]
            the_index = map_foreword[old_index] if - \
                1 != old_index else old_index
            new_hierarchy[new_index, sub_index] = the_index
    labels_hierarchy = new_hierarchy
    areas = areas[filter_mask]
    lengths = lengths[filter_mask]
    rectangles = rectangles[filter_mask]
    print('去除小物体', datetime.now() - tst)
    tst = datetime.now()

    # 子轮廓集
    childrens: list[list[int]] = []
    for hierarchy in labels_hierarchy:
        children: list[int] = []
        index = hierarchy[HIER_CHILD]
        while -1 != index:
            children.append(index)
            index = labels_hierarchy[index][HIER_NEXT]
        childrens.append(children)
    # 等效轮廓
    equivalents = np.arange(len(labels_contours))
    for index, children in enumerate(childrens):
        if 1 == len(children):
            child_index = children[0]
            if EQU_THRESH_SINGLE < (areas[child_index]+lengths[child_index]) / areas[index]:
                equivalents[index] = child_index
                equivalents[child_index] = index
    # 最外层轮廓
    outer_indices = np.where(np.equal(labels_hierarchy[:, HIER_PARENT], -1))[0]
    # 第二层轮廓
    second_indices = []
    for index in outer_indices:
        second_indices.extend(childrens[index])
    # print(second_indices)
    print('子轮廓集、等效轮廓', datetime.now() - tst)
    tst = datetime.now()

    # 轮廓的颜色标签
    labels = np.full(len(labels_contours), fill_value=-1, dtype=int)
    is_whites = np.full(len(labels_contours), fill_value=False, dtype=bool)
    for index in range(len(labels_contours)):
        contour = labels_contours[index]
        rectangle = rectangles[index]
        scaled_contour = None
        cx, cy = rectangle[0] + rectangle[2] / \
            2, rectangle[1] + rectangle[3] / 2
        pt = labels_contours[index][0].reshape(-1)
        px, py = pt
        dx, dy = cx-px, cy-py
        l = np.sqrt(dx**2 + dy**2) + 0.00001
        dx, dy = dx / l, dy / l
        color_label = -1
        for step in range(2, 51, 2):
            nx, ny = int(px + dx*step), int(py + dy*step)
            if ny < 0 or nx < 0 or color_label_map.shape[0] <= ny or color_label_map.shape[1] <= nx:
                break
            if cv2.pointPolygonTest(labels_contours[index], [nx, ny], False) < 0.5:
                continue
            if 0 == region_fence_map[ny, nx]:
                color_label = color_label_map[ny, nx]
                break
        if -1 == color_label:
            if rectangle[2] <= MIN_SIZE_TO_SCALE or rectangle[3] <= MIN_SIZE_TO_SCALE:
                scaled_contour = contour
            else:
                scaled_contour = scalePointSet(
                    contour, rectangle, scale_abs=-MIN_SIZE_TO_SCALE)
            color_label = stats.mode(
                color_label_map[(scaled_contour[:, 0, 1], scaled_contour[:, 0, 0])]).mode
        labels[index] = color_label

        if index in second_indices:
            if scaled_contour is None:
                if rectangle[2] <= MIN_SIZE_TO_SCALE or rectangle[3] <= MIN_SIZE_TO_SCALE:
                    scaled_contour = contour
                else:
                    scaled_contour = scalePointSet(
                        contour, rectangle, scale_abs=-MIN_SIZE_TO_SCALE)
            # if 39 == index:
            #     something = np.zeros(
            #         (rectangle[1]+rectangle[3], rectangle[0]+rectangle[2]), dtype=np.uint8)
            #     cv2.drawContours(something, [contour], 0, 120, 1)
            #     cv2.drawContours(something, [scaled_contour], 0, 255, 1)
            #     cv2.namedWindow('something', cv2.WINDOW_KEEPRATIO)
            #     cv2.imshow('something', something)
            #     cv2.waitKey()
            is_white_arr: np.ndarray = np.greater_equal(
                image[(scaled_contour[:, 0, 1], scaled_contour[:, 0, 0])], 240)
            if 1 < is_white_arr.ndim:
                is_white_arr = is_white_arr.reshape((len(is_white_arr), -1))
                is_white_arr = is_white_arr.all(axis=1)
            is_white = stats.mode(
                is_white_arr.astype(np.uint8), axis=None).mode
            is_whites[index] = bool(is_white)
    # [print(ind, val) for ind, val in enumerate(is_whites)]
    print('提取颜色标签', datetime.now() - tst)
    tst = datetime.now()

    # 执行正向操作开关
    positive_operations = np.full(len(labels_contours), True, bool)
    # 不描边一致性索引
    homochromy_in_stroke = []
    # 可能要描边的索引
    indices_with_stroke = []
    # 描边标记
    with_stroke = []
    for index, children in enumerate(childrens):
        has_appended_to_stroke = False
        if -1 != labels_hierarchy[index][HIER_PARENT] and labels_hierarchy[index][HIER_PARENT] == equivalents[index]:
            positive_operations[index] = False
        if 1 < len(children):
            if EQU_THRESH_MERGE < sum([areas[child_index]+lengths[child_index] for child_index in children]) / areas[index]:
                color_labels = np.array([labels[child_index]
                                        for child_index in children])
                color_labels_mask = np.not_equal(color_labels, -1)
                child_areas = np.array([areas[child_index]
                                       for child_index in children])
                color_labels_unique = np.unique(
                    color_labels[color_labels_mask])
                max_area = 0
                max_area_label = -1
                for unique_label in color_labels_unique:
                    area = child_areas[unique_label == color_labels].sum()
                    if max_area < area:
                        max_area = area
                        max_area_label = unique_label
                if -1 != max_area_label:
                    children_arr = np.array(children)
                    max_mask_arr = np.equal(color_labels, max_area_label)
                    index_to_negative = children_arr[max_mask_arr]
                    positive_operations[index_to_negative] = False
                    if index in outer_indices:
                        for child_index in children:
                            positive_operations[child_index] = is_whites[child_index]
                        homochromy_in_stroke.append(list(index_to_negative))
                        indices_with_stroke.append(children_arr)
                        with_stroke.append(np.logical_not(max_mask_arr))
                        has_appended_to_stroke = True
        if index in outer_indices and not has_appended_to_stroke:
            indices_with_stroke.append(np.array(children))
            with_stroke.append(
                np.full(len(children), fill_value=False, dtype=bool))
    homochromy_in_stroke = list(
        itertools.chain.from_iterable(homochromy_in_stroke))
    indices_with_stroke = np.concatenate(indices_with_stroke, axis=0)
    with_stroke = np.concatenate(with_stroke, axis=0)
    print('标记反向操作', datetime.now() - tst)
    tst = datetime.now()

    # # 外轮廓特殊处理标识
    # box_buffer_size = 2
    # distance_thresh = (3**2 + 3**2) / 2
    # ratio_threshold = 0.4
    # ratio_threshold_whole = 0.6
    # is_care_nest = False
    # indices_with_stroke = []
    # with_stroke = []
    # for out_cid in outer_indices:
    #     stoke_indices = np.array(childrens[out_cid])
    #     if 1 < len(stoke_indices):
    #         bboxes = [
    #             (box[0]-box_buffer_size, box[1]-box_buffer_size,
    #              box[0]+box[2]+box_buffer_size, box[1]+box[3]+box_buffer_size)
    #             for box in rectangles[stoke_indices]]
    #         nChilds = [len(childrens[index]) for index in stoke_indices]
    #         contours = [contours_label[index] for index in stoke_indices]
    #         matrix_size = len(stoke_indices)
    #         immerse_matrix = np.full(
    #             (matrix_size, matrix_size), False, np.bool_)
    #         immerse_float_matrix = np.full(
    #             (matrix_size, matrix_size), 0, np.float32)
    #         with_stoke = np.full(matrix_size, False, np.bool_)
    #         for row in range(matrix_size):
    #             one = np.transpose(contours[row], (1, 0, 2))
    #             for col in range(row+1, matrix_size):
    #                 inter_x = min(bboxes[row][2], bboxes[col][2]) - \
    #                     max(bboxes[row][0], bboxes[col][0])
    #                 inter_y = min(bboxes[row][3], bboxes[col][3]) - \
    #                     max(bboxes[row][1], bboxes[col][1])
    #                 if inter_x <= 0 or inter_y <= 0:
    #                     continue
    #                 tow = contours[col]
    #                 mask_one = ((np.array(bboxes[col][:2]).reshape((1, 1, 2)) <= one) &
    #                             (one <= np.array(bboxes[col][2:]).reshape((1, 1, 2)))).all(-1)
    #                 mask_tow = ((np.array(bboxes[row][:2]).reshape((1, 1, 2)) <= tow) &
    #                             (tow <= np.array(bboxes[row][2:]).reshape((1, 1, 2)))).all(-1)
    #                 new_one = one[mask_one]
    #                 new_tow = tow[mask_tow]
    #                 if min(new_one.shape) < 1 or min(new_tow.shape) < 1:
    #                     continue
    #                 if len(new_one.shape) == 2:
    #                     new_one = new_one.reshape((1,)+new_one.shape)
    #                 if len(new_tow.shape) == 2:
    #                     new_tow = np.expand_dims(new_tow, axis=1)
    #                 inter = np.abs(
    #                     new_tow - new_one).sum(axis=-1) < distance_thresh
    #                 immerse_float_matrix[row, col] = inter.any(
    #                     axis=0).sum() / one.shape[1]
    #                 immerse_float_matrix[col, row] = inter.any(
    #                     axis=1).sum() / tow.shape[0]
    #                 immerse_matrix[row,
    #                                col] = ratio_threshold < immerse_float_matrix[row, col]
    #                 immerse_matrix[col,
    #                                row] = ratio_threshold < immerse_float_matrix[col, row]
    #             with_stoke[row] = (immerse_matrix[row].any() or ratio_threshold_whole <
    #                                immerse_float_matrix[row].sum()) and (0 == nChilds[row] if is_care_nest else True)
    #     else:
    #         with_stoke = np.full_like(stoke_indices, False, bool)
    #     indices_with_stroke.append(stoke_indices)
    #     with_stroke.append(with_stoke)
    # indices_with_stroke = np.concatenate(indices_with_stroke, axis=0)
    # with_stroke = np.concatenate(with_stroke, axis=0)
    # # print(with_stroke)
    # print('标记描边操作', datetime.now() - tst)
    # tst = datetime.now()

    # 要描边的轮廓层级
    level_with_stroke = 1
    # 轮廓的层级
    contour_levels = np.full(len(labels_contours), -1)
    # 填充的颜色
    contour_colors = np.zeros(len(labels_contours), np.uint8)
    contour_index = 0  # 当前轮廓索引
    contour_level = 0  # 当前轮廓层级
    drawing_color = np.full(shape=1, fill_value=255, dtype=np.uint8)  # 当前轮廓颜色
    temp_stack: list[tuple[int, int, np.ndarray]] = []  # 临时堆栈
    while -1 != contour_index:
        # 更新层级
        contour_levels[contour_index] = contour_level
        # 更新颜色
        actual_color = drawing_color
        if not positive_operations[contour_index]:
            actual_color = ~drawing_color
        contour_colors[contour_index] = actual_color[0]
        # 压入同级以待后续
        if -1 != labels_hierarchy[contour_index][HIER_NEXT]:
            temp_stack.append(
                (labels_hierarchy[contour_index][HIER_NEXT], contour_level, drawing_color))
        # 优先处理子级
        if -1 != labels_hierarchy[contour_index][HIER_CHILD]:
            contour_index = labels_hierarchy[contour_index][HIER_CHILD]
            contour_level += 1
            drawing_color = ~actual_color
        elif len(temp_stack):
            # 弹出待处理
            contour_index, contour_level, drawing_color = temp_stack.pop()
        else:
            # 遍历结束
            contour_index = -1
    print('构建层级与分配颜色', datetime.now() - tst)
    tst = datetime.now()

    # 画图
    drawn_umask = np.zeros_like(region_fence_map, np.uint8)
    stroke_width = int(len(str(sum(drawn_umask.shape[:2]))) * 4.3 + 2)
    for level in range(contour_levels.max()+1):
        index_sequence = np.where(level == contour_levels)[0]
        if level_with_stroke == level and with_stroke.any():
            np.concatenate([index_sequence[np.logical_not(with_stroke)],
                           index_sequence[with_stroke]], out=index_sequence)
        for index in index_sequence:

            # # 这段调试代码很重要，莫删。
            # show_cont = ~region_fence_map.copy()*100
            # cv2.rectangle(show_cont, rectangles[index], 240, 3)
            # cv2.drawContours(show_cont, labels_contours, index, 255, 1)
            # cv2.namedWindow('show_cont', cv2.WINDOW_KEEPRATIO)
            # cv2.imshow('show_cont', show_cont)
            # print('level', level)
            # print('index', index)
            # print('color', contour_colors[index])
            # print('area', areas[index])
            # print('length', lengths[index])
            # print('rectangle[x,y,w,h]', rectangles[index])
            # if level_with_stroke == level:
            #     print('stroke', with_stroke[np.where(
            #         indices_with_stroke == index)[0]][0])
            # if -1 != labels_hierarchy[index][3]:
            #     print('----------------------------------------')
            #     print('parent level', level-1)
            #     print('parent index', labels_hierarchy[index][3])
            #     print('parent color',
            #           contour_colors[labels_hierarchy[index][3]])
            #     if level_with_stroke == level-1:
            #         print('parent stroke', with_stroke[np.where(
            #             indices_with_stroke == labels_hierarchy[index][3])[0]][0])
            # cv2.waitKey()
            # print('——————————————————————————————————————————————————')
            # print()
            # # 上面这段调试代码很重要，莫删。

            if areas[index] < FILTER_AREA and (rectangles[index][2] < FILTER_WIDTH or rectangles[index][3] < FILTER_HEIGHT):
                continue
            if areas[index] / lengths[index] < FILTER_A_DIV_L:
                continue

            if level_with_stroke != level and \
                -1 != labels_hierarchy[index][HIER_PARENT] and \
                    contour_colors[labels_hierarchy[index][HIER_PARENT]] == contour_colors[index]:
                continue

            if level_with_stroke == level and \
                with_stroke[np.where(indices_with_stroke == index)[0]][0] and \
                    not is_whites[index] and index not in homochromy_in_stroke:
                cv2.drawContours(drawn_umask, labels_contours, index, int(
                    ~contour_colors[index]), stroke_width)
            cv2.drawContours(drawn_umask, labels_contours, index,
                             int(contour_colors[index]), cv2.FILLED)

            # # 这一段调试也很重要。
            # cv2.namedWindow('drawn_umask', cv2.WINDOW_KEEPRATIO)
            # cv2.imshow('drawn_umask', drawn_umask)
            # cv2.waitKey()
            # # 以上一段调试也很重要。
    drawn_morph = drawn_umask
    # drawn_morph = cv2.morphologyEx(
    #     drawn_umask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, [5, 5]))
    print('绘制色块', datetime.now() - tst)
    tst = datetime.now()

    # 计算主色，用于填充反白后背景
    major_colour = None
    if isinstance(coloring_bg, str) and len(coloring_bg):
        color_str = ''.join(filter(str.isalnum, coloring_bg))
        if len(color_str) == 6:
            color = [int(color_str[:2], 16),
                     int(color_str[2:4], 16),
                     int(color_str[4:], 16)]
            if reverse_bg_color:
                color = color[::-1]
            major_colour = np.append(np.array(color).astype(np.float32), 0)
    if major_colour is None:
        major_colour = np.array([0, 0, 0, 0])
    # logo的填充颜色
    logo_colour = None
    if isinstance(coloring_logo, str) and len(coloring_logo):
        color_str = ''.join(filter(str.isalnum, coloring_logo))
        if len(color_str) == 6:
            color = [int(color_str[:2], 16),
                     int(color_str[2:4], 16),
                     int(color_str[4:], 16)]
            if reverse_logo_color:
                color = color[::-1]
            logo_colour = np.append(np.array(color).astype(np.float32), 255)
    print('计算颜色', datetime.now() - tst)
    tst = datetime.now()

    drawn_alpha = drawn_morph
    if logo_colour is None:
        drawn_white = cv2.cvtColor(drawn_alpha, cv2.COLOR_GRAY2BGRA)
    else:
        drawn_white = np.full(drawn_alpha.shape+(4,), logo_colour, np.uint8)
    drawn_color = np.full_like(drawn_white, major_colour, np.uint8)
    drawn_light = cv2.add(cv2.bitwise_and(drawn_white, drawn_white, mask=drawn_alpha),
                          cv2.bitwise_and(drawn_color, drawn_color, mask=~drawn_alpha))
    print('生成效果图', datetime.now() - tst)
    tst = datetime.now()

    # 按指定宽度扩展边界
    if expands is None or sum(expands) == 0:
        return drawn_light
    else:
        return expandBorder(drawn_light, expands, value=[float(val) for val in major_colour])




def whiteningDirect(
    image: np.ndarray, expands: list[int] = None,
    coloring_logo: str = None, coloring_bg: str = None,
    reverse_logo_color: bool = True, reverse_bg_color: bool = True,
    out_coordinate: list[int] = None
):

    raw_input_image = image
    if image is None:
        print('空图片!')
        return None

    # 计算前景掩码 foreground，同时将 image 的透明通道去除
    kmeans_K = 6
    kmeans_max_iter = 10
    kmeans_epsilon = 0.1
    kmeans_attempts = 3
    kmeans_flags = cv2.KMEANS_RANDOM_CENTERS
    if 3 == image.ndim and 4 == image.shape[-1]:
        foreground_mask = image[:, :, -1] > 0
        image = image[:, :, :-1]
    else:
        background_mask = segmentBackground(image, is_all_in_one=False,
                                            kmeans_K=kmeans_K, kmeans_max_iter=kmeans_max_iter, kmeans_epsilon=kmeans_epsilon, kmeans_attempts=kmeans_attempts,
                                            border_thickness=5, border_buffer=1, min_object_size=3)
        foreground_mask = ~background_mask

    # 先把周围空白区去掉，加下速
    expand_size = 3
    content_stddev_thresh = 1.0
    box_area_ratio_thresh = 0.8
    bbox, bbox_ex = findMaskBox(foreground_mask, expand_size)
    image = image[bbox_ex[1]:bbox_ex[3], bbox_ex[0]:bbox_ex[2]]
    foreground_mask = foreground_mask[bbox_ex[1]:bbox_ex[3],
                                      bbox_ex[0]:bbox_ex[2]]
    bounding_box = [bbox[0] - bbox_ex[0], bbox[1] - bbox_ex[1],
                    bbox[2] - bbox_ex[0], bbox[3] - bbox_ex[1]]
    if expands is None or sum(expands) == 0:
        top_left_xy = [-bbox_ex[0], -bbox_ex[1]]
    else:
        exps = (expands*2)[:2]
        top_left_xy = [-bbox_ex[0]+exps[0], -bbox_ex[1]+exps[1]]
    if isinstance(out_coordinate, list):
        out_coordinate.clear()
        out_coordinate.extend(top_left_xy)
    # 针对logo内容跑到透明通道的情况的处理
    # 先搁置，以后再优化此问题
    is_fresh_image = False
    if image.std() < content_stddev_thresh and \
            3 == len(raw_input_image.shape) and 4 == raw_input_image.shape[-1]:
        image = cv2.cvtColor(raw_input_image[:, :, -1], cv2.COLOR_GRAY2BGR)
        image = ~image
        is_fresh_image = True
    cbox, _ = findContentBox2(image)
    if (cbox[2]-cbox[0])*(cbox[3]-cbox[1]) < (bounding_box[2]-bounding_box[0])*(bounding_box[3]-bounding_box[1])*box_area_ratio_thresh and \
            3 == len(raw_input_image.shape) and 4 == raw_input_image.shape[-1]:
        umask_for_alpha_content = raw_input_image[:, :, -1].copy()
        umask_for_alpha_content[cbox[1]:cbox[3], cbox[0]:cbox[2]] = 0
        umask_for_BGR_content = umask_for_alpha_content ^ raw_input_image[:, :, -1]
        content_from_alpha = cv2.cvtColor(
            ~umask_for_alpha_content, cv2.COLOR_GRAY2BGR)
        image = cv2.add(cv2.bitwise_and(raw_input_image[:, :, :-1], raw_input_image[:, :, :-1], mask=umask_for_BGR_content),
                        cv2.bitwise_and(content_from_alpha, content_from_alpha, mask=~umask_for_BGR_content))
        is_fresh_image = True
    if is_fresh_image:
        image = image[bbox_ex[1]:bbox_ex[3], bbox_ex[0]:bbox_ex[2]]

    # 单色直接反白
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.threshold(
        gray_image, 120, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    majorV, _ = calcMajorInThickBorder(binary_image)
    if 0 < majorV:
        binary_image = ~binary_image

    # 计算前景背景颜色
    bg_color = np.array([0, 0, 0, 0], np.float32)
    if isinstance(coloring_bg, str) and len(coloring_bg):
        color_str = ''.join(filter(str.isalnum, coloring_bg))
        if len(color_str) == 6:
            color = [int(color_str[:2], 16),
                     int(color_str[2:4], 16),
                     int(color_str[4:], 16)]
            if reverse_bg_color:
                color = color[::-1]
            bg_color = np.append(np.array(color).astype(np.float32), 0)
    fg_color = None
    if isinstance(coloring_logo, str) and len(coloring_logo):
        color_str = ''.join(filter(str.isalnum, coloring_logo))
        if len(color_str) == 6:
            color = [int(color_str[:2], 16),
                     int(color_str[2:4], 16),
                     int(color_str[4:], 16)]
            if reverse_logo_color:
                color = color[::-1]
            fg_color = np.append(np.array(color).astype(np.float32), 255)
    # 生成
    if fg_color is None:
        the_white = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGRA)
    else:
        the_white = np.full(binary_image.shape+(4,), fg_color, np.uint8)
    the_color = np.full_like(the_white, bg_color, np.uint8)
    the_light = cv2.add(cv2.bitwise_and(the_white, the_white, mask=binary_image),
                        cv2.bitwise_and(the_color, the_color, mask=~binary_image))

    if expands is None or sum(expands) == 0:
        return the_light
    else:
        return expandBorder(the_light, expands, value=[float(val) for val in bg_color])