# Data Model: Isaac Sim & AI Perception Tools

## Isaac Sim Entities

### Synthetic Dataset
- **name**: String (identifier for the dataset)
- **description**: String (overview of dataset contents)
- **image_count**: Number (total number of images in the dataset)
- **annotations**: Array of Annotation objects (labeling information for each image)
- **generated_at**: Date (timestamp when dataset was generated)
- **format**: String (format of the dataset, e.g., COCO, YOLO, TFRecord)
- **source_scene**: String (name of Isaac Sim scene used for generation)
- **camera_configurations**: Array of CameraConfig objects (camera settings used)

### Annotation
- **image_id**: String (identifier for the source image)
- **type**: String ("bbox", "segmentation", "keypoints", etc.)
- **labels**: Array of String (object labels in the image)
- **bounding_boxes**: Array of BoundingBox objects (if bbox annotations)
- **segmentation_masks**: Array of SegmentationMask objects (if segmentation annotations)
- **metadata**: Object (additional annotation metadata)

### BoundingBox
- **label**: String (object class label)
- **x_min**: Number (normalized x coordinate of top-left corner)
- **y_min**: Number (normalized y coordinate of top-left corner)
- **x_max**: Number (normalized x coordinate of bottom-right corner)
- **y_max**: Number (normalized y coordinate of bottom-right corner)

### CameraConfig
- **camera_name**: String (identifier for the camera)
- **position**: Object (x, y, z coordinates)
- **rotation**: Object (quaternion or euler angles)
- **resolution**: Object (width and height in pixels)
- **fov**: Number (field of view in degrees)

## VSLAM Entities

### VSLAM Pose Graph
- **graph_id**: String (unique identifier for the pose graph)
- **robot_trajectory**: Array of Pose objects (robot poses over time)
- **landmarks**: Array of Landmark objects (environment features)
- **constraints**: Array of Constraint objects (relationships between poses)
- **created_at**: Date (timestamp when graph was created)
- **map_size**: Number (number of poses in the graph)
- **coverage_area**: Number (area covered by the map in square meters)

### Pose
- **pose_id**: String (unique identifier for this pose)
- **timestamp**: Date (time when pose was captured)
- **position**: Object (x, y, z coordinates in world frame)
- **orientation**: Object (quaternion representing orientation)
- **covariance**: Array of Number (uncertainty in pose estimate)

### Landmark
- **landmark_id**: String (unique identifier for the landmark)
- **position**: Object (x, y, z coordinates in world frame)
- **observations**: Array of Observation objects (times when landmark was seen)
- **descriptor**: Array of Number (feature descriptor for the landmark)

## Navigation Entities

### Bipedal Navigation Plan
- **plan_id**: String (unique identifier for the navigation plan)
- **start_pose**: Pose object (starting position of the robot)
- **goal_pose**: Pose object (target position for navigation)
- **waypoints**: Array of Waypoint objects (intermediate navigation points)
- **path_cost**: Number (cost of the planned path)
- **planning_time**: Number (time taken to generate the plan in seconds)
- **created_at**: Date (timestamp when plan was created)

### Waypoint
- **waypoint_id**: String (unique identifier for the waypoint)
- **position**: Object (x, y, z coordinates)
- **orientation**: Object (quaternion or euler angles)
- **step_type**: String ("left_foot", "right_foot", "balance", etc.)
- **time_from_start**: Number (time offset from beginning of plan)

### Navigation Goal
- **goal_id**: String (unique identifier for the navigation goal)
- **target_position**: Object (x, y, z coordinates of target)
- **target_orientation**: Object (quaternion or euler angles of target)
- **robot_model**: String (identifier for the bipedal robot model)
- **costmap_resolution**: Number (resolution of the navigation costmap)
- **planner_type**: String ("global_planner", "local_planner", etc.)
- **status**: String ("pending", "active", "succeeded", "failed", "canceled")