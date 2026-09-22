# Output Policy v1.1

## Authority and boundary

This policy governs result content and presentation for this Skill. It does not implement a renderer, operational workflow, repair loop, prompt, or orchestration. The bundled result contract defines the canonical schema and deterministic invariants.

## Canonical result and presentation

Validated UTF-8 JSON is the structured source of truth. Any later human-readable presentation MUST derive from the validated canonical result and MUST NOT introduce, omit, or alter decision-relevant facts, classifications, provenance, Findings, Human Review items, Verdict, or limitations.

The practitioner-facing presentation SHOULD remain concise by default and auditable on inspection. It SHOULD distinguish the Decision View from supporting audit detail without making free-form prose the only record.

## Non-completed Focused Review reporting

When a Focused Review does not complete because a scope-required input is missing or unusable, the canonical result and its presentation MUST visibly report, through the existing contract fields and without inventing new fields: the requested scope, Run Status, the missing or unusable required input, a null Verdict, and the material limitation plus the next input or capability needed. `INCOMPLETE_INPUT` identifies a required input not supplied; `CAPABILITY_BLOCKED` identifies a supplied required input the host cannot read, access, or use because a required capability is unavailable.

## Findings and actions

Findings MUST be concise, specific, traceable, and actionable. State the draft location or claim, the professional problem, relevant evidence relationship, publication significance, and safe next action. Recommendations MUST remain tied to Findings rather than appearing as free-floating advice.

Order attention by gate and action significance: established blockers, unresolved Human Review matters, other material actionable Findings, then non-material Findings. Severity alone MUST NOT control priority.

## Recommendation safety

Recommended Action MUST NOT outrun evidence.

- When the correction itself is directly supported and applicable, a specific correction is permitted.
- When the defect is established but the correct replacement is unknown, recommend confirmation and correction; do not invent replacement facts.
- For `UNSUPPORTED`, request approved evidence, removal, or appropriate qualification; do not invent a number or fact.
- For an unverifiable quotation, request an authoritative quotation or approval; do not rewrite a speaker's words as approved.
- For messaging, align to supplied applicable approved messaging; do not invent a message house.
- For editorial issues, bounded actions such as clarifying attribution or splitting a compound sentence are permitted; do not expand into full release rewriting.

Rule: make a specific correction only when that correction is itself supported. Otherwise recommend the next safe professional action.

## Human Review wording

Every Human Review item MUST retain its original Finding and clearly state:

- the unresolved matter;
- why available evidence or context cannot safely resolve it;
- the approved primary Human Review reason; and
- exactly what the human must confirm or decide.

MUST NOT use vague requests such as “please review” when a concrete confirmation or decision can be named. Human Review MUST NOT be presented as proof that the release is wrong.

## Coverage, limitations, and PASS

Every Full Gate result MUST surface a concise Coverage & Limitations summary. Include material inaccessible or unusable sources, unassessable areas, material reliance on `DERIVED` evidence, cross-language limitations, and non-applicable optional checks such as an absent Style Guide.

A `PASS` MUST state the verification basis: Review Type and Scope, what was verified, relevant limitations, and confirmation that no blocking or unresolved material Findings remain within scope. “No issues found” alone is insufficient. Limitations MUST NOT disappear because the Verdict is `PASS`.

## Communications-risk wording

Describe the observable wording or evidence trigger and the professional communications concern. MUST NOT predict media attack, public anger, certain reputational damage, crisis outcomes, coverage volume, or audience behavior. Keep a factual or evidence defect as the owning Finding when risk is only a consequence of that defect.

## Language behavior

Arabic and English are first-class output languages. Preserve factual meaning, names, titles, organizations, figures, attribution, scope, certainty, and provenance in either language. Do not hide cross-language uncertainty behind fluent prose. Surface the limitation and Human Review requirement when language prevents safe resolution.

Automatic translation is not a standalone product capability, and wording differences MUST NOT be presented as contradictions without a reliable semantic basis.

## Prohibited output behavior

MUST NOT:

- invent factual corrections, evidence, provenance, or approvals;
- expose numerical or categorical model confidence or quality scores;
- create a standalone Repair or Rewrite Mode;
- rewrite a full release as the default response;
- imply that a `FOCUSED_REVIEW` establishes publication readiness;
- predict media or public reaction as fact; or
- let human-readable prose contradict validated canonical JSON.
