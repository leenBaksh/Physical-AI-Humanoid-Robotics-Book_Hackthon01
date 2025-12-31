---
sidebar_position: 4
title: "Collision Detection and Response"
---

# Collision Detection and Response

Collision detection is essential for realistic physics simulation. In this section, we'll explore how Gazebo handles collisions between objects and how to configure collision properties for humanoid robots.

## Understanding Collision Detection

Gazebo uses a multi-stage collision detection system:

1. **Broad Phase**: Quick elimination of non-colliding pairs using bounding boxes
2. **Narrow Phase**: Precise collision detection using geometric algorithms
3. **Contact Generation**: Computing contact points and forces

## Collision Properties

Collision properties are defined in the `<collision>` tag:

```xml
<collision name="collision">
  <geometry>
    <box>
      <size>1 1 1</size>
    </box>
  </geometry>
  <surface>
    <friction>
      <ode>
        <mu>1.0</mu>
        <mu2>1.0</mu2>
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

### Key Collision Parameters

- **mu/mu2**: Friction coefficients (static and dynamic)
- **restitution_coefficient**: Bounciness (0 = no bounce, 1 = perfectly elastic)
- **soft_cfm/soft_erp**: Constraint Force Mixing and Error Reduction Parameters
- **kp/kd**: Spring stiffness and damping coefficients

## Collision Detection for Humanoid Robots

For humanoid robots, collision detection is critical for:

- **Self-collision avoidance**: Preventing robot parts from intersecting
- **Environment interaction**: Detecting contact with objects and surfaces
- **Safety**: Ensuring robots don't damage themselves or surroundings
- **Realistic movement**: Proper contact handling during walking and manipulation

## Collision Meshes vs Visual Meshes

It's important to distinguish between collision and visual geometries:

```xml
<link name="link">
  <!-- Visual geometry (what you see) -->
  <visual name="visual">
    <geometry>
      <mesh>
        <uri>model://humanoid/meshes/complex_shape.dae</uri>
      </mesh>
    </geometry>
  </visual>

  <!-- Collision geometry (physics interaction) -->
  <collision name="collision">
    <geometry>
      <!-- Often simplified for performance -->
      <box>
        <size>0.1 0.1 0.3</size>
      </box>
    </geometry>
  </collision>
</link>
```

## Practical Example: Collision Configuration

```xml
<model name="humanoid_robot">
  <link name="torso">
    <collision name="torso_collision">
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
        <contact>
          <ode>
            <soft_erp>0.2</soft_erp>
            <soft_cfm>0.0</soft_cfm>
          </ode>
        </contact>
      </surface>
    </collision>
  </link>
</model>
```

## Hands-On Exercise

1. Create a world with multiple objects that can collide
2. Configure different collision properties for each object
3. Observe how different friction and restitution values affect collisions
4. Add a simple humanoid model and test collision detection with the environment
5. Experiment with different collision geometries (box, sphere, cylinder)