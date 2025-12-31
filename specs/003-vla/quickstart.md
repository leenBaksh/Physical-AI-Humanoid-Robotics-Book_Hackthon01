# Quickstart Guide: Vision-Language-Action (VLA) for Cognitive Robotics

## Prerequisites

Before starting with the Vision-Language-Action module, ensure you have the following:

1. **ROS 2 Humble Hawksbill**: Installed and properly configured
2. **Python 3.8+**: For ROS 2 compatibility
3. **OpenAI Account**: For API access (or local Whisper model setup)
4. **Microphone**: For audio input (for testing)
5. **Previous Modules**: Complete Module 1 (ROS 2), Module 2 (Gazebo/Unity), and Module 3 (Isaac Sim)
6. **Simulation Environment**: Gazebo or Isaac Sim properly configured

## Setting Up the Development Environment

### 1. Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv vla_env
source vla_env/bin/activate  # On Windows: vla_env\Scripts\activate

# Install Whisper and OpenAI libraries
pip install openai
pip install openai-whisper
pip install torch torchaudio  # For local Whisper processing

# Install ROS 2 Python libraries
pip install rclpy

# Install other dependencies
pip install numpy transforms3d
```

### 2. Set Up OpenAI API Key

```bash
# Set your OpenAI API key as environment variable
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Create ROS 2 Workspace for VLA

```bash
# Create workspace
mkdir -p ~/vla_ws/src
cd ~/vla_ws

# Build the workspace
colcon build
source install/setup.bash
```

## Module 4: Vision-Language-Action (VLA)

### Chapter 1: Voice-to-Action with Whisper

#### Setting Up the Whisper Node

1. Create the Whisper ROS 2 node package:
```bash
cd ~/vla_ws/src
ros2 pkg create --build-type ament_python whisper_ros_node
```

2. The Whisper node will subscribe to audio topics and publish transcriptions.

#### Running the Whisper Node

```bash
# Terminal 1: Source the workspace
cd ~/vla_ws
source install/setup.bash

# Terminal 1: Run the Whisper node
ros2 run whisper_ros_node whisper_node

# Terminal 2: Test with audio input
# You can publish audio data to the appropriate topic
```

### Chapter 2: Cognitive Planning with LLMs

#### Setting Up the LLM Action Server

1. Create the LLM action server package:
```bash
cd ~/vla_ws/src
ros2 pkg create --build-type ament_python llm_action_server
```

2. The LLM action server will receive natural language commands and generate action plans.

#### Running the LLM Action Server

```bash
# Terminal 1: Source the workspace
cd ~/vla_ws
source install/setup.bash

# Terminal 1: Run the LLM action server
ros2 run llm_action_server llm_server

# Terminal 2: Send a natural language command
# Use the action client to send commands
```

### Chapter 3: Capstone Integration

#### Running the Full Pipeline

1. Launch the complete cognitive pipeline:
```bash
# Create a launch file that starts all components
cd ~/vla_ws/src
mkdir -p vla_launch/launch
```

2. Create a launch file that combines all components:
```xml
<!-- vla_pipeline.launch.py -->
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    return LaunchDescription([
        # Whisper node
        Node(
            package='whisper_ros_node',
            executable='whisper_node',
            name='whisper_node'
        ),

        # LLM action server
        Node(
            package='llm_action_server',
            executable='llm_server',
            name='llm_server'
        ),

        # Integration node
        Node(
            package='vla_integration',
            executable='vla_pipeline',
            name='vla_pipeline'
        )
    ])
```

3. Run the complete pipeline:
```bash
# Terminal 1: Source the workspace and launch
cd ~/vla_ws
source install/setup.bash
ros2 launch vla_launch vla_pipeline.launch.py
```

## Testing Your Setup

### Test Voice Recognition

```bash
# Test the Whisper node independently
ros2 topic echo /whisper/transcription std_msgs/String
```

### Test LLM Integration

```bash
# Test the LLM action server
ros2 action send_goal /llm_plan llm_interfaces/action/NaturalLanguageCommand "{command: 'Go to the kitchen and pick up the red cup'}"
```

### Test Complete Pipeline

```bash
# Run the full integration test
cd ~/vla_ws
source install/setup.bash
ros2 run vla_integration test_pipeline
```

## Troubleshooting

### Common Issues

1. **Whisper Installation Issues**: Ensure you have the correct PyTorch version installed
2. **OpenAI API Connection**: Verify your API key is set correctly
3. **ROS 2 Topic Connection**: Check that nodes are properly connected
4. **Simulation Environment**: Ensure Isaac Sim or Gazebo is properly configured

### Checking System Status

```bash
# Check running nodes
ros2 node list

# Check topics
ros2 topic list

# Check actions
ros2 action list
```

## Next Steps

1. Complete Chapter 1: Implement Whisper-based voice recognition
2. Proceed to Chapter 2: Build LLM-based action planning
3. Complete Chapter 3: Integrate the full cognitive pipeline
4. Test the complete end-to-end system