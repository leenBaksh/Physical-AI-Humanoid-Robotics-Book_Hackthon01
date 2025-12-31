---
sidebar_position: 3
---

# Publisher-Subscriber Patterns

The publisher-subscriber pattern is the primary communication mechanism in ROS 2. It enables nodes to exchange data through topics in a decoupled manner.

## How It Works

In the publisher-subscriber pattern:
1. A **publisher** node creates and sends messages to a specific topic
2. A **subscriber** node receives messages from that topic
3. Multiple publishers and subscribers can exist for the same topic
4. Publishers and subscribers are unaware of each other's existence

## Message Types

ROS 2 uses standardized message types to ensure compatibility between nodes. Common message types include:
- `std_msgs/String` - for string data
- `std_msgs/Int32` - for integer data
- `sensor_msgs/LaserScan` - for laser scanner data
- `geometry_msgs/Twist` - for velocity commands

## Quality of Service (QoS)

ROS 2 provides Quality of Service settings that allow you to control how messages are delivered:
- Reliability: Reliable (all messages delivered) or Best Effort (try to deliver messages)
- Durability: Volatile (new subscribers don't receive old messages) or Transient Local (new subscribers receive recent messages)

## Creating a Publisher

To create a publisher in Python using rclpy:
1. Create a publisher object with a specific message type and topic name
2. Publish messages to the topic using the publish() method
3. Handle the ROS 2 node lifecycle

## Creating a Subscriber

To create a subscriber in Python using rclpy:
1. Create a subscription object with a specific message type and topic name
2. Define a callback function to process incoming messages
3. Handle the ROS 2 node lifecycle

In the next section, we'll create our first hands-on example with publisher and subscriber nodes.