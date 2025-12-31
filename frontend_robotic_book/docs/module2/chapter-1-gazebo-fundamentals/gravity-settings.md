---
sidebar_position: 3
title: "Gravity Settings and Configuration"
---

# Gravity Settings and Configuration

Gravity is a fundamental force in physics simulation that affects all objects in the simulation environment. Understanding how to configure and manipulate gravity settings is crucial for creating realistic humanoid robot simulations.

## Default Gravity Settings

By default, Gazebo uses Earth's gravity of 9.8 m/s² in the negative Z direction:

```xml
<gravity>0 0 -9.8</gravity>
```

This means objects will fall downward at the rate of 9.8 meters per second squared.

## Customizing Gravity

You can customize gravity in several ways:

### Changing Gravity Magnitude

To simulate different planetary environments:

```xml
<!-- Moon gravity (~1.62 m/s²) -->
<gravity>0 0 -1.62</gravity>

<!-- Mars gravity (~3.71 m/s²) -->
<gravity>0 0 -3.71</gravity>

<!-- Zero gravity (space simulation) -->
<gravity>0 0 0</gravity>
```

### Changing Gravity Direction

You can also change the direction of gravity:

```xml
<!-- Horizontal gravity -->
<gravity>9.8 0 0</gravity>

<!-- Diagonal gravity -->
<gravity>0 5 -5</gravity>
```

## Gravity and Humanoid Robots

For humanoid robots, proper gravity settings are crucial for:

- **Walking simulations**: Gravity affects balance and gait patterns
- **Falling behaviors**: Understanding how robots fall helps with safety
- **Manipulation tasks**: Gravity affects how objects are handled
- **Stability analysis**: How robots maintain balance under gravitational forces

## Practical Example: Adjusting Gravity for Humanoid Simulation

```xml
<world name="humanoid_gravity_test">
  <physics type="ode">
    <!-- Standard Earth gravity -->
    <gravity>0 0 -9.8</gravity>
    <max_step_size>0.001</max_step_size>
    <real_time_factor>1</real_time_factor>
    <real_time_update_rate>1000</real_time_update_rate>
  </physics>

  <!-- Humanoid robot model would go here -->
  <!-- The robot's behavior will be affected by the gravity settings -->
</world>
```

## Hands-On Exercise

1. Create a world file with different gravity settings
2. Add a simple humanoid model or box to the simulation
3. Observe how changing gravity affects the model's behavior
4. Try zero gravity and see how the model behaves
5. Document the differences in behavior between different gravity settings