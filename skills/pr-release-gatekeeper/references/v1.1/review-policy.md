# Review Policy v1.1

## Authority and boundary

This policy governs semantic classification for this Skill. It does not authorize execution, orchestration, tools, prompts, or changes to the bundled result contract.

## Review Domains and Finding Types

Use `Review Domain → Finding Type`. The closed registry is:

- `FACTUAL_INTEGRITY`
  - `CLAIM_CONTRADICTED_BY_EVIDENCE`
  - `INTERNAL_CONTRADICTION`
  - `QUOTE_INTEGRITY_MISMATCH`
  - `ATTRIBUTION_ERROR`
- `EVIDENCE_SUFFICIENCY`
  - `MATERIAL_CLAIM_UNSUPPORTED`
  - `MATERIAL_CONTEXT_OMISSION`
  - `UNRESOLVED_EVIDENCE_CONFLICT`
- `MESSAGING_ALIGNMENT`
  - `APPROVED_MESSAGING_MISALIGNMENT`
  - `KEY_MESSAGE_OMISSION`
- `EDITORIAL_USABILITY`
  - `MATERIAL_AMBIGUITY`
  - `UNCLEAR_ATTRIBUTION`
  - `HEADLINE_BODY_MISMATCH`
  - `PRESS_RELEASE_USABILITY_ISSUE`
- `STYLE_COMPLIANCE`
  - `STYLE_GUIDE_VIOLATION`
- `COMMUNICATIONS_RISK`
  - `OVERSTATEMENT_RISK`
  - `MATERIAL_COMMUNICATIONS_RISK`

MUST NOT invent Finding Types or use Evidence Status as a Finding Type. `MESSAGING_ALIGNMENT` requires applicable supplied approved messaging. `STYLE_COMPLIANCE` requires an applicable supplied style guide.

## Finding ownership and deduplication

One underlying problem SHOULD normally produce one actionable Finding. Select the Primary Domain and Finding Type according to the professional problem that determines the primary user action. Use Secondary Concerns for other relevant lenses.

- An established factual contradiction normally belongs to `FACTUAL_INTEGRITY`.
- Missing, ambiguous, or conflicting evidence without established falsity normally belongs to `EVIDENCE_SUFFICIENCY`.
- An editorial symptom MUST NOT duplicate its underlying factual or evidence problem.
- Communications risk rooted in a factual or evidence defect SHOULD normally be a Secondary Concern.
- Create a separate Finding only for an independent problem or materially different user action.

Do not impose a universal domain precedence; apply root-action ownership to the actual issue.

Evidence Status applies to factual and non-factual Findings on the same basis: it describes the relationship between the issue-bearing draft element or proposition and applicable supplied evidence or normative input. It is not confidence that the Finding exists, and Finding Type MUST NOT mechanically determine Evidence Status. Apply the definitions and non-exhaustive examples in `evidence-policy.md`.

## Materiality

Materiality is separate from Severity.

- `MATERIAL`: use when resolving or leaving the issue unresolved could reasonably change core factual meaning, accuracy of an important claim, identity or attribution, understanding of a material proposition, alignment with applicable approved messaging, the publication decision, or the need for substantive correction before publication.
- `NON_MATERIAL`: use for a localized issue that does not materially change meaning, factual integrity, attribution, or publication readiness.
- `UNCERTAIN`: use only when available context or evidence does not allow a reliable determination between `MATERIAL` and `NON_MATERIAL`.

MUST NOT infer Materiality from predicted outrage, media reaction, document position, length, or prominence alone. `UNCERTAIN` is uncertainty about Materiality, not an intermediate Severity.

## Severity

Severity measures publication significance, not model confidence.

- `CRITICAL`: rare and highest permitted impact within the Finding Type's defined cap; unresolved publication could create a very serious integrity error in a central claim, attribution, or core release meaning. It does not automatically determine Verdict.
- `HIGH`: clear major publication impact requiring correction or decision before release, below `CRITICAL`.
- `MEDIUM`: a real professional issue with narrower or lower publication consequence.
- `LOW`: a limited non-material professional or editorial issue.

Assess centrality, consequence if unresolved, and scope. MUST obey the bundled contract's Materiality/Severity compatibility bounds, Finding-Type caps, and required-Materiality constraints enforced by the contract validator. MUST NOT invent levels or scores.

## Human Review

Require Human Review only when the matter is `MATERIAL`, or Materiality is `UNCERTAIN`; it cannot be safely resolved from available evidence or context; and a genuine human confirmation or decision is needed. Human Review is not a generic uncertainty escape hatch.

Use exactly one primary reason:

- `INSUFFICIENT_EVIDENCE`: a material matter lacks enough evidence.
- `UNRESOLVED_SOURCE_CONFLICT`: relevant evidence conflicts and cannot be resolved.
- `AUTHORITY_UNRESOLVED`: applicable source authority cannot be resolved.
- `AMBIGUOUS_MEANING`: materially different interpretations remain possible.
- `MATERIALITY_UNCERTAIN`: available context cannot determine whether impact is material.
- `CROSS_LANGUAGE_UNCERTAINTY`: cross-language comparison itself prevents safe resolution.
- `PROFESSIONAL_JUDGMENT_REQUIRED`: the factual record is sufficiently clear, but publication or communications judgment is required. Use only when no more specific reason applies.

Rules:

- `NON_MATERIAL` Findings MUST NOT require Human Review.
- Gate-relevant `UNCERTAIN` Materiality requires Human Review with `MATERIALITY_UNCERTAIN`.
- When a matter remains unresolved and `MATERIAL`, `UNSUPPORTED`, `AMBIGUOUS`, and `CONFLICTING_EVIDENCE` each MUST require Human Review.
- A clear `CONTRADICTED` Finding does not require Human Review merely because it is serious.
- A material communications-risk judgment may use `PROFESSIONAL_JUDGMENT_REQUIRED`.
- The request MUST state what the human must confirm or decide.

Select the reason that best names the primary unresolved cause. When multiple approved reasons genuinely describe that same cause at the same level, apply this specificity order:

1. `UNRESOLVED_SOURCE_CONFLICT`
2. `AUTHORITY_UNRESOLVED`
3. `INSUFFICIENT_EVIDENCE`
4. `CROSS_LANGUAGE_UNCERTAINTY`
5. `AMBIGUOUS_MEANING`
6. `MATERIALITY_UNCERTAIN`
7. `PROFESSIONAL_JUDGMENT_REQUIRED`

Primary-cause mapping controls before the tie-break order: use `MATERIALITY_UNCERTAIN` when Materiality itself cannot be determined, and use `CROSS_LANGUAGE_UNCERTAINTY` when cross-language uncertainty is the primary unresolved cause. `PROFESSIONAL_JUDGMENT_REQUIRED` is fallback-only when no factual or evidence uncertainty reason better describes the required decision. MUST NOT infer a reason mechanically from keywords or assign multiple primary reasons to one Finding.

Human Review remains Finding-specific. An established blocker may determine the overall Verdict while a separate unresolved Human Review Finding remains visible.

## `MATERIAL_CONTEXT_OMISSION`

Use `MATERIAL_CONTEXT_OMISSION` only when all of these are true:

1. supplied evidence supports the omitted context;
2. the context directly relates to the draft claim;
3. omission could materially change understanding;
4. it is more than helpful background; and
5. the review is not merely demanding every caveat or source detail.

If the proposition itself is affirmatively wrong, prefer the applicable factual-contradiction Finding. If the statement may be literally true but omits a necessary qualification that materially distorts understanding, `MATERIAL_CONTEXT_OMISSION` may apply. MUST NOT classify every omitted caveat as material.

## Communications-risk classification

Raise communications-risk observations only from an observable trigger in the draft or evidence. Valid triggers include certainty exceeding evidence, unestablished partnership or endorsement implications, unsupported exclusivity or superlative framing, materially interpretable wording, or an independent framing concern.

MUST describe the trigger and professional concern. MUST NOT predict media attack, public anger, certain reputational damage, or crisis outcomes. If the same root issue is factual or evidential, that Finding normally owns the problem and communications risk is a Secondary Concern unless a distinct action is required. A risk Finding alone is not blocker-eligible under the bundled contract.

## Confidence boundary

MUST NOT expose numerical confidence, categorical model confidence, quality scores, or risk scores. Represent professional uncertainty through Evidence Status, Materiality, Human Review, provenance, and limitations.
