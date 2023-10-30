import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import random

class RandomNumberPublisher(Node):
    def __init__(self):
        super().__init__('random_number_publisher')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.publish_random_number)

    def publish_random_number(self):
        random_number_linear = random.randint(-10, 10)
        random_number_angular = random.randint(-10, 10)
        self.get_logger().info(f'Publishing: linear: {random_number_linear} angular: {random_number_angular}')
        msg = Twist()
        msg.linear.x = float(random_number_linear)
        msg.angular.z = float(random_number_angular)
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    random_number_publisher = RandomNumberPublisher()
    rclpy.spin(random_number_publisher)
    random_number_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()