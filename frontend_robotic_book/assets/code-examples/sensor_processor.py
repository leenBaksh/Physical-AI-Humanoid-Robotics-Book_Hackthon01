import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SensorProcessor(Node):
    def __init__(self):
        super().__init__('sensor_processor')

        # Subscribe to raw sensor data
        self.subscription = self.create_subscription(
            String,
            'raw_sensor_data',
            self.raw_sensor_callback,
            10)

        # Publisher for processed sensor data
        self.publisher = self.create_publisher(String, 'sensor_data', 10)

        self.get_logger().info('Sensor Processor Node initialized')

    def raw_sensor_callback(self, msg):
        """Process raw sensor data and publish processed data"""
        # In a real system, this would perform more complex processing
        processed_data = f"Processed: {msg.data}"
        self.publisher.publish(String(data=processed_data))
        self.get_logger().info(f'Published processed data: {processed_data}')

def main(args=None):
    rclpy.init(args=args)
    sensor_processor = SensorProcessor()

    try:
        rclpy.spin(sensor_processor)
    except KeyboardInterrupt:
        pass
    finally:
        sensor_processor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()