---
sidebar_position: 2
title: "Implementing Whisper-Based Voice Recognition in ROS 2"
---

# Implementing Whisper-Based Voice Recognition in ROS 2

## Introduction

In this chapter, we'll implement a ROS 2 node that uses OpenAI Whisper to process live audio commands and publish transcriptions to a ROS 2 topic. Whisper is a state-of-the-art speech recognition model that provides high accuracy for voice-to-text conversion. By integrating Whisper with ROS 2, we can enable voice-controlled robots that can understand and respond to spoken commands.

## Prerequisites

Before starting this tutorial, ensure you have:

1. ROS 2 Humble Hawksbill installed and properly configured
2. Python 3.8+ for ROS 2 compatibility
3. OpenAI API key (or local Whisper model setup)
4. Completed Module 1: ROS 2 Fundamentals
5. Basic understanding of Python programming

## Setting Up Dependencies

### Installing Whisper and OpenAI Libraries

First, let's install the necessary Python libraries for Whisper integration:

```bash
# Create a virtual environment for VLA components
python3 -m venv vla_env
source vla_env/bin/activate  # On Windows: vla_env\Scripts\activate

# Install OpenAI library
pip install openai

# Install Whisper (choose one of the following options)
# Option 1: Install openai-whisper (easier to set up)
pip install openai-whisper

# Option 2: Install from source for latest features
pip install git+https://github.com/openai/whisper.git

# Install additional dependencies
pip install torch torchaudio
```

### Setting Up OpenAI API Key

If using the OpenAI API for Whisper, set your API key:

```bash
# Set OpenAI API key as environment variable
export OPENAI_API_KEY="your-api-key-here"
```

## Creating the Whisper ROS 2 Node

### Project Structure

First, create a ROS 2 package for the Whisper node:

```bash
# Navigate to your ROS 2 workspace
cd ~/vla_ws/src

# Create the Whisper node package
ros2 pkg create --build-type ament_python whisper_ros_node

# Navigate to the package directory
cd whisper_ros_node
```

### Creating the Whisper Node Implementation

Create the main node file at `whisper_ros_node/whisper_node.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import AudioData
import openai
import tempfile
import os
import wave
import numpy as np


class WhisperNode(Node):
    def __init__(self):
        super().__init__('whisper_node')

        # Declare parameters
        self.declare_parameter('model', 'whisper-1')
        self.declare_parameter('use_local_model', False)
        self.declare_parameter('language', 'en')
        self.declare_parameter('temperature', 0.0)

        # Get parameters
        self.model = self.get_parameter('model').value
        self.use_local_model = self.get_parameter('use_local_model').value
        self.language = self.get_parameter('language').value
        self.temperature = self.get_parameter('temperature').value

        # Initialize OpenAI client
        if not self.use_local_model:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                self.get_logger().error('OpenAI API key not found in environment variables')
                raise ValueError('OpenAI API key is required')
            openai.api_key = api_key

        # Create subscriber for audio data
        self.audio_sub = self.create_subscription(
            AudioData,
            'audio_input',
            self.audio_callback,
            10
        )

        # Create publisher for transcriptions
        self.transcription_pub = self.create_publisher(
            String,
            'whisper/transcription',
            10
        )

        self.get_logger().info('Whisper node initialized')

    def audio_callback(self, msg):
        """Process incoming audio data and generate transcription"""
        try:
            # Convert AudioData to WAV file
            wav_file_path = self.audio_data_to_wav(msg)

            # Generate transcription
            if self.use_local_model:
                transcription = self.transcribe_with_local_model(wav_file_path)
            else:
                transcription = self.transcribe_with_api(wav_file_path)

            # Publish transcription
            transcription_msg = String()
            transcription_msg.data = transcription
            self.transcription_pub.publish(transcription_msg)

            self.get_logger().info(f'Transcription: {transcription}')

            # Clean up temporary file
            os.remove(wav_file_path)

        except Exception as e:
            self.get_logger().error(f'Error processing audio: {e}')

    def audio_data_to_wav(self, audio_msg):
        """Convert sensor_msgs/AudioData to WAV file"""
        # Create a temporary WAV file
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_wav.close()

        # Write audio data to WAV file
        with wave.open(temp_wav.name, 'wb') as wav_file:
            # Set WAV parameters (these should match the audio message)
            wav_file.setnchannels(1)  # Assuming mono
            wav_file.setsampwidth(2)  # Assuming 16-bit samples
            wav_file.setframerate(16000)  # Assuming 16kHz sample rate
            wav_file.writeframes(audio_msg.data)

        return temp_wav.name

    def transcribe_with_api(self, wav_file_path):
        """Transcribe audio using OpenAI API"""
        with open(wav_file_path, 'rb') as audio_file:
            response = openai.Audio.transcribe(
                model=self.model,
                file=audio_file,
                language=self.language,
                temperature=self.temperature
            )
        return response['text']

    def transcribe_with_local_model(self, wav_file_path):
        """Transcribe audio using local Whisper model"""
        import whisper

        # Load model (you may want to cache this)
        model = whisper.load_model(self.model)

        # Transcribe
        result = model.transcribe(wav_file_path, language=self.language)
        return result['text']


def main(args=None):
    rclpy.init(args=args)
    node = WhisperNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Creating the Setup File

Create `whisper_ros_node/setup.py`:

```python
from setuptools import setup
import os
from glob import glob

package_name = 'whisper_ros_node'

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
    description='ROS 2 node for OpenAI Whisper integration',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'whisper_node = whisper_ros_node.whisper_node:main',
        ],
    },
)
```

### Creating the Package XML

Create `whisper_ros_node/package.xml`:

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>whisper_ros_node</name>
  <version>0.0.1</version>
  <description>ROS 2 node for OpenAI Whisper integration</description>
  <maintainer email="your.email@example.com">Your Name</maintainer>
  <license>Apache License 2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>sensor_msgs</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

## Building the Package

Build your ROS 2 workspace with the new package:

```bash
# Navigate to your workspace
cd ~/vla_ws

# Build the workspace
colcon build --packages-select whisper_ros_node

# Source the workspace
source install/setup.bash
```

## Testing the Whisper Node

### Running the Node

```bash
# Terminal 1: Run the Whisper node
cd ~/vla_ws
source install/setup.bash
ros2 run whisper_ros_node whisper_node
```

### Publishing Test Audio Data

To test the node, you can publish audio data to the `/audio_input` topic. Here's a simple test script:

Create `test_audio_publisher.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import AudioData
import wave
import sys


class AudioPublisher(Node):
    def __init__(self):
        super().__init__('audio_publisher')
        self.publisher = self.create_publisher(AudioData, 'audio_input', 10)

        # Read audio file and publish
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.publish_audio)

        if len(sys.argv) < 2:
            self.get_logger().error('Please provide a WAV file path as argument')
            return

        self.audio_file_path = sys.argv[1]

    def publish_audio(self):
        """Read audio file and publish as AudioData message"""
        try:
            with wave.open(self.audio_file_path, 'rb') as wav_file:
                # Read audio frames
                frames = wav_file.readframes(wav_file.getnframes())

                # Create AudioData message
                msg = AudioData()
                msg.data = frames

                self.publisher.publish(msg)
                self.get_logger().info('Published audio data')

        except Exception as e:
            self.get_logger().error(f'Error reading audio file: {e}')


def main(args=None):
    rclpy.init(args=args)
    audio_publisher = AudioPublisher()

    try:
        rclpy.spin(audio_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        audio_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Alternative: Local Whisper Model Setup

If you prefer to use Whisper locally without the OpenAI API, you can set up a local model:

```bash
# Install Whisper with local model support
pip install openai-whisper

# Install additional dependencies
pip install torch torchaudio
```

Then modify your node to use local models by setting the `use_local_model` parameter to `True` and using appropriate model names like "tiny", "base", "small", "medium", or "large".

## Configuration Parameters

The Whisper node supports several configuration parameters:

- `model`: Whisper model to use (e.g., "whisper-1" for API, "small" for local)
- `use_local_model`: Whether to use local model instead of API
- `language`: Language of the audio (e.g., "en", "es", "fr")
- `temperature`: Sampling temperature for transcription

## Performance Considerations

### Latency Optimization

To minimize transcription latency:

1. **Use appropriate model size**: Smaller models (tiny, base) are faster but less accurate
2. **Optimize audio input**: Use appropriate sample rates (16kHz is often sufficient)
3. **Batch processing**: Process longer audio segments for better accuracy

### Resource Management

- **Memory usage**: Local Whisper models can use significant memory (up to 10GB for large model)
- **CPU/GPU usage**: Models can be run on CPU, but GPU acceleration significantly improves performance
- **API costs**: Using OpenAI API has cost implications based on usage

## Troubleshooting Common Issues

### Audio Format Issues

If you encounter audio format issues:

1. Ensure your audio is in a compatible format (WAV, MP3, etc.)
2. Check sample rate compatibility (16kHz recommended)
3. Verify audio channel configuration (mono vs stereo)

### API Connection Issues

For OpenAI API connection problems:

1. Verify your API key is set correctly
2. Check your internet connection
3. Ensure you have sufficient API quota

### Installation Issues

For installation problems:

1. Ensure you have the correct Python version (3.8+)
2. Install PyTorch with appropriate CUDA support if using GPU
3. Check that all dependencies are properly installed

## Integration with Other ROS 2 Nodes

The Whisper node publishes transcriptions to the `/whisper/transcription` topic, which can be subscribed to by other ROS 2 nodes:

```python
# Example subscriber to the transcription topic
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TranscriptionSubscriber(Node):
    def __init__(self):
        super().__init__('transcription_subscriber')
        self.subscription = self.create_subscription(
            String,
            'whisper/transcription',
            self.transcription_callback,
            10
        )

    def transcription_callback(self, msg):
        self.get_logger().info(f'Received transcription: {msg.data}')
        # Process the transcription further (e.g., send to LLM for action planning)
```

## Summary

In this chapter, you learned how to:
- Set up OpenAI Whisper for voice recognition in ROS 2
- Create a ROS 2 node that processes audio input through Whisper
- Publish transcriptions to ROS 2 topics for other nodes to use
- Configure and optimize the Whisper node for performance

## Next Steps

In the next chapter, we'll explore how to build an LLM action server that takes these transcriptions and converts them into structured action plans for robotic execution. You'll learn how to bridge natural language understanding with robotic action planning.