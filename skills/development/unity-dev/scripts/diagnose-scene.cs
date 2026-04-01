// Unity RunCommand: Scene Diagnostic
// Copy-paste into Unity_RunCommand to diagnose common scene issues.
// Output goes to console log, not context window.

using UnityEngine;
using UnityEditor;
using UnityEngine.AI;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        result.Log("=== SCENE DIAGNOSTIC ===");

        // 1. NavMesh Agents
        var agents = Object.FindObjectsByType<NavMeshAgent>(FindObjectsSortMode.None);
        result.Log($"NavMeshAgents: {agents.Length}");
        foreach (var a in agents)
            result.Log($"  {a.name}: onNavMesh={a.isOnNavMesh}, pos={a.transform.position}, pathStatus={a.pathStatus}");

        // 2. Triggers (need Rigidbody?)
        var colliders = Object.FindObjectsByType<Collider>(FindObjectsSortMode.None);
        int triggerCount = 0;
        foreach (var c in colliders)
        {
            if (!c.isTrigger) continue;
            triggerCount++;
            var rb = c.GetComponent<Rigidbody>();
            if (rb == null)
                result.LogWarning($"  Trigger '{c.name}' has NO Rigidbody — OnTriggerEnter won't fire!");
            else
                result.Log($"  Trigger '{c.name}': Rigidbody(kinematic={rb.isKinematic})");
        }
        result.Log($"Triggers: {triggerCount}");

        // 3. Canvas
        var canvases = Object.FindObjectsByType<Canvas>(FindObjectsSortMode.None);
        result.Log($"Canvases: {canvases.Length}");
        foreach (var c in canvases)
            result.Log($"  {c.name}: renderMode={c.renderMode}, sortOrder={c.sortingOrder}, active={c.gameObject.activeInHierarchy}");

        // 4. Camera
        var cameras = Object.FindObjectsByType<Camera>(FindObjectsSortMode.None);
        result.Log($"Cameras: {cameras.Length}");
        foreach (var cam in cameras)
            result.Log($"  {cam.name}: tag={cam.tag}, enabled={cam.enabled}, depth={cam.depth}");

        // 5. Input System
        var settings = AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/ProjectSettings.asset");
        if (settings.Length > 0)
        {
            var so = new SerializedObject(settings[0]);
            var prop = so.FindProperty("activeInputHandler");
            string[] modes = { "Legacy", "New Input System", "Both" };
            int mode = prop.intValue;
            result.Log($"Input Handling: {(mode < modes.Length ? modes[mode] : "Unknown")} ({mode})");
        }

        // 6. CharacterController
        var ccs = Object.FindObjectsByType<CharacterController>(FindObjectsSortMode.None);
        foreach (var cc in ccs)
            result.Log($"CharacterController '{cc.name}': grounded={cc.isGrounded}, pos={cc.transform.position}");

        // 7. Missing components
        var allGOs = Object.FindObjectsByType<GameObject>(FindObjectsSortMode.None);
        int missingCount = 0;
        foreach (var go in allGOs)
        {
            var comps = go.GetComponents<Component>();
            foreach (var c in comps)
                if (c == null) { missingCount++; result.LogWarning($"  Missing component on '{go.name}'"); }
        }
        result.Log($"Missing components: {missingCount}");

        result.Log("=== DIAGNOSTIC COMPLETE ===");
    }
}
