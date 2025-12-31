---
sidebar_position: 3
title: "Building an LLM-Based Cognitive Planning System in ROS 2"
---

# Building an LLM-Based Cognitive Planning System in ROS 2

## Introduction

In this chapter, we'll build a ROS 2 action server that uses a Large Language Model (LLM) to parse natural language commands into structured sequences of ROS 2 actions and goals. The cognitive planning system bridges the gap between human language and robotic action execution, enabling robots to understand complex, high-level instructions and break them down into executable steps.

This system represents the cognitive aspect of our robotic system, enabling natural language understanding and intelligent action planning. It's the core component that translates human intent into robot behavior.

## Prerequisites

Before starting this tutorial, ensure you have:

1. ROS 2 Humble Hawksbill installed and properly configured
2. Python 3.8+ for ROS 2 compatibility
3. OpenAI API key (or local LLM model setup)
4. Completed Chapter 1: Voice-to-Action with Whisper
5. Basic understanding of ROS 2 actions and action servers
6. Familiarity with JSON data structures

## Setting Up Dependencies

### Installing LLM Libraries

First, let's install the necessary Python libraries for LLM integration:

```bash
# Create a virtual environment for LLM components
python3 -m venv llm_env
source llm_env/bin/activate  # On Windows: llm_env\Scripts\activate

# Install OpenAI library
pip install openai

# Install other dependencies
pip install rclpy std_msgs sensor_msgs action_msgs

# For JSON parsing and validation
pip install jsonschema
```

### Setting Up OpenAI API Key

Set your OpenAI API key for the LLM integration:

```bash
# Set OpenAI API key as environment variable
export OPENAI_API_KEY="your-api-key-here"
```

## Creating the LLM Action Server

### Project Structure

Create a ROS 2 package for the LLM action server:

```bash
# Navigate to your ROS 2 workspace
cd ~/vla_ws/src

# Create the LLM action server package
ros2 pkg create --build-type ament_python llm_action_server

# Navigate to the package directory
cd llm_action_server
```

### Defining the Action Interface

We need to define a custom action interface for the LLM cognitive planning. Create the action definition file at `llm_action_server/action/NaturalLanguageCommand.action`:

```action
# Input: Natural language command from user
string command
string context

---
# Result: Generated action plan and success status
string plan_json
bool success
string error_message

---
# Feedback: Current status and progress of the planning process
string status
float32 progress
string current_step
```

### Creating the Action Server Implementation

Create the main action server file at `llm_action_server/llm_action_server.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.qos import QoSProfile, QoSDurabilityPolicy
import openai
import json
import os
import threading
from action_msgs.msg import GoalStatus
from llm_action_server.action import NaturalLanguageCommand


class LLMActionServer(Node):
    def __init__(self):
        super().__init__('llm_action_server')

        # Declare parameters
        self.declare_parameter('model', 'gpt-4-turbo')
        self.declare_parameter('temperature', 0.3)
        self.declare_parameter('max_tokens', 1000)
        self.declare_parameter('response_format', 'json')

        # Get parameters
        self.model = self.get_parameter('model').value
        self.temperature = self.get_parameter('temperature').value
        self.max_tokens = self.get_parameter('max_tokens').value
        self.response_format = self.get_parameter('response_format').value

        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            self.get_logger().error('OpenAI API key not found in environment variables')
            raise ValueError('OpenAI API key is required')

        openai.api_key = api_key

        # Initialize action server
        self._action_server = ActionServer(
            self,
            NaturalLanguageCommand,
            'llm_plan',
            self.execute_callback,
            callback_group=ReentrantCallbackGroup(),
            goal_service_qos_profile=QoSProfile(depth=10),
            result_service_qos_profile=QoSProfile(depth=10),
            cancel_service_qos_profile=QoSProfile(depth=10),
            feedback_pub_qos_profile=QoSProfile(depth=10)
        )

        self.get_logger().info('LLM Action Server initialized')

    def execute_callback(self, goal_handle):
        """Execute the action goal - convert natural language to action plan"""
        self.get_logger().info(f'Executing goal: {goal_handle.request.command}')

        # Send initial feedback
        feedback_msg = NaturalLanguageCommand.Feedback()
        feedback_msg.status = 'Processing natural language command'
        feedback_msg.progress = 0.0
        feedback_msg.current_step = 'Parsing command'
        goal_handle.publish_feedback(feedback_msg)

        try:
            # Generate action plan from natural language command
            result = NaturalLanguageCommand.Result()

            # Update feedback
            feedback_msg.progress = 0.3
            feedback_msg.current_step = 'Generating action plan'
            goal_handle.publish_feedback(feedback_msg)

            action_plan = self.generate_action_plan(
                goal_handle.request.command,
                goal_handle.request.context
            )

            # Update feedback
            feedback_msg.progress = 0.7
            feedback_msg.current_step = 'Validating action plan'
            goal_handle.publish_feedback(feedback_msg)

            # Validate the action plan
            if self.validate_action_plan(action_plan):
                result.success = True
                result.plan_json = json.dumps(action_plan)
                result.error_message = ''

                # Log the successful plan
                self.get_logger().info(f'Generated action plan: {json.dumps(action_plan, indent=2)}')

                goal_handle.succeed()
            else:
                result.success = False
                result.plan_json = '{}'
                result.error_message = 'Generated action plan failed validation'
                goal_handle.abort()

        except Exception as e:
            self.get_logger().error(f'Error generating action plan: {str(e)}')
            result = NaturalLanguageCommand.Result()
            result.success = False
            result.plan_json = '{}'
            result.error_message = f'Error: {str(e)}'
            goal_handle.abort()

        # Update final feedback
        feedback_msg.progress = 1.0
        feedback_msg.current_step = 'Completed'
        goal_handle.publish_feedback(feedback_msg)

        return result

    def generate_action_plan(self, command, context):
        """Generate action plan from natural language command using LLM"""

        # Craft the prompt for the LLM
        prompt = f"""
        You are a robotic cognitive planner. Your task is to convert natural language commands into structured action plans for a robot.

        The robot has the following capabilities:
        - Navigation: Can move to specific locations (requires x, y, z coordinates and orientation)
        - Object Detection: Can identify objects in the environment
        - Manipulation: Can pick up, place, and move objects
        - Communication: Can provide status updates

        Given the command: "{command}"

        Additional context: {context}

        Respond ONLY with a valid JSON object containing the action plan. The JSON must contain an array called 'actions', where each action has:
        - 'type': The action type (navigation, manipulation, detection, communication)
        - 'parameters': An object containing the specific parameters for the action
        - 'description': A brief description of the action

        Example format:
        {{
            "actions": [
                {{
                    "type": "navigation",
                    "parameters": {{
                        "target_location": {{
                            "x": 1.0,
                            "y": 2.0,
                            "z": 0.0,
                            "orientation": {{
                                "w": 1.0,
                                "x": 0.0,
                                "y": 0.0,
                                "z": 0.0
                            }}
                        }},
                        "behavior_tree": "default_nav_tree"
                    }},
                    "description": "Move to the kitchen area"
                }},
                {{
                    "type": "detection",
                    "parameters": {{
                        "object_name": "red cup",
                        "camera_source": "front_camera"
                    }},
                    "description": "Look for the red cup"
                }},
                {{
                    "type": "manipulation",
                    "parameters": {{
                        "action": "pick",
                        "target_object": "red cup",
                        "end_effector_pose": {{
                            "position": {{
                                "x": 0.5,
                                "y": 0.0,
                                "z": 0.0
                            }},
                            "orientation": {{
                                "w": 1.0,
                                "x": 0.0,
                                "y": 0.0,
                                "z": 0.0
                            }}
                        }}
                    }},
                    "description": "Pick up the red cup"
                }}
            ],
            "plan_metadata": {{
                "estimated_duration": "300",
                "success_criteria": ["object_picked", "location_reached"],
                "dependencies": []
            }}
        }}
        """

        # Call the OpenAI API
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a robotic cognitive planner that outputs only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )

            # Extract the plan from the response
            plan_text = response.choices[0].message.content

            # Parse the JSON
            plan = json.loads(plan_text)

            return plan

        except Exception as e:
            self.get_logger().error(f'Error calling LLM: {str(e)}')
            # Return a default plan if LLM fails
            return {
                "actions": [],
                "plan_metadata": {
                    "estimated_duration": "0",
                    "success_criteria": [],
                    "dependencies": []
                },
                "error": f"Failed to generate plan: {str(e)}"
            }

    def validate_action_plan(self, plan):
        """Validate the action plan to ensure it's executable"""

        # Check if plan has the required structure
        if not isinstance(plan, dict):
            self.get_logger().error('Plan is not a dictionary')
            return False

        if 'actions' not in plan:
            self.get_logger().error('Plan does not contain "actions" key')
            return False

        if not isinstance(plan['actions'], list):
            self.get_logger().error('Actions in plan is not a list')
            return False

        # Validate each action in the plan
        for i, action in enumerate(plan['actions']):
            if not isinstance(action, dict):
                self.get_logger().error(f'Action {i} is not a dictionary')
                return False

            if 'type' not in action:
                self.get_logger().error(f'Action {i} does not have a type')
                return False

            # Check if action type is valid
            valid_types = ['navigation', 'manipulation', 'detection', 'communication']
            if action['type'] not in valid_types:
                self.get_logger().error(f'Action {i} has invalid type: {action["type"]}')
                return False

            if 'parameters' not in action:
                self.get_logger().error(f'Action {i} does not have parameters')
                return False

            if not isinstance(action['parameters'], dict):
                self.get_logger().error(f'Parameters for action {i} is not a dictionary')
                return False

        return True


def main(args=None):
    rclpy.init(args=args)

    # Create executor with multiple threads to handle the action server
    executor = MultiThreadedExecutor(num_threads=4)

    node = LLMActionServer()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Creating the Setup File

Create `llm_action_server/setup.py`:

```python
from setuptools import setup
import os
from glob import glob

package_name = 'llm_action_server'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='ROS 2 action server for LLM-based cognitive planning',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'llm_action_server = llm_action_server.llm_action_server:main',
        ],
    },
)
```

### Creating the Package XML

Create `llm_action_server/package.xml`:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>llm_action_server</name>
  <version>0.0.1</version>
  <description>ROS 2 action server for LLM-based cognitive planning</description>
  <maintainer email="your.email@example.com">Your Name</maintainer>
  <license>Apache License 2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>action_msgs</depend>
  <buildtool_depend>ament_python</buildtool_depend>
  <exec_depend>rosidl_py_common</exec_depend>

  <member_of_group>rosidl_interface_packages</member_of_group>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

### Creating the Action Package Configuration

Create `llm_action_server/setup.cfg`:

```cfg
[develop]
script_dir=$base/lib/llm_action_server
[install]
install_scripts=$base/lib/llm_action_server
```

## Building the Package

Build your ROS 2 workspace with the new package:

```bash
# Navigate to your workspace
cd ~/vla_ws

# Build the workspace
colcon build --packages-select llm_action_server

# Source the workspace
source install/setup.bash
```

## Creating a Client to Test the Action Server

Create a test client to send natural language commands to the LLM action server:

Create `llm_action_server/test_llm_client.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
import json
from llm_action_server.action import NaturalLanguageCommand


class LLMClient(Node):
    def __init__(self):
        super().__init__('llm_client')
        self._action_client = ActionClient(
            self,
            NaturalLanguageCommand,
            'llm_plan'
        )

    def send_command(self, command, context=""):
        """Send a natural language command to the LLM action server"""

        self.get_logger().info(f'Sending command: {command}')

        goal_msg = NaturalLanguageCommand.Goal()
        goal_msg.command = command
        goal_msg.context = context

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handle the goal response from the action server"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """Handle the result from the action server"""
        result = future.result().result

        if result.success:
            self.get_logger().info('Successfully generated action plan:')
            try:
                # Pretty print the action plan
                plan_dict = json.loads(result.plan_json)
                self.get_logger().info(json.dumps(plan_dict, indent=2))
            except json.JSONDecodeError:
                self.get_logger().info(f'Plan JSON: {result.plan_json}')
        else:
            self.get_logger().error(f'Failed to generate action plan: {result.error_message}')

    def feedback_callback(self, feedback_msg):
        """Handle feedback from the action server"""
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Feedback: {feedback.status} ({feedback.progress:.1%}), '
            f'Current step: {feedback.current_step}'
        )


def main(args=None):
    rclpy.init(args=args)

    client = LLMClient()

    # Send a test command
    command = "Go to the kitchen and pick up the red cup from the table"
    client.send_command(command)

    # Spin to process callbacks
    rclpy.spin(client)


if __name__ == '__main__':
    main()
```

## Running the LLM Action Server

### Starting the Server

```bash
# Terminal 1: Run the LLM action server
cd ~/vla_ws
source install/setup.bash
ros2 run llm_action_server llm_action_server
```

### Testing with the Client

```bash
# Terminal 2: Test the server with natural language commands
cd ~/vla_ws
source install/setup.bash
ros2 run llm_action_server test_llm_client
```

## Advanced Features and Customization

### Custom Action Types

You can extend the system to support additional action types by modifying the validation logic and adding new action handlers in your robotic system. Common extensions include:

- **Monitoring**: Continuously observe the environment
- **Waiting**: Pause execution until a condition is met
- **Looping**: Repeat a sequence of actions
- **Conditional**: Execute different actions based on sensor input

### Context Integration

The LLM can be provided with contextual information to generate more relevant plans:

```python
# Example context about the current environment
context = {
    "robot_capabilities": ["navigation", "manipulation", "vision"],
    "current_location": {"x": 0.0, "y": 0.0, "z": 0.0},
    "known_objects": ["red cup", "blue box", "kitchen counter"],
    "environment_layout": "home environment with kitchen, living room, bedroom"
}

# Pass context to the action server
client.send_command(command, json.dumps(context))
```

### Error Handling and Fallback Strategies

The system includes several error handling mechanisms:

1. **Plan Validation**: Ensures generated plans are executable
2. **API Connection Recovery**: Handles network issues with the LLM provider
3. **Fallback Plans**: Generates default plans when LLM fails

### Performance Considerations

When deploying the LLM action server, consider these performance factors:

1. **API Latency**: LLM API calls can take several seconds; plan accordingly
2. **Rate Limits**: OpenAI APIs have rate limits that may affect responsiveness
3. **Caching**: Consider caching common command interpretations for faster response
4. **Local Models**: For low-latency applications, consider local LLM models

## Integration with Other Systems

### Integration with Voice Recognition (Chapter 1)

Connect the LLM action server with the Whisper voice recognition system:

```python
# Example of integrating with the Whisper system from Chapter 1
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.action import ActionClient
from llm_action_server.action import NaturalLanguageCommand


class VoiceToPlanBridge(Node):
    def __init__(self):
        super().__init__('voice_to_plan_bridge')

        # Subscribe to Whisper transcriptions
        self.transcription_sub = self.create_subscription(
            String,
            'whisper/transcription',
            self.transcription_callback,
            10
        )

        # Action client for LLM planning
        self._action_client = ActionClient(
            self,
            NaturalLanguageCommand,
            'llm_plan'
        )

    def transcription_callback(self, msg):
        """Handle incoming transcriptions from Whisper"""
        self.get_logger().info(f'Received transcription: {msg.data}')

        # Send to LLM for action planning
        self.send_command_to_llm(msg.data)

    def send_command_to_llm(self, command):
        """Send command to LLM action server"""
        goal_msg = NaturalLanguageCommand.Goal()
        goal_msg.command = command
        goal_msg.context = "Command received from voice recognition system"

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.plan_result_callback)

    def plan_result_callback(self, future):
        """Handle the action plan result"""
        goal_handle = future.result()
        result = goal_handle.get_result_async().result().result

        if result.success:
            self.get_logger().info('Action plan received successfully')
            # Forward the plan to the execution system
            # This could publish to a planning topic or trigger execution
        else:
            self.get_logger().error(f'Planning failed: {result.error_message}')
```

## Troubleshooting Common Issues

### API Connection Issues

If you encounter OpenAI API connection problems:

1. Verify your API key is set correctly
2. Check your internet connection
3. Ensure you have sufficient API quota
4. Consider using environment variables for key management

### Plan Generation Issues

If the LLM generates invalid plans:

1. Check the prompt engineering for clarity
2. Ensure the response format is set to JSON
3. Validate that action parameters match your robotic system capabilities
4. Add more examples to the prompt to guide the LLM

### Performance Issues

For slow response times:

1. Use smaller models for faster inference
2. Implement caching for common commands
3. Consider local LLM models for better performance
4. Optimize the prompt for more efficient generation

## Summary

In this chapter, you learned how to:
- Create an LLM-based cognitive planning system in ROS 2
- Build an action server that converts natural language to action plans
- Validate and structure action plans as JSON
- Integrate with other systems like voice recognition
- Handle errors and optimize performance

## Next Steps

In the next chapter, we'll combine everything to create the complete capstone integration. You'll learn how to tie together voice recognition, cognitive planning, navigation, vision, and manipulation into a complete cognitive robotics pipeline that can execute complex tasks in simulation.