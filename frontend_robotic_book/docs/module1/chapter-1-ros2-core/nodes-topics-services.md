---
sidebar_position: 2
---

# Understanding Nodes, Topics, and Services

## Nodes

A **node** is a fundamental component in ROS 2 that performs computation. Nodes are distributed across a ROS system and can be written in different programming languages. Each node typically performs a specific task, such as sensor data processing, control algorithm execution, or user interface handling.

### Key Characteristics of Nodes:
- Each node runs as an independent process
- Nodes communicate with other nodes through topics and services
- Nodes can be written in different programming languages (C++, Python, etc.)
- Nodes are managed by the ROS 2 runtime system

## Topics

**Topics** are named buses over which nodes exchange messages. The communication is based on a publish/subscribe pattern where publishers send messages to a topic and subscribers receive messages from a topic.

### Publisher-Subscriber Pattern:
- Publishers send data to a topic without knowing who (if anyone) is subscribed
- Subscribers receive data from a topic without knowing who (if anyone) is publishing
- Multiple publishers and subscribers can exist for the same topic
- This pattern promotes loose coupling between nodes

## Services

**Services** provide a request/reply communication pattern. A service client sends a request to a service server, which processes the request and sends back a response.

### Service Characteristics:
- Synchronous communication (client waits for response)
- Request/Response pattern
- One-to-one communication (one client, one server)
- Useful for actions that require immediate feedback

## Example: Node Communication

Let's look at how these components work together in a simple robot system:
- A sensor node publishes sensor data to a `/sensor_data` topic
- A control node subscribes to `/sensor_data` and publishes commands to `/robot_commands`
- A diagnostics service provides system status when requested by other nodes

In the next section, we'll dive deeper into the publisher-subscriber pattern and create our first ROS 2 nodes.