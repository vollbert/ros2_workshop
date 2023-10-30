import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class RandomNumberSubscriber(Node):
    def __init__(self):
        super().__init__('random_number_subscriber')
        self.subscription = self.create_subscription(
            Int32,
            'random_numbers',
            self.random_number_callback,
            10
        )
        self.subscription

    def random_number_callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    random_number_subscriber = RandomNumberSubscriber()
    rclpy.spin(random_number_subscriber)
    random_number_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
