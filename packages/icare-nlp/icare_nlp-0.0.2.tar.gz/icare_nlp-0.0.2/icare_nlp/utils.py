import math

def determine_relative_pos(target_obj,cen_x, cen_y, tar_x, tar_y, hand_centric=False):
    # 判断垂直位置
    if tar_y > cen_y:
        vertical = '下'
    elif tar_y < cen_y:
        vertical = '上'
    else:
        vertical = '水平对齐'
    # 判断水平位置
    if tar_x > cen_x:
        horizontal = '右'
    elif tar_x < cen_x:
        horizontal = '左'
    else:
        horizontal = '垂直对齐'
    # 组合位置
    if vertical == '水平对齐' and horizontal == '垂直对齐':
        res=target_obj+"同中心點重合"
    elif vertical == '水平对齐':
        res=target_obj+"喺中心點嘅"+horizontal+"方"
        if hand_centric:
            res=target_obj+"喺手嘅"+horizontal+"方"
    elif horizontal == '垂直对齐':
        res = target_obj+"喺中心點嘅" + vertical + "方"
        if hand_centric:
            res=target_obj+"喺手嘅"+vertical+"方"
    else:
        res = target_obj+"喺中心點嘅" + horizontal+vertical + "方"
        if hand_centric:
            res=target_obj+"喺手嘅"+ horizontal+vertical +"方"
    return res

def cal_iou(box1, box2):
    # 解构两个边界框的参数
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    # 计算每个边界框的左上角和右下角坐标
    left1, top1 = x1 - w1 / 2, y1 - h1 / 2
    right1, bottom1 = x1 + w1 / 2, y1 + h1 / 2
    left2, top2 = x2 - w2 / 2, y2 - h2 / 2
    right2, bottom2 = x2 + w2 / 2, y2 + h2 / 2
    # 计算交集的坐标
    inter_left = max(left1, left2)
    inter_top = max(top1, top2)
    inter_right = min(right1, right2)
    inter_bottom = min(bottom1, bottom2)
    # 计算交集的面积
    if inter_right > inter_left and inter_bottom > inter_top:
        inter_area = (inter_right - inter_left) * (inter_bottom - inter_top)
    else:
        inter_area = 0
    # 计算每个边界框的面积
    area1 = w1 * h1
    area2 = w2 * h2
    # 计算并集的面积
    union_area = area1 + area2 - inter_area
    # 计算IoU
    iou = inter_area / union_area if union_area != 0 else 0
    return iou


def determine_relative_pos_sur(obj_1,cen_x, cen_y, obj_2, tar_x, tar_y):
    # 判断垂直位置
    if tar_y > cen_y:
        vertical = '下'
    elif tar_y < cen_y:
        vertical = '上'
    else:
        vertical = '水平对齐'
    # 判断水平位置
    if tar_x > cen_x:
        horizontal = '右'
    elif tar_x < cen_x:
        horizontal = '左'
    else:
        horizontal = '垂直对齐'
    # 组合位置
    if vertical == '水平对齐' and horizontal == '垂直对齐':
        res=obj_2+"同"+obj_1+"重合."
    elif vertical == '水平对齐':
        res=obj_2+"喺"+obj_1+"嘅"+horizontal+"方."
    elif horizontal == '垂直对齐':
        res = obj_2+"喺"+obj_1+"嘅" + vertical + "方."
    else:
        res = obj_2+"喺"+obj_1+"嘅" + horizontal+vertical + "方."
    return res




def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

