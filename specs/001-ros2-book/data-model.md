# Data Model: Module 1 - The Robotic Nervous System (ROS 2)

## Book Structure

### Chapter
- **name**: String (e.g., "ROS 2 Core – Nodes, Topics, & Services")
- **description**: String (overview of chapter content)
- **sections**: Array of Section objects
- **tutorials**: Array of Tutorial objects

### Section
- **title**: String (e.g., "Publisher-Subscriber Patterns")
- **content**: String (Markdown content)
- **prerequisites**: Array of String (what reader should know)
- **learning_objectives**: Array of String (what reader will learn)

### Tutorial
- **title**: String (e.g., "Create Two Nodes for Sensor Data")
- **description**: String (what the tutorial covers)
- **prerequisites**: Array of String (what is needed before starting)
- **steps**: Array of Step objects
- **expected_outcomes**: Array of String (what reader should achieve)

### Step
- **title**: String (e.g., "Create Publisher Node")
- **description**: String (detailed instructions)
- **code_examples**: Array of CodeExample objects
- **verification**: String (how to check if step was successful)

### CodeExample
- **language**: String (e.g., "python", "bash")
- **code**: String (the actual code)
- **explanation**: String (what the code does)

### CodeBlock
- **title**: String (e.g., "publisher_node.py")
- **content**: String (the complete code file)
- **file_path**: String (where to save the file)
- **description**: String (purpose of the code block)

## ROS 2 Concepts

### ROS2Node
- **name**: String (name of the node)
- **type**: String (publisher, subscriber, service_server, service_client)
- **topics**: Array of Topic objects
- **services**: Array of Service objects
- **description**: String (what the node does)

### Topic
- **name**: String (name of the topic)
- **type**: String (message type, e.g., std_msgs/String)
- **direction**: String (publisher, subscriber, or both)
- **description**: String (what data is communicated)

### Service
- **name**: String (name of the service)
- **type**: String (service type, e.g., std_srvs/SetBool)
- **description**: String (what the service does)

## AI Agent Components

### AIAgent
- **name**: String (name of the AI agent)
- **input_topics**: Array of String (topics the agent subscribes to)
- **output_topics**: Array of String (topics the agent publishes to)
- **logic**: String (description of decision-making process)
- **dependencies**: Array of String (required libraries/packages)

## URDF Components

### URDFModel
- **name**: String (name of the robot)
- **joints**: Array of Joint objects
- **links**: Array of Link objects
- **materials**: Array of Material objects
- **description**: String (overview of the robot model)

### Joint
- **name**: String (name of the joint)
- **type**: String (revolute, prismatic, fixed, etc.)
- **parent**: String (parent link name)
- **child**: String (child link name)
- **limits**: Object (min/max values for joint movement)

### Link
- **name**: String (name of the link)
- **visual**: Object (visual properties)
- **collision**: Object (collision properties)
- **inertial**: Object (mass, inertia properties)