#!/usr/bin/env python
import rclpy
from rclpy.node import Node

import math

from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

class GetEulerNode(Node):

    def __init__(self):
        super().__init__('turtlesim_subscriber')
        topic_name = '/olive/imu/x1690895648100/imu'
        qos_profile = 10
        self.subscription = self.create_subscription(
            Imu,
            topic_name,
            self.get_message,
            qos_profile)
        self.subscription

        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.publish_angle)
        self.orientation = Quaternion()

    # callback function from the subscription to get the orientation of the Imu
    def get_message(self, msg):
        self.orientation = msg.orientation


 
    def euler_from_quaternion(self, orientation):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        x = orientation.x
        y = orientation.y
        z = orientation.z
        w = orientation.w
        
        t0 = +2.0 * (w * z + x * y)
        t1 = +1.0 - 2.0 * (y * y + z * z)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - x * z)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * x + y * z)
        t4 = +1.0 - 2.0 * (x * x + y * y)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians
    
    def publish_angle(self):
        self.angles = self.euler_from_quaternion(self.orientation)
        
        self.get_logger().info(
            f'publishing: Roll: {self.angles[0]} Pitch: {self.angles[1]} Yaw: {self.angles[2]}')


def main(args=None):
    rclpy.init(args=args)

    euler_node = GetEulerNode()

    rclpy.spin(euler_node)

    euler_node.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()