---
sidebar_position: 24
title: "Interaction Scenarios in Unity"
---

# Interaction Scenarios in Unity

This section covers how to create and simulate human-robot interaction scenarios in Unity, focusing on simulation rather than advanced rendering or game logic. We'll explore various types of interactions and how to implement them in a simulation environment.

## Types of Interaction Scenarios

### 1. Proximity-Based Interactions

Proximity-based interactions occur when humans and robots come within certain distances of each other. These are fundamental to HRI and can be easily simulated.

#### Implementation Approach

```csharp
// ProximityInteraction.cs - Basic proximity detection
using UnityEngine;
using System.Collections.Generic;

public class ProximityInteraction : MonoBehaviour
{
    [Header("Interaction Settings")]
    public float detectionRadius = 3.0f;
    public float communicationRadius = 1.5f;
    public float safeDistance = 0.5f;

    [Header("Interaction Types")]
    public bool enableProximityAlert = true;
    public bool enableCommunication = true;
    public bool enableSafety = true;

    private List<GameObject> nearbyHumans;
    private List<GameObject> nearbyRobots;

    void Start()
    {
        nearbyHumans = new List<GameObject>();
        nearbyRobots = new List<GameObject>();
    }

    void Update()
    {
        DetectNearbyAgents();
    }

    void DetectNearbyAgents()
    {
        nearbyHumans.Clear();
        nearbyRobots.Clear();

        Collider[] nearbyColliders = Physics.OverlapSphere(transform.position, detectionRadius);

        foreach (Collider collider in nearbyColliders)
        {
            if (collider.CompareTag("Human"))
            {
                nearbyHumans.Add(collider.gameObject);
            }
            else if (collider.CompareTag("Robot"))
            {
                nearbyRobots.Add(collider.gameObject);
            }
        }

        HandleInteractions();
    }

    void HandleInteractions()
    {
        foreach (GameObject human in nearbyHumans)
        {
            float distance = Vector3.Distance(transform.position, human.transform.position);

            if (enableProximityAlert && distance <= detectionRadius)
            {
                OnProximityDetected(human, distance);
            }

            if (enableCommunication && distance <= communicationRadius)
            {
                OnCommunicationRange(human, distance);
            }

            if (enableSafety && distance <= safeDistance)
            {
                OnSafetyViolation(human, distance);
            }
        }
    }

    void OnProximityDetected(GameObject human, float distance)
    {
        // Handle general proximity detection
        Debug.Log($"Proximity detected: Human at {distance:F2}m");
    }

    void OnCommunicationRange(GameObject human, float distance)
    {
        // Handle communication-specific behavior
        Debug.Log($"Communication range: Human at {distance:F2}m");
    }

    void OnSafetyViolation(GameObject human, float distance)
    {
        // Handle safety violation
        Debug.Log($"Safety violation: Human too close at {distance:F2}m");
    }

    void OnDrawGizmos()
    {
        // Visualize detection zones in the editor
        Gizmos.color = Color.yellow;
        Gizmos.DrawWireSphere(transform.position, detectionRadius);

        Gizmos.color = Color.green;
        Gizmos.DrawWireSphere(transform.position, communicationRadius);

        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, safeDistance);
    }
}
```

### 2. Gesture-Based Interactions

Gesture-based interactions involve humans using body movements to communicate with robots.

#### Implementation Approach

```csharp
// GestureInteraction.cs - Basic gesture recognition
using UnityEngine;
using System.Collections.Generic;

public class GestureInteraction : MonoBehaviour
{
    [Header("Gesture Settings")]
    public float gestureRecognitionDistance = 2.0f;
    public float gestureDurationThreshold = 0.5f;
    public float gestureVelocityThreshold = 1.0f;

    [Header("Gesture Types")]
    public bool recognizeWave = true;
    public bool recognizePoint = true;
    public bool recognizeStop = true;

    private Dictionary<GameObject, GestureTracker> gestureTrackers;

    void Start()
    {
        gestureTrackers = new Dictionary<GameObject, GestureTracker>();
    }

    void Update()
    {
        UpdateGestureTracking();
    }

    void UpdateGestureTracking()
    {
        Collider[] nearbyHumans = Physics.OverlapSphere(transform.position, gestureRecognitionDistance);

        foreach (Collider humanCollider in nearbyHumans)
        {
            GameObject human = humanCollider.gameObject;

            if (!gestureTrackers.ContainsKey(human))
            {
                gestureTrackers[human] = new GestureTracker(human);
            }

            GestureTracker tracker = gestureTrackers[human];
            tracker.UpdateTracking();

            if (tracker.IsGestureComplete())
            {
                ProcessGesture(human, tracker.GetCurrentGesture());
                tracker.Reset();
            }
        }
    }

    void ProcessGesture(GameObject human, GestureType gesture)
    {
        switch (gesture)
        {
            case GestureType.Wave:
                if (recognizeWave)
                    OnWaveGesture(human);
                break;
            case GestureType.Point:
                if (recognizePoint)
                    OnPointGesture(human);
                break;
            case GestureType.Stop:
                if (recognizeStop)
                    OnStopGesture(human);
                break;
        }
    }

    void OnWaveGesture(GameObject human)
    {
        Debug.Log($"Wave gesture detected from {human.name}");
        // Handle wave gesture (e.g., acknowledge greeting)
    }

    void OnPointGesture(GameObject human)
    {
        Debug.Log($"Point gesture detected from {human.name}");
        // Handle point gesture (e.g., follow direction)
    }

    void OnStopGesture(GameObject human)
    {
        Debug.Log($"Stop gesture detected from {human.name}");
        // Handle stop gesture (e.g., pause robot movement)
    }

    void OnDrawGizmos()
    {
        Gizmos.color = Color.cyan;
        Gizmos.DrawWireSphere(transform.position, gestureRecognitionDistance);
    }

    public enum GestureType
    {
        None,
        Wave,
        Point,
        Stop
    }

    public class GestureTracker
    {
        private GameObject human;
        private Vector3 previousPosition;
        private float gestureStartTime;
        private float gestureDuration;
        private Vector3 gestureDirection;
        private GestureType currentGesture;

        public GestureTracker(GameObject humanObject)
        {
            human = humanObject;
            Reset();
        }

        public void UpdateTracking()
        {
            Vector3 currentPosition = human.transform.position;

            if (previousPosition != Vector3.zero)
            {
                Vector3 velocity = (currentPosition - previousPosition) / Time.deltaTime;

                if (velocity.magnitude > gestureVelocityThreshold)
                {
                    if (gestureStartTime == 0)
                    {
                        gestureStartTime = Time.time;
                        gestureDirection = velocity.normalized;
                    }

                    gestureDuration = Time.time - gestureStartTime;
                }
                else
                {
                    // Reset if no significant movement
                    if (gestureDuration > 0 && gestureDuration < gestureDurationThreshold)
                    {
                        // Too short to be a gesture
                        Reset();
                    }
                }
            }

            previousPosition = currentPosition;
        }

        public bool IsGestureComplete()
        {
            return gestureDuration >= gestureDurationThreshold;
        }

        public GestureType GetCurrentGesture()
        {
            // Simple gesture recognition based on movement pattern
            if (gestureDuration >= gestureDurationThreshold)
            {
                // Determine gesture type based on movement pattern
                if (Mathf.Abs(gestureDirection.y) > Mathf.Abs(gestureDirection.x) &&
                    Mathf.Abs(gestureDirection.y) > Mathf.Abs(gestureDirection.z))
                {
                    // Vertical movement - could be wave
                    return GestureType.Wave;
                }
                else if (gestureDirection.magnitude > 0.5f)
                {
                    // Horizontal movement - could be point or stop
                    return GestureType.Point;
                }
            }

            return GestureType.None;
        }

        public void Reset()
        {
            gestureStartTime = 0;
            gestureDuration = 0;
            gestureDirection = Vector3.zero;
            currentGesture = GestureType.None;
            previousPosition = Vector3.zero;
        }
    }
}
```

### 3. Task-Based Interactions

Task-based interactions involve humans and robots working together on specific tasks.

#### Implementation Approach

```csharp
// TaskInteraction.cs - Basic task coordination
using UnityEngine;
using System.Collections.Generic;

public class TaskInteraction : MonoBehaviour
{
    [Header("Task Settings")]
    public float taskCompletionDistance = 1.0f;
    public float taskTimeout = 30.0f;

    [Header("Task Types")]
    public bool enableNavigation = true;
    public bool enableObjectTransfer = true;
    public bool enableInformationSharing = true;

    private List<ActiveTask> activeTasks;

    void Start()
    {
        activeTasks = new List<ActiveTask>();
    }

    void Update()
    {
        UpdateActiveTasks();
    }

    public void CreateNavigationTask(GameObject human, Vector3 targetPosition)
    {
        if (enableNavigation)
        {
            ActiveTask task = new ActiveTask
            {
                taskType = TaskType.Navigation,
                human = human,
                robot = this.gameObject,
                targetPosition = targetPosition,
                startTime = Time.time,
                status = TaskStatus.Assigned
            };

            activeTasks.Add(task);
        }
    }

    public void CreateObjectTransferTask(GameObject human, GameObject objectToTransfer)
    {
        if (enableObjectTransfer)
        {
            ActiveTask task = new ActiveTask
            {
                taskType = TaskType.ObjectTransfer,
                human = human,
                robot = this.gameObject,
                objectToTransfer = objectToTransfer,
                startTime = Time.time,
                status = TaskStatus.Assigned
            };

            activeTasks.Add(task);
        }
    }

    void UpdateActiveTasks()
    {
        for (int i = activeTasks.Count - 1; i >= 0; i--)
        {
            ActiveTask task = activeTasks[i];

            // Check for timeout
            if (Time.time - task.startTime > taskTimeout)
            {
                task.status = TaskStatus.Failed;
                OnTaskFailed(task);
                activeTasks.RemoveAt(i);
                continue;
            }

            // Update task progress based on type
            switch (task.taskType)
            {
                case TaskType.Navigation:
                    UpdateNavigationTask(task);
                    break;
                case TaskType.ObjectTransfer:
                    UpdateObjectTransferTask(task);
                    break;
            }

            // Check if task is complete
            if (task.status == TaskStatus.Complete)
            {
                OnTaskCompleted(task);
                activeTasks.RemoveAt(i);
            }
        }
    }

    void UpdateNavigationTask(ActiveTask task)
    {
        float distance = Vector3.Distance(this.transform.position, task.targetPosition);

        if (distance <= taskCompletionDistance)
        {
            task.status = TaskStatus.Complete;
        }
    }

    void UpdateObjectTransferTask(ActiveTask task)
    {
        if (task.objectToTransfer != null)
        {
            float distance = Vector3.Distance(this.transform.position, task.objectToTransfer.transform.position);

            if (distance <= taskCompletionDistance)
            {
                task.status = TaskStatus.Complete;
            }
        }
    }

    void OnTaskCompleted(ActiveTask task)
    {
        Debug.Log($"Task completed: {task.taskType} for {task.human.name}");

        switch (task.taskType)
        {
            case TaskType.Navigation:
                OnNavigationCompleted(task);
                break;
            case TaskType.ObjectTransfer:
                OnObjectTransferCompleted(task);
                break;
        }
    }

    void OnTaskFailed(ActiveTask task)
    {
        Debug.Log($"Task failed: {task.taskType} for {task.human.name}");
    }

    void OnNavigationCompleted(ActiveTask task)
    {
        Debug.Log($"Navigation task completed successfully");
        // Additional navigation-specific completion logic
    }

    void OnObjectTransferCompleted(ActiveTask task)
    {
        Debug.Log($"Object transfer task completed successfully");
        // Additional object transfer-specific completion logic
    }

    public enum TaskType
    {
        Navigation,
        ObjectTransfer,
        InformationSharing
    }

    public enum TaskStatus
    {
        Assigned,
        InProgress,
        Complete,
        Failed
    }

    public class ActiveTask
    {
        public TaskType taskType;
        public GameObject human;
        public GameObject robot;
        public Vector3 targetPosition;
        public GameObject objectToTransfer;
        public float startTime;
        public TaskStatus status;
    }
}
```

### 4. Communication-Based Interactions

Communication-based interactions involve information exchange between humans and robots.

#### Implementation Approach

```csharp
// CommunicationInteraction.cs - Basic communication handling
using UnityEngine;
using System.Collections.Generic;

public class CommunicationInteraction : MonoBehaviour
{
    [Header("Communication Settings")]
    public float communicationRange = 3.0f;
    public float messageTimeout = 10.0f;

    [Header("Communication Types")]
    public bool enableTextCommunication = true;
    public bool enableStatusCommunication = true;
    public bool enableRequestCommunication = true;

    private List<CommunicationMessage> activeMessages;
    private Queue<CommunicationMessage> messageQueue;

    void Start()
    {
        activeMessages = new List<CommunicationMessage>();
        messageQueue = new Queue<CommunicationMessage>();
    }

    void Update()
    {
        ProcessMessageQueue();
        UpdateActiveMessages();
    }

    public void SendMessage(GameObject recipient, string message, CommunicationType type)
    {
        CommunicationMessage msg = new CommunicationMessage
        {
            sender = this.gameObject,
            recipient = recipient,
            message = message,
            type = type,
            timestamp = Time.time,
            status = MessageStatus.Sent
        };

        messageQueue.Enqueue(msg);
    }

    public void SendStatusUpdate(GameObject recipient, string statusMessage)
    {
        if (enableStatusCommunication)
        {
            SendMessage(recipient, statusMessage, CommunicationType.Status);
        }
    }

    public void SendRequest(GameObject recipient, string requestMessage)
    {
        if (enableRequestCommunication)
        {
            SendMessage(recipient, requestMessage, CommunicationType.Request);
        }
    }

    void ProcessMessageQueue()
    {
        while (messageQueue.Count > 0)
        {
            CommunicationMessage msg = messageQueue.Dequeue();

            if (IsInRange(msg.recipient, communicationRange))
            {
                activeMessages.Add(msg);
                OnMessageReceived(msg);
            }
        }
    }

    void UpdateActiveMessages()
    {
        for (int i = activeMessages.Count - 1; i >= 0; i--)
        {
            CommunicationMessage msg = activeMessages[i];

            if (Time.time - msg.timestamp > messageTimeout)
            {
                activeMessages.RemoveAt(i);
                continue;
            }

            // Check if message has been acknowledged
            if (msg.status == MessageStatus.Acknowledged)
            {
                activeMessages.RemoveAt(i);
            }
        }
    }

    bool IsInRange(GameObject target, float range)
    {
        if (target == null) return false;
        return Vector3.Distance(transform.position, target.transform.position) <= range;
    }

    void OnMessageReceived(CommunicationMessage message)
    {
        Debug.Log($"Message received: {message.message} (Type: {message.type})");

        switch (message.type)
        {
            case CommunicationType.Request:
                HandleRequest(message);
                break;
            case CommunicationType.Status:
                HandleStatus(message);
                break;
            case CommunicationType.Information:
                HandleInformation(message);
                break;
        }
    }

    void HandleRequest(CommunicationMessage message)
    {
        Debug.Log($"Handling request: {message.message}");
        // Process the request and potentially send a response
        SendResponse(message.sender, "Request received and processing", CommunicationType.Information);
    }

    void HandleStatus(CommunicationMessage message)
    {
        Debug.Log($"Received status: {message.message}");
        // Update internal state based on status
    }

    void HandleInformation(CommunicationMessage message)
    {
        Debug.Log($"Received information: {message.message}");
        // Process informational message
    }

    void SendResponse(GameObject recipient, string response, CommunicationType responseType)
    {
        SendMessage(recipient, response, responseType);
    }

    public enum CommunicationType
    {
        Request,
        Status,
        Information
    }

    public enum MessageStatus
    {
        Sent,
        Received,
        Acknowledged,
        Failed
    }

    public class CommunicationMessage
    {
        public GameObject sender;
        public GameObject recipient;
        public string message;
        public CommunicationType type;
        public float timestamp;
        public MessageStatus status;
    }
}
```

## Scenario Implementation Example

Here's how to combine multiple interaction types into a complete scenario:

```csharp
// HRI_Scenario.cs - Complete HRI scenario implementation
using UnityEngine;

public class HRIScenario : MonoBehaviour
{
    [Header("Scenario Configuration")]
    public Transform humanSpawnPoint;
    public Transform robotSpawnPoint;
    public float scenarioDuration = 60.0f;

    [Header("Interaction Components")]
    public ProximityInteraction proximityComponent;
    public GestureInteraction gestureComponent;
    public TaskInteraction taskComponent;
    public CommunicationInteraction communicationComponent;

    private bool scenarioActive = false;
    private float scenarioStartTime;

    void Start()
    {
        InitializeScenario();
    }

    void Update()
    {
        if (scenarioActive)
        {
            UpdateScenario();
        }
    }

    void InitializeScenario()
    {
        // Spawn human and robot at designated points
        GameObject human = SpawnHuman(humanSpawnPoint.position);
        GameObject robot = SpawnRobot(robotSpawnPoint.position);

        // Attach interaction components
        proximityComponent = robot.AddComponent<ProximityInteraction>();
        gestureComponent = robot.AddComponent<GestureInteraction>();
        taskComponent = robot.AddComponent<TaskInteraction>();
        communicationComponent = robot.AddComponent<CommunicationInteraction>();

        scenarioActive = true;
        scenarioStartTime = Time.time;
    }

    GameObject SpawnHuman(Vector3 position)
    {
        GameObject human = new GameObject("Human");
        human.transform.position = position;
        human.tag = "Human";

        // Add basic human model components
        HumanModel humanModel = human.AddComponent<HumanModel>();
        humanModel.height = 1.7f;
        humanModel.radius = 0.15f;
        humanModel.humanColor = Color.green;

        return human;
    }

    GameObject SpawnRobot(Vector3 position)
    {
        GameObject robot = new GameObject("Robot");
        robot.transform.position = position;
        robot.tag = "Robot";

        // Add basic robot model components
        RobotModel robotModel = robot.AddComponent<RobotModel>();
        robotModel.height = 1.7f;
        robotModel.radius = 0.2f;
        robotModel.robotColor = Color.blue;

        return robot;
    }

    void UpdateScenario()
    {
        float elapsed = Time.time - scenarioStartTime;

        if (elapsed >= scenarioDuration)
        {
            EndScenario();
            return;
        }

        // Execute scenario-specific behaviors
        ExecuteScenarioBehaviors(elapsed);
    }

    void ExecuteScenarioBehaviors(float elapsed)
    {
        // Example: Simple scenario where robot approaches human
        GameObject human = GameObject.FindGameObjectWithTag("Human");
        GameObject robot = GameObject.FindGameObjectWithTag("Robot");

        if (human != null && robot != null)
        {
            // Move robot toward human at a controlled pace
            Vector3 direction = (human.transform.position - robot.transform.position).normalized;
            robot.transform.position += direction * Time.deltaTime * 0.5f; // Slow approach
        }
    }

    void EndScenario()
    {
        scenarioActive = false;
        Debug.Log("HRI scenario completed");
    }
}
```

## Best Practices for HRI Scenarios

### 1. Safety Considerations
- Always implement safety zones and distance limits
- Include emergency stop capabilities
- Test scenarios thoroughly before implementation

### 2. Realism vs. Simplicity
- Balance realistic behavior with computational efficiency
- Focus on essential interaction patterns
- Avoid over-complicating scenarios

### 3. Scalability
- Design scenarios that can be extended
- Use modular components for easy modification
- Consider multiple humans and robots

### 4. Evaluation
- Include metrics for scenario success
- Log interaction data for analysis
- Provide visualization for debugging

## Summary

This section covered various types of human-robot interaction scenarios that can be implemented in Unity simulation environments. The implementations focus on simulation aspects rather than advanced rendering or game logic, following the project constraints. The examples provide a foundation for creating more complex HRI scenarios while maintaining the simulation-focused approach. By combining different interaction types (proximity, gesture, task, communication), you can create rich and meaningful HRI experiences in the Unity simulation environment.