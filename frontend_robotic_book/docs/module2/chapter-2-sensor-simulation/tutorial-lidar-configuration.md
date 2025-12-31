---
sidebar_position: 14
title: "Hands-On: Configuring LiDAR Sensor on Robot Model"
---

# Hands-On: Configuring LiDAR Sensor on Robot Model

In this tutorial, you'll learn how to configure a LiDAR sensor on a robot model in Gazebo. This will give you hands-on experience with integrating sensors into robot models and understanding their configuration parameters.

## Prerequisites

- Understanding of SDF structure
- Basic knowledge of robot models
- Gazebo installed and running

## Step 1: Create a Base Robot Model

First, let's create a simple robot model to which we'll add the LiDAR sensor. Create `robot_with_lidar.sdf`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="robot_with_lidar">
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

## Step 2: Add LiDAR Sensor to the Robot

Now, let's add a LiDAR sensor to the robot model. We'll position it on top of the chassis:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="robot_with_lidar">
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

    <!-- LiDAR sensor -->
    <link name="lidar_link">
      <pose>0 0 0.25 0 0 0</pose>  <!-- Position on top of chassis -->
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.03</radius>
            <length>0.06</length>
          </cylinder>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.03</radius>
            <length>0.06</length>
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
      <sensor name="lidar_sensor" type="ray">
        <always_on>true</always_on>
        <update_rate>10</update_rate>
        <ray>
          <scan>
            <horizontal>
              <samples>720</samples>
              <resolution>1</resolution>
              <min_angle>-1.570796</min_angle>  <!-- -90 degrees -->
              <max_angle>1.570796</max_angle>   <!-- 90 degrees -->
            </horizontal>
          </scan>
          <range>
            <min>0.1</min>
            <max>10.0</max>
            <resolution>0.01</resolution>
          </range>
        </ray>
      </sensor>
    </link>

    <!-- Joints to connect wheels and LiDAR to chassis -->
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

    <joint name="lidar_joint" type="fixed">
      <parent>chassis</parent>
      <child>lidar_link</child>
    </joint>
  </model>
</sdf>
```

## Step 3: Create a Test World

Create `lidar_test_world.sdf` to test the robot with LiDAR in a simple environment:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="lidar_test_world">
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

    <!-- Some obstacles for the LiDAR to detect -->
    <model name="obstacle_1">
      <pose>2 0 0.5 0 0 0</pose>
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

    <model name="obstacle_2">
      <pose>-1 1 0.3 0 0 0</pose>
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

    <!-- Include the robot with LiDAR -->
    <include>
      <uri>model://robot_with_lidar.sdf</uri>
      <pose>0 0 0.2 0 0 0</pose>
    </include>
  </world>
</sdf>
```

## Step 4: Launch the Simulation

Save all files and launch the simulation:

```bash
gz sim -r lidar_test_world.sdf
```

## Step 5: Observe LiDAR Data

In the Gazebo interface:
1. Use the visualization tools to see the LiDAR rays
2. Move the robot around using the GUI or by applying forces
3. Observe how the LiDAR detects obstacles
4. Check the sensor output in the Gazebo terminal or via ROS topics

## Step 6: Modify LiDAR Parameters

Try modifying the LiDAR parameters to see how they affect performance:

### Change Angular Resolution
```xml
<ray>
  <scan>
    <horizontal>
      <samples>360</samples>  <!-- Lower resolution -->
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
```

### Change Range
```xml
<range>
  <min>0.05</min>  <!-- Closer minimum range -->
  <max>15.0</max>   <!-- Further maximum range -->
  <resolution>0.005</resolution>  <!-- Higher resolution -->
</range>
```

### Change Update Rate
```xml
<update_rate>20</update_rate>  <!-- Higher update rate -->
```

## Step 7: Add Multiple LiDAR Sensors

You can add multiple LiDAR sensors to the same robot:

```xml
<!-- Front-facing LiDAR -->
<link name="front_lidar">
  <pose>0.2 0 0.25 0 0 0</pose>  <!-- Position at front -->
  <sensor name="front_lidar_sensor" type="ray">
    <!-- LiDAR configuration -->
  </sensor>
</link>

<!-- Rear-facing LiDAR -->
<link name="rear_lidar">
  <pose>-0.2 0 0.25 0 0 3.14159</pose>  <!-- Position at rear with 180° rotation -->
  <sensor name="rear_lidar_sensor" type="ray">
    <!-- LiDAR configuration -->
  </sensor>
</link>
```

## Step 8: Performance Considerations

When configuring LiDAR sensors, consider these performance factors:

- **Sample count**: Higher samples = better resolution but slower simulation
- **Update rate**: Higher rate = more data but higher CPU usage
- **Range**: Longer range requires more computation
- **Number of sensors**: More sensors = more data but higher CPU usage

## Step 9: Troubleshooting

Common issues and solutions:

1. **No LiDAR data**: Check if the sensor is properly attached and powered
2. **Inaccurate measurements**: Verify range settings and environment
3. **Performance issues**: Reduce sample count or update rate
4. **Ray intersection problems**: Check collision geometries

## Step 10: Advanced Configuration

For advanced LiDAR configurations, you can add:

```xml
<sensor name="advanced_lidar" type="ray">
  <always_on>true</always_on>
  <update_rate>10</update_rate>
  <ray>
    <scan>
      <horizontal>
        <samples>1081</samples>
        <resolution>1</resolution>
        <min_angle>-2.35619</min_angle>  <!-- -135 degrees -->
        <max_angle>2.35619</max_angle>   <!-- 135 degrees -->
      </horizontal>
      <vertical>
        <samples>16</samples>  <!-- For 3D LiDAR -->
        <resolution>1</resolution>
        <min_angle>-0.2618</min_angle>  <!-- -15 degrees -->
        <max_angle>0.2618</max_angle>   <!-- 15 degrees -->
      </vertical>
    </scan>
    <range>
      <min>0.05</min>
      <max>30.0</max>
      <resolution>0.001</resolution>
    </range>
  </ray>
</sensor>
```

## Summary

In this tutorial, you learned how to:
- Add a LiDAR sensor to a robot model
- Configure LiDAR parameters for different applications
- Test LiDAR performance in a simulated environment
- Understand the trade-offs between performance and accuracy
- Troubleshoot common LiDAR configuration issues

This hands-on experience will help you integrate LiDAR sensors into your own robot designs for navigation, mapping, and obstacle detection applications.