---
name: unity-physics-navmesh-ai
description: "Senior-level Unity 3D physics, NavMesh navigation, and NPC AI patterns. Use when implementing NPC movement, pathfinding, trigger zones, physics optimization, behavior trees, GOAP, or crowd simulation. Triggers: NavMesh, pathfinding, NPC, AI, behavior tree, FSM, GOAP, physics, trigger, CharacterController, Rigidbody, raycast, crowd"
---

# Unity 3D Physics, NavMesh & AI — Senior Reference

## AI Architecture Decision Matrix

| Agent Count | Behavior Complexity | Recommended |
|---|---|---|
| 1-5 simple NPCs | Patrol/idle/chase | **FSM** |
| 5-20 complex NPCs | Multi-phase, priority-based | **Behavior Tree** |
| 20+ adaptive NPCs | Emergent, reacts to world state | **GOAP** |
| Mixed | Varies per NPC type | **Hybrid** (Utility AI sets priorities → BT executes → FSM animates) |

---

## 1. NavMesh Best Practices

**Setup:**
- Add `NavMeshSurface` to ground/floor
- Mark walkable geometry as Navigation Static
- Call `BuildNavMesh()` after all geometry is placed

**Runtime obstacles:**
- `NavMeshObstacle` Carving: for doors/barricades (expensive, batch)
- `NavMeshObstacle` Obstructing: for moving objects (cheap, reactive)
- `NavMeshModifier`: area costs for soft influence (prefer gravel vs road)

**Gotchas:**
- Enable "Carve Only Stationary" with Move Threshold
- Never rebuild NavMesh per-frame
- `isOnNavMesh` can be false if agent spawns outside NavMesh bounds

---

## 2. NPC Patrol Pattern

```csharp
agent.autoBraking = false; // continuous movement

void UpdatePatrol() {
    if (!agent.pathPending && agent.remainingDistance < 0.5f) {
        index = (index + 1) % waypoints.Length;
        agent.SetDestination(waypoints[index].position);
    }
}
```

**Rules:**
- Only call `SetDestination` when waypoint changes (NOT every frame)
- Always gate with `!pathPending` before checking `remainingDistance`
- Stagger SetDestination across frames for large NPC counts

---

## 3. Behavior Tree (Event-Driven)

**Use NPBehave or Unity Behavior Graph** — event-driven BTs only re-evaluate on blackboard changes, not every tick.

**Structure:**
```
Selector (priority)
├── Sequence: [IsPlayerInRange?] → [Chase] → [Attack]
├── Sequence: [HeardNoise?] → [Investigate]
└── Patrol
```

**Gotchas:**
- Traditional BTs traverse from root every tick (wasteful)
- IMMEDIATE_RESTART abort logic is tricky — prefer explicit stop rules

---

## 4. GOAP (Goal-Oriented Action Planning)

**When:** NPCs dynamically adapt to changing environments. Adding behaviors = adding actions, no rewrite.

**Libraries:** crashkonijn/GOAP (multi-threaded), luxkun/ReGoap

**Rules:**
- Cache plans, only re-plan on world state change
- Keep action set <10 per agent type
- Event-driven plan invalidation, not polled

---

## 5. CharacterController vs Rigidbody

| | CharacterController | Rigidbody |
|---|---|---|
| Feel | Snappy, immediate | Momentum, inertia |
| Physics response | None | Full |
| Slope/step | Built-in | Manual |
| Best for | FPS/TPS precise control | Physics-heavy platformer |

**Rules:**
- Never put CharacterController + NavMeshAgent on same object
- Rigidbody movement in `FixedUpdate()`, not `Update()`
- `SimpleMove()` auto-applies gravity; `Move()` does not

---

## 6. Trigger Zone Pattern

```csharp
void OnTriggerEnter(Collider other) {
    if (!other.CompareTag("Player")) return; // FIRST line always
    // Zone logic here
}
```

**Requirements:**
- At least one object MUST have Rigidbody (use kinematic if no physics needed)
- Use `CompareTag()` not `tag ==` (latter allocates string)
- Use Layer Collision Matrix to prevent irrelevant trigger checks

---

## 7. Physics Optimization

**Collider rules:**
- Primitive > Mesh. Always.
- Compound primitives for complex dynamic shapes
- Never non-convex MeshCollider on Rigidbody

**Raycast rules:**
```csharp
// GOOD: layer mask + NonAlloc + max distance
int mask = LayerMask.GetMask("Enemy", "Environment");
int hits = Physics.RaycastNonAlloc(origin, dir, _buffer, maxDist, mask);
```
- Pre-cache LayerMask values in Awake()
- Stagger NPC raycasts across frames
- Use `RaycastCommand` + Jobs for bulk queries

**Layer Collision Matrix:**
- Edit > Project Settings > Physics
- Disable all unnecessary layer pairs
- Biggest single optimization for physics-heavy scenes

---

## 8. Crowd Scaling

| Count | Approach |
|---|---|
| <30 | Standard NavMeshAgent |
| 30-100 | Staggered path updates, reduced frequency |
| 100-1000+ | DOTS navigation or flow fields |

**Key insight:** 15 fully-rigged Humanoid NavMeshAgents can drop FPS from 300 to 90. Animation + navigation combined is the killer.

---

## 9. Procedural Animation / IK

- Use **Animation Rigging** package (modern replacement for Animator IK)
- Two Bone IK for feet/hands, Multi-Aim for head tracking
- Blend IK weight smoothly (0→1 over time), never snap
- Disable IK rigs on off-screen/distant characters
