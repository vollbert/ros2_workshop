#! /usr/bin/env python3

import cv2
from cv_bridge import CvBridge

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import CompressedImage

from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy



class CameraSubscriber(Node):
    
    def __init__(self):
        super().__init__('camera_subscriber')
        camera_topic = '/olive/camera/eye/image/compressed'
        qos_profile = QoSProfile(
            depth=10,
            durability=QoSDurabilityPolicy.VOLATILE,
            reliability=QoSReliabilityPolicy.BEST_EFFORT)

        self.subscription = self.create_subscription(
            CompressedImage,
            camera_topic,
            self.callback,
            qos_profile)
        self.subscription  # prevent unused variable warning
        self.br = CvBridge()

    def callback(self, msg):
        self.get_logger().info('Receiving video frame')
        cv2_image = self.br.compressed_imgmsg_to_cv2(msg)
        cv2.imshow('Camera Image', cv2_image)
        cv2.waitKey(1)
 

def main(args=None):
    rclpy.init(args=args)

    camera_subscriber = CameraSubscriber()

    rclpy.spin(camera_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    camera_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()