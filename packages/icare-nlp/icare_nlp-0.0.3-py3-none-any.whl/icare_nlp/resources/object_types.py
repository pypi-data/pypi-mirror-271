import json
import pdb
obj_types={0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}





obj_expressions = {
    0: 'hand, 手, 手',
    1: 'bicycle, 自行车, 單車',
    2: 'car, 汽车, 車',
    3: 'motorcycle, 摩托车, 電單車',
    4: 'airplane, 飞机, 飛機',
    5: 'bus, 公交车, 巴士',
    6: 'train, 火车, 火車',
    7: 'truck, 卡车, 貨車',
    8: 'boat, 船, 船',
    9: 'traffic light, 交通灯, 紅綠燈',
    10: 'fire hydrant, 消防栓, 消防喉',
    11: 'stop sign, 停车标志, 停車標誌',
    12: 'parking meter, 停车计时器, 泊車錶',
    13: 'bench, 长椅, 長凳',
    14: 'bird, 鸟, 鳥',
    15: 'cat, 猫, 貓',
    16: 'dog, 狗, 狗',
    17: 'horse, 马, 馬',
    18: 'sheep, 羊, 羊',
    19: 'cow, 牛, 牛',
    20: 'elephant, 大象, 大象',
    21: 'bear, 熊, 熊',
    22: 'zebra, 斑马, 斑馬',
    23: 'giraffe, 长颈鹿, 長頸鹿',
    24: 'backpack, 背包, 書包',
    25: 'umbrella, 伞, 雨傘',
    26: 'handbag, 手提包, 手袋',
    27: 'tie, 领带, 領呔',
    28: 'suitcase, 行李箱, 行李箱',
    29: 'frisbee, 飞盘, 飛碟',
    30: 'skis, 滑雪板, 滑雪板',
    31: 'snowboard, 滑雪板, 單板滑雪',
    32: 'sports ball, 运动球, 波',
    33: 'kite, 风筝, 風箏',
    34: 'baseball bat, 棒球棒, 棒球棒',
    35: 'baseball glove, 棒球手套, 棒球手套',
    36: 'skateboard, 滑板, 滑板',
    37: 'surfboard, 冲浪板, 沖浪板',
    38: 'tennis racket, 网球拍, 網球拍',
    39: 'bottle, 瓶子, 樽',
    40: 'wine glass, 酒杯, 酒杯',
    41: 'cup, 杯子, 杯',
    42: 'fork, 叉子, 叉',
    43: 'knife, 刀, 刀',
    44: 'spoon, 勺子, 匙',
    45: 'bowl, 碗, 碗',
    46: 'banana, 香蕉, 香蕉',
    47: 'apple, 苹果, 蘋果',
    48: 'sandwich, 三明治, 三文治',
    49: 'orange, 橙子, 橙',
    50: 'broccoli, 西兰花, 西蘭花',
    51: 'carrot, 胡萝卜, 蘿蔔',
    52: 'hot dog, 热狗, 熱狗',
    53: 'pizza, 比萨, 薄餅',
    54: 'donut, 甜甜圈, 甜甜圈',
    55: 'cake, 蛋糕, 蛋糕',
    56: 'chair, 椅子, 椅',
    57: 'couch, 沙发, 梳化',
    58: 'potted plant, 盆栽, 盆栽',
    59: 'bed, 床, 床',
    60: 'dining table, 餐桌, 飯枱',
    61: 'toilet, 厕所, 廁所',
    62: 'tv, 电视, 電視',
    63: 'laptop, 笔记本电脑, 手提電腦',
    64: 'mouse, 鼠标, 滑鼠',
    65: 'remote, 遥控器, 遙控',
    66: 'keyboard, 键盘, 鍵盤',
    67: 'cell phone, 手机, 手提電話',
    68: 'microwave, 微波炉, 微波爐',
    69: 'oven, 烤箱, 焗爐',
    70: 'toaster, 烤面包机, 多士爐',
    71: 'sink, 水槽, 水槽',
    72: 'refrigerator, 冰箱, 雪櫃',
    73: 'book, 书, 書',
    74: 'clock, 钟, 鐘',
    75: 'vase, 花瓶, 花瓶',
    76: 'scissors, 剪刀, 剪刀',
    77: 'teddy bear, 泰迪熊, 泰迪熊',
    78: 'hair drier, 吹风机, 風筒',
    79: 'toothbrush, 牙刷, 牙刷'
}


reverse_mapping = {}
for key, values in obj_expressions.items():
    expressions = values.split(', ')
    for expression in expressions:
        reverse_mapping[expression.strip()] = key
print(reverse_mapping)

with open("rev_yolo_obj_class_def.json", "w", encoding="utf-8") as f:
    json.dump(reverse_mapping, f, indent=2, ensure_ascii=False)


import torch
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('indiejoseph/bert-cantonese-sts')
emb_list=[]
for i in range(80):
    sentence_i=obj_expressions[i]
    emb_i=model.encode(sentence_i, convert_to_tensor=True)
    emb_list.append(emb_i)
embeddings_tensor = torch.stack(emb_list)
print(embeddings_tensor.shape)
torch.save(embeddings_tensor, 'category_emb_tensor.pt')








obj_tactile_description={
  "0": "一個人嘅結構多變，通常直立，外觀柔軟。",
  "1": "自行車有一個金屬架構，配有兩個輪子，手感堅硬光滑。",
  "2": "汽車係一個大型堅硬物件，外層係光滑嘅金屬，並配有滾動輪子。",
  "3": "摩托車有一個堅硬嘅金屬框架，配有兩個橡膠輪胎和多個光滑嘅組件。",
  "4": "飛機很大，主要係金屬製，外觀光滑堅硬，有寬大嘅翼。",
  "5": "巴士係一個大型嘅矩形車輛，表面係光滑嘅堅硬金屬。",
  "6": "火車由相連嘅車廂組成，長而堅硬，表面係光滑嘅金屬。",
  "7": "卡車有一個大型堅硬嘅金屬車身，後部通常有一個矩形嘅貨物區。",
  "8": "船通常係光滑而堅硬嘅，大小極為不同，外層防水。",
  "9": "交通燈係一個小型嘅豎立桿，表面堅硬光滑，並有彩色燈罩。",
  "10": "消防栓小而矮，質感堅硬，金屬質感略顯粗糙。",
  "11": "停車標誌係一個大型嘅八角形金屬板，裝在桿上，質感光滑堅硬。",
  "12": "停車錶係一個小型嘅金屬柱，堅硬而圓柱形，質感光滑。",
  "13": "長椅通常長而堅硬，由木頭或金屬製成，表面光滑或略帶粗糙。",
  "14": "鳥類體型小，有柔軟嘅羽毛和堅硬嘅喙。",
  "15": "貓嘅體型從小到中等，全身覆蓋著柔軟嘅毛發，觸感溫和。",
  "16": "狗嘅大小各異，通常覆有柔軟嘅毛皮和濕潤嘅鼻子。",
  "17": "馬體型大，肌肉發達，外層係光滑柔軟嘅皮毛，並有長鬃毛。",
  "18": "綿羊體型中等，毛茸茸嘅，有柔軟嘅羊毛。",
  "19": "牛體型大而結實，有柔軟厚實嘅皮膚。",
  "20": "大象體型非常大，皮膚粗糙堅硬，有大而堅固嘅耳朵。",
  "21": "熊體型大而笨重，有厚厚嘅柔軟皮毛。",
  "22": "斑馬體型與馬相似，外層係柔軟嘅皮毛，有獨特嘅條紋圖案。",
  "23": "長頸鹿非常高大，有長頸，覆蓋在柔軟嘅皮毛上，有獨特嘅圖案。",
  "24": "背包通常係中等大小，根據材料可能係軟嘅或硬嘅，有拉鍊和口袋。",
  "25": "傘由金屬框架和光滑防水嘅布料製成。",
  "26": "手袋嘅大小各異，由軟皮革至硬合成材料製成。",
  "27": "領帶長而瘦，由柔軟嘅布料製成，質感光滑。",
  "28": "手提箱通常係堅硬嘅，矩形，表面光滑，有把手。",
  "29": "飛盤小而平，由堅硬嘅塑料製成，表面光滑。",
  "30": "滑雪板長而窄，堅硬，表面光滑且滑溜。",
  "31": "單板滑雪板寬而平，堅硬，表面光滑且有光澤。",
  "32": "運動球嘅大小和材料各異，通常係圓形，堅硬而光滑。",
  "33": "風箏輕便，由薄布或紙張緊繃在框架上，並有尾巴。",
  "34": "棒球棒長而圓柱形，堅硬，由木頭或金屬製成。",
  "35": "棒球手套大小適中，由皮革製成，柔軟且有彈性，有獨特嘅氣味。",
  "36": "滑板係一塊窄而平嘅板，有堅硬光滑嘅輪子。",
  "37": "衝浪板長而平，輕便，表面光滑堅硬。",
  "38": "網球拍有圓形嘅開口頭，用線繩串起，和長把手，堅硬且光滑。",
  "39": "瓶子通常係圓柱形嘅，由堅硬嘅塑料或玻璃製成。",
  "40": "紅酒杯脆弱，由薄玻璃製成，有莖。",
  "41": "杯子小，通常係圓柱形嘅，由堅硬或略帶彈性嘅材料製成。",
  "42": "叉子小，由金屬製成，有尖銳嘅叉子，堅硬且光滑。",
  "43": "刀子有一個堅硬嘅、鋒利嘅金屬刀片，連接著一個光滑嘅手柄。",
  "44": "匙子小，頭部圓形凹陷，由光滑堅硬嘅金屬製成。",
  "45": "碗寬而開口，由陶瓷或玻璃等堅硬材料製成。",
  "46": "香蕉長且略呈弧形，外層柔軟，可撕開。",
  "47": "蘋果圓形，觸感堅實，表面光滑略帶蠟質。",
  "48": "三文治大小各異，通常柔軟，有麵包、肉和蔬菜層。",
  "49": "橙子圓形，堅實，表面有質感，可剝皮。",
  "50": "西蘭花中等大小，莖部堅實，頂部粗糙似樹梢。",
  "51": "胡蘿蔔長而窄，堅實，質地光滑且脆。",
  "52": "熱狗柔軟，外層係光滑略粗糙嘅麵包。",
  "53": "比薩通常係圓形，底部柔軟且有嚼勁，上面有各種質地嘅配料。",
  "54": "甜甜圈柔軟而蓬鬆，通常係圓形，表面有光滑嘅糖衣。",
  "55": "蛋糕通常柔軟，有層次嘅奶油和柔軟嘅底部。",
  "56": "椅子有一個堅硬嘅框架，通常由木頭或金屬製成，座位和背部軟。",
  "57": "沙發大，表面係柔軟嘅坐墊，框架結實。",
  "58": "盆栽由一個堅硬嘅盆和一個柔軟嘅、多葉嘅植物組成。",
  "59": "床很大，有一個柔軟嘅床墊和通常係堅硬嘅框架。",
  "60": "飯桌大而平坦，通常由堅硬嘅木頭或金屬製成。",
  "61": "廁所由堅硬嘅陶瓷製成，小型，表面光滑。",
  "62": "電視係矩形嘅，有一個堅硬嘅、平坦嘅屏幕和窄嘅深度。",
  "63": "手提電腦小而矩形，外殼堅硬，屏幕光滑可折疊。",
  "64": "滑鼠小，塑料製，表面光滑且呈曲線形以適合手部休息。",
  "65": "遙控器小，堅硬，表面光滑並有多個按鈕。",
  "66": "鍵盤係矩形平板，有許多小嘅、堅硬嘅鍵位於光滑嘅底座上。",
  "67": "手機小而矩形，有一個堅硬嘅、光滑嘅玻璃屏幕。",
  "68": "微波爐中等大小，盒形，外部堅硬，有一扇鉸接門。",
  "69": "烤箱大，主要係金屬製，表面堅硬光滑，有前門。",
  "70": "多士爐小，盒形，由堅硬嘅金屬製成，頂部有縫隙。",
  "71": "洗碗槽通常係堅硬嘅，由金屬或陶瓷製成，表面光滑且凹陷。",
  "72": "雪櫃大且盒形，堅硬，表面係金屬或塑料製嘅光滑材料。",
  "73": "書通常係矩形嘅，由光滑嘅紙頁製成，封面堅硬或軟。",
  "74": "時鐘通常係圓形或方形嘅，表面光滑堅硬，有移動嘅指針。",
  "75": "花瓶通常係圓柱形或球狀嘅，由堅硬光滑嘅材料如玻璃或陶瓷製成。",
  "76": "剪刀由兩個交叉嘅刀片組成，堅硬而鋒利，手柄光滑。",
  "77": "泰迪熊柔軟而豐滿，通常係毛絨嘅，質地舒適。",
  "78": "吹風機係手持式嘅，由堅硬嘅塑料製成，外形光滑且符合人體工程學。",
  "79": "牙刷小，手柄堅硬光滑，一端有一排柔軟嘅刷毛。"
}

# cate_tac_list=[]
# for i in range(80):
#   cate_tac_list.append({"index": i,"category":obj_types[i],"cate_expressions": obj_expressions[i], "tactile": obj_tactile_description[str(i)]})
#
# with open("category_tactile_description.json", "w", encoding="utf-8") as f:
#     json.dump(cate_tac_list, f, ensure_ascii=False, indent=2)




