// Unity RunCommand: Input System Diagnostic
// Checks which input handling mode is active and reports all input-related components.

using UnityEngine;
using UnityEditor;

internal class CommandScript : IRunCommand
{
    public void Execute(ExecutionResult result)
    {
        result.Log("=== INPUT SYSTEM DIAGNOSTIC ===");

        // Check active input handler
        var settings = AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/ProjectSettings.asset");
        if (settings.Length > 0)
        {
            var so = new SerializedObject(settings[0]);
            var prop = so.FindProperty("activeInputHandler");
            int mode = prop.intValue;
            string[] modes = { "Legacy (Input class)", "New Input System (Keyboard.current)", "Both" };
            string modeStr = mode < modes.Length ? modes[mode] : $"Unknown ({mode})";
            result.Log($"Active Input Handling: {modeStr}");

            if (mode == 0)
                result.Log("  → Use Input.GetKey(), Input.GetAxis()");
            else if (mode == 1)
                result.Log("  → Use Keyboard.current, Mouse.current, Gamepad.current");
            else
                result.Log("  → Both APIs work. Prefer New Input System for new code.");
        }

        // Check for InputActionAsset
        var guids = AssetDatabase.FindAssets("t:InputActionAsset");
        result.Log($"InputActionAssets found: {guids.Length}");
        foreach (var guid in guids)
        {
            var path = AssetDatabase.GUIDToAssetPath(guid);
            result.Log($"  {path}");
        }

        // Check PlayerInput components
        #if ENABLE_INPUT_SYSTEM
        var playerInputs = Object.FindObjectsByType<UnityEngine.InputSystem.PlayerInput>(FindObjectsSortMode.None);
        result.Log($"PlayerInput components in scene: {playerInputs.Length}");
        foreach (var pi in playerInputs)
            result.Log($"  {pi.name}: actions={pi.actions?.name ?? "null"}, scheme={pi.currentControlScheme}");
        #else
        result.Log("ENABLE_INPUT_SYSTEM not defined — New Input System package may not be installed.");
        #endif

        // Check for legacy Input usage in scripts (quick scan)
        var scriptGuids = AssetDatabase.FindAssets("t:MonoScript", new[] { "Assets/Scripts" });
        int legacyCount = 0;
        foreach (var guid in scriptGuids)
        {
            var path = AssetDatabase.GUIDToAssetPath(guid);
            var text = System.IO.File.ReadAllText(path);
            if (text.Contains("Input.GetKey") || text.Contains("Input.GetAxis") || text.Contains("Input.GetButton"))
            {
                legacyCount++;
                if (legacyCount <= 5)
                    result.LogWarning($"  Legacy Input usage: {path}");
            }
        }
        if (legacyCount > 5)
            result.LogWarning($"  ... and {legacyCount - 5} more files with legacy Input usage");
        result.Log($"Scripts with legacy Input calls: {legacyCount}");

        result.Log("=== DIAGNOSTIC COMPLETE ===");
    }
}
