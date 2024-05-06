import math
import torch
import torchvision.transforms.functional as F


def get_padding(img, des_h, des_w, margin=5):
    """
    img: PIL img
    des_h, des_w : int
    margin: int
    """
    # get padding size for padding and resize transform, the destination w and h are inputs
    w, h = img.size[0], img.size[1]
    scale = min(float(des_h-2*margin)/h, float(des_w-2*margin)/w)
    pad_h, pad_w = math.ceil((des_h-scale*h)/(2*scale)), math.ceil((des_w-scale*w)/(2*scale))
    return pad_h, pad_w


def pad_and_resize(img, des_h, des_w, margin=5):
    """
    img: PIL img
    des_h, des_w : int
    margin: int
    """
    w, h = img.size[0], img.size[1]
    pad_h, pad_w = get_padding(img, des_h, des_w, margin)
    img = F.pad(img,padding=[pad_w,pad_h],fill=150)
    mid_w, mid_h = img.size[0], img.size[1]
    img = F.resize(img,[des_h,des_w])
    h_scale, w_scale = float(des_h)/mid_h, float(des_w)/mid_w
    return img, (h_scale,w_scale),(pad_h,pad_w),(w,h)


def transform_to_origin(xyxy, mid_scale, paddings,ori_size):
    """
    xyxy: torch tensor shape (N,4)
    mid_scale: tuple(int, int)
    paddings: tuple(int, int)
    ori_size: tuple(int, int)
    """
    h_scale, w_scale = mid_scale
    pad_h, pad_w = paddings
    w,h = ori_size
    x1, y1, x2, y2 = xyxy[:,0:1], xyxy[:, 1:2],xyxy[:, 2:3],xyxy[:,3:4]
    x1, y1, x2, y2 = x1/w_scale-pad_w, y1/h_scale-pad_h, x2/w_scale-pad_w, y2/h_scale-pad_h
    x1, y1, x2, y2 = x1.clamp(0,w), y1.clamp(0,h), x2.clamp(0,w), y2.clamp(0,h)
    new_xyxy = torch.concat([x1,y1,x2,y2],dim=-1)
    return new_xyxy


# custom pad and torch resize transformation
class PadAndResize(object):
    def __init__(self, output_size, margin=5):
        assert isinstance(output_size, int)
        self.output_size = output_size
        self.margin = margin

    def __call__(self, image):
        output_img,_,_,_ = pad_and_resize(image,self.output_size,self.output_size,self.margin)
        return output_img


def bboxes_iou(bboxes_a, bboxes_b, xyxy=True, giou=False):
    """
    Args:
        bboxes_a: tensor, shape [N,4]
        bboxes_b: tensor, shape [M,4]
        xyxy: bool, true if bboxes are in xyxy format,
              flase if bboxes are in xywh format
    Return:
        pairwise iou: tensor, shape [N,M]
    """
    if bboxes_a.shape[1] != 4 or bboxes_b.shape[1] != 4:
        raise IndexError

    if xyxy:
        tl = torch.max(bboxes_a[:, None, :2], bboxes_b[None, :, :2])  # [N,M,2]
        br = torch.min(bboxes_a[:, None, 2:], bboxes_b[None, :, 2:])  # [N,M,2]
        area_a = torch.prod(bboxes_a[:, 2:] - bboxes_a[:, :2], 1)  # [N]
        area_b = torch.prod(bboxes_b[:, 2:] - bboxes_b[:, :2], 1)  # [M]
        if giou:
            enclosed_tl = torch.min(bboxes_a[:, None, :2], bboxes_b[None, :, :2])  # [N,M,2]
            enclosed_br = torch.max(bboxes_a[:, None, 2:], bboxes_b[None, :, 2:])
    else:
        tl = torch.max(bboxes_a[:, None, :2], bboxes_b[None, :, :2])
        br = torch.min(
            bboxes_a[:, None, :2] + bboxes_a[:, None, 2:],
            bboxes_b[None, :, :2] + bboxes_b[None, :, 2:]
        )
        area_a = torch.prod(bboxes_a[:, 2:], 1)  # [N]
        area_b = torch.prod(bboxes_b[:, 2:], 1)  # [M]
        if giou:
            enclosed_tl = torch.min(bboxes_a[:, None, :2], bboxes_b[None, :, :2])
            enclosed_br = torch.max(
                bboxes_a[:, None, :2] + bboxes_a[:, None, 2:],
                bboxes_b[None, :, :2] + bboxes_b[None, :, 2:]
            )  # [N,M,2]


    is_overlapped = (tl < br).type(tl.dtype).prod(dim=2)  # [N,M]
    area_overlap = torch.prod(br-tl, 2) * is_overlapped  # [N,M]
    union = area_a[:, None] + area_b[None, :] - area_overlap
    ious = area_overlap/union
    if giou:
        enclosed_wh = (enclosed_br-enclosed_tl).clamp(min=0)
        enclosed_area = torch.maximum(torch.tensor([1e-6]).to(enclosed_wh.device),
                                      enclosed_wh[:,:,0] * enclosed_wh[:,:,1])
        gious = ious - (enclosed_area-union)/enclosed_area
        return 1 - gious
    else:
        return ious


def bboxes_overlap(bboxes_a, bboxes_b, xyxy=True):
    """
    Args:
        bboxes_a: tensor, shape [N,4]
        bboxes_b: tensor, shape [M,4]
        xyxy: bool, true if bboxes are in xyxy format,
              flase if bboxes are in xywh format
    Return:
        pairwise overlap_ratio: tensor, shape [N,M]
    """
    if bboxes_a.shape[1] != 4 or bboxes_b.shape[1] != 4:
        raise IndexError

    if xyxy:
        tl = torch.max(bboxes_a[:, None, :2], bboxes_b[None, :, :2])  # [N,M,2]
        br = torch.min(bboxes_a[:, None, 2:], bboxes_b[None, :, 2:])  # [N,M,2]
        area_a = torch.prod(bboxes_a[:, 2:] - bboxes_a[:, :2], 1)  # [N]
        area_b = torch.prod(bboxes_b[:, 2:] - bboxes_b[:, :2], 1)  # [M]

    else:
        tl = torch.max(bboxes_a[:, None, :2], bboxes_b[None, :, :2])
        br = torch.min(
            bboxes_a[:, None, :2] + bboxes_a[:, None, 2:],
            bboxes_b[None, :, :2] + bboxes_b[None, :, 2:]
        )
        area_a = torch.prod(bboxes_a[:, 2:], 1)  # [N]
        area_b = torch.prod(bboxes_b[:, 2:], 1)  # [M]


    is_overlapped = (tl < br).type(tl.dtype).prod(dim=2)  # [N,M]
    area_overlap = torch.prod(br-tl, 2) * is_overlapped  # [N,M]
    min_area = torch.minimum(area_a[:, None],area_b[None, :])
    overlap_ratio = area_overlap/min_area

    return overlap_ratio