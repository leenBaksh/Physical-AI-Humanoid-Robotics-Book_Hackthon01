---
sidebar_position: 18
title: "Depth Camera Examples: Accurate Depth Maps"
---

# Depth Camera Examples: Accurate Depth Maps

This section provides practical examples of how depth cameras produce accurate depth maps in Gazebo simulation. You'll learn how to interpret depth camera data and understand its applications in robotics.

## Understanding Depth Camera Data

Depth cameras output three types of data:
- **Color image**: Standard RGB image for visual reference
- **Depth image**: 2D array of distance values for each pixel
- **Point cloud**: 3D coordinates derived from depth information

### Basic Depth Image Structure

A depth image is a 2D array where each pixel contains a distance value:

```
Depth Image (640x480):
[
  [2.1, 2.1, 2.1, ..., 2.1],  // Row 0
  [2.1, 2.1, 2.0, ..., 2.1],  // Row 1
  [2.1, 2.0, 1.9, ..., 2.0],  // Row 2
  ...
  [2.1, 2.1, 2.1, ..., 2.1]   // Row 479
]
```

Each value represents the distance from the camera to the object at that pixel location, typically in meters.

## Example 1: Empty Room Depth Map

Consider a depth camera in an empty 10x10 meter room:

```
Depth Image:
[
  [9.8, 9.8, 9.8, ..., 9.8],  // All pixels show maximum range
  [9.8, 9.8, 9.8, ..., 9.8],  // No obstacles in view
  [9.8, 9.8, 9.8, ..., 9.8],
  ...
  [9.8, 9.8, 9.8, ..., 9.8]
]
```

- All pixels show maximum range (9.8m) because no obstacles are present
- Small variations due to sensor noise and wall surface properties
- This represents the "free space" baseline

## Example 2: Wall Detection

When the depth camera faces a wall 2 meters away:

```
Depth Image:
[
  [2.0, 2.0, 2.0, ..., 2.0],  // Central region shows wall
  [2.0, 2.0, 2.0, ..., 2.0],  // Uniform distance
  [2.0, 2.0, 2.0, ..., 2.0],  // Wall fills most of the view
  [9.8, 9.8, 9.8, ..., 9.8],  // Edge pixels may show farther objects
  [9.8, 9.8, 9.8, ..., 9.8]   // Or be at maximum range
]
```

- Clear detection of the wall at 2 meters across the central pixels
- Edge pixels may show maximum range or other environmental features

## Example 3: Object Detection

When detecting a box 3 meters away with dimensions 1x1x1 meter:

```
Depth Image:
[
  [9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, ...],  // Background
  [9.8, 9.8, 3.5, 3.5, 3.5, 3.5, 3.5, 9.8, 9.8, 9.8, ...],  // Box top
  [9.8, 9.8, 3.3, 3.2, 3.1, 3.1, 3.2, 9.8, 9.8, 9.8, ...],  // Box front
  [9.8, 9.8, 3.2, 3.0, 3.0, 3.0, 3.1, 9.8, 9.8, 9.8, ...],  // Box center
  [9.8, 9.8, 3.1, 3.0, 3.0, 3.0, 3.1, 9.8, 9.8, 9.8, ...],  // Box center
  [9.8, 9.8, 3.2, 3.1, 3.1, 3.1, 3.2, 9.8, 9.8, 9.8, ...],  // Box bottom
  [9.8, 9.8, 3.4, 3.4, 3.4, 3.4, 3.4, 9.8, 9.8, 9.8, ...],  // Box bottom
  [9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, ...],  // Background
  ...
]
```

- The box appears as a region of consistent depth values (around 3 meters)
- Slight variations due to the box's geometry and surface properties
- Background shows maximum range values

## Example 4: Humanoid Robot Detection

When detecting a humanoid robot (cylindrical torso, spherical head):

```
Depth Image:
[
  [9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, ...],  // Background
  [9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, ...],  // Background
  [9.8, 9.8, 2.5, 2.5, 2.5, 2.5, 2.5, 9.8, 9.8, 9.8, ...],  // Head region
  [9.8, 9.8, 2.4, 2.3, 2.2, 2.3, 2.4, 9.8, 9.8, 9.8, ...],  // Head (spherical)
  [9.8, 9.8, 2.3, 2.1, 2.0, 2.1, 2.3, 9.8, 9.8, 9.8, ...],  // Torso top
  [9.8, 9.8, 2.3, 2.0, 2.0, 2.0, 2.3, 9.8, 9.8, 9.8, ...],  // Torso center
  [9.8, 9.8, 2.3, 2.0, 2.0, 2.0, 2.3, 9.8, 9.8, 9.8, ...],  // Torso center
  [9.8, 9.8, 2.3, 2.1, 2.0, 2.1, 2.3, 9.8, 9.8, 9.8, ...],  // Torso bottom
  [9.8, 9.8, 2.4, 2.3, 2.2, 2.3, 2.4, 9.8, 9.8, 9.8, ...],  // Legs start
  [9.8, 9.8, 2.5, 2.5, 2.5, 2.5, 2.5, 9.8, 9.8, 9.8, ...],  // Legs
  [9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, 9.8, ...],  // Background
  ...
]
```

- Head appears as a circular region with slightly varying depths (spherical shape)
- Torso appears as a rectangular region with consistent depth (cylindrical shape)
- Legs create additional depth variations

## Example 5: Complex Environment

In a more complex environment with multiple objects:

```
Depth Image:
[
  [2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 2.5, 2.5, 3.0, 3.0, ...],  // Row showing multiple objects
  [2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 2.5, 2.5, 3.0, 3.0, ...],  // Objects at different depths
  [2.0, 2.0, 2.0, 1.5, 1.5, 1.5, 1.5, 2.5, 2.5, 3.0, 3.0, ...],
  ...
]
```

- Multiple depth clusters correspond to different objects
- 2.0m: Close wall or object
- 1.5m: Table or chair
- 2.5m, 3.0m: Various other objects

## Real-World Depth Camera Characteristics

### Resolution and Accuracy
- **Resolution**: Typically 640x480, 1280x720, or higher
- **Accuracy**: Generally 1-5% of measured distance
- **Precision**: Repeatability of measurements across scans

### Depth Range
- **Near range**: Usually 0.1-0.5 meters minimum
- **Far range**: Typically 3-10 meters maximum (varies by sensor)
- **Optimal range**: Where accuracy is highest

### Environmental Factors
- **Lighting**: Performance can vary with ambient lighting
- **Surface properties**: Reflective or transparent surfaces may cause artifacts
- **Temperature**: Can affect sensor calibration

## Processing Depth Camera Data

### Filtering
```python
import numpy as np

# Example: Remove invalid measurements
def filter_depth_image(depth_image, min_range=0.1, max_range=10.0):
    # Set invalid values to 0 (or NaN)
    filtered = np.copy(depth_image)
    filtered[(depth_image <= min_range) | (depth_image >= max_range)] = 0
    return filtered
```

### Surface Normal Estimation
```python
# Example: Estimate surface normals from depth image
def estimate_normals(depth_image, focal_length):
    # Compute gradients
    dz_dx = np.gradient(depth_image, axis=1)
    dz_dy = np.gradient(depth_image, axis=0)

    # Compute surface normals
    normals = np.zeros((depth_image.shape[0], depth_image.shape[1], 3))
    normals[:, :, 0] = -dz_dx / focal_length
    normals[:, :, 1] = -dz_dy / focal_length
    normals[:, :, 2] = 1.0

    # Normalize
    norm = np.linalg.norm(normals, axis=2, keepdims=True)
    normals = normals / norm

    return normals
```

## Common Depth Camera Patterns

### Planar Surface Detection
```
Depth Image: Uniform values across a region indicate a flat surface
```
- Consistent depth values in a rectangular region
- Characteristic of walls, floors, or tables

### Object Edge Detection
```
Depth Image: Sharp transitions indicate object boundaries
```
- Sudden changes from near to far depth values
- Indicate object edges or boundaries

### Occlusion Detection
```
Depth Image: Areas where depth is missing or invalid
```
- Regions with maximum range or invalid values
- May indicate occluded areas or transparent objects

## Depth Camera Applications in Robotics

### 3D Reconstruction
- **Point cloud generation**: Converting depth images to 3D point clouds
- **Mesh generation**: Creating 3D models from depth data
- **Surface mapping**: Understanding surface properties

### Object Detection and Recognition
- **Segmentation**: Identifying objects based on depth discontinuities
- **Classification**: Using 3D shape information for object recognition
- **Tracking**: Following objects in 3D space over time

### Navigation and Mapping
- **Obstacle detection**: Identifying obstacles in the robot's path
- **Free space mapping**: Determining navigable areas
- **Terrain analysis**: Understanding surface properties for locomotion

### Human-Robot Interaction
- **Gesture recognition**: Understanding human hand and body movements
- **Pose estimation**: Determining human body pose for interaction
- **Proximity detection**: Sensing when humans are near the robot

## Quality Metrics for Depth Data

### Accuracy
- Mean absolute error compared to ground truth
- Systematic bias in depth measurements

### Precision
- Standard deviation of repeated measurements
- Consistency across different lighting conditions

### Completeness
- Percentage of valid depth measurements
- Coverage of the expected field of view

### Temporal Consistency
- Smoothness of depth values over time
- Absence of temporal artifacts

## Troubleshooting Common Issues

### Depth Inaccuracy
- **Symptoms**: Systematic errors in distance measurements
- **Causes**: Poor calibration, environmental factors
- **Solutions**: Recalibration, environmental compensation

### Missing Data
- **Symptoms**: Invalid or maximum range values in some regions
- **Causes**: Reflective surfaces, transparent objects, occlusions
- **Solutions**: Multi-sensor fusion, inpainting algorithms

### Noise
- **Symptoms**: Random variations in depth measurements
- **Causes**: Environmental conditions, sensor limitations
- **Solutions**: Filtering, averaging, sensor fusion

## Advanced Depth Processing

### Point Cloud Generation
Converting depth images to 3D point clouds:
```
Depth Image + Camera Intrinsics → Point Cloud
```

### Surface Reconstruction
Building 3D surfaces from depth data:
```
Point Cloud → Mesh → 3D Model
```

### Depth-Based SLAM
Using depth data for mapping and localization:
```
Depth Images + Camera Motion → 3D Map + Robot Pose
```

## Integration with Other Sensors

### LiDAR-Depth Fusion
- **Complementary strengths**: LiDAR accuracy + depth texture
- **Multi-modal mapping**: Combining geometric and visual information

### IMU-Depth Fusion
- **Motion compensation**: Correcting for camera motion during capture
- **Pose estimation**: Improving depth accuracy with IMU data

## Summary

Depth cameras provide rich 3D information that is crucial for robotics applications. Understanding how to interpret depth maps and recognize common patterns enables effective 3D reconstruction, object detection, and navigation. The accurate depth maps produced by Gazebo's depth camera simulation closely match real-world sensors, making it an excellent tool for developing and testing robotics algorithms.