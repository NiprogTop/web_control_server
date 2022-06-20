#!/usr/bin/env python
from __future__ import print_function
from flask import Flask, render_template, Response, request
import os

import threading
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


app=Flask(__name__)
bridge = CvBridge()
frame_r = 0


def callback(data):
    try:
        ###  обработка кадра  ###
      global frame_r
      frame = bridge.imgmsg_to_cv2(data, "bgr8")
      #rospy.loginfo(frame_r)
      ret,buffer=cv2.imencode('.jpg',frame)
      frame=buffer.tobytes()
      frame_r = frame

    except CvBridgeError as e:
      print(e)


def web_gen():
    while True:
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_r + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(web_gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


threading.Thread(target=lambda: rospy.init_node('image_converter', anonymous=True, disable_signals=True)).start()
rospy.Subscriber("image",Image,callback)
# threading.Thread(rospy.spin()).start()
#app.run(debug=False)
app.run(host="127.0.0.1", port=3000)
