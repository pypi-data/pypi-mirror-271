import json
import torch
from sentence_transformers import SentenceTransformer, util
import utils
class ObjectQA(object):
    def __init__(self):
        self.cls_model = SentenceTransformer('indiejoseph/bert-cantonese-sts')
        self.sentences1 = ["點樣可以攞到", "喺我手嘅邊個方向", "喺邊?", "tv喺邊？"]
        self.sentences2 = ["附近有冇其他物體"]
        self.embeddings1 = self.cls_model.encode(self.sentences1, convert_to_tensor=True)
        self.embeddings2 = self.cls_model.encode(self.sentences2, convert_to_tensor=True)
        with open("resources/yolo_obj_class_def.json", "r") as f:
            self.yolo_cls = json.load(f)
        with open("resources/inv_yolo_obj_class_def.json", "r") as f:
            self.inv_yolo_cls = json.load(f)
        with open("resources/rev_yolo_obj_class_def.json", "r", encoding="utf-8") as f:
            self.rev_yolo_cls = json.load(f)
        self.category_emb_tensor = torch.load('resources/category_emb_tensor.pt')
        self.hand_centric=False
        self.target_obj=''
        with open("resources/category_tactile_description.json", "r", encoding="utf-8") as f:
            self.cate_tac_desc = json.load(f)
    def classify_query(self, question):
        input_embedding = self.cls_model.encode(question, convert_to_tensor=True)
        similarities1 = util.pytorch_cos_sim(input_embedding, self.embeddings1)
        similarities2 = util.pytorch_cos_sim(input_embedding, self.embeddings2)
        max_similarity1 = torch.max(similarities1)
        max_similarity2 = torch.max(similarities2)
        return 1 if max_similarity1 > max_similarity2 else 2

    def determine_centric(self, obj_detect):
        hand_centric=False
        hand = [d for d in obj_detect if d['text'] == "hand" or d['text'] == "person"]
        if hand:
            hand_centric=True
            cent_x, cent_y, cent_w, cent_h = hand[0]["position"]
        else:
            cent_x, cent_y, cent_w, cent_h = 640, 720, 0, 0
        return (cent_x, cent_y, cent_w, cent_h), hand_centric

    def get_short_expression(self, question):
        self.centric_hand = False
        word_set = {'？', '冇', '條', '到', '別嘅', '東西', '邊', '點樣', '頭', '某个', '喺', '物', '我', '附近', '其他',
                    '物件', '物體', '體', '到', '攞', '可以', '有', '我點樣', '嗎', '物體', '嘅', '哪', '上', '個',
                    '方向'}
        for word in word_set:
            if word in question:
                question = question.replace(word, '_')
        tmp_list = question.split('_')
        cleaned_list = [item for item in tmp_list if item != '']
        if '手' in cleaned_list:
            self.centric_hand = True
            cleaned_list.remove('手')
        res = ''.join(cleaned_list)
        return res, self.centric_hand

    def get_target_obj(self, question, obj_detect):
        obj_list = [item['text'] for item in obj_detect]
        obj_index_list = []
        for obj in obj_list:
            obj_index_list.append(int(self.inv_yolo_cls[obj]))
        selected_embs = self.category_emb_tensor[obj_index_list]
        short, centric_hand = self.get_short_expression(question)
        short_emb = self.cls_model.encode(short, convert_to_tensor=True)
        if short in self.rev_yolo_cls:
            tmp=self.rev_yolo_cls[short]
            self.target_obj=self.yolo_cls[str(tmp)]
        else:
            similarities = util.pytorch_cos_sim(short_emb, selected_embs)
            most_similar_idx = torch.argmax(similarities).item()
            self.target_obj=self.yolo_cls[str(obj_index_list[most_similar_idx])]

        for obj in obj_detect:
            if obj["text"] == self.target_obj:
                target_pos = obj["position"]
                break
            else:
                target_pos =(0,0,0,0)
        return self.target_obj, target_pos


    def process_qa_1(self, question, obj_detect):
        (cent_x,cent_y,cent_w,cent_h), self.hand_centric=self.determine_centric(obj_detect)
        self.target_obj, [tar_x,tar_y,tar_w,tar_h]=self.get_target_obj(question, obj_detect)
        if self.hand_centric:
            # 1. 计算重叠面积
            iou_rate=utils.cal_iou((cent_x,cent_y,cent_w,cent_h), (tar_x,tar_y,tar_w,tar_h))
            if iou_rate>0.4:
                rela_pos="你已經掂到"+self.target_obj
            else:
                rela_pos = utils.determine_relative_pos(self.target_obj,cent_x, cent_y, tar_x, tar_y,self.hand_centric)
        else:
            rela_pos=utils.determine_relative_pos(self.target_obj,cent_x,cent_y,tar_x,tar_y)
        return rela_pos


    def process_qa_2(self,question,obj_detect):
        self.target_obj, [tar_x, tar_y, tar_w, tar_h] = self.get_target_obj(question, obj_detect)
        cen_obj=self.target_obj
        cen_obj_item = next(item for item in obj_detect if item['text'] == cen_obj)
        cen_x, cen_y, _, _ = cen_obj_item["position"]
        obj_detect.remove(cen_obj_item)

        for item in obj_detect:
            item_x, item_y = item["position"][:2]
            item["distance"] = utils.calculate_distance(cen_x, cen_y, item_x, item_y)
        sorted_obj_detect = sorted(obj_detect, key=lambda x: x['distance'])
        if len(sorted_obj_detect) < 3:
            output_objects = sorted_obj_detect
        else:
            output_objects = sorted_obj_detect[:3]
        if output_objects:
            obj_names = ''
            relative_poses = ''
            for obj in output_objects:
                object_name = obj['text']
                relative_position = utils.determine_relative_pos_sur(cen_obj, cen_x, cen_y, object_name, obj['position'][0],
                                                               obj['position'][1])
                relative_poses += relative_position
                obj_names += object_name + ','
            objects_sentence = cen_obj+"最近嘅物件系 " + obj_names[:-1] + '.' + relative_poses
        else:
            objects_sentence="冇检测到其他物体."
        return objects_sentence

    def add_tactile(self):
        for item in self.cate_tac_desc:
            if item['category'] == self.target_obj:
                return item['tactile']

    def form_response(self,question, obj_detect):
        q_cls=self.classify_query(question)
        if q_cls==1:
            ans_1=self.process_qa_1(question, obj_detect)
        else:
            ans_1=self.process_qa_2(question, obj_detect)
        ans_2=self.add_tactile()
        return ans_1+'. '+ans_2