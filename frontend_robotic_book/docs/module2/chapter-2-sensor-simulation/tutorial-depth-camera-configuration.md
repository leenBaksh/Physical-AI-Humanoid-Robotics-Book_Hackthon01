---
sidebar_position: 15
title: "Hands-On: Configuring Depth Camera Sensor on Robot Model"
---

# Hands-On: Configuring Depth Camera Sensor on Robot Model

In this tutorial, you'll learn how to configure a depth camera sensor on a robot model in Gazebo. This will give you hands-on experience with integrating depth cameras into robot models and understanding their configuration parameters.

## Prerequisites

- Understanding of SDF structure
- Basic knowledge of robot models
- Gazebo installed and running

## Step 1: Create a Base Robot Model

First, let's create a simple robot model to which we'll add the depth camera. Create `robot_with_camera.sdf`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="robot_with_camera">
    <!-- Robot chassis -->
    <link name="chassis">
      <pose>0 0 0.1 0 0 0</pose>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.5 0.5 0.3</size>
          </box>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <box>
            <size>0.5 0.5 0.3</size>
          </box>
        </geometry>
        <material>
          <diffuse>0.8 0.8 0.2 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <inertial>
        <mass>5.0</mass>
        <inertia>
          <ixx>0.1</ixx>
          <iyy>0.1</iyy>
          <izz>0.1</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Robot wheels -->
    <link name="left_wheel">
      <pose>-0.2 0.3 0 0 1.5707 0</pose>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.05</length>
          </cylinder>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.05</length>
          </cylinder>
        </geometry>
        <material>
          <diffuse>0.3 0.3 0.3 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <inertial>
        <mass>0.5</mass>
        <inertia>
          <ixx>0.001</ixx>
          <iyy>0.001</iyy>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>

    <link name="right_wheel">
      <pose>-0.2 -0.3 0 0 1.5707 0</pose>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.05</length>
          </cylinder>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.05</length>
          </cylinder>
        </geometry>
        <material>
          <diffuse>0.3 0.3 0.3 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <inertial>
        <mass>0.5</mass>
        <inertia>
          <ixx>0.001</ixx>
          <iyy>0.001</iyy>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Joints to connect wheels to chassis -->
    <joint name="left_wheel_joint" type="continuous">
      <parent>chassis</parent>
      <child>left_wheel</child>
      <axis>
        <xyz>0 1 0</xyz>
      </axis>
    </joint>

    <joint name="right_wheel_joint" type="continuous">
      <parent>chassis</parent>
      <child>right_wheel</child>
      <axis>
        <xyz>0 1 0</xyz>
      </axis>
    </joint>
  </model>
</sdf>
```

## Step 2: Add Depth Camera to the Robot

Now, let's add a depth camera to the robot model. We'll position it on the front of the chassis:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="robot_with_camera">
    <!-- Robot chassis -->
    <link name="chassis">
      <pose>0 0 0.1 0 0 0</pose>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.5 0.5 0.3</size>
          </box>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <box>
            <size>0.5 0.5 0.3</size>
          </box>
        </geometry>
        <material>
          <diffuse>0.8 0.8 0.2 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <inertial>
        <mass>5.0</mass>
        <inertia>
          <ixx>0.1</ixx>
          <iyy>0.1</iyy>
          <izz>0.1</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Robot wheels -->
    <link name="left_wheel">
      <pose>-0.2 0.3 0 0 1.5707 0</pose>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.05</length>
          </cylinder>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.05</length>
          </cylinder>
        </geometry>
        <material>
          <diffuse>0.3 0.3 0.3 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <inertial>
        <mass>0.5</mass>
        <inertia>
          <ixx>0.001</ixx>
          <iyy>0.001</iyy>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>

    <link name="right_wheel">
      <pose>-0.2 -0.3 0 0 1.5707 0</pose>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.05</length>
          </cylinder>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.05</length>
          </cylinder>
        </geometry>
        <material>
          <diffuse>0.3 0.3 0.3 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <inertial>
        <mass>0.5</mass>
        <inertia>
          <ixx>0.001</ixx>
          <iyy>0.001</iyy>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Depth camera -->
    <link name="camera_link">
      <pose>0.25 0 0.15 0 0 0</pose>  <!-- Position on front of chassis -->
      <collision name="collision">
        <geometry>
          <box>
            <size>0.05 0.05 0.05</size>
          </box>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <box>
            <size>0.05 0.05 0.05</size>
          </box>
        </geometry>
        <material>
          <diffuse>0.5 0.5 0.5 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <inertial>
        <mass>0.1</mass>
        <inertia>
          <ixx>0.001</ixx>
          <iyy>0.001</iyy>
          <izz>0.001</izz>
        </inertia>
      </inertial>
      <sensor name="depth_camera" type="depth">
        <always_on>true</always_on>
        <update_rate>30</update_rate>
        <camera name="camera">
          <horizontal_fov>1.047</horizontal_fov>  <!-- 60 degrees -->
          <image>
            <width>640</width>
            <height>480</height>
            <format>R_FLOAT32</format>
          </image>
          <clip>
            <near>0.1</near>
            <far>10</far>
          </clip>
          <noise>
            <type>gaussian</type>
            <mean>0.0</mean>
            <stddev>0.05</stddev>
          </noise>
        </camera>
      </sensor>
    </link>

    <!-- Joints to connect wheels and camera to chassis -->
    <joint name="left_wheel_joint" type="continuous">
      <parent>chassis</parent>
      <child>left_wheel</child>
      <axis>
        <xyz>0 1 0</xyz>
      </axis>
    </joint>

    <joint name="right_wheel_joint" type="continuous">
      <parent>chassis</parent>
      <child>right_wheel</child>
      <axis>
        <xyz>0 1 0</xyz>
      </axis>
    </joint>

    <joint name="camera_joint" type="fixed">
      <parent>chassis</parent>
      <child>camera_link</child>
    </joint>
  </model>
</sdf>
```

## Step 3: Create a Test World

Create `camera_test_world.sdf` to test the robot with depth camera in a simple environment:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="camera_test_world">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- Ground plane -->
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
              <size>20 20</size>
            </plane>
          </geometry>
          <material>
            <diffuse>0.7 0.7 0.7 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Some objects for the depth camera to see -->
    <model name="box_obstacle">
      <pose>1 0 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 1.0</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 1.0</size>
            </box>
          </geometry>
          <material>
            <diffuse>0.8 0.2 0.2 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>2.0</mass>
          <inertia>
            <ixx>0.1042</ixx>
            <iyy>0.1042</iyy>
            <izz>0.0417</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <model name="cylinder_obstacle">
      <pose>-1 0.5 0.3 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <cylinder>
              <radius>0.2</radius>
              <length>0.6</length>
            </cylinder>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <cylinder>
              <radius>0.2</radius>
              <length>0.6</length>
            </cylinder>
          </geometry>
          <material>
            <diffuse>0.2 0.8 0.2 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.0167</ixx>
            <iyy>0.0167</iyy>
            <izz>0.02</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <model name="sphere_obstacle">
      <pose>-1 -0.5 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <sphere>
              <radius>0.2</radius>
            </sphere>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <sphere>
              <radius>0.2</radius>
            </sphere>
          </geometry>
          <material>
            <diffuse>0.2 0.2 0.8 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>0.5</mass>
          <inertia>
            <ixx>0.004</ixx>
            <iyy>0.004</iyy>
            <izz>0.004</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Include the robot with depth camera -->
    <include>
      <uri>model://robot_with_camera.sdf</uri>
      <pose>0 0 0.2 0 0 0</pose>
    </include>
  </world>
</sdf>
```

## Step 4: Launch the Simulation

Save all files and launch the simulation:

```bash
gz sim -r camera_test_world.sdf
```

## Step 5: Observe Depth Camera Data

In the Gazebo interface:
1. Use the visualization tools to see the camera's field of view
2. Move the robot around using the GUI or by applying forces
3. Observe how the depth camera captures the scene
4. Check the depth data output in the Gazebo terminal or via ROS topics

## Step 6: Modify Camera Parameters

Try modifying the depth camera parameters to see how they affect performance:

### Change Resolution
```xml
<image>
  <width>1280</width>  <!-- Higher resolution -->
  <height>720</height>
  <format>R_FLOAT32</format>
</image>
```

### Change Field of View
```xml
<camera name="camera">
  <horizontal_fov>1.5708</horizontal_fov>  <!-- 90 degrees, wider FOV -->
  <image>
    <width>640</width>
    <height>480</height>
    <format>R_FLOAT32</format>
  </image>
  <clip>
    <near>0.05</near>  <!-- Closer near clipping -->
    <far>15</far>      <!-- Further far clipping -->
  </clip>
</camera>
```

### Change Update Rate
```xml
<update_rate>60</update_rate>  <!-- Higher update rate -->
```

## Step 7: Add Multiple Cameras

You can add multiple cameras to the same robot:

```xml
<!-- Front-facing camera -->
<link name="front_camera">
  <pose>0.25 0 0.15 0 0 0</pose>  <!-- Position at front -->
  <sensor name="front_camera" type="depth">
    <!-- Camera configuration -->
  </sensor>
</link>

<!-- Upward-facing camera -->
<link name="upward_camera">
  <pose>0 0 0.2 0 0 1.5708</pose>  <!-- Position on top with 90° pitch -->
  <sensor name="upward_camera" type="depth">
    <!-- Camera configuration -->
  </sensor>
</link>
```

## Step 8: Performance Considerations

When configuring depth cameras, consider these performance factors:

- **Resolution**: Higher resolution = better detail but slower processing
- **Update rate**: Higher rate = more data but higher CPU usage
- **Range**: Longer range requires more computation
- **Number of cameras**: More cameras = more data but higher CPU usage
- **Noise modeling**: More realistic but computationally expensive

## Step 9: Troubleshooting

Common issues and solutions:

1. **No camera data**: Check if the camera is properly attached and powered
2. **Black images**: Verify camera clipping distances and orientation
3. **Performance issues**: Reduce resolution or update rate
4. **Inaccurate depth**: Check noise parameters and calibration
5. **Missing point clouds**: Verify camera info and coordinate systems

## Step 10: Advanced Configuration

For advanced depth camera configurations, you can add:

```xml
<sensor name="advanced_camera" type="depth">
  <always_on>true</always_on>
  <update_rate>30</update_rate>
  <camera name="camera">
    <horizontal_fov>1.047</horizontal_fov>  <!-- 60 degrees -->
    <image>
      <width>1920</width>  <!-- Full HD -->
      <height>1080</height>
      <format>R_FLOAT32</format>
    </image>
    <clip>
      <near>0.05</near>
      <far>20</far>
    </clip>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.02</stddev>
    </noise>
  </camera>
  <plugin name="camera_plugin" filename="libDepthCameraPlugin.so">
    <baseline>0.1</baseline>
    <focal_length>500</focal_length>
  </plugin>
</sensor>
```

## Step 11: Point Cloud Generation

Depth cameras can generate point clouds. The point cloud is derived from the depth image using the camera's intrinsic parameters:

```
X = (u - cx) * depth / fx
Y = (v - cy) * depth / fy
Z = depth
```

Where:
- (u, v) are pixel coordinates
- (cx, cy) are principal point coordinates
- (fx, fy) are focal lengths
- depth is the distance from the camera

## Step 12: Practical Applications

Depth cameras can be used for:
- **Object detection and recognition**
- **3D reconstruction**
- **Navigation and obstacle avoidance**
- **Human-robot interaction**
- **Augmented reality applications**

## Summary

In this tutorial, you learned how to:
- Add a depth camera to a robot model
- Configure camera parameters for different applications
- Test camera performance in a simulated environment
- Understand the trade-offs between performance and quality
- Troubleshoot common camera configuration issues

This hands-on experience will help you integrate depth cameras into your own robot designs for perception, navigation, and interaction applications.