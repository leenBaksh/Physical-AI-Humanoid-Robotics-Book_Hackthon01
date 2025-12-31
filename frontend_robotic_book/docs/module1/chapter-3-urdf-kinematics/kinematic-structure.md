---
sidebar_position: 3
---

# Kinematic Structure

## Understanding Robot Kinematics

Robot kinematics is the study of motion in robotic systems. It deals with the relationship between joint positions and the position and orientation of the robot's end-effector. Understanding kinematics is crucial for robot control and motion planning.

## Types of Kinematics

### Forward Kinematics

Forward kinematics calculates the position and orientation of the end-effector given the joint angles. It answers the question: "Where is the end-effector given these joint angles?"

### Inverse Kinematics

Inverse kinematics calculates the required joint angles to achieve a desired end-effector position and orientation. It answers the question: "What joint angles are needed to place the end-effector here?"

## Kinematic Chains

A kinematic chain is a series of rigid bodies (links) connected by joints. In robotics, we typically have:

- **Open chains**: Single path from base to end-effector (like a robotic arm)
- **Closed chains**: Multiple paths between base and end-effector (like parallel robots)

## Degrees of Freedom (DOF)

The degrees of freedom of a robot determine how many independent movements it can perform. For a spatial mechanism:
- Each joint contributes up to 6 DOF
- The total DOF depends on the joint types and their configuration
- A robot needs at least 6 DOF to position and orient its end-effector arbitrarily in 3D space

## Joint Types and Their DOF

- **Revolute joint**: 1 DOF (rotation about the joint axis)
- **Prismatic joint**: 1 DOF (translation along the joint axis)
- **Cylindrical joint**: 2 DOF (rotation + translation)
- **Spherical joint**: 3 DOF (3 rotations)
- **Planar joint**: 3 DOF (2 translations + 1 rotation)
- **Fixed joint**: 0 DOF (no movement)

## Kinematic Equations

### Transformation Matrices

Each joint can be represented by a transformation matrix that describes how coordinates in the child frame relate to coordinates in the parent frame:

```
T = [R  p]
    [0  1]
```

Where R is a 3x3 rotation matrix and p is a 3x1 position vector.

### Denavit-Hartenberg Parameters

The Denavit-Hartenberg (DH) convention is a systematic method for defining coordinate frames on a robot's links:

- **a (link length)**: Distance along the common normal
- **α (link twist)**: Angle between axes
- **d (link offset)**: Distance along the previous z-axis
- **θ (joint angle)**: Angle about the previous z-axis

## URDF and Kinematics

URDF files define the kinematic structure of a robot through the joint connections between links. Each joint specifies:

- Parent and child links
- Joint type
- Joint limits
- Joint axis
- Origin transformation

## Kinematic Analysis with URDF

To analyze the kinematic structure of a robot from its URDF:

1. **Parse the URDF**: Extract links and joints
2. **Build kinematic tree**: Create parent-child relationships
3. **Calculate DOF**: Sum DOF of all joints
4. **Identify chains**: Find paths from base to end-effectors
5. **Analyze workspace**: Determine reachable space

## Kinematic Solvers

ROS provides several kinematic solvers:

### KDL (Kinematics and Dynamics Library)
- Provides forward and inverse kinematics
- Available through `python_orocos_kdl` package
- Good for basic kinematic calculations

### MoveIt!
- Advanced motion planning framework
- Includes inverse kinematics solvers
- Supports collision detection and path planning

## Example: Simple 2-DOF Arm

Consider a simple 2-DOF planar arm:

```xml
<robot name="simple_arm">
  <link name="base_link"/>

  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>

  <link name="link1">
    <visual>
      <geometry>
        <cylinder length="0.5" radius="0.05"/>
      </geometry>
      <origin xyz="0 0 0.25" rpy="0 0 0"/>
    </visual>
  </link>

  <joint name="joint2" type="revolute">
    <parent link="link1"/>
    <child link="link2"/>
    <origin xyz="0 0 0.5" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>

  <link name="link2">
    <visual>
      <geometry>
        <cylinder length="0.5" radius="0.05"/>
      </geometry>
      <origin xyz="0 0 0.25" rpy="0 0 0"/>
    </visual>
  </link>
</robot>
```

For this arm:
- Total DOF: 2 (both joints are revolute)
- Forward kinematics: Calculate end-effector position from joint angles
- Workspace: Circular area reachable by the end-effector

## Humanoid Robot Considerations

Humanoid robots have complex kinematic structures with multiple chains:

- **Leg chains**: For locomotion and balance
- **Arm chains**: For manipulation
- **Head chain**: For vision and interaction
- **Torso**: Connecting element between chains

Each chain may have its own end-effector and kinematic considerations.

In the next section, we'll look at how to interpret URDF files to understand these kinematic structures.