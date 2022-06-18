#!/usr/bin/python
import rospy
import std_msgs.msg

class Web:
    def __init__(self):
        rospy.init_node('web_server', anonymous=True)
        self.pud = rospy.Publisher('text_line', std_msgs.msg.String, queue_size=10)
        self.rate = rospy.Rate(10)


    def start(ip):
        rospy.init_node('web_server', anonymous=True)


    def loop(self, Text):
        while not rospy.is_shutdown():
            self.pud.publish(Text)
            self.rate.sleep()

if __name__ == "__main__":
    try:
        test = Web()
        test.loop("Hello")
    except rospy.ROSInterruptException:
        pass