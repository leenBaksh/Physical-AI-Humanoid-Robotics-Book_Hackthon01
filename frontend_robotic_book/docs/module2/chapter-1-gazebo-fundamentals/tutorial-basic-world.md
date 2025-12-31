---
sidebar_position: 5
title: "Hands-On: Creating a Basic Gazebo World"
---

# Hands-On: Creating a Basic Gazebo World

In this tutorial, you'll create your first Gazebo world with physics simulation enabled. This will give you hands-on experience with the fundamental concepts of Gazebo simulation.

## Prerequisites

- Gazebo installed (Harmonic or Fortress)
- Basic understanding of XML structure
- Terminal/command prompt access

## Step 1: Create the World File

Create a new file called `my_first_world.sdf` with the following content:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="my_first_world">
    <!-- Physics engine configuration -->
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
              <size>10 10</size>
            </plane>
          </geometry>
          <material>
            <diffuse>0.7 0.7 0.7 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- A simple box to demonstrate physics -->
    <model name="falling_box">
      <pose>0 0 5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 1 1</size>
            </box>
          </geometry>
          <material>
            <diffuse>1 0 0 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.1667</ixx>
            <iyy>0.1667</iyy>
            <izz>0.1667</izz>
          </inertia>
        </inertial>
      </link>
    </model>
  </world>
</sdf>
```

## Step 2: Launch the World

Save the file and launch it in Gazebo:

```bash
gz sim -r my_first_world.sdf
```

Or if you're using the older gazebo command:

```bash
gazebo my_first_world.sdf
```

## Step 3: Observe the Simulation

You should see:

1. A gray ground plane
2. A red box positioned 5 meters above the ground
3. The box falling due to gravity

## Step 4: Experiment with Different Settings

Try modifying the world file to:

1. Change the box's starting height (modify the Y value in `<pose>0 0 5 0 0 0</pose>`)
2. Change the box's size (modify `<size>1 1 1</size>`)
3. Change the gravity value (modify `<gravity>0 0 -9.8</gravity>`)

For example, to change gravity to zero:

```xml
<physics type="ode">
  <gravity>0 0 0</gravity>
</physics>
```

## Step 5: Add More Objects

Add a sphere to your world by including this model in your world file:

```xml
<!-- A sphere that will also fall -->
<model name="falling_sphere">
  <pose>2 0 5 0 0 0</pose>
  <link name="link">
    <collision name="collision">
      <geometry>
        <sphere>
          <radius>0.5</radius>
        </sphere>
      </geometry>
    </collision>
    <visual name="visual">
      <geometry>
        <sphere>
          <radius>0.5</radius>
        </sphere>
      </geometry>
      <material>
        <diffuse>0 1 0 1</diffuse>
      </material>
    </visual>
    <inertial>
      <mass>0.5</mass>
      <inertia>
        <ixx>0.0417</ixx>
        <iyy>0.0417</iyy>
        <izz>0.0417</izz>
      </inertia>
    </inertial>
  </link>
</model>
```

## Troubleshooting Tips

- **Model not showing**: Check that the pose values position the model within the camera view
- **Physics not working**: Ensure the physics engine is properly configured
- **File not loading**: Verify the XML syntax and SDF version

## Summary

In this tutorial, you learned how to:

- Create a basic SDF world file
- Configure physics properties
- Add static and dynamic models
- Launch and observe a simulation
- Modify parameters to experiment with different behaviors

This foundation will help you create more complex simulations in future chapters.