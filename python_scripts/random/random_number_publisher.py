import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import random

class RandomNumberPublisher(Node):
    def __init__(self):
        super().__init__('random_number_publisher')
        self.publisher_ = self.create_publisher(Int32, 'random_numbers', 10)
        self.declare_parameter('upper_limit', 100)   #change
        self.timer = self.create_timer(1.0, self.publish_random_number)
        

    def publish_random_number(self):
        upper_limit = self.get_parameter('upper_limit').get_parameter_value().integer_value  #change
        random_number = random.randint(1, upper_limit)    #change
        self.get_logger().info(f'Publishing: {random_number}')
        msg = Int32()
        msg.data = random_number
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    random_number_publisher = RandomNumberPublisher()
    rclpy.spin(random_number_publisher)
    random_number_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
