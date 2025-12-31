---
sidebar_position: 2
title: "Physics Simulation in Gazebo"
---

# Physics Simulation in Gazebo

Physics simulation is a core component of realistic robot simulation. In this section, we'll explore how Gazebo handles physics and how to configure it for humanoid robotics applications.

## Understanding Physics Engines

Gazebo supports several physics engines including:

- **ODE (Open Dynamics Engine)**: The default engine, suitable for most applications
- **Bullet**: Good for real-time simulation with stable contact handling
- **DART**: Advanced engine with support for soft-body dynamics

## Basic Physics Configuration

A basic physics configuration in Gazebo looks like this:

```xml
<physics type="ode">
  <gravity>0 0 -9.8</gravity>
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1</real_time_factor>
  <real_time_update_rate>1000</real_time_update_rate>
</physics>
```

### Key Physics Parameters

- **gravity**: Sets the gravitational acceleration vector (x, y, z)
- **max_step_size**: Maximum simulation time step size
- **real_time_factor**: Target simulation speed relative to real time
- **real_time_update_rate**: Update rate in Hz

## Creating a Physics-Enabled World

Let's create a simple world with physics enabled:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="physics_world">
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
        </visual>
      </link>
    </model>

    <!-- A simple box that will be affected by gravity -->
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

## Hands-On Exercise

1. Create a new world file called `physics_world.sdf` with the above configuration
2. Launch Gazebo with this world: `gz sim -r physics_world.sdf`
3. Observe how the box falls due to gravity
4. Try changing the gravity vector to see how it affects the simulation