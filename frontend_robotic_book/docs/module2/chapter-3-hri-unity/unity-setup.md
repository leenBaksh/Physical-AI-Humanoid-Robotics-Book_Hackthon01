---
sidebar_position: 22
title: "Unity Environment Setup for HRI Simulation"
---

# Unity Environment Setup for HRI Simulation

This section covers setting up a Unity environment specifically for human-robot interaction (HRI) simulation. We'll focus on simulation aspects rather than advanced rendering or game logic, following the project constraints.

## Prerequisites

Before setting up Unity for HRI simulation, ensure you have:

- Unity Hub installed
- Unity LTS (Long Term Support) version installed (2022.3.x or later recommended)
- Basic understanding of Unity interface and concepts
- A computer with sufficient resources (minimum 8GB RAM, dedicated GPU recommended)

## Unity Project Configuration

### Creating a New Project

1. Open Unity Hub
2. Click "New Project"
3. Select the "3D (Built-in Render Pipeline)" template (not HDRP or URP)
4. Name your project (e.g., "HRI_Simulation")
5. Choose a location for your project
6. Click "Create Project"

### Project Settings for Simulation

After creating the project, configure these settings for simulation-focused work:

1. **Quality Settings** (Edit → Project Settings → Quality):
   - Set Quality Level to "Fastest" to optimize for simulation performance
   - Disable anti-aliasing, shadows, and other rendering-intensive features

2. **Physics Settings** (Edit → Project Settings → Physics):
   - Adjust Fixed Timestep to 0.02 (50 FPS) for consistent simulation
   - Set Maximum Allowed Timestep to 0.333 for stability

3. **Input Manager** (Edit → Project Settings → Input Manager):
   - Configure inputs for simulation controls if needed

## Scene Structure for HRI

### Basic Scene Setup

Create a simple scene structure for HRI simulation:

1. **Main Camera**: Set up for simulation viewing
2. **Directional Light**: Minimal lighting for visibility
3. **Environment**: Simple ground plane and basic objects
4. **Robot Model**: Placeholder for humanoid robot
5. **Human Model**: Placeholder for human character

### Hierarchy Organization

```
HRI_Simulation
├── Environment
│   ├── GroundPlane
│   ├── Walls
│   └── Obstacles
├── HumanoidRobot
│   ├── RobotBody
│   ├── RobotHead
│   ├── RobotArms
│   └── RobotLegs
├── HumanCharacter
│   ├── HumanBody
│   ├── HumanHead
│   ├── HumanArms
│   └── HumanLegs
├── InteractionZones
│   ├── SafeZone
│   ├── WorkZone
│   └── CommunicationZone
└── Main Camera
```

## Basic Models and Components

### Robot Model Setup

For simulation purposes, create a simplified humanoid robot using Unity primitives:

```csharp
// RobotModel.cs - Basic robot representation for simulation
using UnityEngine;

public class RobotModel : MonoBehaviour
{
    [Header("Robot Configuration")]
    public float height = 1.7f;
    public float radius = 0.2f;
    public Color robotColor = Color.blue;

    [Header("Interaction Properties")]
    public float interactionRange = 2.0f;
    public bool isOperational = true;

    void Start()
    {
        SetupRobotVisuals();
    }

    void SetupRobotVisuals()
    {
        // Create basic robot body using primitives
        GameObject body = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        body.transform.SetParent(transform);
        body.transform.localPosition = Vector3.zero;
        body.transform.localScale = new Vector3(radius * 2, height / 2, radius * 2);
        body.GetComponent<Renderer>().material.color = robotColor;

        // Add interaction sphere collider
        SphereCollider interactionCollider = body.AddComponent<SphereCollider>();
        interactionCollider.radius = interactionRange;
        interactionCollider.isTrigger = true;
        interactionCollider.enabled = false; // Enable when needed
    }

    public void SetOperational(bool operational)
    {
        isOperational = operational;
        // Update visual representation based on operational status
    }
}
```

### Human Model Setup

Create a simple human model for simulation:

```csharp
// HumanModel.cs - Basic human representation for simulation
using UnityEngine;

public class HumanModel : MonoBehaviour
{
    [Header("Human Configuration")]
    public float height = 1.7f;
    public float radius = 0.15f;
    public Color humanColor = Color.green;

    [Header("Behavior Properties")]
    public float walkingSpeed = 1.0f;
    public float interactionRange = 1.5f;

    void Start()
    {
        SetupHumanVisuals();
    }

    void SetupHumanVisuals()
    {
        // Create basic human body using primitives
        GameObject body = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        body.transform.SetParent(transform);
        body.transform.localPosition = Vector3.zero;
        body.transform.localScale = new Vector3(radius * 2, height / 2, radius * 2);
        body.GetComponent<Renderer>().material.color = humanColor;

        // Add interaction sphere collider
        SphereCollider interactionCollider = body.AddComponent<SphereCollider>();
        interactionCollider.radius = interactionRange;
        interactionCollider.isTrigger = true;
    }

    public void SetWalkingSpeed(float speed)
    {
        walkingSpeed = speed;
    }
}
```

## Interaction Zone Setup

Create trigger zones for different types of interactions:

```csharp
// InteractionZone.cs - Define different interaction zones
using UnityEngine;

public class InteractionZone : MonoBehaviour
{
    public enum ZoneType
    {
        SafeZone,      // Safe distance for humans
        WorkZone,      // Operational area for robot
        CommunicationZone // Area for human-robot communication
    }

    public ZoneType zoneType;
    public Color zoneColor = Color.white;
    public float radius = 3.0f;

    void Start()
    {
        SetupZone();
    }

    void SetupZone()
    {
        // Create a wireframe sphere to visualize the zone
        GameObject zoneObject = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        zoneObject.transform.SetParent(transform);
        zoneObject.transform.localScale = Vector3.one * radius * 2;

        // Make it transparent and wireframe
        Renderer renderer = zoneObject.GetComponent<Renderer>();
        renderer.material = new Material(Shader.Find("Unlit/Color"));
        renderer.material.color = zoneColor;
        renderer.material.SetFloat("_Mode", 3); // Transparent
        renderer.material.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.SrcAlpha);
        renderer.material.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
        renderer.material.SetInt("_ZWrite", 0);
        renderer.material.DisableKeyword("_ALPHATEST_ON");
        renderer.material.EnableKeyword("_ALPHABLEND_ON");
        renderer.material.DisableKeyword("_ALPHAPREMULTIPLY_ON");

        // Make it a trigger
        SphereCollider collider = zoneObject.GetComponent<SphereCollider>();
        if (collider != null)
        {
            collider.isTrigger = true;
        }

        // Remove the mesh collider to avoid physics interactions
        Destroy(zoneObject.GetComponent<MeshCollider>());
    }
}
```

## Simulation-Specific Components

### HRI Simulator Component

Create a component to manage HRI simulation:

```csharp
// HRISimulator.cs - Main HRI simulation manager
using UnityEngine;
using System.Collections.Generic;

public class HRISimulator : MonoBehaviour
{
    [Header("Simulation Parameters")]
    public float simulationSpeed = 1.0f;
    public bool enableInteractionLogging = true;

    [Header("Interaction Detection")]
    public float interactionDetectionRange = 3.0f;

    private List<GameObject> robots;
    private List<GameObject> humans;
    private List<InteractionEvent> interactionEvents;

    void Start()
    {
        robots = new List<GameObject>();
        humans = new List<GameObject>();
        interactionEvents = new List<InteractionEvent>();

        FindRobotsAndHumans();
    }

    void Update()
    {
        DetectInteractions();
    }

    void FindRobotsAndHumans()
    {
        // Find all robot and human objects in the scene
        GameObject[] allObjects = GameObject.FindGameObjectsWithTag("Untagged"); // You may want to use tags

        foreach (GameObject obj in allObjects)
        {
            if (obj.GetComponent<RobotModel>() != null)
            {
                robots.Add(obj);
            }
            else if (obj.GetComponent<HumanModel>() != null)
            {
                humans.Add(obj);
            }
        }
    }

    void DetectInteractions()
    {
        foreach (GameObject robot in robots)
        {
            foreach (GameObject human in humans)
            {
                float distance = Vector3.Distance(robot.transform.position, human.transform.position);

                if (distance <= interactionDetectionRange)
                {
                    // Record interaction event
                    if (enableInteractionLogging)
                    {
                        RecordInteraction(robot, human, distance);
                    }
                }
            }
        }
    }

    void RecordInteraction(GameObject robot, GameObject human, float distance)
    {
        InteractionEvent interaction = new InteractionEvent
        {
            robot = robot,
            human = human,
            distance = distance,
            timestamp = Time.time
        };

        interactionEvents.Add(interaction);

        // Limit the number of stored events to prevent memory issues
        if (interactionEvents.Count > 1000)
        {
            interactionEvents.RemoveAt(0);
        }
    }

    [System.Serializable]
    public class InteractionEvent
    {
        public GameObject robot;
        public GameObject human;
        public float distance;
        public float timestamp;
    }
}
```

## Environment Setup

### Basic Environment

Create a simple environment for HRI simulation:

1. **Ground Plane**: A large plane to serve as the floor
2. **Boundary Walls**: Optional walls to contain the simulation
3. **Simple Objects**: Basic shapes to represent furniture or obstacles

```csharp
// EnvironmentSetup.cs - Basic environment for HRI
using UnityEngine;

public class EnvironmentSetup : MonoBehaviour
{
    [Header("Environment Configuration")]
    public float groundSize = 20f;
    public Color groundColor = Color.gray;
    public float wallHeight = 3f;
    public float wallThickness = 0.1f;

    void Start()
    {
        CreateGround();
        CreateBoundaryWalls();
    }

    void CreateGround()
    {
        GameObject ground = GameObject.CreatePrimitive(PrimitiveType.Plane);
        ground.transform.SetParent(transform);
        ground.transform.position = Vector3.zero;
        ground.transform.localScale = Vector3.one * (groundSize / 10); // Plane is 10 units by default

        Renderer groundRenderer = ground.GetComponent<Renderer>();
        groundRenderer.material = new Material(Shader.Find("Unlit/Color"));
        groundRenderer.material.color = groundColor;
    }

    void CreateBoundaryWalls()
    {
        // Create four walls around the perimeter
        CreateWall(new Vector3(0, wallHeight/2, groundSize/2), new Vector3(groundSize, wallThickness, wallHeight));
        CreateWall(new Vector3(0, wallHeight/2, -groundSize/2), new Vector3(groundSize, wallThickness, wallHeight));
        CreateWall(new Vector3(groundSize/2, wallHeight/2, 0), new Vector3(wallThickness, wallThickness, groundSize));
        CreateWall(new Vector3(-groundSize/2, wallHeight/2, 0), new Vector3(wallThickness, wallThickness, groundSize));
    }

    void CreateWall(Vector3 position, Vector3 size)
    {
        GameObject wall = GameObject.CreatePrimitive(PrimitiveType.Cube);
        wall.transform.SetParent(transform);
        wall.transform.position = position;
        wall.transform.localScale = size;

        Renderer wallRenderer = wall.GetComponent<Renderer>();
        wallRenderer.material = new Material(Shader.Find("Unlit/Color"));
        wallRenderer.material.color = Color.white;
    }
}
```

## Performance Optimization for Simulation

### Simulation-Specific Optimizations

1. **Disable Unnecessary Features**:
   - Disable shadows, reflections, and post-processing
   - Use simple materials and shaders
   - Reduce draw call complexity

2. **Physics Optimization**:
   - Use simple collision shapes (spheres, capsules, boxes)
   - Disable physics for static objects
   - Adjust physics settings for simulation rather than realism

3. **Rendering Optimization**:
   - Use simple shaders (Unlit/Color)
   - Reduce texture resolution
   - Disable anti-aliasing and other rendering effects

## Testing the Setup

### Basic Test Scene

Create a simple test scene with:
- One robot model
- One human model
- One interaction zone
- Basic environment

This setup provides a foundation for HRI simulation without complex rendering or game logic, focusing on the simulation aspects as required by the project constraints.

## Summary

This setup provides a simulation-focused Unity environment for HRI research. The configuration prioritizes performance and simulation accuracy over visual quality, which aligns with the project's focus on simulation rather than advanced rendering. The modular component structure allows for easy expansion of HRI scenarios while maintaining the simulation-focused approach.