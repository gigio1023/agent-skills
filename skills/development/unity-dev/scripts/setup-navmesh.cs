// Unity RunCommand: NavMesh Setup & Bake
// Finds the ground object, adds NavMeshSurface, and bakes.
// Modify GROUND_NAME if your ground object has a different name.

using UnityEngine;
using UnityEditor;
using Unity.AI.Navigation;

internal class CommandScript : IRunCommand
{
    const string GROUND_NAME = "Ground"; // Change this to match your ground object

    public void Execute(ExecutionResult result)
    {
        var ground = GameObject.Find(GROUND_NAME);
        if (ground == null)
        {
            result.LogError($"Ground object '{GROUND_NAME}' not found. Change GROUND_NAME constant.");
            return;
        }

        var surface = ground.GetComponent<NavMeshSurface>();
        if (surface == null)
        {
            surface = ground.AddComponent<NavMeshSurface>();
            result.Log("Added NavMeshSurface to " + GROUND_NAME);
        }

        surface.collectObjects = CollectObjects.All;
        surface.BuildNavMesh();
        result.RegisterObjectModification(ground);

        // Verify agents
        var agents = Object.FindObjectsByType<UnityEngine.AI.NavMeshAgent>(FindObjectsSortMode.None);
        int onMesh = 0, offMesh = 0;
        foreach (var a in agents)
        {
            if (a.isOnNavMesh) onMesh++;
            else { offMesh++; result.LogWarning($"Agent '{a.name}' NOT on NavMesh at {a.transform.position}"); }
        }

        result.Log($"NavMesh baked. Agents: {onMesh} on mesh, {offMesh} off mesh.");
    }
}
