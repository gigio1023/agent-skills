---
name: unity-workflow-testing-ci
description: "Senior-level Unity testing, CI/CD, Git workflow, prefab management, scene management, and build automation. Use when setting up tests, CI pipelines, managing scenes, organizing prefabs, or structuring projects. Triggers: test, CI, GitHub Actions, GameCI, Git, LFS, merge conflict, prefab, scene management, additive loading, build pipeline, project structure, asmdef, code review"
---

# Unity Workflow, Testing & CI — Senior Reference

## 1. Testing Strategy (Two-Tier Pyramid)

| Tier | Use For | Speed | Framework |
|------|---------|-------|-----------|
| **EditMode** | Pure logic, SO config, data transforms | Sub-second | NUnit `[Test]` |
| **PlayMode** | MonoBehaviour lifecycle, physics, UI flows | Seconds | `[UnityTest]` with yield |

**Rules:**
- Structure logic into pure C# classes (no MonoBehaviour dep) → testable in EditMode
- Use `[UnityTest]` ONLY when you need yield instructions
- Test assemblies need `.asmdef` referencing tested code assemblies
- Run tests in CI — tests only matter if they run automatically

---

## 2. CI/CD with GameCI + GitHub Actions

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { lfs: true }
      - uses: actions/cache@v4
        with: { path: Library, key: Library-${{ hashFiles('Assets/**', 'Packages/**') }} }
      - uses: game-ci/unity-test-runner@v4
        with: { unityVersion: auto, testMode: all }
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: game-ci/unity-builder@v4
        with: { targetPlatform: StandaloneWindows64 }
```

**Key:** Cache `Library/` folder. Use `UNITY_LICENSE` secret. Run builds only on merge to main.

---

## 3. Git Workflow (Force Text + LFS + SmartMerge)

**Setup checklist:**
- [x] Asset Serialization = Force Text
- [x] Version Control = Visible Meta Files
- [x] `.gitattributes`: `*.unity merge=unityyamlmerge`, `*.png filter=lfs`
- [x] SmartMerge configured in `.gitconfig`
- [x] `git lfs lock <scene>` before editing, `unlock` when done

**Scene merge conflict prevention:**
1. Decompose into additive sub-scenes
2. One person owns a scene file at a time (LFS locking)
3. Short-lived branches (merge frequently)

**Never:** Binary serialization. Long-lived branches. Missing `.meta` files.

---

## 4. Prefab Workflow

**Hierarchy:** Atomic prefabs → Composed prefabs → Scene instances

| Concept | Use |
|---------|-----|
| **Nested prefabs** | Building = Room prefabs = Furniture prefabs |
| **Prefab variants** | Door_Base → Door_Wooden, Door_Iron (share 80%+ of base) |
| **Prefab Mode** | Always edit in isolation, not in-scene |

**Rules:** Max 3-4 nesting levels. Always Apply after editing instances. Never nest variants of variants.

---

## 5. Scene Management: Persistent Scene Pattern

```
_Boot (index 0)
  └─ BootstrapLoader.Start()
      ├─ LoadAsync("Persistent", Additive)  → managers, player, camera
      └─ LoadAsync("Level_01", Additive)    → gameplay content
```

**Scene transition:** Unload gameplay scene → Load next additively. Persistent stays.

**Rules:**
- Never use `DontDestroyOnLoad` — use the persistent scene instead
- Always `LoadSceneAsync` (never sync `LoadScene`)
- `SetActiveScene()` for correct lighting + new object spawning

---

## 6. Build Automation

```csharp
// Assets/Editor/BuildAutomation.cs
public static class BuildAutomation {
    [MenuItem("Build/Windows")]
    public static void BuildWindows() {
        BuildPipeline.BuildPlayer(new BuildPlayerOptions {
            scenes = EditorBuildSettings.scenes.Select(s => s.path).ToArray(),
            locationPathName = "Builds/Win/Game.exe",
            target = BuildTarget.StandaloneWindows64,
            options = BuildOptions.None
        });
    }
}
```

**CI invoke:** `unity -batchmode -quit -executeMethod BuildAutomation.BuildWindows`

---

## 7. Code Review Checklist

**Architecture:**
- [ ] No business logic in `Update()` — delegate to services
- [ ] Interfaces for dependencies (testable)
- [ ] ScriptableObjects for config (not hardcoded values)

**Performance:**
- [ ] No allocations in hot paths
- [ ] No `Find()`/`GetComponent()` every frame — cached
- [ ] No string concatenation in loops
- [ ] Coroutines cleaned up in `OnDisable()`

**Unity-specific:**
- [ ] `[SerializeField]` not `public` fields
- [ ] `CompareTag()` not `== "string"`
- [ ] Non-allocating physics queries (`RaycastNonAlloc`)
- [ ] Textures power-of-2, correct import settings

---

## 8. Asset Pipeline

**Automated enforcement:**
```csharp
class TexturePostprocessor : AssetPostprocessor {
    void OnPreprocessTexture() {
        if (assetPath.Contains("/UI/")) {
            var imp = (TextureImporter)assetImporter;
            imp.textureType = TextureImporterType.Sprite;
            imp.maxTextureSize = 2048;
            imp.mipmapEnabled = false;
        }
    }
}
```

**Rules:** Folder-based Presets for defaults. ASTC for mobile, BC7 for desktop. Enable Parallel Import. Enable "Optimize Mesh Data" in Player Settings.

---

## 9. Project Structure

```
Assets/
  _Boot/              # Bootstrap scene
  Art/Materials|Models|Textures|Animations/
  Audio/Music|SFX/
  Prefabs/Characters|Environment|UI/
  Scenes/Levels|Additive/
  Scripts/
    Core/             # Core.asmdef (shared, zero deps)
    Features/Combat|Inventory|UI/  # Feature asmdefs
    Editor/           # Editor-only asmdef
  Tests/EditMode|PlayMode/
  Plugins/            # Third-party (untouched)
  Resources/          # Nearly empty — use Addressables
  Settings/           # URP, Quality, Input
```

**Rules:** No spaces in names. Reference asmdef by GUID. `Resources/` nearly empty. Document naming in style guide.

---

## 10. Debug Workflow

```csharp
// Custom profiler marker (zero overhead in release)
static readonly ProfilerMarker s_Marker = new("MySystem.Update");
void Update() { using (s_Marker.Auto()) { /* code */ } }
```

**Process:** Profile on target device → Identify CPU vs GPU bound → Drill into markers → Fix → Re-profile

**Tip:** Disable Domain Reload for faster Play Mode iteration. Use `[RuntimeInitializeOnLoadMethod(SubsystemRegistration)]` to reset statics.
