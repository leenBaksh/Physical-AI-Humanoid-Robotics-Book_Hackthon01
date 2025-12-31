---
sidebar_position: 25
title: "Unity Concept Diagrams for HRI"
---

# Unity Concept Diagrams for HRI

This section explores how to create and utilize concept diagrams for human-robot interaction (HRI) in Unity environments. These diagrams help visualize interaction scenarios, system components, and behavioral patterns without requiring advanced rendering or complex game logic.

## Understanding Concept Diagrams in HRI

Concept diagrams in HRI serve to visualize:
- Interaction patterns between humans and robots
- System architecture and component relationships
- Behavioral sequences and state transitions
- Spatial relationships and interaction zones

### Key Principles for HRI Concept Diagrams

1. **Clarity**: Diagrams should clearly communicate the intended concept
2. **Simplicity**: Avoid unnecessary complexity while maintaining essential information
3. **Consistency**: Use consistent symbols and representations
4. **Relevance**: Focus on aspects important for HRI simulation

## Types of HRI Concept Diagrams

### 1. Interaction Flow Diagrams

Interaction flow diagrams show the sequence of actions and responses in human-robot interactions.

#### Example: Basic Greeting Interaction
```
[Human approaches robot]
        ↓
[Robot detects human] → [Robot acknowledges] → [Human acknowledges]
        ↓
[Interaction begins] ←→ [Task execution] → [Interaction ends]
```

**Implementation in Unity:**
```csharp
// InteractionFlow.cs - Visualize interaction flow in Unity
using UnityEngine;

public class InteractionFlow : MonoBehaviour
{
    [Header("Flow Visualization")]
    public Color humanColor = Color.green;
    public Color robotColor = Color.blue;
    public Color interactionColor = Color.yellow;
    public float nodeSize = 0.2f;
    public float arrowSize = 0.1f;

    [Header("Flow Nodes")]
    public Transform[] flowNodes;
    public string[] nodeLabels;

    void OnDrawGizmos()
    {
        if (flowNodes == null || flowNodes.Length == 0) return;

        // Draw nodes
        for (int i = 0; i < flowNodes.Length; i++)
        {
            Gizmos.color = interactionColor;
            Gizmos.DrawSphere(flowNodes[i].position, nodeSize);

            // Draw node labels (in a real implementation, you'd use UI elements)
            if (nodeLabels != null && i < nodeLabels.Length)
            {
                // Visualize the label near the node
                Vector3 labelPos = flowNodes[i].position + Vector3.up * 0.5f;
                // Note: Gizmos can't draw text, so this would require a separate text component
            }
        }

        // Draw arrows between nodes
        for (int i = 0; i < flowNodes.Length - 1; i++)
        {
            DrawArrow(flowNodes[i].position, flowNodes[i + 1].position, interactionColor);
        }
    }

    void DrawArrow(Vector3 start, Vector3 end, Color color)
    {
        Gizmos.color = color;
        Gizmos.DrawLine(start, end);

        // Draw arrowhead
        Vector3 direction = (end - start).normalized;
        Vector3 perpendicular = Vector3.Cross(direction, Vector3.up).normalized;

        Vector3 arrowPoint1 = end - direction * arrowSize + perpendicular * arrowSize * 0.5f;
        Vector3 arrowPoint2 = end - direction * arrowSize - perpendicular * arrowSize * 0.5f;

        Gizmos.DrawLine(end, arrowPoint1);
        Gizmos.DrawLine(end, arrowPoint2);
    }
}
```

### 2. Spatial Relationship Diagrams

Spatial relationship diagrams show the positioning and interaction zones between humans and robots.

#### Proxemics Diagram
```
        Public Distance (3.6m+)
┌─────────────────────────────────┐
│                                 │
│        Social Distance          │
│      (1.2m - 3.6m)            │
│  ┌─────────────────────────┐    │
│  │                       │    │
│  │   Personal Distance   │    │
│  │   (0.5m - 1.2m)     │    │
│  │  ┌─────────────────┐  │    │
│  │  │               │  │    │
│  │  │ Intimate Zone │  │    │
│  │  │ (0m - 0.5m) │  │    │
│  │  │               │  │    │
│  │  └─────────────────┘  │    │
│  │                       │    │
│  └─────────────────────────┘    │
│                                 │
└─────────────────────────────────┘
```

**Implementation in Unity:**
```csharp
// SpatialRelationships.cs - Visualize proxemics in Unity
using UnityEngine;

public class SpatialRelationships : MonoBehaviour
{
    [Header("Proxemics Configuration")]
    public float intimateDistance = 0.5f;
    public float personalDistance = 1.2f;
    public float socialDistance = 3.6f;
    public float publicDistance = 7.0f;

    [Header("Zone Colors")]
    public Color intimateColor = new Color(1.0f, 0.0f, 0.0f, 0.2f);  // Red
    public Color personalColor = new Color(1.0f, 0.5f, 0.0f, 0.2f);  // Orange
    public Color socialColor = new Color(1.0f, 1.0f, 0.0f, 0.2f);   // Yellow
    public Color publicColor = new Color(0.0f, 1.0f, 0.0f, 0.2f);   // Green

    void OnDrawGizmos()
    {
        DrawProxemicsZones();
    }

    void DrawProxemicsZones()
    {
        // Draw concentric spheres representing different proxemic zones
        DrawSemiTransparentSphere(intimateDistance, intimateColor);
        DrawSemiTransparentSphere(personalDistance, personalColor);
        DrawSemiTransparentSphere(socialDistance, socialColor);
        DrawSemiTransparentSphere(publicDistance, publicColor);
    }

    void DrawSemiTransparentSphere(float radius, Color color)
    {
        // Create a temporary material for the transparent sphere
        Material tempMaterial = new Material(Shader.Find("Unlit/Color"));
        tempMaterial.color = color;

        // Create a sphere mesh
        Mesh sphereMesh = CreateSphereMesh(radius);

        // Draw the sphere with the transparent material
        Graphics.DrawMesh(sphereMesh, transform.position, Quaternion.identity, tempMaterial, 0);

        // Clean up
        DestroyImmediate(tempMaterial);
        DestroyImmediate(sphereMesh);
    }

    Mesh CreateSphereMesh(float radius)
    {
        // This is a simplified approach - in practice, you'd use a proper sphere mesh
        // For concept visualization, we can use Unity's built-in sphere primitive
        GameObject sphereObject = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        sphereObject.transform.localScale = Vector3.one * radius * 2; // Sphere primitive is 1 unit in size

        MeshFilter meshFilter = sphereObject.GetComponent<MeshFilter>();
        Mesh sphereMesh = Instantiate(meshFilter.mesh); // Clone the mesh

        DestroyImmediate(sphereObject);

        return sphereMesh;
    }
}
```

### 3. System Architecture Diagrams

System architecture diagrams show the components and their relationships in an HRI system.

#### Example: HRI System Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Human Model   │    │  Robot Model    │    │ Interaction     │
│                 │    │                 │    │ Manager         │
│ • Position      │    │ • Position      │    │                 │
│ • Behavior      │    │ • Sensors       │    │ • Proximity     │
│ • State         │    │ • Actuators     │    │ • Gesture       │
│                 │    │ • State         │    │ • Task          │
└─────────────────┘    └─────────────────┘    │ • Communication │
         │                       │              └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Environment   │
                    │                 │
                    │ • Physics       │
                    │ • Obstacles     │
                    │ • Boundaries    │
                    └─────────────────┘
```

**Implementation in Unity:**
```csharp
// SystemArchitecture.cs - Visualize system architecture in Unity
using UnityEngine;
using System.Collections.Generic;

public class SystemArchitecture : MonoBehaviour
{
    [Header("System Components")]
    public Transform humanModel;
    public Transform robotModel;
    public Transform interactionManager;
    public Transform environment;

    [Header("Connection Settings")]
    public Color componentColor = Color.gray;
    public Color connectionColor = Color.cyan;
    public float componentSize = 0.3f;

    private List<Connection> connections;

    void Start()
    {
        InitializeConnections();
    }

    void InitializeConnections()
    {
        connections = new List<Connection>
        {
            new Connection(humanModel, interactionManager),
            new Connection(robotModel, interactionManager),
            new Connection(interactionManager, environment),
            new Connection(humanModel, environment),
            new Connection(robotModel, environment)
        };
    }

    void OnDrawGizmos()
    {
        DrawComponents();
        DrawConnections();
    }

    void DrawComponents()
    {
        Gizmos.color = componentColor;

        if (humanModel != null)
        {
            Gizmos.DrawWireCube(humanModel.position, Vector3.one * componentSize);
        }

        if (robotModel != null)
        {
            Gizmos.DrawWireCube(robotModel.position, Vector3.one * componentSize);
        }

        if (interactionManager != null)
        {
            Gizmos.DrawWireCube(interactionManager.position, Vector3.one * componentSize);
        }

        if (environment != null)
        {
            Gizmos.DrawWireCube(environment.position, Vector3.one * componentSize);
        }
    }

    void DrawConnections()
    {
        Gizmos.color = connectionColor;

        foreach (Connection conn in connections)
        {
            if (conn.from != null && conn.to != null)
            {
                Gizmos.DrawLine(conn.from.position, conn.to.position);
            }
        }
    }

    [System.Serializable]
    public class Connection
    {
        public Transform from;
        public Transform to;

        public Connection(Transform fromTransform, Transform toTransform)
        {
            from = fromTransform;
            to = toTransform;
        }
    }
}
```

### 4. Behavioral State Diagrams

Behavioral state diagrams show the different states a robot can be in during HRI and transitions between states.

#### Example: Robot Interaction States
```
           [Idle]
              ↓
        [Detected Human]
              ↓
    ┌─────────────────┐
    │  Approaching    │ ←──────┐
    │   Human         │        │
    └─────────────────┘        │
              ↓                │
    ┌─────────────────┐        │
    │  Ready for      │ ───────┘
    │  Interaction    │
    └─────────────────┘
              ↓
    ┌─────────────────┐
    │  Engaging       │
    │  Interaction    │
    └─────────────────┘
              ↓
    ┌─────────────────┐
    │  Completing     │
    │  Interaction    │
    └─────────────────┘
              ↓
         [Idle] (or back to [Detected Human] for ongoing interaction)
```

**Implementation in Unity:**
```csharp
// BehavioralStates.cs - Visualize behavioral states in Unity
using UnityEngine;
using System.Collections.Generic;

public class BehavioralStates : MonoBehaviour
{
    [Header("State Configuration")]
    public float stateNodeSize = 0.4f;
    public Color stateColor = Color.blue;
    public Color transitionColor = Color.yellow;

    [Header("State Positions")]
    public Transform idleState;
    public Transform detectedState;
    public Transform approachingState;
    public Transform readyState;
    public Transform engagingState;
    public Transform completingState;

    private Dictionary<RobotState, Transform> statePositions;
    private List<StateTransition> transitions;

    public enum RobotState
    {
        Idle,
        DetectedHuman,
        Approaching,
        ReadyForInteraction,
        Engaging,
        Completing
    }

    void Start()
    {
        InitializeStatePositions();
        InitializeTransitions();
    }

    void InitializeStatePositions()
    {
        statePositions = new Dictionary<RobotState, Transform>
        {
            { RobotState.Idle, idleState },
            { RobotState.DetectedHuman, detectedState },
            { RobotState.Approaching, approachingState },
            { RobotState.ReadyForInteraction, readyState },
            { RobotState.Engaging, engagingState },
            { RobotState.Completing, completingState }
        };
    }

    void InitializeTransitions()
    {
        transitions = new List<StateTransition>
        {
            new StateTransition(RobotState.Idle, RobotState.DetectedHuman),
            new StateTransition(RobotState.DetectedHuman, RobotState.Approaching),
            new StateTransition(RobotState.Approaching, RobotState.ReadyForInteraction),
            new StateTransition(RobotState.ReadyForInteraction, RobotState.Engaging),
            new StateTransition(RobotState.Engaging, RobotState.Completing),
            new StateTransition(RobotState.Completing, RobotState.Idle),
            // Loop back for ongoing interactions
            new StateTransition(RobotState.Approaching, RobotState.DetectedHuman) // Back to detected if needed
        };
    }

    void OnDrawGizmos()
    {
        DrawStateNodes();
        DrawTransitions();
    }

    void DrawStateNodes()
    {
        Gizmos.color = stateColor;

        foreach (var kvp in statePositions)
        {
            if (kvp.Value != null)
            {
                Gizmos.DrawWireSphere(kvp.Value.position, stateNodeSize);
            }
        }
    }

    void DrawTransitions()
    {
        Gizmos.color = transitionColor;

        foreach (StateTransition transition in transitions)
        {
            if (statePositions.ContainsKey(transition.from) &&
                statePositions.ContainsKey(transition.to))
            {
                Transform fromPos = statePositions[transition.from];
                Transform toPos = statePositions[transition.to];

                if (fromPos != null && toPos != null)
                {
                    DrawArrow(fromPos.position, toPos.position, transitionColor);
                }
            }
        }
    }

    void DrawArrow(Vector3 start, Vector3 end, Color color)
    {
        Gizmos.color = color;
        Gizmos.DrawLine(start, end);

        // Draw arrowhead
        Vector3 direction = (end - start).normalized;
        Vector3 perpendicular = Vector3.Cross(direction, Vector3.up).normalized;

        Vector3 arrowPoint1 = end - direction * 0.1f + perpendicular * 0.05f;
        Vector3 arrowPoint2 = end - direction * 0.1f - perpendicular * 0.05f;

        Gizmos.DrawLine(end, arrowPoint1);
        Gizmos.DrawLine(end, arrowPoint2);
    }

    [System.Serializable]
    public class StateTransition
    {
        public RobotState from;
        public RobotState to;

        public StateTransition(RobotState fromState, RobotState toState)
        {
            from = fromState;
            to = toState;
        }
    }
}
```

## Creating Concept Diagrams in Unity

### 1. Using Gizmos for Visualization

Gizmos are excellent for creating concept diagrams directly in the Unity editor:

```csharp
// ConceptDiagram.cs - Base class for concept diagrams
using UnityEngine;

public abstract class ConceptDiagram : MonoBehaviour
{
    [Header("Diagram Settings")]
    public bool showDiagram = true;
    public Color diagramColor = Color.white;
    public float diagramScale = 1.0f;

    protected virtual void OnDrawGizmos()
    {
        if (!showDiagram) return;

        Gizmos.color = diagramColor;
        DrawDiagram();
    }

    protected abstract void DrawDiagram();

    protected void DrawText(string text, Vector3 position)
    {
        // Note: Gizmos can't draw text directly
        // You would need to use a separate text component or custom solution
    }

    protected void DrawArrow(Vector3 start, Vector3 end, Color color)
    {
        Gizmos.color = color;
        Gizmos.DrawLine(start, end);

        // Simple arrowhead
        Vector3 direction = (end - start).normalized;
        Vector3 arrowPoint1 = end - direction * 0.1f + Vector3.Cross(direction, Vector3.up) * 0.05f;
        Vector3 arrowPoint2 = end - direction * 0.1f - Vector3.Cross(direction, Vector3.up) * 0.05f;

        Gizmos.DrawLine(end, arrowPoint1);
        Gizmos.DrawLine(end, arrowPoint2);
    }
}
```

### 2. Using UI Elements for Complex Diagrams

For more complex diagrams, UI elements can provide better visualization:

```csharp
// UIDiagram.cs - Create concept diagrams using UI elements
using UnityEngine;
using UnityEngine.UI;

public class UIDiagram : MonoBehaviour
{
    [Header("UI Diagram Settings")]
    public Canvas canvas;
    public GameObject nodePrefab;
    public GameObject connectionPrefab;

    private RectTransform diagramContainer;

    void Start()
    {
        CreateDiagramContainer();
        CreateExampleDiagram();
    }

    void CreateDiagramContainer()
    {
        GameObject containerObj = new GameObject("DiagramContainer");
        diagramContainer = containerObj.AddComponent<RectTransform>();
        diagramContainer.SetParent(canvas.transform, false);
        diagramContainer.sizeDelta = new Vector2(800, 600);
        diagramContainer.anchoredPosition = Vector2.zero;
    }

    void CreateExampleDiagram()
    {
        // Create nodes
        RectTransform node1 = CreateNode("Human", new Vector2(-200, 0));
        RectTransform node2 = CreateNode("Robot", new Vector2(200, 0));

        // Create connection
        CreateConnection(node1, node2, "Interaction");
    }

    RectTransform CreateNode(string name, Vector2 position)
    {
        GameObject nodeObj = Instantiate(nodePrefab);
        RectTransform nodeTransform = nodeObj.GetComponent<RectTransform>();
        nodeTransform.SetParent(diagramContainer, false);
        nodeTransform.anchoredPosition = position;

        // Set node name
        Text nodeName = nodeObj.GetComponentInChildren<Text>();
        if (nodeName != null)
        {
            nodeName.text = name;
        }

        return nodeTransform;
    }

    void CreateConnection(RectTransform from, RectTransform to, string label)
    {
        GameObject connectionObj = Instantiate(connectionPrefab);
        RectTransform connectionTransform = connectionObj.GetComponent<RectTransform>();
        connectionTransform.SetParent(diagramContainer, false);

        // Position connection between the two nodes
        Vector2 center = (from.anchoredPosition + to.anchoredPosition) / 2;
        connectionTransform.anchoredPosition = center;

        // Additional connection setup would go here
    }
}
```

## Best Practices for Concept Diagrams

### 1. Keep It Simple
- Focus on essential elements
- Avoid cluttering with unnecessary details
- Use consistent visual representations

### 2. Make It Meaningful
- Ensure diagrams represent actual system behavior
- Align diagrams with simulation goals
- Focus on HRI-relevant aspects

### 3. Use Appropriate Tools
- Use Gizmos for simple editor visualization
- Use UI elements for complex diagrams
- Consider external tools for publication-quality diagrams

### 4. Document Clearly
- Include legends when necessary
- Use consistent labeling
- Provide context for the diagrams

## Summary

Concept diagrams are essential tools for visualizing human-robot interaction scenarios in Unity. They help clarify system design, interaction patterns, and behavioral states without requiring complex rendering or game logic. By using Unity's visualization tools like Gizmos and UI elements, you can create meaningful concept diagrams that enhance understanding of HRI systems. The examples provided demonstrate how to create different types of diagrams while maintaining the simulation-focused approach required by the project constraints.