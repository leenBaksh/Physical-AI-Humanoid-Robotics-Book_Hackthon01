# Data Model: Module 2 - The Digital Twin (Gazebo & Unity)

## Book Structure

### Module
- **name**: String (e.g., "Module 2: The Digital Twin")
- **description**: String (overview of digital twin concepts with Gazebo and Unity)
- **chapters**: Array of Chapter objects
- **prerequisites**: Array of String (what student should know before starting)
- **learning_outcomes**: Array of String (what student will learn)

### Chapter
- **title**: String (e.g., "Gazebo Fundamentals")
- **description**: String (overview of chapter content)
- **sections**: Array of Section objects
- **files**: Array of String (file paths for chapter content)
- **prerequisites**: Array of String (what reader should know for this chapter)
- **learning_objectives**: Array of String (what reader will learn in this chapter)

### Section
- **title**: String (e.g., "Physics Simulation in Gazebo")
- **content**: String (path to content file)
- **prerequisites**: Array of String (what reader should know)
- **learning_objectives**: Array of String (what reader will learn)
- **examples**: Array of Example objects (code/config examples)

### Example
- **title**: String (e.g., "Basic Physics World Configuration")
- **type**: String ("gazebo-config", "unity-concept", "code-snippet")
- **language**: String (e.g., "sdf", "xml", "csharp", "python")
- **content**: String (the actual example content)
- **explanation**: String (what the example demonstrates)

## Gazebo Configuration Elements

### GazeboWorld
- **name**: String (name of the world)
- **physics_engine**: String (e.g., "ode", "bullet", "dart")
- **gravity**: Object (x, y, z components of gravity vector)
- **models**: Array of GazeboModel objects
- **plugins**: Array of GazeboPlugin objects

### GazeboModel
- **name**: String (name of the model)
- **pose**: Object (position and orientation)
- **link**: GazeboLink object
- **joint**: Array of GazeboJoint objects

### GazeboLink
- **name**: String (name of the link)
- **inertial**: Object (mass, inertia properties)
- **collision**: Object (collision geometry)
- **visual**: Object (visual properties)
- **sensor**: Array of GazeboSensor objects

### GazeboSensor
- **name**: String (name of the sensor)
- **type**: String ("lidar", "camera", "imu", "depth")
- **pose**: Object (position and orientation)
- **sensor_specific_config**: Object (configuration specific to sensor type)

### GazeboPlugin
- **name**: String (name of the plugin)
- **filename**: String (plugin library file)
- **parameters**: Object (plugin-specific parameters)

## Unity Elements

### UnityScene
- **name**: String (name of the scene)
- **objects**: Array of UnityObject objects
- **lighting**: Object (lighting configuration)
- **environment**: Object (environment settings)

### UnityObject
- **name**: String (name of the object)
- **type**: String ("robot", "human", "environment", "interaction-point")
- **position**: Object (x, y, z coordinates)
- **rotation**: Object (rotation quaternion)
- **components**: Array of UnityComponent objects

### UnityComponent
- **type**: String ("mesh-renderer", "collider", "interaction-script")
- **properties**: Object (component-specific properties)

## Content Files

### MarkdownFile
- **path**: String (relative path from docs/ directory)
- **frontmatter**: Object (YAML frontmatter with metadata)
- **content**: String (markdown content)
- **sidebar_position**: Number (position in sidebar navigation)

### Frontmatter
- **title**: String (page title)
- **sidebar_label**: String (label to display in sidebar)
- **sidebar_position**: Number (position in sidebar)
- **description**: String (page description for SEO)

## Sensor Simulation Models

### LidarConfig
- **name**: String (name of the LiDAR configuration)
- **type**: String ("ray", "gpu_ray")
- **scan**: Object (range, resolution, and angle settings)
- **render_rate**: Number (how often to render)
- **topic**: String (ROS topic name)

### DepthCameraConfig
- **name**: String (name of the depth camera configuration)
- **image**: Object (width, height, format)
- **clip**: Object (near and far clipping distances)
- **noise**: Object (noise parameters)
- **topic**: String (ROS topic name)

### ImuConfig
- **name**: String (name of the IMU configuration)
- **always_on**: Boolean (whether always active)
- **update_rate**: Number (how often to update)
- **topic**: String (ROS topic name)
- **noise**: Object (noise parameters for measurements)

## Human-Robot Interaction Concepts

### InteractionScenario
- **name**: String (name of the interaction scenario)
- **description**: String (description of the interaction)
- **participants**: Array of String ("human", "robot", "environment")
- **actions**: Array of InteractionAction objects
- **outcomes**: Array of String (possible outcomes)

### InteractionAction
- **name**: String (name of the action)
- **actor**: String ("human", "robot")
- **description**: String (what the actor does)
- **trigger**: String (what triggers the action)
- **result**: String (what happens as a result)