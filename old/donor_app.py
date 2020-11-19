import cv2
import sys
import os
import time
import numpy as np
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap

# import custom module
from gui_yolo import main
import imutils

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        
        # paths
        yolo_path = 'yolo-coco'
        confidence_arg = 0.5
        threshold_arg = 0.3

        # load the COCO class labels our YOLO model was trained on
        labelsPath = os.path.sep.join([yolo_path, "coco.names"])
        LABELS = open(labelsPath).read().strip().split("\n")

        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
            dtype="uint8")

        # derive the paths to the YOLO weights and model configuration
        weightsPath = os.path.sep.join([yolo_path, "yolov3_mask_2000.weights"])
        configPath = os.path.sep.join([yolo_path, "yolov3_mask.cfg"])

        # load our YOLO object detector trained on COCO dataset (80 classes)
        # and determine only the *output* layer names that we need from YOLO
        #print("[INFO] loading YOLO from disk...")
        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)


        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


        vs = cv2.VideoCapture(0)
        (W, H) = (None, None)
        while True:
            grabbed, frame = vs.read()
            if grabbed:
                # https://stackoverflow.com/a/55468544/6622587
                # rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # if the frame was not grabbed, then we have reached the end
                # of the stream


                # if the frame dimensions are empty, grab them
                if W is None or H is None:
                    (H, W) = frame.shape[:2]

                # construct a blob from the input frame and then perform a forward
                # pass of the YOLO object detector, giving us our bounding boxes
                # and associated probabilities
                blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                    swapRB=True, crop=False)
                net.setInput(blob)
                start = time.time()
                layerOutputs = net.forward(ln)
                end = time.time()

                # initialize our lists of detected bounding boxes, confidences,
                # and class IDs, respectively
                boxes = []
                confidences = []
                classIDs = []

                # loop over each of the layer outputs
                for output in layerOutputs:
                    # loop over each of the detections
                    for detection in output:
                        # extract the class ID and confidence (i.e., probability)
                        # of the current object detection
                        scores = detection[5:]
                        classID = np.argmax(scores)
                        confidence = scores[classID]

                        # filter out weak predictions by ensuring the detected
                        # probability is greater than the minimum probability
                        if confidence > confidence_arg:
                            # scale the bounding box coordinates back relative to
                            # the size of the image, keeping in mind that YOLO
                            # actually returns the center (x, y)-coordinates of
                            # the bounding box followed by the boxes' width and
                            # height
                            box = detection[0:4] * np.array([W, H, W, H])
                            (centerX, centerY, width, height) = box.astype("int")

                            # use the center (x, y)-coordinates to derive the top
                            # and and left corner of the bounding box
                            x = int(centerX - (width / 2))
                            y = int(centerY - (height / 2))

                            # update our list of bounding box coordinates,
                            # confidences, and class IDs
                            boxes.append([x, y, int(width), int(height)])
                            confidences.append(float(confidence))
                            classIDs.append(classID)

                # apply non-maxima suppression to suppress weak, overlapping
                # bounding boxes
                idxs = cv2.dnn.NMSBoxes(boxes, confidences, confidence_arg,
                    threshold_arg)

                # ensure at least one detection exists
                if len(idxs) > 0:
                    # loop over the indexes we are keeping
                    for i in idxs.flatten():
                        # extract the bounding box coordinates
                        (x, y) = (boxes[i][0], boxes[i][1])
                        (w, h) = (boxes[i][2], boxes[i][3])

                        # draw a bounding box rectangle and label on the frame
                        color = [int(c) for c in COLORS[classIDs[i]]]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                        text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                            confidences[i])
                        cv2.putText(frame, text, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                h, w, ch = frame.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)




class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()



    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)
        # create a label
        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
