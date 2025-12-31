# Research: Module 2 - The Digital Twin (Gazebo & Unity)

## Decision: Gazebo Harmonic as Primary Simulation Environment
**Rationale**: Gazebo Harmonic is the latest stable version with robust support for physics simulation, sensor modeling, and humanoid robotics. It provides the necessary features for simulating gravity, collisions, and various sensor types (LiDAR, depth cameras, IMUs) required for this module.

**Alternatives considered**:
- Gazebo Fortress: Stable but older than Harmonic
- Ignition Gazebo: More modern but less documentation for humanoid robotics
- Webots: Alternative simulator but less ROS 2 integration

## Decision: Unity LTS for Human-Robot Interaction
**Rationale**: Unity LTS (Long Term Support) provides stability and extensive documentation for 3D environment creation. It's appropriate for modeling human-robot interaction scenarios without requiring advanced game logic or rendering as specified in the constraints.

**Alternatives considered**:
- Unity Personal: Free but less support
- Unreal Engine: More powerful but overkill for simulation focus
- Blender: Good for modeling but not for interaction simulation

## Decision: Docusaurus .md Format for Content
**Rationale**: Following the established pattern from Module 1, Docusaurus .md files provide the best format for technical documentation with support for embedded code snippets, images, and structured content.

**Alternatives considered**:
- Jupyter notebooks: Good for interactive content but less suitable for documentation
- PDF format: Less interactive and harder to update
- HTML: More complex to maintain

## Decision: Focus on Simulation Over Rendering
**Rationale**: The requirement specifically states "simulation only. No advanced rendering or game logic in Unity," so the content will focus on physics simulation, sensor modeling, and interaction concepts rather than visual effects.

**Alternatives considered**:
- Full Unity features: Would violate the specified constraints
- Advanced rendering: Not needed for simulation-focused content

## Decision: Include Gazebo Configuration Snippets
**Rationale**: Students need practical examples of how to configure Gazebo worlds, robots, and sensors. Including actual configuration snippets will enhance the learning experience.

**Alternatives considered**:
- Generic examples: Less practical for implementation
- External references: Less accessible during learning

## Decision: Unity Concept Diagrams Over Complex Tutorials
**Rationale**: Since the focus is on simulation rather than advanced Unity features, concept diagrams will be more appropriate than complex Unity tutorials that might involve game logic.

**Alternatives considered**:
- Full Unity projects: Would exceed the simulation-only constraint
- Video tutorials: Less accessible and harder to reference