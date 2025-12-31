---
sidebar_position: 2
---

# URDF Overview

## What is URDF?

URDF (Unified Robot Description Format) is an XML-based format used in ROS to describe robot models. It defines the physical and visual properties of a robot, including its links, joints, and other components.

## Key Components of URDF

### Links

Links represent the rigid parts of a robot. Each link has:

- **Visual**: How the link appears in simulation and visualization
- **Collision**: How the link interacts with other objects in collision detection
- **Inertial**: Physical properties like mass and moment of inertia

### Joints

Joints define the connections between links. Types of joints include:

- **Revolute**: Rotational joint with limited range
- **Continuous**: Rotational joint without limits
- **Prismatic**: Linear sliding joint with limited range
- **Fixed**: No movement between links
- **Floating**: 6 DOF (degrees of freedom)
- **Planar**: Motion on a plane

### Materials

Materials define the visual appearance of links, including color and texture properties.

## Basic URDF Structure

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- Define materials -->
  <material name="blue">
    <color rgba="0 0 0.8 1.0"/>
  </material>

  <!-- Define links -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
      <material name="blue"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Define joints -->
  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0 0.2 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.1"/>
      </geometry>
    </visual>
  </link>
</robot>
```

## URDF Tools

### Viewing URDF Models

You can visualize URDF models using RViz or the `check_urdf` command:

```bash
# Check URDF validity
check_urdf /path/to/robot.urdf

# View the model in RViz
ros2 run rviz2 rviz2
```

### Converting XACRO to URDF

XACRO is a macro language that makes URDF more readable:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="my_robot">
  <xacro:property name="wheel_radius" value="0.1"/>

  <link name="wheel">
    <visual>
      <geometry>
        <cylinder radius="${wheel_radius}" length="0.1"/>
      </geometry>
    </visual>
  </link>
</robot>
```

Convert XACRO to URDF:
```bash
xacro input_file.xacro -o output_file.urdf
```

## Best Practices

- Use XACRO for complex robots to avoid repetition
- Organize links and joints logically
- Use consistent naming conventions
- Include proper inertial properties for simulation
- Validate URDF files before use

## Common URDF Elements

### Geometry Types
- `<box>`: Box shape with size="x y z"
- `<cylinder>`: Cylinder with radius and length
- `<sphere>`: Sphere with radius
- `<mesh>`: Mesh file (STL, DAE, etc.)

### Joint Limits
For revolute and prismatic joints, specify:
- `lower`: Lower limit
- `upper`: Upper limit
- `effort`: Maximum effort
- `velocity`: Maximum velocity

In the next section, we'll explore kinematic structures in detail.