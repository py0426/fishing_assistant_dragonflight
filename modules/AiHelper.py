import yolov5


class AiHelper:

    def __init__(self, setting_helper):
        self.setting_helper = setting_helper
        self.model_path = f'{self.setting_helper["ai"]["model_path"]}'
        self.model = yolov5.load(self.model_path)


    def find_location(self, screenshot):

        results = self.model(screenshot)

        detections = results.pred[0]

        best_det = dict()
        init_conf = 0
        if len(detections) <= 0:
            return(0, 0, 0)

        for det in detections:
            x1, y1, x2, y2, conf, cls = det

            if float(conf) > init_conf:
                init_conf = float(conf)
                best_det["x1"] = round(float(x1), 2)
                best_det["y1"] = round(float(y1), 2)
                best_det["x2"] = round(float(x2), 2)
                best_det["y2"] = round(float(y2), 2)
                best_det["conf"] = conf
                best_det["cls"] = cls

        center_x = (best_det["x1"] + best_det["x2"]) / 2
        center_y = (best_det["y1"] + best_det["y2"]) / 2

        return best_det["conf"], center_x, center_y
