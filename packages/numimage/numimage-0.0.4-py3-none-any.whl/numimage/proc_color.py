import cv2
import json
import math
import typing
import numpy as np
import pandas as pd
from itertools import combinations
from configurations import GRAY2K, HRANK


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as load_f:
        str_f = load_f.read()
        if len(str_f) > 0:
            datas = json.loads(str_f)
        else:
            datas = {}
    return datas


def hex2rgb(hex:str="#ff7722"):

    if len(hex[1:]) == 3:
        hex = "#" + hex[1] + hex[1] + hex[2] +hex[2] + hex[3]+ hex[3]

    b = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    r = int(hex[5:7], 16)

    return r,g,b
def hex2bgr(hex:str="#ff7722"):

    if len(hex[1:]) == 3:
        hex = "#" + hex[1] + hex[1] + hex[2] +hex[2] + hex[3]+ hex[3]

    b = int(hex[1:3], 16)
    g = int(hex[3:5], 16)
    r = int(hex[5:7], 16)

    return b,g,r

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def normalization(array,k):
    ymax = 255
    ymin = 0
    xmax = max(array)
    xmin = min(array)


    for j in range(k):
        array[j] = round(((ymax - ymin) * (array[j] - xmin) / (xmax - xmin)) + ymin)

    return array


def RGB_to_Hex(rgb):

    strs = '#'
    for i in rgb:
        num = int(i) 
        strs += str(hex(num))[-2:].replace('x', '0').upper()

    return strs


def rgb2hsv(r, g, b):

    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


def rgb2cymk(R,G,B):
    gray2k = load_json(GRAY2K)
    gray = R * 0.30 * 255  + G * 0.59 *255  + B * 0.11 * 255
    K = gray2k[str(int(gray))]
    C = (1 - R ) * 100
    M = (1 - G ) * 100
    Y = (1 - B ) * 100

    return int(C), int(Y), int(M), int(K)


def overlap_color(original_color):
    r,g,b = hex2rgb(original_color)
    h,s,v = rgb2hsv(r/255,g/255,b/255)
    s,v = s*100,v*100
    s = s + 10
    if s >=100:
        s = 100
    
    v = v-5
    if v<0:
        v = 0
    r,g,b = hsv2rgb(h,s/100,v/100)
    return RGB_to_Hex([r,g,b])


def generate_light_color(original_color):
    r,g,b = hex2rgb(original_color)
    h,s,v = rgb2hsv(r/255,g/255,b/255)
    s,v = s*100,v*100
    s = s - 50
    if s <=20:
        s = 20
    
    v = v + 40
    if v>=100:
        v = 100
    r,g,b = hsv2rgb(h,s/100,v/100)
    return RGB_to_Hex([r,g,b])


def generate_dark_color(original_color):
    r,g,b = hex2rgb(original_color)
    h,s,v = rgb2hsv(r/255,g/255,b/255)
    s,v = s*100,v*100
    s = s + 50
    if s >=100:
        s = 100
    
    v = v - 30
    if v<=30:
        v = 30
    r,g,b = hsv2rgb(h,s/100,v/100)
    return RGB_to_Hex([r,g,b])



def mainColorSelection(all_colors_rgb,all_colors_cmyk,all_colors_hsv,k_value=30):
    '''
    B1-a 颜色逻辑
    :param main_color:  粗提取的主色
    :param second_color: 粗提取的副色
    :param main_color_k: 粗提取的主色k值
    :param second_color_k:粗体取得副色k值
    :return: main_color_list 颜色列表（按顺序）
    '''
    h_degree = load_json(HRANK)
    if len(all_colors_rgb) == 1:
        return all_colors_rgb


    if len(all_colors_rgb) == 2:
        for i in range(0,len(all_colors_rgb)):
           
            if all_colors_cmyk[i][3] > 90:
                all_colors_rgb.remove(all_colors_rgb[i])
                all_colors_hsv.remove(all_colors_hsv[i])
                all_colors_cmyk.remove(all_colors_cmyk[i])
                return all_colors_rgb
        
        if len(all_colors_rgb) == 2:
            if all_colors_hsv[0][1] < 0.1 or all_colors_hsv[1][1] < 0.1:
                if all_colors_hsv[0][1] < all_colors_hsv[1][1]:
                    all_colors_rgb[0],all_colors_rgb[1] = all_colors_rgb[1],all_colors_rgb[0]
                return all_colors_rgb


            kmax,kmin = 0,100
            for i in range(0,len(all_colors_rgb)):
                if all_colors_cmyk[i][3] > kmax:
                    kmax = all_colors_cmyk[i][3]
                if all_colors_cmyk[i][3] < kmin:
                    kmin = all_colors_cmyk[i][3]

            if kmin > k_value or kmax < k_value:
                if all_colors_rgb[1][0] > all_colors_rgb[0][0]:
                    all_colors_rgb[0],all_colors_rgb[1] = all_colors_rgb[1],all_colors_rgb[0]
            else:
                if all_colors_cmyk[1][3] > all_colors_cmyk[0][3]:
                    all_colors_rgb[0], all_colors_rgb[1] = all_colors_rgb[1], all_colors_rgb[0]
            

            if len(all_colors_rgb) ==2:
                for key, value in h_degree.items():
                    if all_colors_hsv[0][0] > value[0] and all_colors_hsv[0][0] <= value[1]:
                        first_color_H = key
                    if all_colors_hsv[0][0] > 337.5 or all_colors_hsv[0][0] <= 22.5:
                        first_color_H = 'red'
                    if all_colors_hsv[1][0] > value[0] and all_colors_hsv[1][0] <= value[1]:
                        second_color_H = key
                    if all_colors_hsv[1][0] > 337.5 or all_colors_hsv[1][0] <= 22.5:
                        second_color_H = 'red'
                if first_color_H == second_color_H:
                    all_colors_rgb = [all_colors_rgb[0]]



        return all_colors_rgb


    if len(all_colors_rgb) >= 3:
        
        low_s = []
        all_colors_rgbs,all_colors_hsvs,all_colors_cmyks = [],[],[]

        for i in range(0, len(all_colors_rgb)):
            if all_colors_cmyk[i][3] <90 and all_colors_hsv[i][1] >=0.1:
                all_colors_rgbs.append(all_colors_rgb[i])
                all_colors_cmyks.append(all_colors_cmyk[i])
                all_colors_hsvs.append(all_colors_hsv[i])

            if all_colors_hsv[i][1] < 0.1:
                low_s.append(all_colors_rgb[i])

        if all_colors_rgbs == []:
            output_rgb = []
            output_rgb.append([low_s[0][0],low_s[0][1],low_s[0][2]])
            return output_rgb
    


        all_colors_rgb = all_colors_rgbs
        all_colors_hsv = all_colors_hsvs
        all_colors_cmyk = all_colors_cmyks

        all_colors = []
        for i in range(0,len(all_colors_rgb)):
            all_color = all_colors_rgb[i] + all_colors_hsv[i] + all_colors_cmyk[i]
            all_colors.append(all_color)

        df = pd.DataFrame(all_colors, columns=list('RGBHSVCMYK'))

        df.loc[:,'HH'] = ''
        for idx, data in df.iterrows():
            for key, value in h_degree.items():
                if data.H > value[0] and data.H <= value[1]:
                    df.loc[idx,'HH'] = key
                if data.H > 337.5 or data.H <= 22.5:
                    df.loc[idx,'HH'] = 'red'

        k30_upper = df[df.K>k_value]
        k30_lower = df[df.K<=k_value]

        k30_lower = k30_lower[(k30_lower.R < 200) & (k30_lower.G >= 150)]
        k30_lower = k30_lower[(k30_lower.R < 200) & (k30_lower.B >= 150)]
        k30_lower = k30_lower.sort_values("R", inplace=False)
        try:
            k30_lower_r = k30_lower.head(1)
        except:
            k30_lower_r = pd.DataFrame({})
        k30_upper = k30_upper.sort_values(by=['R', 'S'], inplace=False,ascending = False)

        df_new = k30_upper.drop_duplicates(subset="HH")
        df_new = df_new.sort_values(by='HH', ascending=False)
        df_new = df_new.sort_values("R", inplace=False, ascending=False)

        df_new = pd.concat([df_new, k30_lower_r], ignore_index=True)
        df_new = df_new.sort_values(by=['R', 'S'], inplace=False, ascending=False)
        if df_new.shape[0] >=4:
            output = df_new.iloc[0:4,0:3]
            output_rgb = []
            for idx,data in output.iterrows():
                output_rgb.append([data.R,data.G,data.B])

        else:
            output_old = df_new.iloc[0:4, 0:3]
            output_rgb = []
            for idx,data in output_old.iterrows():
                output_rgb.append([data.R,data.G,data.B])
            if len(low_s) >0:
                output_rgb.append([low_s[0][0],low_s[0][1],low_s[0][2]])

        if output_rgb == []:
            output = df.iloc[0:4, 0:3]
            for idx,data in output.iterrows():
                output_rgb.append([data.R,data.G,data.B])
            if len(low_s) > 0:
                output_rgb.append([low_s[0][0],low_s[0][1],low_s[0][2]])
        if output_rgb == []:
            output_rgb.append([0,0,0])
        return output_rgb

def doubleColorCollection(all_colors_rgb, all_colors_cmyk, all_colors_hsv):

    h_degree = load_json(HRANK)
    all_colors_rgbs, all_colors_hsvs, all_colors_cmyks = [], [], []

    for i in range(0, len(all_colors_rgb)):
        if all_colors_cmyk[i][3] != 100 or all_colors_cmyk[i][3] >= 20:
            all_colors_rgbs.append(all_colors_rgb[i])
            all_colors_cmyks.append(all_colors_cmyk[i])
            all_colors_hsvs.append(all_colors_hsv[i])

    all_colors_rgb = all_colors_rgbs
    all_colors_hsv = all_colors_hsvs
    all_colors_cmyk = all_colors_cmyks

    all_colors = []
    for i in range(0, len(all_colors_rgb)):
        all_color = all_colors_rgb[i] + all_colors_hsv[i] + all_colors_cmyk[i]
        all_colors.append(all_color)
    df = pd.DataFrame(all_colors, columns=list('RGBHSVCMYK'))
    df.loc[:, 'T'] = ''
    for idx, data in df.iterrows():
        for key, value in h_degree.items():
            if data.H > value[0] and data.H <= value[1]:
                df.loc[idx, 'T'] = key
            if data.H > 337.5 or data.H <= 22.5:
                if data.H != 0:
                    df.loc[idx,'T'] = 'red'
                else:
                    df.loc[idx,'T'] = 'black' 


    output_rgb = all_colors_rgb
  
    if len(output_rgb) == 2:
        return [output_rgb]
    if len(output_rgb) >= 3:
        if "#000000" in output_rgb:
            return [output_rgb.remove('#000000')]
        else:
            screen_rgb = []
            for rgb in output_rgb:
                screen_rgb.append(df[(df.R == rgb[0]) & (df.G ==rgb[1]) & (df.B ==rgb[2])].iloc[0,:].tolist())

            df = pd.DataFrame(screen_rgb, columns=list('RGBHSVCMYKT'))

            combine_array = list(combinations([x for x in range(df.shape[0])],2))
            combine_list = []
            for combine in combine_array:
                a = df.iloc[combine[0],:]
                b = df.iloc[combine[1],:]
                combine_list.append([a.R,a.G,a.B,b.R,b.G,b.B,abs(a.H-b.H) if abs(a.H-b.H) < 180 else 360 - abs(a.H-b.H),abs(a.K-b.K),a["T"],b["T"]])

            df = pd.DataFrame(combine_list, columns=list('RGBrgbHKTt')).sort_values(by=['H', 'K'], inplace=False, ascending=False)

            df60 = df[df.H>=60]
            df30 = df[df.H<30]
            df30 = df30[df30['K']>=20]
            df40 = df[(df.H<60) & (df.H>=30)]


            df = pd.concat([df60,df30,df40])

            output_rgb = []
            output = df.iloc[0:3, 0:6]
            for idx, data in output.iterrows():
                a = [[data.R, data.G, data.B], [data.r, data.g, data.b]]
                output_rgb.append(a)

            return output_rgb



def drawPalette(colors: np.ndarray, size_mul: int = 1):
    
    size_mul = int(size_mul)
    size_mul = 1 if size_mul < 1 else size_mul
    global_size = 600*size_mul
    if len(colors) <= 4:
        rows = 2
    elif len(colors) <= 9:
        rows = 3
    elif len(colors) <= 16:
        rows = 4
    else:
        rows = 5
    cols = rows
    size = global_size // rows
    palette = np.full(
        (rows*size, cols*size, colors.shape[-1]), fill_value=180, dtype=np.uint8)
    for ind in range(rows+cols):
        cv2.line(palette, (ind*size, 0), (0, ind*size), [80]*3, 2)
    for ind in range(rows+cols):
        cv2.line(palette, ((ind-rows)*size, 0),
                 (ind*size, rows*size), [80]*3, 2)
    for row in range(rows):
        for col in range(cols):
            index = row*cols+col
            if index < len(colors):
                palette[row*size:(row+1)*size, col *
                        size:(col+1)*size] = colors[index]
    for col in range(cols+1):
        cv2.line(palette, (col*size, 0), (col*size, rows*size), [255]*3, 1)
    for row in range(rows+1):
        cv2.line(palette, (0, row*size), (cols*size, row*size), [255]*3, 1)
    return palette


def mergeColor(colors: np.ndarray, numbers: np.ndarray, distance_thresh: float = 20.0, max_iter: int = 2):
 
    max_iter -= 1
    colors_h = np.expand_dims(colors, axis=0)
    colors_v = np.expand_dims(colors, axis=1)
    distances = np.linalg.norm(colors_v-colors_h, axis=2)
    equal_mask = np.less_equal(distances, distance_thresh)
    one_to_N = [set(np.where(ids)[0]) for ids in equal_mask]
    dealt = np.zeros_like(numbers, dtype=bool)
    clusters_indices = []
    for index in range(len(dealt)):
        if dealt[index]:
            continue
        dealt[index] = True
        total_set = one_to_N[index]
        done_set = set([index])
        wait_set = total_set - done_set
        while len(wait_set):
            new_index = list(wait_set)[0]
            dealt[new_index] = True
            total_set.update(one_to_N[new_index])
            done_set.add(new_index)
            # wait_set.remove(new_index)
            wait_set = total_set - done_set
        clusters_indices.append(np.array(list(total_set)))
    new_numbers = np.array([np.sum(numbers[indices])
                           for indices in clusters_indices])
    new_colors = np.array([np.sum(colors[indices]*np.expand_dims(numbers[indices], axis=1), axis=0) /
                           new_numbers[index] for index, indices in enumerate(clusters_indices)])
    if 0 < max_iter:
        return mergeColor(new_colors, new_numbers, distance_thresh, max_iter)
    return new_colors, new_numbers


def pickColor(
    image: np.ndarray,
    degenerate_order: typing.Literal[2, 4, 8, 16] = 8,
    edge_threshold: int | float | None = None,
    edge_diffuse_width: typing.Literal[3, 5] | None = 3,
    kmeans_max_iter: int = 10,
    kmeans_eps: float = 0.1,
    kmeans_attempts: int = 3,
    color_dist_thresh: float = 20.0,
    merge_max_iter: int = 2,
    *,
    drop_white: bool = True,
    sort_base_num: bool = True,
    return_palette: bool = False,
):
    input_image = image
    ret_dict = {}

    if image is None or 0 == image.size:
        return ret_dict

    if image.dtype != np.uint8:
        return ret_dict

    if image.ndim < 2 or 3 < image.ndim:
        return ret_dict

    if image.ndim == 2:
        image = image.reshape(image.shape+(1,))

    alpha_u8 = None
    alpha_fg = None
    if 4 == image.shape[-1]:
        alpha_u8 = image[:, :, 3]
        image = image[:, :, :3]
        alpha_fg = 127 < alpha_u8

    lut = np.array(
        [i//degenerate_order*degenerate_order for i in range(256)], dtype=np.uint8)
    degenerated = cv2.LUT(image, lut)
    # cv2.namedWindow('degenerated', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('degenerated', degenerated)

    if edge_threshold is None:
        edge_threshold = 256/degenerate_order
    edge = cv2.Canny(degenerated, edge_threshold, edge_threshold)
    # cv2.namedWindow('edge', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('edge', edge)

    diffused_edge = edge
    if edge_diffuse_width:
        diffused_edge = cv2.dilate(edge, cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (edge_diffuse_width,)*2))
    # cv2.namedWindow('diffused_edge', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('diffused_edge', diffused_edge)
    flat_region = diffused_edge < 128

    if alpha_fg is None:
        flat_fg_region = flat_region
    else:
        flat_fg_region = np.logical_and(alpha_fg, flat_region)
    if not flat_fg_region.any():
        flat_fg_region = np.full_like(
            flat_fg_region, fill_value=True, dtype=bool)
    # cv2.namedWindow('flat_fg_region', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('flat_fg_region', flat_fg_region.astype(np.uint8)*255)
    masked_low_order = degenerated[flat_fg_region]

    nBits = int(round(math.log(degenerate_order, 2)))
    set_in_1 = np.zeros(len(masked_low_order), dtype=np.uint32)
    for ch in range(masked_low_order.shape[-1]):
        set_in_1 += masked_low_order[:,
                                     ch].astype(np.uint32)//degenerate_order << ch*nBits

    the_1color, the_inv_ind, the_count = np.unique(
        set_in_1, return_inverse=True, return_counts=True)
    # print(the_1color)
    # print(the_inv_ind)
    # print(the_count)
    pick_1mask = np.zeros_like(the_count, dtype=bool)
    rank_threshold = np.array(sorted(list(set([
        len(str(image.shape[0])),
        len(str(image.shape[1])),
        len(str(sum(image.shape[:2]))),
    ])))[::-1])
    the_ranks = np.array([len(str(int(count))) for count in the_count])
    for rank_thresh in rank_threshold:
        pick_1mask = np.greater_equal(the_ranks, rank_thresh)
        if pick_1mask.any():
            break
    if not pick_1mask.any():
        pick_1mask = np.greater(the_count, np.mean(the_count))
    if not pick_1mask.any():
        pick_1mask[np.argmax(the_count)] = True
    pick_1color = the_1color[pick_1mask]
    pick_count = the_count[pick_1mask]
    # print(pick_1color)
    # print(pick_count)
    pick_inv_mask = np.zeros_like(the_inv_ind, dtype=bool)
    for ind in np.where(pick_1mask)[0]:
        pick_inv_mask |= np.equal(the_inv_ind, ind)
    # print(pick_inv_mask.all(), pick_inv_mask.any())
    # print(len(set_in_1) == len(pick_inv_mask))

    _, label_m, colors_in_raw = cv2.kmeans(
        image[flat_fg_region][pick_inv_mask].astype(np.float32),
        K=len(pick_1color),
        bestLabels=None,
        criteria=(cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS,
                  kmeans_max_iter, kmeans_eps),
        attempts=kmeans_attempts,
        flags=cv2.KMEANS_RANDOM_CENTERS)
    # print(label_m.max())
    # print(colors_in_raw.shape)
    numbers = np.array([np.sum(np.equal(label_m, label_id))
                       for label_id in range(len(colors_in_raw))])

    colors_new, numbers_new = mergeColor(
        colors_in_raw, numbers, distance_thresh=color_dist_thresh, max_iter=merge_max_iter)
    if drop_white:
        no_white_mask = np.any(np.less(colors_new, 240), axis=1)
        colors_new = colors_new[no_white_mask]
        numbers_new = numbers_new[no_white_mask]
    if sort_base_num:
        descend_indices = np.argsort(numbers_new)[::-1]
        colors_new = colors_new[descend_indices]
        numbers_new = numbers_new[descend_indices]

    ret_dict.update({
        'colors': colors_new,
        'numbers': numbers_new
    })

    if return_palette:
        palette = drawPalette(colors_new)
        ret_dict.update({
            'palette': palette
        })

    return ret_dict

