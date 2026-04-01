---
name: unity-senior-architecture
description: "Senior-level Unity 3D architecture patterns. Use when designing game systems, choosing between DI/singleton/events, structuring code for maintainability, or making architecture decisions. Triggers: architecture, DI, singleton, event channel, state machine, command pattern, ScriptableObject, SOLID, MVP, asmdef"
---

# Senior Unity 3D Architecture Patterns

## Decision Matrix — Which Pattern When?

| Need | Pattern | Complexity |
|------|---------|------------|
| Shared data across scenes | ScriptableObject Variables | Low |
| Decoupled event broadcast | SO Event Channels | Low |
| Testable dependency management | VContainer DI | Medium |
| Character/AI behavior modes | FSM / HFSM | Low-Medium |
| Undo/redo, action queues | Command Pattern | Medium |
| Complex UI with data binding | MVP / MVVM | Medium |
| Module boundaries, compile time | Assembly Definitions | Low |

---

## 1. ScriptableObject Architecture (Ryan Hipple / Schell Games)

**Use for:** Shared game data, cross-scene communication, event broadcasting.
**Don't use for:** Per-instance state (individual enemy HP), frame-critical high-frequency data.

```csharp
// Shared variable (asset in project)
[CreateAssetMenu] public class FloatVariable : ScriptableObject { public float Value; }

// Event channel
[CreateAssetMenu(menuName = "Events/Void Event")]
public class VoidEventChannel : ScriptableObject {
    public event System.Action OnRaised;
    public void Raise() => OnRaised?.Invoke();
}
```

**Senior rule:** Always unsubscribe in `OnDisable()`. Never put per-instance data in SOs.

---

## 2. Dependency Injection (VContainer)

**Use for:** Medium-large projects, testability, complex lifetime management.
**Don't use for:** Game jams, solo prototypes, teams unfamiliar with DI.

```csharp
public class GameLifetimeScope : LifetimeScope {
    protected override void Configure(IContainerBuilder builder) {
        builder.Register<IRouteSearch, AStarRouteSearch>(Lifetime.Singleton);
        builder.Register<CharacterService>(Lifetime.Scoped);
        builder.RegisterEntryPoint<GamePresenter>();
    }
}
```

**Senior rule:** Components receive dependencies via constructor — never pull from container.

---

## 3. Service Locator vs Singleton vs DI

| | Singleton | Service Locator | DI |
|---|---|---|---|
| Testable? | Hard | Medium | Easy |
| Dependencies visible? | No | No | Yes |
| Multiplayer-safe? | No | Yes | Yes |

**Senior default:** Pass dependency as parameter. No framework needed for simple cases.

---

## 4. State Machine (FSM / HFSM)

**Use for:** Character controllers, game flow, UI navigation, AI with <15 states.
**Don't use for:** >15 states (use Behavior Tree), concurrent behaviors, simple bool toggles.

```csharp
public interface IState { void Enter(); void Execute(); void Exit(); }

public class StateMachine {
    IState _current;
    public void ChangeState(IState next) {
        _current?.Exit(); _current = next; _current.Enter();
    }
    public void Update() => _current?.Execute();
}
```

**Senior rule:** Define allowed transitions explicitly. Never allow any-to-any transitions.

---

## 5. Command Pattern

**Use for:** Undo/redo, action queues, replay systems, turn-based games.
**Don't use for:** Continuous per-frame movement, one-shot actions with no history.

```csharp
public interface ICommand { void Execute(); void Undo(); }
```

**Senior rule:** Cap undo stack. Clear redo stack on new action. Handle destroyed-object references.

---

## 6. MVP for Game UI

**Use for:** Non-trivial UI (inventory, shop, settings). Separates data/logic/presentation.

```
Model (pure C#, no Unity) ←→ Presenter (mediates) ←→ View (MonoBehaviour on UI)
```

**Senior rule:** View only forwards user intent. Never put game logic in Button.onClick.

---

## 7. Assembly Definitions

**Recommended structure:**
```
Core/          Core.asmdef          (zero dependencies)
Services/      Services.asmdef      (→ Core)
Gameplay/      Gameplay.asmdef      (→ Core, Services)
UI/            UI.asmdef            (→ Core, Services)
Editor/        Editor.asmdef        (→ all, Editor-only)
Tests/         Tests.EditMode.asmdef (→ tested assemblies)
```

**Senior rule:** Reference by GUID not name. Never create circular dependencies.

---

## SOLID in Unity (Practical)

| Principle | Unity Application |
|-----------|-------------------|
| **S** | One MonoBehaviour per concern (PlayerMovement, PlayerHealth, PlayerInventory) |
| **O** | Abstract base / interface for weapons. New weapon = new class, not edit switch |
| **L** | If Sword can't Reload(), Weapon interface is too broad — split it |
| **I** | IDamageable, IHealable, IInteractable as separate interfaces |
| **D** | PlayerController depends on IInputProvider, not KeyboardInput directly |

---

## Anti-Patterns Seniors Avoid

- 2000-line Manager MonoBehaviours
- Singletons for everything (breaks multiplayer, split-screen, testing)
- String-keyed event managers (zero type safety)
- Over-engineering prototypes with 50 tiny classes
- Mixing ECS and MonoBehaviour without a clear bridge
