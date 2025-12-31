---
sidebar_position: 4
---

# AI Agent Tutorial: Building an Intelligent ROS 2 Node

In this hands-on tutorial, you'll build a simple "AI Agent" node that subscribes to a sensor topic, processes the data with Python logic, and publishes commands to control the robot.

## Prerequisites

Before starting this tutorial, ensure you have:
- Completed Chapter 1 (ROS 2 Core concepts)
- ROS 2 Humble Hawksbill installed
- Python 3.8 or higher
- rclpy library installed

## Creating the AI Agent Node

Create a file named `ai_agent_node.py`:

```python
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
```

## Creating a Sensor Processor

Create a file named `sensor_processor.py`:

```python
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
```

## Running the AI Agent System

1. Open a terminal and source your ROS 2 environment:
   ```bash
   source /opt/ros/humble/setup.bash
   ```

2. In one terminal, run the sensor publisher (from Chapter 1):
   ```bash
   python3 publisher_node.py
   ```

3. In another terminal, run the AI agent:
   ```bash
   python3 ai_agent_node.py
   ```

4. In a third terminal, run a simple robot controller that listens to commands:
   ```bash
   # Subscribe to the robot commands
   ros2 topic echo /robot_commands
   ```

## Advanced AI Integration

For more complex AI integration, consider:

### Using External AI Libraries

```python
import tensorflow as tf  # or pytorch, scikit-learn, etc.
import numpy as np

class AdvancedAIAgentNode(Node):
    def __init__(self):
        super().__init__('advanced_ai_agent_node')

        # Load your AI model
        self.model = self.load_model()

        # Rest of the node setup...

    def load_model(self):
        """Load your trained AI model"""
        # Example with TensorFlow
        # model = tf.keras.models.load_model('path/to/model')
        # return model
        pass

    def make_decision(self, sensor_data):
        """Use AI model to make decisions"""
        # Preprocess sensor data for the model
        # input_data = self.preprocess(sensor_data)
        #
        # # Run inference
        # prediction = self.model.predict(input_data)
        #
        # # Convert prediction to robot command
        # command = self.convert_prediction_to_command(prediction)
        #
        # return command
        pass
```

## Testing and Validation

1. **Unit Testing**: Test individual components in isolation
2. **Integration Testing**: Test the complete AI-ROS communication chain
3. **Performance Testing**: Ensure the AI agent responds within required time constraints
4. **Robustness Testing**: Test with various sensor data inputs and error conditions

## Best Practices

- Keep AI processing time minimal to maintain real-time responsiveness
- Implement proper error handling for AI model failures
- Log decision-making process for debugging and analysis
- Consider safety constraints in AI decision-making
- Validate AI outputs before sending to robot systems

This tutorial demonstrates how to connect AI decision-making with ROS 2 robot control systems, forming the bridge between artificial intelligence and physical robot control.