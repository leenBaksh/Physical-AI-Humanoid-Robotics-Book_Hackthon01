---
sidebar_position: 6
title: "Hands-On: Adding a Robot Model to Physics Environment"
---

# Hands-On: Adding a Robot Model to Physics Environment

In this tutorial, you'll learn how to create and add a simple robot model to a physics-enabled Gazebo environment. This will demonstrate how robots interact with physical forces in simulation.

## Prerequisites

- Basic understanding of SDF structure
- Understanding of physics simulation concepts
- Gazebo installed and running

## Step 1: Understanding Robot Model Structure

A robot model in SDF consists of:

- **Links**: Rigid bodies that make up the robot
- **Joints**: Connections between links that define how they can move
- **Inertial properties**: Mass, center of mass, and inertia for physics simulation
- **Visual properties**: How the robot appears in the simulation
- **Collision properties**: How the robot interacts with other objects

## Step 2: Create a Simple Robot Model

Let's create a simple wheeled robot model. Create a file called `simple_wheeled_robot.sdf`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_wheeled_robot">
    <!-- Main body/chassis -->
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
        <material>
          <diffuse>0.8 0.8 0.2 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
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

    <!-- Left wheel -->
    <link name="left_wheel">
      <pose>-0.3 0.3 0 0 1.5707 0</pose>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.1</length>
          </cylinder>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.1</length>
          </cylinder>
        </geometry>
        <material>
          <diffuse>0.3 0.3 0.3 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <inertial>
        <mass>0.2</mass>
        <inertia>
          <ixx>0.001</ixx>
          <iyy>0.001</iyy>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Right wheel -->
    <link name="right_wheel">
      <pose>-0.3 -0.3 0 0 1.5707 0</pose>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.1</length>
          </cylinder>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.1</radius>
            <length>0.1</length>
          </cylinder>
        </geometry>
        <material>
          <diffuse>0.3 0.3 0.3 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>
      <inertial>
        <mass>0.2</mass>
        <inertia>
          <ixx>0.001</ixx>
          <iyy>0.001</iyy>
          <izz>0.001</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Joint to connect left wheel to chassis -->
    <joint name="left_wheel_joint" type="continuous">
      <parent>chassis</parent>
      <child>left_wheel</child>
      <axis>
        <xyz>0 1 0</xyz>
      </axis>
    </joint>

    <!-- Joint to connect right wheel to chassis -->
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

## Step 3: Create a World with the Robot

Now, create a world file that includes both the ground plane and your robot. Create `robot_world.sdf`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="robot_world">
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
            <specular>0.01 0.01 0.01 1</specular>
          </material>
        </visual>
      </link>
    </model>

    <!-- Include the robot model -->
    <include>
      <uri>model://simple_wheeled_robot.sdf</uri>
      <pose>0 0 0.5 0 0 0</pose>
    </include>
  </world>
</sdf>
```

## Step 4: Launch the Simulation

Launch the simulation with your robot:

```bash
gz sim -r robot_world.sdf
```

You should see your robot positioned above the ground, and it should fall due to gravity until it lands on the ground plane.

## Step 5: Understanding the Physics Interactions

Observe how:

1. The robot falls due to gravity
2. The wheels and chassis come to rest on the ground plane
3. The robot maintains its structural integrity through the joints
4. Collision detection prevents the robot from falling through the ground

## Step 6: Modify Robot Properties

Try modifying the robot's properties to see how it affects the simulation:

1. **Change mass**: Modify the mass values in the `<inertial>` tags to see how it affects how the robot responds to forces
2. **Change friction**: Add surface friction properties to see how it affects movement
3. **Change dimensions**: Modify the size of the chassis or wheels

For example, to add friction to the wheels:

```xml
<link name="left_wheel">
  <!-- ... other content ... -->
  <surface>
    <friction>
      <ode>
        <mu>1.0</mu>
        <mu2>1.0</mu2>
      </ode>
    </friction>
  </surface>
</link>
```

## Step 7: Creating a Humanoid Robot (Advanced)

For a more humanoid robot, you can create a simplified model with a torso, head, arms, and legs:

```xml
<!-- Simplified humanoid torso -->
<link name="torso">
  <pose>0 0 1.0 0 0 0</pose>
  <collision name="collision">
    <geometry>
      <box>
        <size>0.3 0.2 0.5</size>
      </box>
    </geometry>
  </collision>
  <visual name="visual">
    <geometry>
      <box>
        <size>0.3 0.2 0.5</size>
      </box>
    </geometry>
    <material>
      <diffuse>0.2 0.2 0.8 1</diffuse>
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
```

## Troubleshooting Tips

- **Robot falls through the ground**: Check that collision geometries are properly defined
- **Robot explodes or behaves erratically**: Check that inertial values are reasonable
- **Robot doesn't respond to gravity**: Ensure the physics engine is configured correctly
- **Joints behave strangely**: Check joint limits and axes of rotation

## Summary

In this tutorial, you learned how to:

- Create a multi-link robot model with proper inertial properties
- Include a robot model in a physics-enabled world
- Understand how physics properties affect robot behavior
- Modify robot properties to change simulation behavior
- Structure a robot model with appropriate collision and visual properties

This foundation will be essential for more complex humanoid robot simulations in later chapters.