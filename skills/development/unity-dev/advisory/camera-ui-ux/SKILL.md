---
name: unity-camera-ui-ux
description: "Senior-level Unity 3D camera, UI, audio, dialogue, save system, and game feel patterns. Use when implementing cameras, UI architecture, conversation systems, audio, save/load, localization, screen shake, or tutorials. Triggers: camera, Cinemachine, FPS camera, third person, UI, HUD, dialogue, conversation, audio, FMOD, save, serialize, localization, Korean, TMP, CJK, game feel, juice, screen shake, tutorial"
---

# Unity 3D Camera, UI & UX — Senior Reference

## 1. Camera System (Cinemachine)

**Always use Cinemachine.** No reason to hand-roll camera in 2026.

| Mode | Cinemachine Component |
|------|----------------------|
| FPS | `CinemachineFirstPersonFollow` + `CinemachinePOV` |
| TPS | `CinemachineThirdPersonFollow` + `CinemachineCollider` |
| Cutscene | Multiple VCams with custom blend curves |
| State-driven | `CinemachineStateDrivenCamera` tied to Animator |

**FPS Tips:**
- Camera rotation in `LateUpdate()` (not Update) to avoid stutter
- Clamp vertical to ±80° (not 90°)
- Use `Time.unscaledDeltaTime` so pause doesn't break camera
- Provide mouse sensitivity slider in settings

**TPS Collision:**
- `ThirdPersonFollow` + `CinemachineCollider` (strategy: Pull Camera Forward)
- Exclude player layer from collision mask
- Damping 0.1-0.3 for smooth recovery from occlusion

---

## 2. UI Architecture

**Split by system:**
- **uGUI**: In-game HUD, world-space UI, conversation panels
- **UI Toolkit**: Menus, settings, inventory, data-heavy screens

**Canvas rules:**
- Render mode: **Screen Space - Camera** (not Overlay) for post-processing
- Scale mode: **Scale With Screen Size** (1920x1080, match 0.5)
- **Separate canvases** by update frequency (static HUD vs dynamic damage numbers)
- Set `Raycast Target = false` on decorative images

**UIManager pattern:**
```csharp
public class UIManager : MonoBehaviour {
    Stack<GameObject> panelStack = new();
    public void ShowPanel(GameObject panel) { panel.SetActive(true); panelStack.Push(panel); }
    public void Back() { if (panelStack.TryPop(out var p)) p.SetActive(false); }
}
```

---

## 3. Dialogue System

**Options by complexity:**

| Complexity | Solution |
|-----------|----------|
| Simple linear | Custom ScriptableObject graph |
| Branching narrative | **Yarn Spinner** (free, writer-friendly) |
| Deep prose | **Ink** (Inkle, free) |
| Full RPG | **Dialogue System for Unity** (Pixel Crushers, paid) |

**Production tips:**
- Separate data (what's said) from presentation (how it looks) from logic (what happens)
- Typewriter effect: configurable chars/sec, skip-on-click, punctuation pauses
- Handle edge cases: player walks away mid-conversation, dialogue during dialogue
- Localize via string tables keyed by node ID, not hardcoded strings

---

## 4. TextMeshPro + Korean/CJK

**Setup:**
1. Use **Noto Sans CJK KR** (open source, SIL license)
2. Bake high-frequency subset: **2,780 characters** = 99% coverage (not all 11,172)
3. Atlas: 2048x2048 or 4096x4096
4. Set KR font FIRST in fallback chain (TMP stops at first matching glyph)
5. Load CJK font assets via **Addressables** (save 20-40MB memory)

**Common mistakes:**
- Pan-CJK font for all regions (Han unification = wrong glyphs per region)
- Baking ALL Korean characters (enormous texture)
- Not testing with actual Korean text during development

---

## 5. Audio (FMOD Recommended)

| Factor | Native Unity | FMOD Studio | Wwise |
|--------|-------------|-------------|-------|
| Cost | Free | Free <$200K | Free indie |
| Spatial audio | Basic | Excellent | Excellent |
| Adaptive music | Manual | Built-in | Built-in |
| Best for | Simple games | Indie-mid | Mid-large |

**FMOD tips:**
- Multi Instruments for footsteps (randomize clips + pitch/volume)
- Parameter sheets for adaptive audio (e.g., "suspicion" crossfades layers)
- Load banks per scene via Addressables
- 3D spatialization with min/max attenuation

---

## 6. Game Feel / Juice

**Cinemachine Impulse for camera shake:**
```
CinemachineImpulseSource → Raw Signal (6DOF curve) → duration/intensity/range
CinemachineImpulseListener → on virtual camera
```

**Layered impact recipe:**
1. Camera shake (Impulse, 0.1-0.3s)
2. Hitstop (`Time.timeScale = 0` for 0.05-0.1s)
3. Chromatic aberration spike (0.5→0, 0.2s)
4. Vignette pulse
5. Particle burst at impact point

**UI juice:** DOTween for scale punch, color flash, positional shake on damage numbers.

**Rules:** Always provide accessibility toggle. Perlin noise for shake (not random). Ease out, never stop abruptly.

---

## 7. Save System

**Architecture:**
```
SaveManager (singleton)
  → SaveData classes (plain C# [Serializable])
  → JSON serialization (dev) / binary (release)
  → File I/O with temp-file-then-rename (crash safety)
```

**Checklist:**
- [x] `saveVersion` int from day one → migration on load
- [x] `Application.persistentDataPath` (never `dataPath`)
- [x] Try-catch + temp file + rename (crash-safe writes)
- [x] AES encryption for release builds
- [x] Save slots as separate files

| Method | Use For |
|--------|---------|
| PlayerPrefs | Settings only (volume, sensitivity) |
| JSON | Development saves, moddable games |
| Binary | Release, smaller files, anti-tamper |

**Never:** PlayerPrefs for game state. No save versioning. Direct file write without temp.

---

## 8. Tutorial / Onboarding

**Mask-and-highlight pattern:**
1. Dark overlay covers entire screen
2. Cut hole around target element (UI Mask / stencil)
3. Only highlighted element receives raycasts
4. Wait for player action → advance to next step

**TutorialManager (~200 lines):**
```csharp
public class TutorialStep {
    public string id;
    public Func<bool> showCondition;
    public RectTransform highlightTarget;
    public string instructionText;
    public Func<bool> completionCondition;
}
```

**Rules:**
- Progressive disclosure (unlock mechanics gradually)
- First 2 minutes = core gameplay loop, not menus
- Always provide "skip tutorial" option
- Persist completion state in PlayerPrefs
- Track funnel analytics (where do players drop off?)

---

## Decision Matrix for 3D Games

| System | Recommendation |
|--------|---------------|
| Camera | **Cinemachine** — always |
| HUD | **uGUI** Canvas (Screen Space - Camera) |
| Menus | **UI Toolkit** for data-heavy screens |
| Dialogue | **Yarn Spinner** for branching, custom SO for simple |
| Fonts | **Noto Sans CJK** + TMP SDF, subset bake |
| Audio | **FMOD Studio** (free indie) |
| Game feel | **Cinemachine Impulse** + DOTween |
| Saves | **JSON** (dev) / **binary** (release) with SaveManager |
| Tutorial | Custom **TutorialManager** with mask-highlight |
