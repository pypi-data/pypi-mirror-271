import cv2
import numpy as np
from common import removebackground


def Stroke(image,kernel_size,iteration=1):

    kernel = np.ones(kernel_size, np.uint8)
    img_dilate = cv2.dilate(image, kernel, iterations = iteration)

    # gray = cv2.cvtColor(img_dilate,cv2.COLOR_BGR2GRAY)
    gray = img_dilate[:,:,-1]

    contours, hierarchy = cv2.findContours(gray,mode = cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
    return image, contours


def outlineImage_for_1(input: dict, output: dict) -> bool:
    # use_material_pack: bool = input['use_material_pack']
    images: list[np.ndarray] = input['images']
    image: np.ndarray = images[0]
    # 可选参数
    is_fill = bool(input["is_fill"])
    # is_contours = bool(input["is_contours"])
    expand = int(input["expand"])
    color = list(input['color'])
    # color = color[::-1]
    color.append(255)

    if image.shape[2] == 3:
        image = removebackground(image)
    
    image = cv2.copyMakeBorder(image, expand,expand,expand,expand, cv2.BORDER_CONSTANT, value=(255,255,255,0))

    image2 = image.copy()
    image_gray = image[:,:,-1]
    h,w = image.shape[0],image.shape[1]

    if len(image_gray[image_gray != 0]) / (w*h) < 0.4:
        image, contours = Stroke(image, (20,20))
    elif len(image_gray[image_gray != 0]) / (w*h) < 0.5 and len(image_gray[image_gray != 0]) / (w * h) > 0.4:
        image, contours = Stroke(image, (15,15))
    else:
        image, contours = Stroke(image, (12,12))
    # contours, hierarchy = cv2.findContours(image_gray,mode = cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
    temp = np.zeros(image.shape, np.uint8) * 0
    

    px = int(30 * (max(image.shape[0],image.shape[1]) / 500))

    if 0 < expand:
        whitebottom = cv2.drawContours(temp, contours, -1, color, expand)
    else:
        whitebottom = temp
        
        
    if is_fill == True:
        whitebottom = cv2.drawContours(whitebottom, contours, -1, color, -1)
        contours, hierarchy = cv2.findContours(whitebottom[:,:,-1], mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        whitebottom = cv2.drawContours(whitebottom, contours, -1, color, -1)
    alpha = image2[:,:,3]       
    whitebottom = cv2.add(cv2.bitwise_and(image2, image2, mask=alpha), cv2.bitwise_and(whitebottom, whitebottom, mask=~alpha))

    # if is_fill == True and is_contours == False:
    #     whitebottom = cv2.drawContours(whitebottom, contours, -1, color, -1)
    #     contours, hierarchy = cv2.findContours(whitebottom[:,:,-1], mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    #     whitebottom = cv2.drawContours(whitebottom, contours, -1, color, -1)
    #     # alpha = image2[:,:,3]       
    #     # whitebottom = cv2.add(cv2.bitwise_and(image2, image2, mask=alpha), cv2.bitwise_and(whitebottom, whitebottom, mask=~alpha))

    # if is_fill == False and is_contours == True:
    #     whitebottom = cv2.drawContours(whitebottom, contours, -1, color, expand)
    # if 0 == expand:
    #     # 改写一下内填充的部分。多出来的部分不要了,还是会剩1个像素。
    #     alpha = image2[:,:,3]       
    #     whitebottom = cv2.bitwise_and(whitebottom, whitebottom, mask=alpha)
    # if 0 == expand:
    #     for contour in contours:
    #         for point in contour:
    #             x,y = point[0]
    #             whitebottom[y,x,3] = 0

    
    
    output.clear() 
    # images[0]=image
    output['images'] = [whitebottom]
    return True

def outlineImage_for_2(input: dict, output: dict) -> bool:
    # use_material_pack: bool = input['use_material_pack']
    images: list[np.ndarray] = input['images']
    image: np.ndarray = images[0]
    # 可选参数
    is_fill = bool(input["is_fill"])
    is_contours = bool(input["is_contours"])
    expand = int(input["expand"])
    color = list(input['color'])
    # color = color[::-1]
    color.append(255)

    if image.shape[2] == 3:
        image = removebackground(image)
    
    image = cv2.copyMakeBorder(image, expand,expand,expand,expand, cv2.BORDER_CONSTANT, value=(255,255,255,0))

    image2 = image.copy()
    image_gray = image[:,:,-1]
    h,w = image.shape[0],image.shape[1]

    if len(image_gray[image_gray != 0]) / (w*h) < 0.4:
        image, contours = Stroke(image, (20,20))
    elif len(image_gray[image_gray != 0]) / (w*h) < 0.5 and len(image_gray[image_gray != 0]) / (w * h) > 0.4:
        image, contours = Stroke(image, (15,15))
    else:
        image, contours = Stroke(image, (12,12))
    # contours, hierarchy = cv2.findContours(image_gray,mode = cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
    temp = np.zeros(image.shape, np.uint8) * 0
    

    px = int(30 * (max(image.shape[0],image.shape[1]) / 500))

    if 0 < expand:
        whitebottom = cv2.drawContours(temp, contours, -1, color, expand)
    else:
        whitebottom = temp


    if is_contours:
        whitebottom = cv2.drawContours(whitebottom, contours, -1, color, -1)
        contours, hierarchy = cv2.findContours(whitebottom[:,:,-1], mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        temp = np.zeros(image.shape, np.uint8) * 0
        whitebottom = cv2.drawContours(temp, contours, -1, color, expand)

    if is_fill:
        whitebottom = cv2.drawContours(whitebottom, contours, -1, color, -1)
        contours, hierarchy = cv2.findContours(whitebottom[:,:,-1], mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        whitebottom = cv2.drawContours(whitebottom, contours, -1, color, -1)
        alpha = image2[:,:,3]       
        whitebottom = cv2.add(cv2.bitwise_and(image2, image2, mask=alpha), cv2.bitwise_and(whitebottom, whitebottom, mask=~alpha))

    if not is_contours and not is_fill:
        alpha = image2[:,:,3]       
        whitebottom = cv2.add(cv2.bitwise_and(image2, image2, mask=alpha), cv2.bitwise_and(whitebottom, whitebottom, mask=~alpha))


    output.clear() 
    # images[0]=image
    output['images'] = [whitebottom]
    return True
