import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class SimpleTeleop(Node):
    def __init__(self):
        super().__init__('simple_teleop')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.move_robot)
        self.count = 0

    def move_robot(self):
        msg = Twist()
        # simple pattern: move forward and rotate slowly
        msg.linear.x = 0.1  # forward
        msg.angular.z = 0.2  # rotation
        self.pub.publish(msg)
        self.count += 1
        if self.count > 50:  # stop after 5 seconds
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.pub.publish(msg)
            self.destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = SimpleTeleop()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()