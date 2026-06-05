# -*- coding: utf-8 -*-
from ultralytics import YOLO

class WasteDetector:
    # 别乱改路径
    def __init__(self, model_path='best.pt'):
        # 加载模型
        self.model = YOLO(model_path)

        self.cat_names = ['针头', '药瓶', '纱布', '感染性废物']

    def detect(self, img_path):
        """
        识别图片，返回所有检测结果
        """
        results = self.model(img_path)
        dets = []
        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                name = self.cat_names[cls_id] if cls_id < len(self.cat_names) else '未知'
                dets.append({
                    'category': name,
                    'confidence': conf,
                    'bbox': box.xyxy[0].tolist()
                })
        return dets