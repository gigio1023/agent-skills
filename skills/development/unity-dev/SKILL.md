---
name: unity-dev
description: "Unity 3D game development with official Unity MCP tools. Scene manipulation (create/modify/delete GameObjects, wire components, bake NavMesh), C# scripting, architecture patterns (DI, SOA, FSM, GOAP), rendering optimization (URP, LOD, batching), NPC AI (NavMesh, behavior trees), camera (Cinemachine), UI (uGUI, UI Toolkit, TMP Korean/CJK), audio (FMOD), testing (EditMode/PlayMode), CI/CD (GameCI), save systems. Use when working in any Unity project, editing .cs files under Assets/, or using Unity MCP tools."
---

# Unity Dev

## Agent Team — Auto-Spawn for Unity Development

When the user triggers this skill (e.g., `/unity-dev` or asks to work on a Unity feature), follow this workflow:

### When to Spawn Each Agent

| Situation | Spawn | Prompt File |
|-----------|-------|-------------|
| New feature / "만들어줘" / design needed | **game-designer** first | `agents/game-designer.md` |
| Designer spec ready / "구현해" / code work | **gameplay-programmer** | `agents/gameplay-programmer.md` |
| "테스트해" / "확인해" / after implementation | **qa-inspector** | `agents/qa-inspector.md` |
| Bug report from user / "안 돼" / "왜 이래" | **qa-inspector** first, then programmer | both |

### The Flow (Designer → Programmer → QA)

```
1. User: "대화 시스템 만들어줘"
   → Spawn game-designer agent
   → Designer outputs: player journey, game states, input contracts, feedback checklist

2. Take designer output as spec
   → Spawn gameplay-programmer agent (pass designer spec as context)
   → Programmer implements, checks console, saves scene

3. After implementation
   → Spawn qa-inspector agent (pass designer spec + what was built)
   → QA reports blockers/issues

4. If issues found → back to step 2 (or step 1 if design is wrong)
```

### How to Spawn

Read the agent's prompt file, then use the **Agent tool** with the prompt content + task context:

```
Agent(
  prompt = [read agents/game-designer.md] + "\n\nTask: " + [user's request],
  description = "Game Designer: [feature name]"
)
```

### Rules
- **ALWAYS start with designer** for new features (prevents the "builds feature but misses UX" problem)
- **Skip designer** only for pure bug fixes or technical tasks (NavMesh bake, compile error)
- **QA after every implementation** — no exceptions
- **Max 3 agents per feature cycle** (designer → programmer → QA)
- Pass previous agent's output as context to the next agent

---

## Quick Router — Read the right file for your task

| What you're doing | Read this file |
|---|---|
| **MCP scene ops** (create objects, wire refs, bake NavMesh, RunCommand) | `advisory/mcp-recipes/SKILL.md` |
| **Architecture** (DI, events, state machines, SOLID, asmdef) | `advisory/senior-architecture/SKILL.md` |
| **Performance** (URP, draw calls, LOD, profiler, GC, pooling) | `advisory/rendering-performance/SKILL.md` |
| **NPC / Physics** (NavMesh, behavior tree, GOAP, triggers, raycasts) | `advisory/physics-navmesh-ai/SKILL.md` |
| **Camera / UI / Audio** (Cinemachine, dialogue, FMOD, saves, Korean TMP) | `advisory/camera-ui-ux/SKILL.md` |
| **Testing / CI / Git** (EditMode, PlayMode, GameCI, LFS, prefabs, scenes) | `advisory/workflow-testing-ci/SKILL.md` |
| **Project analysis** (inspect existing codebase before changes) | `advisory/project-scout/SKILL.md` |
| **Patterns catalog** (ScriptableObject, observer, pool, etc.) | `advisory/patterns/SKILL.md` |

Load **only the module you need**. Never preload all.

---

## Top 5 Gotchas (always relevant)

**1. RunCommand template (MUST follow exactly):**
```csharp
using UnityEngine; using UnityEditor;
internal class CommandScript : IRunCommand {
    public void Execute(ExecutionResult result) {
        // RegisterObjectCreation AFTER creating
        // RegisterObjectModification BEFORE modifying
        // DestroyObject instead of DestroyImmediate
        // ALWAYS check GetConsoleLogs after
    }
}
```
Class MUST be `CommandScript`. MUST be `internal`.

**2. Input System:** If `InvalidOperationException: Input`, project uses New Input System. Use `Keyboard.current`/`Mouse.current`, not `Input.GetKey`.

**3. NavMesh:** If NPCs don't move, `isOnNavMesh` is false. Add `NavMeshSurface` to ground + `BuildNavMesh()` via RunCommand.

**4. Save scene:** Always `Unity_ManageScene → Save` after MCP changes. Changes exist only in memory until saved.

**5. Namespaces:** If component not found by name, use full namespace (`DreamOfOne.NPC.PoliceController`). `Image` conflicts: `using UImage = UnityEngine.UI.Image;`

---

## Workflow: Query → Mutate → Verify

1. **Query:** `GetHierarchy` (depth=1), `get_components`, `GetConsoleLogs`, `FindProjectAssets`
2. **Mutate:** `ManageGameObject`, `RunCommand` (for batch/complex), `ManageScript`
3. **Verify:** `GetConsoleLogs`, `get_components`, Play → Stop → check logs

**Prefer batch RunCommand over many individual MCP calls** (10x faster).

---

## Diagnostic Scripts

Run these via `Unity_RunCommand` to quickly diagnose issues:

- Scene diagnosis: `scripts/diagnose-scene.cs`
- NavMesh check: `scripts/setup-navmesh.cs`
- Input System check: `scripts/check-input-system.cs`

---

## Reference Docs (load only specific topic)

| Topic | File | Size |
|-------|------|------|
| Scripting | `references/scripting.md` | small |
| Physics | `references/physics.md` | large |
| UI | `references/ui.md` | small |
| Rendering | `references/rendering.md` | medium |
| Editor | `references/editor.md` | small |
| Scene Management | `references/scene_management.md` | medium |
| Shaders | `references/shaders.md` | **92KB — selective** |
| Other | `references/other.md` | **216KB — selective** |
