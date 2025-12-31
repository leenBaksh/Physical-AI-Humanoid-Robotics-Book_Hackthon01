---
sidebar_position: 8
title: "Collision Detection Examples with Humanoid Robot"
---

# Collision Detection Examples with Humanoid Robot

In this tutorial, you'll explore collision detection in Gazebo with a focus on humanoid robots. You'll learn how to configure collision properties and observe their effects on robot behavior.

## Prerequisites

- Understanding of SDF structure
- Basic knowledge of physics simulation
- Gazebo installed and running

## Step 1: Understanding Collision Properties

Collision properties in Gazebo determine how objects interact when they come into contact. Key properties include:

- **Geometry**: Shape of the collision object
- **Friction**: How much resistance to sliding motion
- **Bounce**: How much objects rebound after collision
- **Contact parameters**: How contact forces are calculated

## Step 2: Create a Collision Test World

Create `collision_test.sdf` to test different collision properties:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="collision_test">
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
          <surface>
            <friction>
              <ode>
                <mu>0.8</mu>
                <mu2>0.8</mu2>
              </ode>
            </friction>
          </surface>
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

    <!-- Object with high friction -->
    <model name="high_friction_box">
      <pose>-2 0 2 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>2.0</mu>
                <mu2>2.0</mu2>
              </ode>
            </friction>
          </surface>
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

    <!-- Object with low friction -->
    <model name="low_friction_box">
      <pose>0 0 2 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>0.1</mu>
                <mu2>0.1</mu2>
              </ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
          <material>
            <diffuse>0 1 0 1</diffuse>
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

    <!-- Object with high bounce -->
    <model name="bouncy_sphere">
      <pose>2 0 2 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <sphere>
              <radius>0.25</radius>
            </sphere>
          </geometry>
          <surface>
            <bounce>
              <restitution_coefficient>0.9</restitution_coefficient>
              <threshold>100000</threshold>
            </bounce>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <sphere>
              <radius>0.25</radius>
            </sphere>
          </geometry>
          <material>
            <diffuse>0 0 1 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>0.5</mass>
          <inertia>
            <ixx>0.0083</ixx>
            <iyy>0.0083</iyy>
            <izz>0.0083</izz>
          </inertia>
        </inertial>
      </link>
    </model>
  </world>
</sdf>
```

## Step 3: Launch and Observe

Launch the simulation:

```bash
gz sim -r collision_test.sdf
```

Observe how:
- The red box (high friction) slides less after impact
- The green box (low friction) slides more after impact
- The blue sphere (high bounce) bounces significantly

## Step 4: Create a Humanoid Robot with Collision Properties

Create `humanoid_collision.sdf` with a simplified humanoid model that has different collision properties:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_humanoid">
    <!-- Torso -->
    <link name="torso">
      <pose>0 0 1.0 0 0 0</pose>
      <collision name="collision">
        <geometry>
          <box>
            <size>0.3 0.2 0.5</size>
          </box>
        </geometry>
        <surface>
          <friction>
            <ode>
              <mu>0.8</mu>
              <mu2>0.8</mu2>
            </ode>
          </friction>
        </surface>
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

    <!-- Head -->
    <link name="head">
      <pose>0 0 1.4 0 0 0</pose>
      <collision name="collision">
        <geometry>
          <sphere>
            <radius>0.15</radius>
          </sphere>
        </geometry>
        <surface>
          <friction>
            <ode>
              <mu>0.5</mu>
              <mu2>0.5</mu2>
            </ode>
          </friction>
        </surface>
      </collision>
      <visual name="visual">
        <geometry>
          <sphere>
            <radius>0.15</radius>
          </sphere>
        </geometry>
        <material>
          <diffuse>0.8 0.8 0.8 1</diffuse>
        </material>
      </visual>
      <inertial>
        <mass>1.0</mass>
        <inertia>
          <ixx>0.0045</ixx>
          <iyy>0.0045</iyy>
          <izz>0.0045</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Left arm -->
    <link name="left_arm">
      <pose>0.25 0 1.0 0 0 0</pose>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.4</length>
          </cylinder>
        </geometry>
        <surface>
          <friction>
            <ode>
              <mu>0.6</mu>
              <mu2>0.6</mu2>
            </ode>
          </friction>
        </surface>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.4</length>
          </cylinder>
        </geometry>
        <material>
          <diffuse>0.8 0.2 0.2 1</diffuse>
        </material>
      </visual>
      <inertial>
        <mass>0.5</mass>
        <inertia>
          <ixx>0.0034</ixx>
          <iyy>0.0034</iyy>
          <izz>0.0006</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Right arm -->
    <link name="right_arm">
      <pose>-0.25 0 1.0 0 0 0</pose>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.4</length>
          </cylinder>
        </geometry>
        <surface>
          <friction>
            <ode>
              <mu>0.6</mu>
              <mu2>0.6</mu2>
            </ode>
          </friction>
        </surface>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.4</length>
          </cylinder>
        </geometry>
        <material>
          <diffuse>0.8 0.2 0.2 1</diffuse>
        </material>
      </visual>
      <inertial>
        <mass>0.5</mass>
        <inertia>
          <ixx>0.0034</ixx>
          <iyy>0.0034</iyy>
          <izz>0.0006</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Left leg -->
    <link name="left_leg">
      <pose>0.1 0 0.5 0 0 0</pose>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.06</radius>
            <length>0.6</length>
          </cylinder>
        </geometry>
        <surface>
          <friction>
            <ode>
              <mu>0.9</mu>
              <mu2>0.9</mu2>
            </ode>
          </friction>
        </surface>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.06</radius>
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
          <ixx>0.0126</ixx>
          <iyy>0.0126</iyy>
          <izz>0.0018</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Right leg -->
    <link name="right_leg">
      <pose>-0.1 0 0.5 0 0 0</pose>
      <collision name="collision">
        <geometry>
          <cylinder>
            <radius>0.06</radius>
            <length>0.6</length>
          </cylinder>
        </geometry>
        <surface>
          <friction>
            <ode>
              <mu>0.9</mu>
              <mu2>0.9</mu2>
            </ode>
          </friction>
        </surface>
      </collision>
      <visual name="visual">
        <geometry>
          <cylinder>
            <radius>0.06</radius>
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
          <ixx>0.0126</ixx>
          <iyy>0.0126</iyy>
          <izz>0.0018</izz>
        </inertia>
      </inertial>
    </link>

    <!-- Joints to connect parts -->
    <joint name="torso_head" type="fixed">
      <parent>torso</parent>
      <child>head</child>
    </joint>

    <joint name="torso_left_arm" type="revolute">
      <parent>torso</parent>
      <child>left_arm</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
        </limit>
      </axis>
    </joint>

    <joint name="torso_right_arm" type="revolute">
      <parent>torso</parent>
      <child>right_arm</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
        </limit>
      </axis>
    </joint>

    <joint name="torso_left_leg" type="fixed">
      <parent>torso</parent>
      <child>left_leg</child>
    </joint>

    <joint name="torso_right_leg" type="fixed">
      <parent>torso</parent>
      <child>right_leg</child>
    </joint>
  </model>
</sdf>
```

## Step 5: Create a World with the Humanoid Robot

Create `humanoid_world.sdf`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="humanoid_world">
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
          <surface>
            <friction>
              <ode>
                <mu>0.8</mu>
                <mu2>0.8</mu2>
              </ode>
            </friction>
          </surface>
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

    <!-- Add obstacles to test collision detection -->
    <model name="obstacle_1">
      <pose>1 0 0.5 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 1.0</size>
            </box>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>0.8</mu>
              </ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 1.0</size>
            </box>
          </geometry>
          <material>
            <diffuse>0.5 0.3 0.1 1</diffuse>
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

    <!-- Include the humanoid robot -->
    <include>
      <uri>model://simple_humanoid.sdf</uri>
      <pose>0 0 2 0 0 0</pose>
    </include>
  </world>
</sdf>
```

## Step 6: Launch and Test Humanoid Collision

Launch the simulation:

```bash
gz sim -r humanoid_world.sdf
```

Observe how:
- The humanoid robot falls and lands on the ground
- The robot's legs (with higher friction) grip the ground better
- The robot interacts with obstacles based on its collision properties

## Step 7: Self-Collision Considerations

For humanoid robots, self-collision detection is important. Add self-collision properties by modifying the model to include self-collision awareness:

```xml
<!-- Add to each link to enable self-collision -->
<self_collide>true</self_collide>
```

## Step 8: Advanced Collision Properties

You can also experiment with more advanced collision properties:

```xml
<collision name="collision">
  <geometry>
    <box>
      <size>0.5 0.5 0.5</size>
    </box>
  </geometry>
  <surface>
    <friction>
      <ode>
        <mu>1.0</mu>
        <mu2>1.0</mu2>
        <fdir1>1 0 0</fdir1>
      </ode>
    </friction>
    <bounce>
      <restitution_coefficient>0.1</restitution_coefficient>
      <threshold>100000</threshold>
    </bounce>
    <contact>
      <ode>
        <soft_cfm>0</soft_cfm>
        <soft_erp>0.2</soft_erp>
        <kp>1e+13</kp>
        <kd>1</kd>
        <max_vel>0.01</max_vel>
        <min_depth>0</min_depth>
      </ode>
    </contact>
  </surface>
</collision>
```

## Step 9: Practical Exercise

Create your own humanoid robot with different collision properties for different body parts:

1. **Feet**: High friction for good grip
2. **Hands**: Moderate friction for manipulation
3. **Torso**: Lower friction to reduce sliding
4. **Head**: Low bounce to prevent excessive movement

## Troubleshooting Tips

- **Robot parts passing through each other**: Check joint constraints and collision geometries
- **Unstable simulation**: Adjust physics parameters (time step, ERP, CFM)
- **Robot sliding too much**: Increase friction coefficients
- **Robot bouncing too much**: Reduce restitution coefficients

## Summary

In this tutorial, you learned how to:

- Configure collision properties for different robot parts
- Understand the impact of friction on robot behavior
- Implement collision detection for humanoid robots
- Create worlds that test collision behavior
- Balance different collision properties for realistic simulation

These skills are essential for creating realistic humanoid robot simulations in Gazebo.