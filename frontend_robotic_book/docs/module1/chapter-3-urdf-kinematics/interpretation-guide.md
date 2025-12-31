---
sidebar_position: 4
---

# URDF Interpretation Guide

## Understanding URDF Structure

This guide provides a systematic approach to interpreting URDF files for humanoid robots and understanding their kinematic structure.

## Step-by-Step Interpretation

### 1. Identify the Robot Base

The base link is typically the root of the kinematic tree. Look for links that are not children of any joint:

```xml
<link name="base_link"/>
<!-- This link is not a child of any joint, so it's likely the base -->
```

### 2. Map the Kinematic Tree

Trace all joints to understand parent-child relationships:

```xml
<joint name="base_to_torso" type="fixed">
  <parent link="base_link"/>
  <child link="torso_link"/>
</joint>
```

Build a tree structure starting from the base:
- base_link
  - torso_link
    - head_link
    - left_arm_link_1
      - left_arm_link_2
        - ...
    - right_arm_link_1
      - right_arm_link_2
        - ...
    - left_leg_link_1
      - left_leg_link_2
        - ...
    - right_leg_link_1
      - right_leg_link_2
        - ...

### 3. Identify End Effectors

End effectors are links that don't have children. These are typically:
- Hands (for manipulation)
- Feet (for locomotion)
- Head (for vision)

### 4. Analyze Joint Types and Limits

For each joint, note:
- Joint type (revolute, prismatic, fixed, etc.)
- Joint limits (for revolute and prismatic joints)
- Joint axis (direction of movement)
- Range of motion

### 5. Calculate Degrees of Freedom

Sum the DOF of all joints:
- Revolute/Prismatic: 1 DOF each
- Spherical: 3 DOF
- Planar: 3 DOF
- Fixed: 0 DOF

## Practical Interpretation Example

Let's interpret a simplified humanoid URDF:

```xml
<robot name="simple_humanoid">
  <!-- Base/Root -->
  <link name="base_link">
    <inertial>
      <mass value="10"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="1" ixy="0" ixz="0" iyy="1" iyz="0" izz="1"/>
    </inertial>
  </link>

  <!-- Torso -->
  <joint name="base_to_torso" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.5"/>
  </joint>

  <link name="torso">
    <visual>
      <geometry>
        <box size="0.2 0.2 0.5"/>
      </geometry>
    </visual>
  </link>

  <!-- Left Leg -->
  <joint name="torso_to_left_hip" type="revolute">
    <parent link="torso"/>
    <child link="left_hip"/>
    <origin xyz="-0.1 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <link name="left_hip">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.1"/>
      </geometry>
    </visual>
  </link>

  <!-- Additional joints and links would continue... -->
</robot>
```

**Interpretation:**
- **Base**: base_link
- **Structure**: base → torso → left leg chain
- **DOF**: 1 (from the revolute hip joint)
- **End effector**: Not shown in this snippet
- **Kinematic chain**: Single chain from torso to leg

## Tools for URDF Interpretation

### 1. Command Line Tools

```bash
# Check URDF validity and show tree structure
check_urdf /path/to/robot.urdf

# Show joint information
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:=$(cat robot.urdf)
```

### 2. Visualization

```bash
# Visualize in RViz
ros2 run rviz2 rviz2

# Or use standalone viewer
ros2 run xacro xacro file.urdf.xacro | ros2 run rviz2 rviz2
```

### 3. Programmatic Access

```python
import xml.etree.ElementTree as ET

def parse_urdf(urdf_path):
    tree = ET.parse(urdf_path)
    root = tree.getroot()

    # Extract links
    links = root.findall('link')
    print(f"Found {len(links)} links")

    # Extract joints
    joints = root.findall('joint')
    print(f"Found {len(joints)} joints")

    # Map parent-child relationships
    for joint in joints:
        parent = joint.find('parent').get('link')
        child = joint.find('child').get('link')
        joint_type = joint.get('type')
        print(f"Joint: {parent} -> {child} ({joint_type})")
```

## Common Humanoid URDF Patterns

### Bipedal Structure
- Base: Usually pelvis or a fixed frame
- Torso: Trunk of the robot
- Legs: Chains from hip to foot
- Arms: Chains from shoulder to hand
- Head: Usually on top of torso

### Joint Configuration
- **Hip joints**: Often 3-6 DOF for full leg movement
- **Knee joints**: Usually 1 DOF (revolute)
- **Ankle joints**: Often 2-3 DOF
- **Shoulder joints**: Often 3 DOF (spherical or 3 revolute)
- **Elbow joints**: Usually 1 DOF (revolute)
- **Wrist joints**: Often 2-3 DOF

## Troubleshooting URDF Issues

### Common Problems
1. **Disconnected links**: Links not connected by joints
2. **Multiple bases**: More than one root link
3. **Inconsistent naming**: Parent/child link names don't match
4. **Missing elements**: Required inertial or visual elements

### Validation Steps
1. Use `check_urdf` to validate syntax
2. Verify all links are connected in a tree structure
3. Check that there's exactly one base link
4. Ensure all joint parent/child names match link names

## Advanced Interpretation

### Understanding Physical Properties

- **Inertial properties**: Affect simulation accuracy
- **Visual properties**: Determine appearance in simulation
- **Collision properties**: Determine collision behavior

### Kinematic Analysis

For complex robots, consider:
- **Redundant chains**: Multiple ways to reach the same pose
- **Singularities**: Configurations where the robot loses DOF
- **Workspace**: Volume reachable by end-effectors
- **Dexterity**: How well the robot can orient its end-effector

## Best Practices for URDF Interpretation

1. **Start with the base**: Always identify the root link first
2. **Follow the tree**: Trace parent-child relationships systematically
3. **Note joint limits**: These determine the robot's capabilities
4. **Visualize**: Use tools to verify your interpretation
5. **Check documentation**: Many URDF files include comments about structure

This guide should help you systematically interpret any humanoid robot URDF file and understand its kinematic structure for control and planning applications.