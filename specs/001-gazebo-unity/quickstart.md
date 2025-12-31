# Quickstart Guide: Module 2 - The Digital Twin (Gazebo & Unity)

## Prerequisites

Before starting Module 2, ensure you have completed Module 1 and have the following installed:

1. **Gazebo**: Gazebo Harmonic or compatible version
2. **Unity**: LTS version (2022.3.x or later)
3. **ROS 2**: Humble Hawksbill or compatible version
4. **Docusaurus**: For documentation development
5. **Basic knowledge**: Physics simulation concepts, ROS 2 fundamentals

## Installation Steps

### 1. Install Gazebo Harmonic

```bash
# For Ubuntu 22.04
sudo apt update
sudo apt install gazebo libgazebo-dev
```

### 2. Install Unity Hub

Download and install Unity Hub from the Unity website, then install the LTS version of Unity.

### 3. Verify ROS 2 Installation

```bash
source /opt/ros/humble/setup.bash
ros2 --version
```

## Getting Started with Gazebo

### 1. Create a Basic World

Create a simple world file (`basic_world.sdf`):

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="basic_world">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>

    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>10 10</size>
            </plane>
          </geometry>
        </visual>
      </link>
    </model>
  </world>
</sdf>
```

### 2. Launch Gazebo with Your World

```bash
gz sim -r basic_world.sdf
```

### 3. Add a Robot Model

Create a simple robot model (`simple_robot.sdf`):

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_robot">
    <link name="chassis">
      <pose>0 0 0.1 0 0 0</pose>
      <collision name="collision">
        <geometry>
          <box>
            <size>1.0 0.5 0.2</size>
          </box>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <box>
            <size>1.0 0.5 0.2</size>
          </box>
        </geometry>
      </visual>
      <inertial>
        <mass>1.0</mass>
        <inertia>
          <ixx>0.01</ixx>
          <iyy>0.01</iyy>
          <izz>0.01</izz>
        </inertia>
      </inertial>
    </link>
  </model>
</sdf>
```

## Getting Started with Unity HRI

### 1. Create a New Unity Project

1. Open Unity Hub
2. Create a new 3D project named "HRI_Simulation"
3. Set up basic scene with lighting and environment

### 2. Create Humanoid Robot Model

For simulation purposes, you can create a simple robot model using Unity primitives:

1. Create a capsule for the body
2. Add sphere joints for head and limbs
3. Set up basic physics properties

### 3. Create Interaction Points

1. Add trigger colliders for interaction zones
2. Create scripts to handle human-robot interaction events
3. Focus on simulation rather than complex game logic

## Creating Sensor Models

### 1. LiDAR Sensor Configuration

Example LiDAR sensor configuration for a robot model:

```xml
<sensor name="lidar_sensor" type="ray">
  <always_on>true</always_on>
  <update_rate>10</update_rate>
  <ray>
    <scan>
      <horizontal>
        <samples>640</samples>
        <resolution>1</resolution>
        <min_angle>-1.570796</min_angle>
        <max_angle>1.570796</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>10.0</max>
      <resolution>0.01</resolution>
    </range>
  </ray>
  <plugin name="ray_sensor" filename="libRayPlugin.so"/>
</sensor>
```

### 2. Depth Camera Configuration

Example depth camera configuration:

```xml
<sensor name="depth_camera" type="depth">
  <always_on>true</always_on>
  <update_rate>30</update_rate>
  <camera name="depth_cam">
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
      <format>R_FLOAT32</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>10</far>
    </clip>
  </camera>
  <plugin name="depth_camera" filename="libDepthCameraPlugin.so"/>
</sensor>
```

### 3. IMU Sensor Configuration

Example IMU sensor configuration:

```xml
<sensor name="imu_sensor" type="imu">
  <always_on>true</always_on>
  <update_rate>100</update_rate>
  <imu>
    <angular_velocity>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.0017</stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.0017</stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.0017</stddev>
        </noise>
      </z>
    </angular_velocity>
    <linear_acceleration>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.017</stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.017</stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.017</stddev>
        </noise>
      </z>
    </linear_acceleration>
  </imu>
</sensor>
```

## Running the Examples

1. Save your SDF files in a models directory
2. Launch Gazebo with your world and robot models
3. Use the Gazebo GUI to interact with and observe your simulation
4. For Unity, build and run your interaction scenarios

## Next Steps

1. Complete the Chapter 1 tutorials on Gazebo fundamentals
2. Move to Chapter 2 to learn about sensor simulation
3. Explore Chapter 3 for Unity-based human-robot interaction concepts
4. Practice with the hands-on exercises provided in each chapter