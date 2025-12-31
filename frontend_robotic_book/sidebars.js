// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  // Manual sidebar structure
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Module 1: ROS 2 Fundamentals',
      items: [
        'module1/chapter-1-ros2-core/index',
        'module1/chapter-1-ros2-core/nodes-topics-services',
        'module1/chapter-1-ros2-core/publisher-subscriber-patterns',
        'module1/chapter-1-ros2-core/hands-on-tutorial',
        'module1/chapter-2-ai-ros-bridge/index',
        'module1/chapter-2-ai-ros-bridge/message-interfaces',
        'module1/chapter-2-ai-ros-bridge/rclpy-integration',
        'module1/chapter-2-ai-ros-bridge/ai-agent-tutorial',
        'module1/chapter-3-urdf-kinematics/index',
        'module1/chapter-3-urdf-kinematics/urdf-overview',
        'module1/chapter-3-urdf-kinematics/kinematic-structure',
        'module1/chapter-3-urdf-kinematics/tools',
        'module1/chapter-3-urdf-kinematics/interpretation-guide',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 2: Gazebo/Unity Digital Twin',
      items: [
        'module2/index',
        'module2/chapter-1-gazebo-fundamentals/index',
        'module2/chapter-1-gazebo-fundamentals/tutorial-basic-world',
        'module2/chapter-1-gazebo-fundamentals/tutorial-robot-model',
        'module2/chapter-1-gazebo-fundamentals/physics-simulation',
        'module2/chapter-1-gazebo-fundamentals/gravity-settings',
        'module2/chapter-1-gazebo-fundamentals/collision-detection',
        'module2/chapter-1-gazebo-fundamentals/tutorial-gravity-adjust',
        'module2/chapter-1-gazebo-fundamentals/tutorial-collision-detection',
        'module2/chapter-1-gazebo-fundamentals/exercises',
        'module2/chapter-2-sensor-simulation/index',
        'module2/chapter-2-sensor-simulation/lidar-modeling',
        'module2/chapter-2-sensor-simulation/depth-camera-simulation',
        'module2/chapter-2-sensor-simulation/imu-simulation',
        'module2/chapter-2-sensor-simulation/tutorial-lidar-configuration',
        'module2/chapter-2-sensor-simulation/tutorial-depth-camera-configuration',
        'module2/chapter-2-sensor-simulation/tutorial-imu-configuration',
        'module2/chapter-2-sensor-simulation/lidar-examples',
        'module2/chapter-2-sensor-simulation/depth-camera-examples',
        'module2/chapter-2-sensor-simulation/imu-examples',
        'module2/chapter-2-sensor-simulation/exercises',
        'module2/chapter-3-hri-unity/index',
        'module2/chapter-3-hri-unity/unity-setup',
        'module2/chapter-3-hri-unity/hri-concepts',
        'module2/chapter-3-hri-unity/unity-concept-diagrams',
        'module2/chapter-3-hri-unity/interaction-scenarios',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 3: Isaac Sim & AI Perception Tools',
      items: [
        'module3/index',
        'module3/chapter1-synthetic-data/index',
        'module3/chapter1-synthetic-data/content',
        'module3/chapter2-vslam/index',
        'module3/chapter2-vslam/content',
        'module3/chapter3-bipedal-nav/index',
        'module3/chapter3-bipedal-nav/content',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA) for Cognitive Robotics',
      items: [
        'module4/index',
        {
          type: 'category',
          label: 'Chapter 1: Voice-to-Action with Whisper',
          items: [
            'module4/chapter1-voice-to-action/index',
            'module4/chapter1-voice-to-action/content',
          ],
          collapsed: false,
        },
        {
          type: 'category',
          label: 'Chapter 2: Cognitive Planning with LLMs',
          items: [
            'module4/chapter2-cognitive-planning/index',
            'module4/chapter2-cognitive-planning/content',
          ],
          collapsed: false,
        },
        {
          type: 'category',
          label: 'Chapter 3: Capstone Integration',
          items: [
            'module4/chapter3-capstone-integration/index',
            'module4/chapter3-capstone-integration/content',
          ],
          collapsed: false,
        },
      ],
      collapsed: false,
    },
  ],
};

export default sidebars;
