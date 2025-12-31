# Data Model: Vision-Language-Action (VLA) for Cognitive Robotics

## Voice Command Processing

### VoiceCommand
- **audio_data**: Binary audio data (raw audio stream or file)
- **transcription**: String (text transcription from Whisper)
- **confidence**: Number (confidence score from voice recognition)
- **timestamp**: Date (when the command was received)
- **language**: String (detected language of the command)
- **processing_status**: String ("pending", "processing", "completed", "failed")

## LLM Action Planning

### LLMActionPlan
- **plan_id**: String (unique identifier for the action plan)
- **natural_language_input**: String (original natural language command)
- **structured_actions**: Array of Action objects (sequence of ROS 2 actions)
- **context**: Object (additional context for the plan)
- **generated_at**: Date (timestamp when plan was generated)
- **valid**: Boolean (whether the plan is executable)
- **validation_errors**: Array of String (errors if plan is invalid)

### Action
- **action_id**: String (unique identifier for the action)
- **action_type**: String ("navigation", "manipulation", "vision", "communication", etc.)
- **parameters**: Object (specific parameters for the action)
- **priority**: Number (execution priority)
- **dependencies**: Array of String (other action IDs this action depends on)
- **timeout**: Number (maximum time allowed for execution in seconds)

### NavigationAction
- **target_pose**: Pose object (target position and orientation)
- **frame_id**: String (coordinate frame for the target)
- **behavior_tree**: String (optional behavior tree to execute during navigation)

### ManipulationAction
- **target_object**: String (name or ID of object to manipulate)
- **manipulation_type**: String ("pick", "place", "move", "grasp", "release")
- **end_effector_pose**: Pose object (target pose for end effector)
- **gripper_position**: Number (gripper position value)

### VisionAction
- **task_type**: String ("object_detection", "pose_estimation", "classification")
- **target_object**: String (object to detect or classify)
- **camera_source**: String (which camera to use)
- **confidence_threshold**: Number (minimum confidence for detection)

## Cognitive Pipeline

### CognitivePipeline
- **pipeline_id**: String (unique identifier for the pipeline instance)
- **voice_command**: VoiceCommand object (input command)
- **action_plan**: LLMActionPlan object (generated plan)
- **execution_status**: String ("idle", "executing", "completed", "failed", "cancelled")
- **current_action_index**: Number (index of currently executing action)
- **execution_log**: Array of ExecutionLogEntry objects (log of executed actions)
- **start_time**: Date (when pipeline started)
- **end_time**: Date (when pipeline completed or failed)

### ExecutionLogEntry
- **action_id**: String (ID of the action being executed)
- **status**: String ("started", "completed", "failed", "skipped")
- **start_time**: Date (when action started)
- **end_time**: Date (when action completed or failed)
- **result**: Object (result of action execution)
- **error_message**: String (error message if action failed)

### Pose
- **position**: Object (x, y, z coordinates)
- **orientation**: Object (quaternion: x, y, z, w)
- **frame_id**: String (coordinate frame identifier)