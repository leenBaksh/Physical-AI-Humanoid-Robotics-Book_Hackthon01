---
sidebar_position: 5
---

# URDF Analysis Tools

This section covers tools and techniques for analyzing and working with URDF files to understand robot kinematic structures.

## Command Line Tools

### 1. check_urdf

The `check_urdf` tool validates URDF files and displays the kinematic tree structure:

```bash
# Check a URDF file
check_urdf /path/to/robot.urdf

# Output includes:
# - Robot name
# - Number of links and joints
# - Kinematic tree structure
# - Joint information
```

Example output:
```
robot name is: my_robot
---------- Successfully Parsed XML ---------------
root Link: base_link has 1 child(ren)
    child(1):  link1
        child(1):  link2
            child(1):  end_effector
```

### 2. xacro

XACRO is a macro language that makes URDF files more readable and maintainable:

```bash
# Convert XACRO to URDF
xacro input_file.xacro -o output_file.urdf

# Or directly use with ROS 2
ros2 run xacro xacro input_file.xacro > output_file.urdf
```

## Visualization Tools

### 1. RViz

RViz is ROS 2's visualization tool for viewing robot models:

1. Launch RViz:
   ```bash
   ros2 run rviz2 rviz2
   ```

2. Add a RobotModel display:
   - Click "Add" in the Displays panel
   - Select "RobotModel" under "By display type"
   - Set the "Robot Description" parameter to your robot description topic

### 2. Gazebo / Ignition

Simulation environments that can load and visualize URDF files:

```bash
# Launch Gazebo with a URDF
ros2 launch gazebo_ros gazebo.launch.py

# Spawn your robot
ros2 run gazebo_ros spawn_entity.py -file /path/to/robot.urdf -entity my_robot
```

## Programming Tools

### 1. Python URDF Parser

The `urdf_parser_py` package provides Python utilities for parsing URDF files:

```bash
pip install urdf-parser-py
```

Example usage:
```python
import urdf_parser_py.urdf as urdf

# Parse URDF from file
robot = urdf.Robot.from_xml_file('/path/to/robot.urdf')

# Access robot properties
print(f"Robot name: {robot.name}")
print(f"Number of links: {len(robot.links)}")
print(f"Number of joints: {len(robot.joints)}")

# Access individual links and joints
for link in robot.links:
    print(f"Link: {link.name}")
    if link.visual:
        print(f"  Visual: {link.visual.geometry.type}")

for joint in robot.joints:
    print(f"Joint: {joint.name} ({joint.type})")
    print(f"  Parent: {joint.parent}")
    print(f"  Child: {joint.child}")
```

### 2. Robot State Publisher

The robot_state_publisher package broadcasts transforms for all joints:

```bash
# Launch robot state publisher
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:=$(cat robot.urdf)
```

## Custom Analysis Tools

### 1. Kinematic Analysis

Create custom scripts for kinematic analysis:

```python
#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import math

def analyze_urdf_kinematics(urdf_path):
    """Analyze the kinematic structure of a URDF file."""
    tree = ET.parse(urdf_path)
    root = tree.getroot()

    # Find all joints
    joints = root.findall('joint')

    # Count degrees of freedom
    dof = 0
    joint_types = {}

    for joint in joints:
        jtype = joint.get('type')
        if jtype not in joint_types:
            joint_types[jtype] = 0

        # Add DOF based on joint type
        if jtype in ['revolute', 'prismatic']:
            dof += 1
        elif jtype == 'continuous':
            dof += 1
        elif jtype == 'spherical':
            dof += 3
        elif jtype == 'planar':
            dof += 3

        joint_types[jtype] += 1

    print(f"Total DOF: {dof}")
    print("Joint types breakdown:")
    for jtype, count in joint_types.items():
        print(f"  {jtype}: {count}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kinematic_analysis.py <urdf_file>")
        sys.exit(1)

    analyze_urdf_kinematics(sys.argv[1])
```

### 2. URDF Validation Script

Create validation scripts to check URDF quality:

```python
#!/usr/bin/env python3
import xml.etree.ElementTree as ET

def validate_urdf(urdf_path):
    """Validate common URDF issues."""
    tree = ET.parse(urdf_path)
    root = tree.getroot()

    issues = []

    # Check for duplicate names
    link_names = set()
    joint_names = set()

    for link in root.findall('link'):
        name = link.get('name')
        if name in link_names:
            issues.append(f"Duplicate link name: {name}")
        link_names.add(name)

    for joint in root.findall('joint'):
        name = joint.get('name')
        if name in joint_names:
            issues.append(f"Duplicate joint name: {name}")
        joint_names.add(name)

    # Check joint parent/child links exist
    for joint in root.findall('joint'):
        parent = joint.find('parent').get('link')
        child = joint.find('child').get('link')

        if parent not in link_names:
            issues.append(f"Joint {joint.get('name')} references non-existent parent link: {parent}")
        if child not in link_names:
            issues.append(f"Joint {joint.get('name')} references non-existent child link: {child}")

    return issues

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python urdf_validator.py <urdf_file>")
        sys.exit(1)

    issues = validate_urdf(sys.argv[1])
    if issues:
        print("URDF validation issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("URDF validation passed!")
```

## MoveIt! Integration

MoveIt! is a motion planning framework that works with URDF files:

```bash
# Install MoveIt!
sudo apt install ros-humble-moveit
```

### Setting up MoveIt! for your robot:
1. Use the MoveIt! Setup Assistant
2. Load your URDF file
3. Configure planning groups (kinematic chains)
4. Generate configuration files

```bash
# Launch MoveIt! Setup Assistant
ros2 run moveit_setup_assistant moveit_setup_assistant
```

## Best Practices for URDF Analysis

### 1. Systematic Approach
- Always start with `check_urdf` to validate the file
- Identify the base link first
- Trace the kinematic tree from base to end-effectors
- Verify joint limits and types

### 2. Documentation
- Comment your URDF files to explain complex structures
- Include kinematic diagrams
- Document coordinate frame conventions

### 3. Validation
- Check that all links have proper inertial properties for simulation
- Ensure visual and collision geometries are defined appropriately
- Verify that joint limits are realistic

### 4. Testing
- Use visualization tools to confirm the model looks correct
- Test kinematic solvers with simple configurations
- Validate that inverse kinematics solutions are achievable

## Troubleshooting Common Issues

### 1. Floating Base Issues
- Ensure there's exactly one base link with no parent
- Check that all other links are connected through joints

### 2. Joint Limit Problems
- Verify joint limits are within reasonable ranges
- Check that joint types match intended motion

### 3. Simulation Issues
- Ensure all links have proper inertial properties
- Verify collision geometries are defined for all links

These tools and techniques will help you effectively analyze and work with URDF files to understand robot kinematic structures for control and planning applications.