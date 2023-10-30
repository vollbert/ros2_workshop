import os
import rclpy
import math

from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import Trigger
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion


class ControlServo(Node):

    def __init__(self):
        super().__init__('control_servo')

        # Call the service to enable the servos' torque
        self.enable_servos()

        self.topic_lm = '/olive/servo/pan/goal/position'
        self.topic_um = '/olive/servo/tilt/goal/position'
        self.publisher_lm = self.create_publisher(Float32, self.topic_lm, 10)
        self.publisher_um = self.create_publisher(Float32, self.topic_um, 10)

        self.imu_topic = '/olive/imu/imu/imu'
        self.orientation = Quaternion()
        self.subscriber_imu = self.create_subscription(Imu, self.imu_topic, self.imu_callback, 10)

        timer_period = 0.001
        self.timer = self.create_timer(timer_period, self.publish_goal)

        self.get_logger().info('Use the Imu to control the Robot.')
        self.motor_lm_position = 0.0
        self.motor_um_position = 0.0

    def enable_servos(self):
        # Call the service to enable the servos' torque
        os.system('ros2 service call /olive/servo/pan/setTorqueEnable std_srvs/srv/Trigger')
        os.system('ros2 service call /olive/servo/tilt/setTorqueEnable std_srvs/srv/Trigger')

    def disable_servos(self):
        # Call the service to disable the servos' torque
        os.system('ros2 service call /olive/servo/pan/setTorqueDisable std_srvs/srv/Trigger')
        os.system('ros2 service call /olive/servo/tilt/setTorqueDisable std_srvs/srv/Trigger')

    def imu_callback(self,msg):
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


    def publish_goal(self):

        [roll_x, pitch_y, yaw_z] = self.euler_from_quaternion(self.orientation)

        # Create messages and publish the positions
        msg_lm = Float32()
        msg_um = Float32()
        msg_lm.data = -roll_x
        msg_um.data = pitch_y
        self.publisher_lm.publish(msg_lm)
        self.publisher_um.publish(msg_um)
        self.get_logger().info(f'Publishing: roll: {msg_lm.data} pitch: {msg_um.data}')


def main(args=None):
    rclpy.init(args=args)

    cntr_publisher = ControlServo()

    try:
        rclpy.spin(cntr_publisher)
    except KeyboardInterrupt:
        # Call the function to disable the servos' torque when exiting
        cntr_publisher.disable_servos()
        cntr_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
