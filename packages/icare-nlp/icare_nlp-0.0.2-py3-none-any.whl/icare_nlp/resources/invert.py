import json

with open("yolo_obj_class_def.json", "r") as f:
    data = json.load(f)

inverted_dict = {value: key for key, value in data.items()}
print(inverted_dict)

with open("inv_yolo_obj_class_def.json", "w") as f:
    json.dump(inverted_dict,f,indent=2)

