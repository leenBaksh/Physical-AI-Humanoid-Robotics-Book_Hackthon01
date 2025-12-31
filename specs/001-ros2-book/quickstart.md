# Quickstart Guide: Module 1 - The Robotic Nervous System (ROS 2)

## Prerequisites

Before starting this book, you'll need:

1. **Operating System**: Ubuntu 22.04 LTS or equivalent Linux distribution
2. **Python**: Python 3.8 or higher
3. **Node.js**: Node.js 16.x or higher for Docusaurus
4. **Git**: Version control system
5. **Basic knowledge**: Python programming and fundamental AI concepts

## Installation Steps

### 1. Install ROS 2 Humble Hawksbill

```bash
# Add the ROS 2 repository
sudo apt update && sudo apt install -y software-properties-common
sudo add-apt-repository universe

# Add the ROS 2 GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add the repository to your sources list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 packages
sudo apt update
sudo apt install ros-humble-desktop
sudo apt install python3-rosdep2
sudo apt install python3-colcon-common-extensions
```

### 2. Install ROS 2 Python Client Library (rclpy)

```bash
pip3 install rclpy
```

### 3. Install Docusaurus

```bash
# Install Node.js dependencies
npm install -g @docusaurus/cli

# Navigate to your project directory and create a Docusaurus site
npx create-docusaurus@latest my-website classic
cd my-website
```

### 4. Set up Environment Variables

```bash
source /opt/ros/humble/setup.bash
```

## Running Your First Example

### 1. Create a Simple Publisher Node

Create a file named `publisher_node.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 2. Run the Publisher

```bash
python3 publisher_node.py
```

### 3. In a new terminal, create and run a Subscriber

Create `subscriber_node.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Run the subscriber in a new terminal:

```bash
python3 subscriber_node.py
```

You should see the publisher sending messages and the subscriber receiving them.

## Building the Documentation Site

1. Navigate to your Docusaurus project directory
2. Add your content to the `docs/` folder
3. Run the development server:

```bash
npm start
```

This will start a local server at `http://localhost:3000` where you can view your documentation.

## Next Steps

1. Continue with Chapter 1 to learn more about ROS 2 core concepts
2. Proceed to Chapter 2 to understand the AI-ROS bridge
3. Explore Chapter 3 to learn about URDF interpretation