# Quickstart Guide: Isaac Sim & AI Perception Tools

## Prerequisites

Before starting with the Isaac Sim & AI Perception Tools module, ensure you have the following:

1. **NVIDIA Isaac Sim**: Download and install Isaac Sim (free tier/trial version)
2. **ROS 2**: Install ROS 2 Humble Hawksbill (should be compatible with Module 1 setup)
3. **Isaac ROS Packages**: Install the Isaac ROS packages for VSLAM
4. **Nav2**: Install Navigation2 stack for ROS 2
5. **Python**: Version 3.8+ for ROS 2 compatibility
6. **Git**: For version control
7. **Docker**: For consistent development environments (optional but recommended)

## Setting Up the Development Environment

### 1. Install Isaac Sim

1. Go to NVIDIA Isaac Sim download page
2. Download the free tier/trial version
3. Follow installation instructions for your operating system
4. Verify installation by launching Isaac Sim

### 2. Set Up ROS 2 Environment

```bash
# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Create workspace for Isaac projects
mkdir -p ~/isaac_ws/src
cd ~/isaac_ws

# Install Isaac ROS packages
sudo apt update
sudo apt install ros-humble-isaac-ros-visual-slam
sudo apt install ros-humble-isaac-ros-common
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup
```

### 3. Install Additional Dependencies

```bash
# Install Python dependencies
pip3 install numpy opencv-python transforms3d

# Install additional tools
sudo apt install ros-humble-rosbridge-suite
sudo apt install ros-humble-rviz2
```

## Module 3: Isaac Sim & AI Perception Tools

### Chapter 1: Isaac Sim Basics

#### Launch Isaac Sim and Create a Scene

1. Open Isaac Sim
2. Create a new scene or load a warehouse environment
3. Add a robot to the scene
4. Configure cameras for RGB and depth capture

#### Capture Synthetic Data

```python
# Example Python script to capture synthetic data
import omni
from omni.isaac.synthetic_utils import SyntheticDataHelper

# Initialize synthetic data helper
synthetic_data = SyntheticDataHelper()
synthetic_data.set_resolution(640, 480)

# Capture RGB and depth images
rgb_image = synthetic_data.get_rgb()
depth_image = synthetic_data.get_depth()
```

### Chapter 2: Isaac ROS VSLAM

#### Set Up VSLAM Nodes

1. Launch Isaac Sim with a moving robot
2. Start the visual SLAM node:

```bash
# Terminal 1: Launch Isaac Sim scene
ros2 launch isaac_ros_visual_slam isaac_ros_visual_slam.launch.py

# Terminal 2: Visualize in RViz
ros2 run rviz2 rviz2 -d /opt/ros/humble/share/isaac_ros_visual_slam/rviz/visual_slam.rviz
```

#### View Pose Graph

1. In RViz, add the pose graph visualization
2. Monitor the robot's trajectory and landmark detection
3. Verify that the map is being built correctly

### Chapter 3: Nav2 for Bipedal Navigation

#### Configure Bipedal Robot Model

1. Create or load a bipedal robot URDF
2. Configure costmaps for bipedal locomotion
3. Set up navigation parameters for walking instead of driving

#### Send Navigation Goals

```bash
# Send a navigation goal using ROS 2
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose "{
  pose: {
    header: {frame_id: 'map'},
    pose: {
      position: {x: 1.0, y: 1.0, z: 0.0},
      orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
    }
  }
}"
```

## Running the Tutorials

### 1. Chapter 1 Tutorial: Synthetic Data Generation

1. Follow the tutorial in `docs/module3/chapter1-synthetic-data/content.md`
2. Practice capturing RGB and depth images
3. Learn to generate labeled datasets for AI training

### 2. Chapter 2 Tutorial: VSLAM Implementation

1. Follow the tutorial in `docs/module3/chapter2-vslam/content.md`
2. Set up Isaac ROS VSLAM nodes
3. Visualize pose graphs in RViz

### 3. Chapter 3 Tutorial: Bipedal Navigation

1. Follow the tutorial in `docs/module3/chapter3-bipedal-nav/content.md`
2. Configure Nav2 for bipedal robot
3. Execute navigation goals in simulation

## Testing Your Setup

### Verify Isaac Sim Installation

```bash
# Check if Isaac Sim can be launched
isaac-sim
```

### Test ROS 2 Integration

```bash
# List available topics
ros2 topic list

# Check Isaac ROS nodes
ros2 node list | grep -i isaac
```

### Build and Test Documentation

```bash
# From project root
cd D:\Physical-AI---Humanoid-Robotics
npm install
npm run build
npm run serve
```

The documentation will be available at `http://localhost:3000`.

## Troubleshooting

### Common Issues

1. **Isaac Sim won't launch**: Check NVIDIA GPU drivers and CUDA compatibility
2. **VSLAM nodes not working**: Verify Isaac ROS packages installation
3. **Navigation fails**: Check costmap configuration for bipedal robot
4. **Documentation build fails**: Verify Node.js and Docusaurus installation

### Checking System Status

```bash
# Check Isaac Sim status
nvidia-smi

# Check ROS 2 nodes
ros2 node list

# Check ROS 2 topics
ros2 topic list
```

## Next Steps

1. Complete Chapter 1: Isaac Sim basics and synthetic data generation
2. Proceed to Chapter 2: Isaac ROS VSLAM implementation
3. Complete Chapter 3: Nav2 configuration for bipedal navigation
4. Integrate with Module 1 ROS 2 concepts