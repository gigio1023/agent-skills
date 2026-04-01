# English AI Patterns — Before / After

## 1. Invented Terminology

| Before (AI) | After (human) | Why |
|---|---|---|
| metric contract | metric spec, metric definition | Not an industry term |
| strategic optionality | future options, flexibility | MBA jargon |
| execution playbook | action plan | Overcomplicated label |

**Test**: Would this term return relevant results in the intended context when searched? If not, it's invented.

## 2. Euphemistic Rephrasing

AI replaces plain language with clinical/formal alternatives. Humans writing for themselves don't do this.

| Before (AI) | After (human) | Why |
|---|---|---|
| strategic regrouping | going home to try again later | Euphemism for failure |
| activate simultaneously | both hit at once | Mechanical language for life events |
| conducted targeted job search | looked for work | Resume-speak in a personal memo |
| prevent emotional decision-making in either direction (staying too long out of stubbornness, or leaving too early out of panic) | so I don't stay out of stubbornness or leave out of panic | Over-explained hedging |
| strictly superior for your situation | clearly better for your case | Game theory jargon |

**Test**: "Would I say this out loud to a friend?" If not, simplify.

## 3. AI Filler Phrases

Words and phrases that are technically correct but humans rarely use:

**Kill list** (replace or remove):
- "It's worth noting that" → just state the thing
- "At its core" → remove
- "Ultimately" → remove or "in the end"
- "In essence" → remove
- "This is particularly relevant" → remove, it's obvious from context
- "robust and scalable" → say what it actually does
- "leverage" → "use"
- "utilize" → "use"
- "facilitate" → "help"
- "endeavor" → "try"
- "aforementioned" → "the X above" or just name it
- "It cannot be overstated" → just state it strongly
- "The real risk is psychological." → fine once, but AI repeats this dramatic-pivot pattern

**Test**: Remove the phrase. Does the sentence still work? If yes, it was filler.

## 4. Over-Hedging

AI qualifies every statement to cover every possible objection. Humans pick one main qualifier.

| Before (AI) | After (human) |
|---|---|
| EU-citizen spouse family reunification visa D is a strong legal basis. Refusal rate is low across consulates. However, document deficiencies can cause rejection. The 2024 regime change means consular experience is still accumulating. | Visa D refusal is unlikely but possible, mainly from missing documents or inconsistent consulate interpretation. |
| This combination is probably uncommon, but I can't prove it quantitatively. The market will be the test. However, the conservative reading of the evidence is not wrong either. | This combination is probably uncommon. I'll see how the market responds. |

**Test**: Count qualifiers in one paragraph. More than 2 → trim to the strongest one.

## 5. Promotional / Optimistic Bias

AI tends to reassure rather than assess neutrally.

| Before (AI) | After (human) |
|---|---|
| You're not overvaluing yourself — you're actually reading the evidence too conservatively. | You're undervaluing yourself, but the market won't do the work for you either. |
| Artifacts provide defense for aging experience. | The paper and OSS repo help, but the experience is getting old. |
| This is not failure. This is strategic regrouping. | Going home isn't failure — it just means trying again later. |

**Test**: Would a blunt friend say it this way? If the answer sounds softer than what a friend would say, it's AI promotional bias.

## 6. Mechanical Symmetry

AI creates perfectly structured documents where every section has identical format. Humans write asymmetrically — important things get more space, less important things get less.

**AI pattern examples**:
- 10 scenarios × identical 5-section template (Assessment table, Root Causes, Early Warning Signs, Contingency Plan, Decision Trigger)
- Every option analyzed with exactly 3 pros and 3 cons
- Three-tier hierarchy for everything (strong/medium/weak)
- Every section has a table

**Human pattern**: Top 3-4 items get detailed treatment. The rest are bullet points or one-liners. Tables only when comparing data, not for every list.

**Test**: "Does every item genuinely need the same depth? Or am I giving equal weight to unequal things?"

## 7. Dramatic Pivot Sentences

AI loves a short, punchy sentence after detailed analysis for rhetorical effect.

| Before (AI) | Better |
|---|---|
| [long analysis paragraph] The real risk is psychological. | Integrate into the analysis: "The bigger worry isn't legal — it's the stress of waiting." |
| [detailed financial breakdown] The math is clear. | Remove — the reader can see the math. |

Fine once in a document. AI does it every 2-3 paragraphs.

## 8. Self-Referential Framing

| Before (AI) | After (human) |
|---|---|
| 한 문장 요약: ... | Just put it at the top. The reader knows it's a summary. |
| To summarize the key takeaway: | [just state the takeaway] |
| Here's the bottom line: | [just state it] |

**Test**: If you remove the meta-label, does the content still read correctly? If yes, the label was AI scaffolding.

## 9. Speech Act Confusion

AI picks the wrong communicative intent. It declares when it should request, concludes when it should propose, and informs when it should ask permission. The surface looks polished — the pragmatics are wrong.

| Before (AI) | After (human) | Why |
|---|---|---|
| I'm sharing this for your reference. | Would this be okay to proceed with? | Situation requires approval, not sharing |
| I'll submit the report once confirmed. | Could I go ahead and submit this? | Conditional promise ≠ asking permission |
| Here's the summary. | Does this direction look right to you? | Closing with a declaration vs opening dialogue |

**Test**: What does the reader need to DO after reading this? Approve? Review? Just know? Match the speech act to that action.

## 10. Negative Enumeration (Disclaimer Syndrome)

AI exhaustively lists what WON'T happen. More disclaimers ≠ more trust; it reads as anxiety.

| Before (AI) | After (human) | Why |
|---|---|---|
| No proprietary information, trade secrets, internal metrics, org structure, or strategic direction will be discussed. | No internal or proprietary information will be discussed. | 5 items → 1 umbrella; context fills the rest |

**Test**: If you have 3+ negatives in a row, keep the most important one and trust context for the rest.

## 11. Attribution Flattening

AI writes everything as first-person declarative, erasing the distinction between your own claims, relayed information, and third-party statements.

| Before (AI) | After (human) | Why |
|---|---|---|
| The interview focuses on personal career experience only. | They said the interview focuses on personal career experience only. | It's the other party's description, not your claim |
| Refusal rate is low. | According to forum reports, refusal rate is low. | Source matters for credibility |

**Test**: "Whose claim is this — mine or someone else's?" If someone else's, signal attribution.

## 12. Declarative Closure

AI closes with a conditional promise ("I will X if you agree"). Humans often close by opening the floor for a response.

| Before (AI) | After (human) | Why |
|---|---|---|
| I'll proceed once you confirm. | Would it be okay to go ahead? | Promise vs. genuine question |
| Let me know if you have questions. | What do you think? | Generic closer vs. inviting actual input |

**Test**: After your last sentence, can the reader naturally respond? If it reads like a full stop, rewrite as a question.
