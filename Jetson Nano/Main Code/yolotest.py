from ctypes import *
import random
import os
from turtle import window_height
import cv2
import time
import darknet
import argparse
from threading import Thread, enumerate
from queue import Queue
import http.client
import pyTigerGraph as tg
import csv

# Connection parameters
hostName = "https://altaga.i.tgcloud.io"
userName = "client"
password = "pass"
authToken = 'token'
conn = tg.TigerGraphConnection(host=hostName, graphname="Subway", username=userName, password=password, apiToken=authToken)

# AI parameters

threshold = .4
weight = 'weights/yolov4-tiny.weights'
cfg = 'cfg/yolov4-tiny.cfg'
scale_percent = 60 # percent of original size
counter = 0

def convert2relative(bbox):
    """
    YOLO format use relative coordinates for annotation
    """
    x, y, w, h  = bbox
    _height     = darknet_height
    _width      = darknet_width
    return x/_width, y/_height, w/_width, h/_height


def convert2original(image, bbox):
    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_x       = int(x * image_w)
    orig_y       = int(y * image_h)
    orig_width   = int(w * image_w)
    orig_height  = int(h * image_h)

    bbox_converted = (orig_x, orig_y, orig_width, orig_height)

    return bbox_converted


def convert4cropping(image, bbox):
    x, y, w, h = convert2relative(bbox)

    image_h, image_w, __ = image.shape

    orig_left    = int((x - w / 2.) * image_w)
    orig_right   = int((x + w / 2.) * image_w)
    orig_top     = int((y - h / 2.) * image_h)
    orig_bottom  = int((y + h / 2.) * image_h)

    if (orig_left < 0): orig_left = 0
    if (orig_right > image_w - 1): orig_right = image_w - 1
    if (orig_top < 0): orig_top = 0
    if (orig_bottom > image_h - 1): orig_bottom = image_h - 1

    bbox_cropping = (orig_left, orig_top, orig_right, orig_bottom)

    return bbox_cropping


def video_capture(frame_queue, darknet_image_queue):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (darknet_width, darknet_height),
                                   interpolation=cv2.INTER_LINEAR)
        frame_queue.put(frame)
        img_for_detect = darknet.make_image(darknet_width, darknet_height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        darknet_image_queue.put(img_for_detect)
    cap.release()


def inference(darknet_image_queue, detections_queue, fps_queue):
    while cap.isOpened():
        darknet_image = darknet_image_queue.get()
        prev_time = time.time()
        detections = darknet.detect_image(network, class_names, darknet_image, thresh=threshold)
        detections_queue.put(detections)
        fps = int(1/(time.time() - prev_time))
        fps_queue.put(fps)
        darknet.free_image(darknet_image)
    cap.release()


def drawing(frame_queue, detections_queue, fps_queue):
    random.seed(3)  # deterministic bbox colors
    while cap.isOpened():
        frame = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()
        detections_adjusted = []
        counter = 0
        if frame is not None:
            for label, confidence, bbox in detections:
                if label == 'person':
                    counter += 1
                    bbox_adjusted = convert2original(frame, bbox)
                    detections_adjusted.append((str(label), confidence, bbox_adjusted))
            image = darknet.draw_boxes(detections_adjusted, frame, class_colors)
            image = cv2.putText(image, "FPS:"+str(fps), (10, 25),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            image = cv2.putText(image, "Person Counter:"+str(counter), (10, 60),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow('Inference', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

def deleteRisk(level):
    conn = http.client.HTTPSConnection("altaga.i.tgcloud.io", 9000)
    payload = ''
    headers = {
    'Authorization': 'Bearer p5td5gnko5abdetcd5d97umfjffpn2va'
    }
    conn.request("DELETE", "/graph/edges/Risk/"+level+"/Level/Station/BELLAS%20ARTES", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print("Risk Deleted")

def addLevel(From,To):
  header = ['From','To','Level']
  data = [From,To,From]

  with open('temp.csv', 'w', encoding='UTF8') as f:
      writer = csv.writer(f)
      writer.writerow(header)
      writer.writerow(data)

  posts_file = 'temp.csv'
  results = conn.uploadFile(posts_file, fileTag='MyDataSource', jobName='load_level')
  print("Risk Added")

if __name__ == '__main__':
    frame_queue = Queue()
    darknet_image_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    fps_queue = Queue(maxsize=1)

    network, class_names, class_colors = darknet.load_network(
            cfg,
            "data/coco.data",
            weight,
            batch_size=1
        )
    darknet_width = darknet.network_width(network)
    darknet_height = darknet.network_height(network)
    cap = cv2.VideoCapture(0)
    Thread(target=video_capture, args=(frame_queue, darknet_image_queue)).start()
    Thread(target=inference, args=(darknet_image_queue, detections_queue, fps_queue)).start()
    Thread(target=drawing, args=(frame_queue, detections_queue, fps_queue)).start()