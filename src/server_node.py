#!/usr/bin/python
import rospy
import std_msgs.msg
from sensor_msgs.msg import Image
from flask import Flask, render_template, Response, request
import cv2
import serial
import threading
import time
import json
import argparse
from cv_bridge import CvBridge, CvBridgeError

app = Flask(__name__)
class server:
    def __init__(self):
        # self.app = Flask(__name__)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/image",Image,self.callback)

    def callback(self,data):
        try:
            cv_image_frame = self.bridge.imgmsg_to_cv2(data, "bgr8")
            return cv_image_frame
        except CvBridgeError as e:
            print(e)

    def getFramesGenerator(self):
        while True:
            #time.sleep(0.01)    # ограничение fps (если видео тупит, можно убрать)
            frame = self.callback()  # Получаем фрейм с камеры                      
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route('/video_feed')
def video_feed(ob):
    return Response(server.getFramesGenerator(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """ Крутим html страницу """
    return render_template('index.html')


    def frame():
        pass


if __name__ == "__main__":
    rospy.init_node('image_server', anonymous=False)
    server1 = server

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000, help="Running port")
    parser.add_argument("-i", "--ip", type=str, default='127.0.0.1', help="Ip address")
    parser.add_argument('-s', '--serial', type=str, default='/dev/ttyUSB0', help="Serial port")
    args = parser.parse_args()

    app.run(debug=False, host=args.ip, port=args.port)
