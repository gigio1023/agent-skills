---
name: unity-rendering-performance
description: "Senior-level Unity 3D rendering and performance optimization. Use when optimizing frame rate, reducing draw calls, setting up lighting, profiling, fixing GC allocations, or implementing object pooling. Triggers: optimize, performance, FPS, draw calls, LOD, lighting, profiler, GC, pooling, memory, batching, URP"
---

# Unity 3D Rendering & Performance — Senior Reference

## Golden Rule: Profile First (#7), Optimize Second

**Never optimize based on assumptions. Always measure.**

## Priority Decision Matrix

| Situation | Start Here |
|---|---|
| Don't know the bottleneck | **Profiler Workflow** |
| CPU-bound, many draw calls | **SRP Batcher / GPU Resident Drawer** |
| GPU-bound, high triangle count | **LOD + Occlusion Culling** |
| GPU-bound, low triangles (fill-rate) | **Shader Optimization + Lighting** |
| Periodic frame spikes | **GC Avoidance + Object Pooling** |
| Memory growing over time | **Addressables + GC Avoidance** |
| Mobile thermal throttling | **URP Config + Baked Lighting** |

---

## 1. URP Configuration Checklist

- [ ] Disable Depth Texture / Opaque Texture unless shader needs them
- [ ] MSAA: Disabled or 2x unless quality demands
- [ ] Enable SRP Batcher
- [ ] Enable Native RenderPass (Vulkan/Metal/DX12)
- [ ] Additional Lights: Disabled or Per Vertex on mobile
- [ ] Consider Deferred+ for >4 overlapping realtime lights

---

## 2. Draw Call Batching

**SRP Batcher:** 1.2x-4x CPU render speedup. Auto-enabled with SRP shaders.
**GPU Instancing:** For thousands of identical meshes (trees, grass).
**GPU Resident Drawer (Unity 6+):** Up to 50% CPU workload reduction.

**NEVER use MaterialPropertyBlock** — breaks SRP Batcher and GPU Resident Drawer.

---

## 3. LOD Setup

- LOD0: 100% tris, LOD1: 50%, LOD2: 25%, Culled: 0%
- Screen percentages: 60% / 30% / 10% / 5%
- Name convention: `mesh_LOD0`, `mesh_LOD1` for auto-import

---

## 4. Occlusion Culling

- Best for indoor/architectural scenes (up to 90% GPU savings)
- Mark walls/floors as Occluder Static, props as Occludee Static
- NOT recommended for open outdoor scenes

---

## 5. Lighting

| Type | Cost | Use For |
|------|------|---------|
| Baked | Zero runtime | Static environments |
| Mixed | Medium | Static indirect + realtime shadows on moving objects |
| Realtime | High | Moving lights (flashlight, fireball) |

**Mobile rule:** Baked > Mixed > Realtime. Always.

---

## 6. GC Allocation Avoidance — Zero Bytes Per Frame

```csharp
// BAD (allocates every frame)
string label = "HP: " + health; // string concat
var enemies = FindObjectsOfType<Enemy>(); // new array
foreach (var item in collection) {} // IEnumerator boxing on interfaces

// GOOD (zero allocation)
_sb.Clear(); _sb.Append("HP: "); _sb.Append(health); // StringBuilder
Physics.OverlapSphereNonAlloc(pos, radius, _buffer); // pre-allocated
for (int i = 0; i < list.Count; i++) {} // indexer, no enumerator
```

**Checklist:** Cache GetComponent in Start(). Use StringBuilder. Pre-allocate collections. No LINQ in gameplay. No closures in hot paths.

---

## 7. Object Pooling

```csharp
// Unity built-in (2021+)
var pool = new ObjectPool<Bullet>(
    createFunc: () => Instantiate(bulletPrefab),
    actionOnGet: b => b.gameObject.SetActive(true),
    actionOnRelease: b => b.gameObject.SetActive(false),
    defaultCapacity: 50);
```

**Rule:** Never Destroy pooled objects. Deactivate and return. Reset ALL state on return.

---

## 8. Profiler Workflow

1. Profile on **target device**, not Editor
2. Frame budget: 16.66ms (60fps) / 33.33ms (30fps)
3. CPU or GPU bound? → Profiler CPU module vs Frame Debugger
4. Enable Allocation Call Stacks for GC tracing
5. Add `ProfilerMarker` to your methods
6. Use Profile Analyzer for multi-frame statistics
