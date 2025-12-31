---
sidebar_position: 6
title: "Nav2 for Bipedal Navigation - Setup and Execution"
---

# Nav2 for Bipedal Navigation - Setup and Execution

## Introduction

In this chapter, we'll explore configuring Navigation2 (Nav2) for bipedal robots. Unlike traditional wheeled robots, bipedal robots have unique locomotion characteristics that require specialized navigation approaches. We'll learn how to set up Nav2 for a humanoid robot model, configure costmaps appropriate for bipedal locomotion, and execute navigation goals in simulation.

Bipedal navigation presents unique challenges including balance constraints, step planning, and the need to consider terrain suitable for walking rather than driving. This chapter builds on the perception capabilities learned in previous chapters to create a complete navigation system for humanoid robots.

## Prerequisites

Before starting this tutorial, ensure you have:

1. Completed Chapter 1: Isaac Sim & Synthetic Data
2. Completed Chapter 2: Isaac ROS & Visual SLAM
3. ROS 2 Humble Hawksbill installed
4. Navigation2 (Nav2) packages installed
5. Isaac Sim with a configured scene
6. Basic understanding of robot navigation concepts

## Installing and Setting Up Nav2

### Prerequisites Check

First, verify that your ROS 2 environment is properly set up:

```bash
# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Check available navigation packages
ros2 pkg list | grep -i nav
```

### Installing Navigation2

Install the Navigation2 packages:

```bash
# Update package lists
sudo apt update

# Install Navigation2
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup
sudo apt install ros-humble-nav2-common
sudo apt install ros-humble-nav2-costmap-2d
sudo apt install ros-humble-nav2-planners
sudo apt install ros-humble-nav2-behaviors
sudo apt install ros-humble-nav2-lifecycle-manager
sudo apt install ros-humble-nav2-msgs
sudo apt install ros-humble-nav2-utilities
```

### Additional Dependencies

Install additional packages that may be needed for bipedal navigation:

```bash
# Install robot state publisher and other utilities
sudo apt install ros-humble-robot-state-publisher
sudo apt install ros-humble-joint-state-publisher
sudo apt install ros-humble-xacro
sudo apt install ros-humble-urdf
```

### Verify Installation

Check if the packages were installed correctly:

```bash
# List Navigation2 packages
ros2 pkg list | grep -i nav2

# Check specific Nav2 packages
ros2 pkg list | grep nav2_msgs
ros2 pkg list | grep nav2_bringup
```

## Configuring Bipedal Robot Model

### Creating a Bipedal Robot URDF

For bipedal navigation, you need a proper URDF model. Here's a simplified example:

```xml
<?xml version="1.0"?>
<robot name="bipedal_robot">
  <!-- Base Link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.8"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.3 0.8"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Torso -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.6"/>
      </geometry>
      <material name="red">
        <color rgba="1 0 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="base_torso_joint" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.5"/>
  </joint>

  <!-- Left Leg -->
  <link name="left_thigh">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.4"/>
      </geometry>
      <material name="green">
        <color rgba="0 1 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="left_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_thigh"/>
    <origin xyz="-0.15 0 -0.3"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
  </joint>

  <link name="left_shin">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.4"/>
      </geometry>
    </visual>
  </link>

  <joint name="left_knee_joint" type="revolute">
    <parent link="left_thigh"/>
    <child link="left_shin"/>
    <origin xyz="0 0 -0.2"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="1.57" effort="100" velocity="1.0"/>
  </joint>

  <link name="left_foot">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
    </visual>
  </link>

  <joint name="left_ankle_joint" type="revolute">
    <parent link="left_shin"/>
    <child link="left_foot"/>
    <origin xyz="0 0 -0.2"/>
    <axis xyz="0 0 1"/>
    <limit lower="-0.5" upper="0.5" effort="100" velocity="1.0"/>
  </joint>

  <!-- Right Leg (similar to left leg) -->
  <link name="right_thigh">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.4"/>
      </geometry>
      <material name="green">
        <color rgba="0 1 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="right_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_thigh"/>
    <origin xyz="0.15 0 -0.3"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
  </joint>

  <link name="right_shin">
    <visual>
      <geometry>
        <box size="0.1 0.1 0.4"/>
      </geometry>
    </visual>
  </link>

  <joint name="right_knee_joint" type="revolute">
    <parent link="right_thigh"/>
    <child link="right_shin"/>
    <origin xyz="0 0 -0.2"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="1.57" effort="100" velocity="1.0"/>
  </joint>

  <link name="right_foot">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
    </visual>
  </link>

  <joint name="right_ankle_joint" type="revolute">
    <parent link="right_shin"/>
    <child link="right_foot"/>
    <origin xyz="0 0 -0.2"/>
    <axis xyz="0 0 1"/>
    <limit lower="-0.5" upper="0.5" effort="100" velocity="1.0"/>
  </joint>

  <!-- Base footprint for navigation -->
  <link name="base_footprint">
    <visual>
      <origin xyz="0 0 0.01"/>
      <geometry>
        <cylinder radius="0.3" length="0.02"/>
      </geometry>
      <material name="transparent">
        <color rgba="0 0 0 0.1"/>
      </material>
    </visual>
  </link>

  <joint name="base_footprint_joint" type="fixed">
    <parent link="base_link"/>
    <child link="base_footprint"/>
    <origin xyz="0 0 -0.4"/>
  </joint>
</robot>
```

### Loading the Robot Model in Isaac Sim

To use the bipedal robot in Isaac Sim:

1. Save the URDF to a file (e.g., `bipedal_robot.urdf`)
2. Import the URDF into Isaac Sim:
   - In Isaac Sim, go to File → Import → URDF
   - Select your URDF file
   - Configure import settings as needed

3. Alternatively, create the robot directly in Isaac Sim using primitives and save as USD

## Creating a Simple Simulation World

### Setting Up the Environment

Create a simple world suitable for bipedal navigation:

1. In Isaac Sim, create a ground plane:
   - Right-click → Create → Mesh → Plane
   - Scale appropriately (e.g., 20x20 units)

2. Add obstacles that are appropriate for bipedal navigation:
   - Small steps (bipedal robots can navigate small steps)
   - Avoid obstacles too high to step over
   - Ensure walkable paths are wide enough

3. Add navigation goals and landmarks:
   - Mark specific locations as potential navigation goals
   - Add visual landmarks to help with localization

### Configuring Physics for Bipedal Simulation

For realistic bipedal simulation:

1. Set appropriate friction coefficients for feet
2. Configure collision properties appropriately
3. Consider adding a simple walking controller (beyond the scope of this tutorial)

## Configuring Costmaps for Bipedal Navigation

### Understanding Costmap Differences for Bipedal Robots

Bipedal robots have different navigation requirements than wheeled robots:

- **Step Height**: Bipedal robots can step over small obstacles
- **Foot Placement**: Need to consider where feet can be placed
- **Balance**: Need to maintain center of mass within support polygon
- **Terrain**: Some terrain may be traversable for bipeds but not wheeled robots

### Creating Costmap Configuration Files

Create a costmap configuration file for bipedal navigation (`bipedal_costmap_params.yaml`):

```yaml
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_footprint"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 100.0
    laser_min_range: -1.0
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05
    scan_topic: scan

amcl_map_client:
  ros__parameters:
    use_sim_time: True

amcl_rclcpp_node:
  ros__parameters:
    use_sim_time: True

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: base_link
    odom_topic: /odom
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    navigate_through_poses: False
    navigate_to_pose: True
    action_server_result_timeout: 900.0
    # Specify the path where the BT XML files are located
    default_nav_through_poses_bt_xml: "package://nav2_bt_navigator/bt_xml_v0/nav_through_poses_w_replanning_and_recovery.xml"
    default_nav_to_pose_bt_xml: "package://nav2_bt_navigator/bt_xml_v0/nav_to_pose_w_replanning_and_recovery.xml"
    plugin_lib_names:
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_compute_path_through_poses_action_bt_node
    - nav2_smooth_path_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_spin_action_bt_node
    - nav2_wait_action_bt_node
    - nav2_assisted_teleop_action_bt_node
    - nav2_back_up_action_bt_node
    - nav2_drive_on_heading_bt_node
    - nav2_clear_costmap_service_bt_node
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
    - nav2_goal_updated_condition_bt_node
    - nav2_globally_updated_goal_condition_bt_node
    - nav2_is_path_valid_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_service_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node
    - nav2_truncate_path_local_action_bt_node
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_time_expired_condition_bt_node
    - nav2_path_expiring_timer_condition
    - nav2_distance_traveled_condition_bt_node
    - nav2_single_trigger_bt_node
    - nav2_is_battery_low_condition_bt_node
    - nav2_navigate_through_poses_action_bt_node
    - nav2_navigate_to_pose_action_bt_node
    - nav2_remove_passed_goals_action_bt_node
    - nav2_planner_selector_bt_node
    - nav2_controller_selector_bt_node
    - nav2_goal_checker_selector_bt_node
    - nav2_controller_cancel_bt_node
    - nav2_path_longer_on_approach_bt_node
    - nav2_wait_cancel_bt_node
    - nav2_spin_cancel_bt_node
    - nav2_back_up_cancel_bt_node
    - nav2_assisted_teleop_cancel_bt_node
    - nav2_drive_on_heading_cancel_bt_node

bt_navigator_rclcpp_node:
  ros__parameters:
    use_sim_time: True

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    failure_tolerance: 0.3
    progress_checker_plugin: "progress_checker"
    goal_checker_plugins: ["general_goal_checker"] # "precise_goal_checker"
    controller_plugins: ["FollowPath"]

    # Progress checker parameters
    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0

    # Goal checker parameters
    general_goal_checker:
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
      stateful: True

    # Controller parameters
    FollowPath:
      plugin: "nav2_rotation_shim_controller::RotationShimController"
      # Inner controller to use
      inner_controller: "FollowPathLocal"
      # How long to hold the final orientation for
      hold_final_orientation_duration: 0.0
      # How long to wait for transform to become available
      transform_tolerance: 0.1
      # How close to get to the goal before switching to final orientation
      distance_to_goal_threshold: 0.5
      # How fast to rotate when adjusting to final orientation
      angular_dist_to_travel_proportional_saturation: 1.0
      # Maximum angular velocity for final orientation
      max_angular_velocity: 1.0
      # Minimum angular velocity for final orientation
      min_angular_velocity: 0.05
      # Inner controller plugin
      FollowPathLocal:
        plugin: "nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController"
        desired_linear_vel: 0.5
        max_linear_accel: 2.5
        max_linear_decel: 2.5
        lookahead_dist: 0.6
        min_lookahead_dist: 0.3
        max_lookahead_dist: 0.9
        lookahead_time: 1.5
        rotate_to_heading_angular_vel: 1.8
        transform_tolerance: 0.1
        use_velocity_scaled_lookahead_dist: false
        min_approach_linear_velocity: 0.05
        approach_velocity_scaling_dist: 0.6
        use_approach_vel_scaling: true
        max_allowed_time_to_collision_up_to_carrot: 1.0
        use_regulated_linear_velocity_scaling: true
        use_cost_regulated_linear_velocity_scaling: true
        regulated_linear_scaling_min_radius: 0.9
        regulated_linear_scaling_min_speed: 0.25
        use_rotate_to_heading: true
        rotate_to_heading_min_angle: 0.785
        max_angular_accel: 3.2
        goal_dist_tol: 0.25

controller_server_rclcpp_node:
  ros__parameters:
    use_sim_time: True

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: odom
      robot_base_frame: base_link
      use_sim_time: True
      rolling_window: true
      width: 6
      height: 6
      resolution: 0.05  # Higher resolution for bipedal navigation
      robot_radius: 0.3  # Radius of the robot footprint
      plugins: ["voxel_layer", "inflation_layer"]
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        enabled: True
        publish_voxel_map: True
        origin_z: 0.0
        z_resolution: 0.2
        z_voxels: 8
        max_obstacle_height: 2.0
        mark_threshold: 0
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0

  local_costmap_client:
    ros__parameters:
      use_sim_time: True

  local_costmap_rclcpp_node:
    ros__parameters:
      use_sim_time: True

global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: map
      robot_base_frame: base_link
      use_sim_time: True
      robot_radius: 0.3  # Adjust for bipedal robot
      resolution: 0.05  # Higher resolution for more precise navigation
      track_unknown_space: false
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: True
        observation_sources: scan
        scan:
          topic: /scan
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
  global_costmap_client:
    ros__parameters:
      use_sim_time: True

  global_costmap_rclcpp_node:
    ros__parameters:
      use_sim_time: True

map_server:
  ros__parameters:
    use_sim_time: True
    yaml_filename: "turtlebot3_world.yaml"

map_saver:
  ros__parameters:
    use_sim_time: True
    save_map_timeout: 5.0
    free_thresh_default: 0.25
    occupied_thresh_default: 0.65

planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    use_sim_time: True
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner::NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true

planner_server_rclcpp_node:
  ros__parameters:
    use_sim_time: True

smoother_server:
  ros__parameters:
    use_sim_time: True
    smoother_plugins: ["simple_smoother"]
    simple_smoother:
      plugin: "nav2_smoother::SimpleSmoother"
      tolerance: 1.0e-10
      max_its: 1000
      w_smooth: 0.3
      w_data: 0.2

behavior_server:
  ros__parameters:
    costmap_topic: local_costmap/costmap_raw
    footprint_topic: local_costmap/published_footprint
    cycle_frequency: 10.0
    behavior_plugins: ["spin", "backup", "wait", "assisted_teleop"]
    spin:
      plugin: "nav2_behaviors::Spin"
      spin_dist: 1.57
    backup:
      plugin: "nav2_behaviors::BackUp"
      backup_dist: 0.15
      backup_speed: 0.025
    wait:
      plugin: "nav2_behaviors::Wait"
      wait_duration: 1.0
    assisted_teleop:
      plugin: "nav2_behaviors::AssistedTeleop"
      min_vel_theta: 0.4

lifecycle_manager:
  ros__parameters:
    use_sim_time: True
    autostart: True
    node_names: ["map_server", "planner_server", "controller_server", "behavior_server"]
```

### Bipedal-Specific Costmap Adjustments

For bipedal navigation, make these key adjustments to the costmap configuration:

1. **Resolution**: Use higher resolution (0.05m) for more precise foot placement
2. **Robot Radius**: Adjust based on the robot's foot spacing and balance requirements
3. **Inflation Radius**: Consider the robot's balance and step capabilities
4. **Obstacle Handling**: Account for the fact that bipedal robots can step over small obstacles

## Sending Navigation Goals via ROS 2

### Launching Nav2 for Bipedal Robot

To launch Nav2 with your bipedal robot configuration:

```bash
# Terminal 1: Launch your robot simulation in Isaac Sim
# (Launch Isaac Sim with your bipedal robot and environment)

# Terminal 2: Launch Nav2 with bipedal configuration
source /opt/ros/humble/setup.bash
ros2 launch nav2_bringup navigation_launch.py \
  use_sim_time:=True \
  params_file:=/path/to/your/bipedal_costmap_params.yaml
```

### Using Navigation Actions

To send navigation goals to your bipedal robot:

```bash
# Using the navigation action interface
ros2 action send_goal /navigate_to_pose \
  nav2_msgs/action/NavigateToPose \
  "{
    pose: {
      header: {frame_id: 'map'},
      pose: {
        position: {x: 1.0, y: 1.0, z: 0.0},
        orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
      }
    }
  }"
```

### Creating a Navigation Script

Here's a Python script to send navigation goals:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
import time

class BipedalNavigator(Node):
    def __init__(self):
        super().__init__('bipedal_navigator')
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self, x, y, theta):
        # Wait for the action server to be available
        self._action_client.wait_for_server()

        # Create the goal message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = 0.0

        # Convert theta (in radians) to quaternion
        from math import sin, cos
        goal_msg.pose.pose.orientation.x = 0.0
        goal_msg.pose.pose.orientation.y = 0.0
        goal_msg.pose.pose.orientation.z = sin(theta / 2.0)
        goal_msg.pose.pose.orientation.w = cos(theta / 2.0)

        # Send the goal
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback}')

def main():
    rclpy.init()

    navigator = BipedalNavigator()

    # Send a navigation goal (example coordinates)
    # Adjust these coordinates based on your simulation environment
    navigator.send_goal(2.0, 2.0, 0.0)  # x=2.0, y=2.0, theta=0.0

    rclpy.spin(navigator)

if __name__ == '__main__':
    main()
```

### Testing Navigation in Simulation

To test navigation:

1. Ensure Isaac Sim is running with your bipedal robot in the environment
2. Launch Nav2 with your bipedal configuration
3. Send navigation goals using the command line or script
4. Monitor the robot's behavior in both Isaac Sim and RViz

## Integration with Isaac Sim and VSLAM

### Combining Navigation with Perception

To create a complete autonomous system, combine navigation with the VSLAM capabilities learned in Chapter 2:

1. Use VSLAM for localization (instead of or in addition to AMCL)
2. Integrate perception data into costmaps
3. Use visual landmarks for navigation assistance

### Example Integration Script

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
import cv2
from cv_bridge import CvBridge

class IntegratedBipedalNavigator(Node):
    def __init__(self):
        super().__init__('integrated_bipedal_navigator')

        # Navigation components
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Perception components
        self.bridge = CvBridge()
        self.image_subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)

        self.latest_image = None

    def image_callback(self, msg):
        """Process incoming camera images"""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.latest_image = cv_image

            # Process image for navigation assistance
            # (e.g., detect obstacles, landmarks, etc.)
            self.process_navigation_image(cv_image)

        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')

    def process_navigation_image(self, image):
        """Process image for navigation assistance"""
        # Example: Simple obstacle detection
        # In a real system, you would use more sophisticated computer vision

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Simple thresholding to detect obstacles
        _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Process contours (simplified example)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Only consider large obstacles
                # Could send this information to costmap or adjust navigation
                self.get_logger().info(f'Detected obstacle with area: {area}')

    def send_navigation_goal(self, x, y, theta):
        """Send navigation goal with perception integration"""
        # Wait for the action server to be available
        self._action_client.wait_for_server()

        # Create the goal message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = 0.0

        # Convert theta to quaternion
        from math import sin, cos
        goal_msg.pose.pose.orientation.x = 0.0
        goal_msg.pose.pose.orientation.y = 0.0
        goal_msg.pose.pose.orientation.z = sin(theta / 2.0)
        goal_msg.pose.pose.orientation.w = cos(theta / 2.0)

        # Send the goal
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

def main():
    rclpy.init()

    navigator = IntegratedBipedalNavigator()

    # Send a navigation goal
    navigator.send_navigation_goal(3.0, 3.0, 0.0)

    rclpy.spin(navigator)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Troubleshooting Navigation Issues

### Common Bipedal Navigation Problems

1. **Robot Not Moving**:
   - Check if all required nodes are running
   - Verify costmap configuration
   - Ensure proper TF tree setup

2. **Path Planning Failures**:
   - Check if the goal is reachable
   - Verify map quality and resolution
   - Ensure costmap inflation parameters are appropriate

3. **Unstable Navigation**:
   - Check controller parameters
   - Verify robot velocity limits
   - Ensure proper obstacle detection

### Debugging Tools

Use these ROS 2 tools to debug navigation issues:

```bash
# Check node status
ros2 node list | grep -i nav

# Monitor topics
ros2 topic list | grep -i cmd_vel
ros2 topic list | grep -i costmap

# Check TF tree
ros2 run tf2_tools view_frames

# Echo navigation topics
ros2 topic echo /local_costmap/costmap
ros2 topic echo /global_costmap/costmap
```

## Performance Optimization

### Bipedal-Specific Optimizations

1. **Footstep Planning**: Consider implementing footstep planning for more realistic bipedal navigation
2. **Balance Constraints**: Integrate balance constraints into path planning
3. **Terrain Analysis**: Consider terrain traversability for bipedal locomotion

### Parameter Tuning

Fine-tune these parameters for better bipedal navigation performance:

- Controller velocity limits (accounting for bipedal walking speed)
- Costmap resolution (higher for precise foot placement)
- Inflation parameters (considering step height capabilities)
- Goal tolerance (accounting for balance requirements)

## Summary

In this chapter, you learned how to:
- Configure Navigation2 for bipedal robot models
- Set up costmaps appropriate for bipedal locomotion
- Create simple simulation worlds for navigation
- Send navigation goals via ROS 2
- Integrate navigation with perception systems
- Troubleshoot common navigation issues

## Next Steps

You've now completed all three chapters of Module 3, covering Isaac Sim synthetic data generation, Isaac ROS Visual SLAM, and Navigation2 for bipedal robots. These technologies form a complete perception and navigation pipeline for humanoid robots. Consider exploring more advanced topics such as:

- Footstep planning for complex terrain
- Dynamic obstacle avoidance for bipedal robots
- Integration with higher-level planning systems
- Real-world deployment considerations