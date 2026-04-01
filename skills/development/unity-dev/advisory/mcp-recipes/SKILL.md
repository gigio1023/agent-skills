---
name: unity-mcp-recipes
description: "Battle-tested MCP recipes for common Unity tasks. Use when building scenes, wiring components, baking NavMesh, setting up UI, fixing Input System issues, or any hands-on Unity MCP operation."
---

# Unity MCP Recipes

Proven RunCommand and MCP patterns from real project experience. Copy-paste ready.

---

## Recipe 1: Full Scene Setup (Batch)

Create an entire scene hierarchy in one RunCommand instead of 20+ individual MCP calls.

```csharp
using UnityEngine;
using UnityEditor;
using Unity.AI.Navigation;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        // Ground
        var ground = GameObject.CreatePrimitive(PrimitiveType.Cube);
        ground.name = "Ground";
        ground.transform.position = new Vector3(0, -0.5f, 0);
        ground.transform.localScale = new Vector3(30, 1, 30);
        ground.isStatic = true;

        // NavMesh
        var surface = ground.AddComponent<NavMeshSurface>();
        surface.collectObjects = CollectObjects.All;

        // Building (visual only — no collider blocks NavMesh)
        var building = GameObject.CreatePrimitive(PrimitiveType.Cube);
        building.name = "Building";
        building.transform.position = new Vector3(0, 2, 8);
        building.transform.localScale = new Vector3(10, 4, 8);
        Object.DestroyImmediate(building.GetComponent<BoxCollider>()); // visual only

        // Player
        var player = GameObject.CreatePrimitive(PrimitiveType.Capsule);
        player.name = "Player";
        player.tag = "Player";
        player.transform.position = new Vector3(0, 0, 0);
        player.AddComponent<CharacterController>();

        // Camera (child of player)
        var cam = new GameObject("MainCamera");
        cam.tag = "MainCamera";
        cam.AddComponent<Camera>();
        cam.transform.SetParent(player.transform);
        cam.transform.localPosition = new Vector3(0, 0.6f, 0); // eye level

        // Bake NavMesh last (after all colliders placed)
        surface.BuildNavMesh();

        result.RegisterObjectCreation(ground);
        result.RegisterObjectCreation(building);
        result.RegisterObjectCreation(player);
        result.Log("Scene created with ground, building, player, camera, NavMesh");
    }
}
```

---

## Recipe 2: Wire SerializedObject References

Wire component references that can't be set via ManageGameObject.

```csharp
using UnityEngine;
using UnityEditor;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        // Example: wire patrol waypoints to a component
        var npc = GameObject.Find("NPC_Police");
        var comp = npc.GetComponent<MyNamespace.PoliceController>();
        var wpA = GameObject.Find("WaypointA");
        var wpB = GameObject.Find("WaypointB");

        var so = new SerializedObject(comp);
        var prop = so.FindProperty("patrolPoints");
        prop.arraySize = 2;
        prop.GetArrayElementAtIndex(0).objectReferenceValue = wpA.transform;
        prop.GetArrayElementAtIndex(1).objectReferenceValue = wpB.transform;
        so.ApplyModifiedProperties();

        result.RegisterObjectModification(npc);
        result.Log("Wired patrol waypoints");
    }
}
```

---

## Recipe 3: Create Full UI Canvas with TMP

```csharp
using UnityEngine;
using UnityEngine.UI;
using UnityEditor;
using TMPro;
using UImage = UnityEngine.UI.Image; // avoid namespace conflict

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        var canvas = new GameObject("HUD");
        canvas.AddComponent<Canvas>().renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.AddComponent<CanvasScaler>().uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
        canvas.AddComponent<GraphicRaycaster>();

        // Text element
        var label = new GameObject("Label");
        label.transform.SetParent(canvas.transform, false);
        var tmp = label.AddComponent<TextMeshProUGUI>();
        tmp.text = "Hello";
        tmp.fontSize = 24;
        var rect = label.GetComponent<RectTransform>();
        rect.anchorMin = new Vector2(0.4f, 0.9f);
        rect.anchorMax = new Vector2(0.6f, 1f);

        // Slider
        var sliderGo = new GameObject("Bar");
        sliderGo.transform.SetParent(canvas.transform, false);
        var slider = sliderGo.AddComponent<Slider>();
        // ... (add fill rect child hierarchy)

        // Panel with Image background
        var panel = new GameObject("Panel");
        panel.transform.SetParent(canvas.transform, false);
        panel.AddComponent<UImage>().color = new Color(0, 0, 0, 0.8f);
        panel.SetActive(false); // hidden by default

        result.RegisterObjectCreation(canvas);
        result.Log("UI Canvas created");
    }
}
```

**Key: Use `UImage = UnityEngine.UI.Image` alias to avoid namespace conflict with System.Drawing.Image.**

---

## Recipe 4: NavMesh Bake

```csharp
using UnityEngine;
using UnityEditor;
using Unity.AI.Navigation;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        var ground = GameObject.Find("Ground");
        var surface = ground.GetComponent<NavMeshSurface>();
        if (surface == null)
            surface = ground.AddComponent<NavMeshSurface>();

        surface.collectObjects = CollectObjects.All;
        surface.BuildNavMesh();

        result.RegisterObjectModification(ground);
        result.Log("NavMesh baked on Ground");
    }
}
```

**After baking, verify NPCs are on NavMesh:**
```
Unity_ManageGameObject → get_components → check NavMeshAgent.isOnNavMesh
```

---

## Recipe 5: Fix Input System

Check which input mode the project uses:

```csharp
using UnityEngine;
using UnityEditor;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        var settings = PlayerSettings.GetScriptingDefineSymbols(
            UnityEditor.Build.NamedBuildTarget.Standalone);
        result.Log("Defines: " + settings);

        // Check active input handling
        var prop = new SerializedObject(
            AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/ProjectSettings.asset")[0])
            .FindProperty("activeInputHandler");
        result.Log("Active Input Handler: " + prop.intValue);
        // 0 = Legacy, 1 = New Input System, 2 = Both
    }
}
```

**If value is 1 (New Input System only):**
- Use `Keyboard.current.eKey.wasPressedThisFrame` instead of `Input.GetKeyDown(KeyCode.E)`
- Use `Mouse.current.delta.ReadValue()` instead of `Input.GetAxis("Mouse X")`
- Add `using UnityEngine.InputSystem;` to scripts

---

## Recipe 6: Diagnose Scene Issues

```csharp
using UnityEngine;
using UnityEditor;
using UnityEngine.AI;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        // Check all NavMeshAgents
        foreach (var agent in Object.FindObjectsByType<NavMeshAgent>(FindObjectsSortMode.None))
        {
            result.Log($"NavAgent '{agent.name}': onNavMesh={agent.isOnNavMesh}, pos={agent.transform.position}");
        }

        // Check all triggers
        foreach (var col in Object.FindObjectsByType<Collider>(FindObjectsSortMode.None))
        {
            if (col.isTrigger)
            {
                var rb = col.GetComponent<Rigidbody>();
                result.Log($"Trigger '{col.name}': hasRigidbody={rb != null}, isKinematic={rb?.isKinematic}");
            }
        }

        // Check Canvas
        foreach (var canvas in Object.FindObjectsByType<Canvas>(FindObjectsSortMode.None))
        {
            result.Log($"Canvas '{canvas.name}': renderMode={canvas.renderMode}, sortOrder={canvas.sortingOrder}");
        }
    }
}
```

---

## Recipe 7: Change Project Input Handling to "Both"

This allows both legacy `Input` and new InputSystem to work simultaneously.

```csharp
using UnityEngine;
using UnityEditor;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        var assets = AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/ProjectSettings.asset");
        var so = new SerializedObject(assets[0]);
        var prop = so.FindProperty("activeInputHandler");
        prop.intValue = 2; // 0=Legacy, 1=NewInputSystem, 2=Both
        so.ApplyModifiedProperties();
        result.Log("Set Active Input Handling to 'Both'. Restart may be required.");
    }
}
```

---

## When To Use Which Recipe

| Situation | Recipe |
|-----------|--------|
| Setting up a new scene | Recipe 1 (batch) |
| Wiring Inspector references | Recipe 2 (SerializedObject) |
| Creating HUD/UI | Recipe 3 (Canvas + TMP) |
| NPCs not moving | Recipe 4 (NavMesh) + Recipe 6 (diagnose) |
| `InvalidOperationException: Input` | Recipe 5 or 7 (Input System) |
| Debugging scene problems | Recipe 6 (diagnose) |
| Everything uses legacy Input | Recipe 7 (change to Both) |
