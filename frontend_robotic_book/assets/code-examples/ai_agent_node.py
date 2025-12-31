import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class AIAgentNode(Node):
    def __init__(self):
        super().__init__('ai_agent_node')

        # Subscribe to sensor data
        self.subscription = self.create_subscription(
            String,
            'sensor_data',
            self.sensor_callback,
            10)
        self.subscription  # prevent unused variable warning

        # Publisher for robot commands
        self.publisher = self.create_publisher(Twist, 'robot_commands', 10)

        # Timer for decision-making loop
        self.timer = self.create_timer(0.5, self.decision_loop)

        # Internal state
        self.latest_sensor_data = None
        self.get_logger().info('AI Agent Node initialized')

    def sensor_callback(self, msg):
        """Process incoming sensor data"""
        self.get_logger().info(f'Received sensor data: {msg.data}')
        self.latest_sensor_data = msg.data
        # Process the sensor data here

    def decision_loop(self):
        """Main decision-making loop"""
        if self.latest_sensor_data:
            # Simple AI decision logic
            command = self.make_decision(self.latest_sensor_data)
            if command:
                self.publisher.publish(command)
                self.get_logger().info(f'Published command: linear.x={command.linear.x}, angular.z={command.angular.z}')

    def make_decision(self, sensor_data):
        """Simple AI decision-making function"""
        # Simple logic: if sensor reading is above threshold, move forward
        try:
            # Extract numeric value from sensor data (assuming format "Sensor reading: N")
            value_str = sensor_data.split(': ')[1]
            value = int(value_str)

            # Create a Twist message for robot movement
            cmd = Twist()

            if value > 5:  # Threshold for action
                cmd.linear.x = 0.5  # Move forward
                cmd.angular.z = 0.0  # No rotation
            else:
                cmd.linear.x = 0.0  # Stop
                cmd.angular.z = 0.1  # Gentle rotation to find better sensor readings

            return cmd
        except (ValueError, IndexError):
            # Handle malformed sensor data
            cmd = Twist()
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            return cmd

def main(args=None):
    rclpy.init(args=args)
    ai_agent_node = AIAgentNode()

    try:
        rclpy.spin(ai_agent_node)
    except KeyboardInterrupt:
        pass
    finally:
        ai_agent_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()