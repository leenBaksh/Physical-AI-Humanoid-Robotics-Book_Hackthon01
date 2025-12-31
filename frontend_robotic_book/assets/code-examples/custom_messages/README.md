# Custom Messages

This directory contains custom ROS 2 message definitions that can be used for specialized AI-robot communication.

## Available Message Types

### ai_decision.msg
```
float64 confidence
string action_type
float64[] parameters
string reason
```

### ai_command.msg
```
string command_type  # "move", "grasp", "inspect", etc.
float64[] parameters # Command-specific parameters
float64 priority     # Execution priority (0.0-1.0)
string ai_id         # ID of the AI agent issuing the command
```

### ai_feedback.msg
```
string command_id    # ID of the command being reported on
string status        # "executing", "completed", "failed", "cancelled"
float64 progress     # Progress percentage (0.0-1.0)
string message       # Human-readable status message
```

## Creating Custom Messages

To create a new custom message:

1. Create a `.msg` file in this directory
2. Define the message fields using the appropriate data types
3. Create a `CMakeLists.txt` to build the message
4. Build your ROS 2 workspace: `colcon build --packages-select your_package_name`

## Using Custom Messages

To use these custom messages in your nodes:

```python
from your_package_name.msg import AiDecision

def callback(msg):
    print(f"Confidence: {msg.confidence}, Action: {msg.action_type}")

subscription = node.create_subscription(AiDecision, 'ai_decision_topic', callback, 10)
```

For more information on creating custom messages, see the ROS 2 documentation on message definition files.