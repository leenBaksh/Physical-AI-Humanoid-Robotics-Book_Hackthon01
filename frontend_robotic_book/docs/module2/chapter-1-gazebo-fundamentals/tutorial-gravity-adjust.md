---
sidebar_position: 7
title: "Hands-On: Adjusting Gravity Parameters and Observing Effects"
---

# Hands-On: Adjusting Gravity Parameters and Observing Effects

In this tutorial, you'll experiment with different gravity settings and observe how they affect robot behavior in Gazebo. This will help you understand how gravity influences humanoid robot simulations.

## Prerequisites

- Understanding of basic SDF world structure
- Gazebo installed and running
- Basic understanding of physics concepts

## Step 1: Create a Test World

First, create a test world with multiple identical objects to compare behavior under different gravity conditions. Create `gravity_test.sdf`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="gravity_test">
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
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

    <!-- Robot model to test gravity effects -->
    <model name="test_robot">
      <pose>0 0 5 0 0 0</pose>
      <link name="body">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
          <material>
            <diffuse>1 0 0 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.0208</ixx>
            <iyy>0.0208</iyy>
            <izz>0.0208</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Additional test objects -->
    <model name="sphere_earth">
      <pose>-2 0 5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <sphere>
              <radius>0.1</radius>
            </sphere>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <sphere>
              <radius>0.1</radius>
            </sphere>
          </geometry>
          <material>
            <diffuse>0 1 0 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>0.1</mass>
          <inertia>
            <ixx>0.0002</ixx>
            <iyy>0.0002</iyy>
            <izz>0.0002</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <model name="sphere_moon">
      <pose>2 0 5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <sphere>
              <radius>0.1</radius>
            </sphere>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <sphere>
              <radius>0.1</radius>
            </sphere>
          </geometry>
          <material>
            <diffuse>0 0 1 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>0.1</mass>
          <inertia>
            <ixx>0.0002</ixx>
            <iyy>0.0002</iyy>
            <izz>0.0002</izz>
          </inertia>
        </inertial>
      </link>
    </model>
  </world>
</sdf>
```

## Step 2: Test Earth Gravity

Launch the simulation with standard Earth gravity:

```bash
gz sim -r gravity_test.sdf
```

Observe:
- How quickly objects fall
- The time it takes for objects to hit the ground
- The impact behavior when objects hit the ground

## Step 3: Create Moon Gravity World

Create `moon_gravity.sdf` with lunar gravity (about 1/6 of Earth's gravity):

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="moon_gravity">
    <physics type="ode">
      <gravity>0 0 -1.62</gravity> <!-- Moon gravity: ~1.62 m/s² -->
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
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

    <!-- Same test objects as before -->
    <model name="test_robot">
      <pose>0 0 5 0 0 0</pose>
      <link name="body">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
          <material>
            <diffuse>1 0 0 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.0208</ixx>
            <iyy>0.0208</iyy>
            <izz>0.0208</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <model name="sphere_moon">
      <pose>0 0 5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <sphere>
              <radius>0.1</radius>
            </sphere>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <sphere>
              <radius>0.1</radius>
            </sphere>
          </geometry>
          <material>
            <diffuse>0 0 1 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>0.1</mass>
          <inertia>
            <ixx>0.0002</ixx>
            <iyy>0.0002</iyy>
            <izz>0.0002</izz>
          </inertia>
        </inertial>
      </link>
    </model>
  </world>
</sdf>
```

Launch and observe the differences:

```bash
gz sim -r moon_gravity.sdf
```

## Step 4: Create Zero Gravity World

Create `zero_gravity.sdf` with no gravity:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="zero_gravity">
    <physics type="ode">
      <gravity>0 0 0</gravity>
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>

    <!-- No ground plane needed in zero gravity -->
    <!-- Objects will not fall -->

    <model name="floating_robot">
      <pose>0 0 0 0 0 0</pose>
      <link name="body">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
          <material>
            <diffuse>1 0 0 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.0208</ixx>
            <iyy>0.0208</iyy>
            <izz>0.0208</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <model name="floating_sphere">
      <pose>1 0 0 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <sphere>
              <radius>0.1</radius>
            </sphere>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <sphere>
              <radius>0.1</radius>
            </sphere>
          </geometry>
          <material>
            <diffuse>0 1 0 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>0.1</mass>
          <inertia>
            <ixx>0.0002</ixx>
            <iyy>0.0002</iyy>
            <izz>0.0002</izz>
          </inertia>
        </inertial>
      </link>
    </model>
  </world>
</sdf>
```

Launch and observe:

```bash
gz sim -r zero_gravity.sdf
```

## Step 5: Create Custom Gravity World

Create `custom_gravity.sdf` with a custom gravity vector:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="custom_gravity">
    <physics type="ode">
      <gravity>5 0 -5</gravity> <!-- Diagonal gravity -->
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>

    <!-- Ground plane at an angle to match diagonal gravity -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0.707 0 0.707</normal> <!-- 45-degree angle -->
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0.707 0 0.707</normal>
              <size>20 20</size>
            </plane>
          </geometry>
          <material>
            <diffuse>0.7 0.7 0.7 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Test objects -->
    <model name="diagonal_fall">
      <pose>0 0 5 0 0 0</pose>
      <link name="body">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.2 0.2 0.2</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.2 0.2 0.2</size>
            </box>
          </geometry>
          <material>
            <diffuse>1 1 0 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>0.1</mass>
          <inertia>
            <ixx>0.0001</ixx>
            <iyy>0.0001</iyy>
            <izz>0.0001</izz>
          </inertia>
        </inertial>
      </link>
    </model>
  </world>
</sdf>
```

## Step 6: Observations and Analysis

For each gravity setting, observe and record:

1. **Fall time**: How long it takes for objects to reach the ground
2. **Velocity**: How fast objects are moving when they impact
3. **Trajectory**: The path objects follow (especially for diagonal gravity)
4. **Impact behavior**: How objects behave when they hit surfaces
5. **Robot stability**: How gravity affects a robot's balance

## Step 7: Gravity and Humanoid Robots

Consider how different gravity values affect humanoid robots:

- **Walking gait**: How does reduced gravity affect walking patterns?
- **Balance**: How do robots maintain balance in different gravity?
- **Jumping**: How does increased gravity affect jumping ability?
- **Manipulation**: How do objects behave differently when handled?

## Step 8: Practical Exercise

Create your own world with a humanoid robot model and experiment with:

1. Different gravity magnitudes (0.1g, 0.5g, 2g, 5g)
2. Different gravity directions (horizontal, diagonal)
3. Time-varying gravity (using plugins - advanced)

## Troubleshooting Tips

- **Objects moving too fast/slow**: Check gravity values and time step settings
- **Simulation instability**: Reduce max_step_size or adjust physics parameters
- **Objects passing through each other**: Check collision geometries and physics settings

## Summary

In this tutorial, you learned how to:

- Create worlds with different gravity settings
- Observe the effects of gravity on robot behavior
- Understand how gravity affects humanoid robot simulations
- Analyze the relationship between gravity and robot dynamics
- Experiment with custom gravity vectors

This understanding is crucial for creating realistic humanoid robot simulations in various environments.