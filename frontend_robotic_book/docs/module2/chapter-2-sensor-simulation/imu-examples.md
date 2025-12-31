---
sidebar_position: 19
title: "IMU Examples: Realistic Acceleration and Orientation Data"
---

# IMU Examples: Realistic Acceleration and Orientation Data

This section provides practical examples of how IMU sensors produce realistic acceleration and orientation data in Gazebo simulation. You'll learn how to interpret IMU data and understand its applications in robotics.

## Understanding IMU Data Output

IMU sensors output three types of measurements:
- **Linear acceleration**: Acceleration along x, y, z axes (m/s²)
- **Angular velocity**: Rotation rate around x, y, z axes (rad/s)
- **Orientation**: Current orientation (Euler angles or quaternions)

### Basic IMU Data Structure

```
Linear Acceleration: [ax, ay, az]  // in m/s²
Angular Velocity:    [wx, wy, wz] // in rad/s
Orientation:         [qx, qy, qz, qw] or [roll, pitch, yaw] // quaternion or Euler angles
```

## Example 1: Stationary Robot (Resting State)

When a robot is stationary and level:

```
Linear Acceleration: [0.01, -0.02, 9.81]  // Noise around expected values
Angular Velocity:    [0.001, -0.002, 0.003] // Near zero with noise
Orientation:         [0.001, -0.002, 0.003, 0.999] // Level (quaternion)
```

- **Linear acceleration**: z-axis shows ~9.81 m/s² due to gravity, x/y near zero
- **Angular velocity**: All axes near zero (no rotation)
- **Orientation**: Level with respect to gravity

## Example 2: Robot Accelerating Forward

When a robot accelerates forward at 1 m/s²:

```
Linear Acceleration: [1.02, -0.01, 9.80]  // Forward acceleration + gravity
Angular Velocity:    [0.002, -0.001, 0.001] // No rotation
Orientation:         [0.002, -0.001, 0.001, 0.999] // Still level
```

- **Linear acceleration**: x-axis shows forward acceleration (1.0 m/s²) plus noise
- **Angular velocity**: Still near zero
- **Orientation**: Unchanged if no rotation occurs

## Example 3: Robot Rotating Clockwise

When a robot rotates clockwise around the z-axis at 0.5 rad/s:

```
Linear Acceleration: [0.02, -0.03, 9.82]  // Centripetal acceleration effects
Angular Velocity:    [0.001, -0.002, 0.501] // Rotation around z-axis
Orientation:         [0.001, -0.002, 0.247, 0.969] // Rotated ~28.5°
```

- **Linear acceleration**: May show slight centripetal effects
- **Angular velocity**: Significant value on z-axis (0.5 rad/s)
- **Orientation**: Changes to reflect rotation

## Example 4: Robot on Inclined Surface

When a robot is on a 15-degree incline (pitched forward):

```
Linear Acceleration: [-2.54, 0.05, 9.47]  // Gravity projected on tilted axes
Angular Velocity:    [0.003, 0.001, -0.002] // No rotation
Orientation:         [0.003, -0.131, 0.001, 0.991] // Pitched ~15°
```

- **Linear acceleration**: Gravity components distributed across x and z axes
- **Angular velocity**: Near zero (no rotation)
- **Orientation**: Shows ~15-degree pitch

## Example 5: Humanoid Robot Walking Gait

During a walking gait cycle (simplified):

```
// Start of step (foot down)
Linear Acceleration: [2.1, 0.3, 9.7]    // Forward acceleration
Angular Velocity:    [0.2, -0.1, 0.3]    // Balance adjustments
Orientation:         [0.1, -0.05, 0.02, 0.99] // Forward lean

// Mid-step (centered)
Linear Acceleration: [0.5, -0.1, 9.8]    // Balanced
Angular Velocity:    [-0.1, 0.0, 0.1]    // Minimal rotation
Orientation:         [0.05, -0.02, 0.01, 0.99] // Upright

// End of step (preparing for next step)
Linear Acceleration: [-1.2, 0.2, 9.9]    // Decelerating
Angular Velocity:    [-0.3, 0.1, -0.2]   // Balance adjustments
Orientation:         [-0.05, 0.03, -0.01, 0.99] // Slight lean back
```

## Real-World IMU Characteristics

### Noise and Bias
- **Gaussian noise**: Random variations around true values
- **Bias**: Systematic offset that can drift over time
- **Scale factor errors**: Multiplier errors in measurements

### Dynamic Range
- **Accelerometer**: Typically ±2g to ±16g (where g = 9.81 m/s²)
- **Gyroscope**: Typically ±250°/s to ±2000°/s
- **Magnetometer**: ±2 Gauss for Earth's magnetic field

### Update Rate
- **Typical rates**: 100 Hz to 1000 Hz
- **Trade-offs**: Higher rates provide more data but require more processing

## Processing IMU Data

### Acceleration Integration
```python
import numpy as np

# Example: Integrate acceleration to get velocity
def integrate_acceleration(acceleration_data, time_intervals):
    velocity = np.zeros_like(acceleration_data)
    for i in range(1, len(acceleration_data)):
        velocity[i] = velocity[i-1] + acceleration_data[i] * time_intervals[i]
    return velocity
```

### Orientation Integration
```python
# Example: Integrate angular velocity to get orientation (simplified)
def integrate_angular_velocity(angular_velocity_data, time_intervals):
    orientation = np.zeros_like(angular_velocity_data)
    for i in range(1, len(angular_velocity_data)):
        # Convert angular velocity to quaternion increment
        dt = time_intervals[i]
        dq = 0.5 * dt * np.array([0, angular_velocity_data[i, 0],
                                  angular_velocity_data[i, 1],
                                  angular_velocity_data[i, 2]])
        # Integrate quaternion
        orientation[i] = orientation[i-1] + dq
        # Normalize quaternion
        orientation[i] = orientation[i] / np.linalg.norm(orientation[i])
    return orientation
```

### Gravity Compensation
```python
# Example: Remove gravity from linear acceleration
def remove_gravity(acceleration, orientation):
    # Convert orientation to rotation matrix
    # Remove gravity component (assuming z-axis is up)
    gravity = np.array([0, 0, 9.81])
    gravity_rotated = rotate_vector_by_quaternion(gravity, orientation)
    corrected_acceleration = acceleration - gravity_rotated
    return corrected_acceleration
```

## Common IMU Patterns

### Vibration Detection
```
Linear Acceleration: [0.5±0.2, 0.3±0.1, 9.8±0.1]
Angular Velocity:    [0.1±0.05, -0.1±0.05, 0.0±0.02]
```
- Periodic variations indicate mechanical vibration
- Useful for detecting motor issues or structural problems

### Impact Detection
```
Linear Acceleration: [15.2, 2.1, 8.9]  // Sudden spike
Angular Velocity:    [0.5, -0.3, 0.1]
```
- Sudden large acceleration values indicate impact
- Useful for collision detection

### Periodic Motion
```
Linear Acceleration: Sinusoidal pattern with walking frequency
Angular Velocity:    Periodic changes during rotation
```
- Regular patterns indicate periodic motion
- Useful for gait analysis or motion recognition

## IMU Applications in Robotics

### State Estimation
- **Position tracking**: Double integration of acceleration
- **Velocity estimation**: Single integration of acceleration
- **Orientation tracking**: Integration of angular velocity

### Attitude Control
- **Balance maintenance**: Using orientation feedback
- **Stabilization**: Correcting for unwanted rotations
- **Posture control**: Maintaining desired orientations

### Motion Detection
- **Activity recognition**: Identifying different movement patterns
- **Gesture detection**: Recognizing specific motion sequences
- **Anomaly detection**: Identifying unusual movement patterns

### Navigation
- **Dead reckoning**: Estimating position from motion
- **Inertial navigation**: Position estimation without external references
- **Motion planning**: Using motion constraints in planning

## Quality Metrics for IMU Data

### Accuracy
- **Static accuracy**: How well it measures known values when stationary
- **Dynamic accuracy**: How well it measures during motion
- **Calibration accuracy**: Effectiveness of bias and scale factor corrections

### Precision
- **Noise density**: Amount of noise in measurements
- **Repeatability**: Consistency of measurements under identical conditions
- **Stability**: How well bias remains constant over time

### Linearity
- **Cross-axis sensitivity**: How much one axis affects another
- **Scale factor linearity**: How accurately scale factors apply across range

## Troubleshooting Common Issues

### Drift
- **Symptoms**: Gradual accumulation of errors in integrated quantities
- **Causes**: Bias in measurements, noise integration
- **Solutions**: Periodic calibration, sensor fusion with other sensors

### Noise
- **Symptoms**: Random variations in measurements
- **Causes**: Electronic noise, mechanical vibrations
- **Solutions**: Filtering, averaging, better sensor placement

### Calibration Errors
- **Symptoms**: Systematic offsets in measurements
- **Causes**: Misaligned sensors, incorrect bias/offset values
- **Solutions**: Proper calibration procedures, temperature compensation

### Integration Errors
- **Symptoms**: Position estimates that drift over time
- **Causes**: Double integration of noise and bias
- **Solutions**: Sensor fusion, zero-velocity updates, external references

## Advanced IMU Processing

### Sensor Fusion
Combining IMU data with other sensors:
```
IMU + GPS → More accurate position
IMU + Camera → Visual-inertial odometry
IMU + LiDAR → Robust navigation
```

### Kalman Filtering
Optimal combination of multiple sensor inputs:
```
State: [position, velocity, orientation, bias]
Prediction: IMU integration
Update: External sensor measurements
```

### Complementary Filtering
Combining high-frequency IMU data with low-frequency corrections:
```
High-pass filter: IMU dynamics
Low-pass filter: External reference
Combined: Balanced estimate
```

## Integration with Other Sensors

### IMU-LiDAR Fusion
- **Motion compensation**: Correcting LiDAR scans for robot motion
- **Odometry**: Combining IMU motion with LiDAR features
- **Mapping**: Creating consistent maps despite motion

### IMU-Camera Fusion
- **Visual-inertial odometry**: Combining visual features with IMU motion
- **Motion blur correction**: Using IMU to correct camera motion blur
- **Feature tracking**: Using IMU to predict feature locations

## Practical Applications

### Humanoid Robot Balance
- **Center of Mass tracking**: Using IMU to maintain balance
- **Step planning**: Adjusting gait based on orientation feedback
- **Fall detection**: Identifying when robot is falling

### Drone Navigation
- **Attitude control**: Maintaining stable flight orientation
- **Altitude estimation**: Combining IMU with barometer
- **Aerobatic maneuvers**: Complex motion control

### Mobile Robot Navigation
- **Dead reckoning**: Short-term position estimation
- **Path following**: Maintaining heading and speed
- **Obstacle avoidance**: Detecting motion constraints

## Summary

IMU sensors provide critical information about motion and orientation that is essential for robotics applications. Understanding how to interpret IMU data and recognize common patterns enables effective state estimation, attitude control, and navigation. The realistic acceleration and orientation data produced by Gazebo's IMU simulation closely matches real-world sensors, making it an excellent tool for developing and testing robotics algorithms.