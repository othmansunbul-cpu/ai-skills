# Gate Policy v1.1

## Authority and boundary

This policy defines gate behavior for this Skill. It does not implement or replace the bundled schema, validator, execution flow, or orchestration. The semantic layer MUST produce contract-valid state and MUST NOT override deterministic invariants.

## Review Type and Full Gate eligibility

A `FULL_GATE_REVIEW` requires a readable press-release draft, at least one usable supporting source, and completion of mandatory Full Gate scope. If the minimum input is not satisfied, issue no publication-readiness Verdict; treat the condition through Run Status. `HUMAN_REVIEW_REQUIRED` is not an input-validity workaround.

A `FOCUSED_REVIEW` MUST expose its scope, MUST NOT issue a Full Gate Verdict, and MUST NOT imply publication readiness. User instructions cannot disable mandatory Full Gate checks while retaining Full Gate eligibility.

A Focused Review requires only the inputs necessary to perform its explicitly requested scope safely and meaningfully. Required inputs are scope-specific; a Focused Review does not make every possible source mandatory, and a readable draft alone is not universally sufficient.

- An `EDITORIAL_USABILITY`-only review may require only a readable draft when the requested judgment is directly observable from the draft.
- A `STYLE_COMPLIANCE` review requires an applicable supplied style guide or equivalent explicitly supplied normative style source for the requested style rule. Factual evidence that merely proves a number is not a substitute for a style guide.
- A `MESSAGING_ALIGNMENT` review requires applicable supplied approved messaging, message house, brief, or equivalent normative messaging source.
- A factual/evidence comparison requires usable evidence applicable to the factual proposition being assessed.
- A quote-integrity comparison requires an applicable supplied quotation or source reference sufficient for the requested comparison.

For an input mandatory to the explicitly requested Focused Review scope:

- if it is not supplied at all, set `run_status` to `INCOMPLETE_INPUT` and `verdict` to null;
- if it is supplied but the host cannot read, access, or use it because a required capability is unavailable, set `run_status` to `CAPABILITY_BLOCKED` and `verdict` to null; and
- if an optional input is unavailable but the requested scope remains safely completable, the result may remain `COMPLETED`; surface the material limitation when relevant.

Do not conflate user-input deficiency, host-capability deficiency, and an optional limitation. In particular, when the declared Focused Review scope is `STYLE_COMPLIANCE`, a readable draft without an applicable supplied style guide or equivalent normative style source is `INCOMPLETE_INPUT` with a null Verdict. No `STYLE_GUIDE_VIOLATION` may be invented from general model preferences. The limitation or request MUST explain that the applicable normative style source is required. MUST NOT silently convert the request into general copy editing, `EDITORIAL_USABILITY`, or model-preference style checking.

## Semantic completeness obligation

For Full Gate review, identify all relevant publication-significant factual propositions that belong in `material_claims`. The represented trace MUST be semantically complete enough to support the requested publication decision.

The validator derives coverage only over represented claims. Contract validity therefore does not prove that every material claim in the draft was extracted. Zero Findings does not establish `PASS`; semantic extraction completeness and sufficient verification of represented material claims are also required.

## Canonical material-claim trace

Each represented material claim MUST include its canonical ID, claim text, draft location, Evidence Status, and evidence references. Claim IDs MUST be unique. Evidence references MUST resolve to usable supplied sources and record `evidence_basis` as `DIRECT` or `DERIVED`.

Minimum evidence-reference expectations are:

- `SUPPORTED`: at least one reference.
- `CONTRADICTED`: at least one reference.
- `AMBIGUOUS`: at least one reference.
- `CONFLICTING_EVIDENCE`: at least two distinct reference objects; distinct source IDs are not required.
- `UNSUPPORTED`: zero or more references.

Exact duplicate reference objects do not count separately. These minimums are contract conditions, not proof that the evidence is semantically sufficient, authoritative, or independent.

## Finding linkage

Every Finding MUST include `material_claim_ids`; the array may be empty for non-claim-specific or non-material issues. Every listed ID MUST identify a represented material claim. One Finding may address multiple claims, and one claim may relate to multiple Findings.

For every represented material claim with Evidence Status `CONTRADICTED`, `UNSUPPORTED`, `AMBIGUOUS`, or `CONFLICTING_EVIDENCE`, at least one linked Finding MUST:

- include the claim ID;
- have Materiality `MATERIAL`; and
- have the same Evidence Status as the material claim.

Do not infer a required Finding Type solely from Evidence Status. Use the professional problem and root action to select it.

## Blockers remain Finding-driven

Material claims do not create a second blocker path. A blocker exists only when a Finding satisfies the bundled blocker conditions, including blocker-eligible Finding Type, `MATERIAL`, permitted `HIGH` or `CRITICAL` Severity, and no unresolved Human Review requirement on that Finding. `is_blocker` is deterministically derived.

A serious or contradicted claim does not bypass Finding construction or blocker derivation. Severity alone does not determine Verdict.

## Deterministic Verdict precedence

For an eligible completed Full Gate result, preserve this precedence:

1. any established blocker → `NOT_READY_FOR_PUBLICATION`;
2. otherwise, any unresolved Human Review requirement or insufficient represented-material-claim coverage → `HUMAN_REVIEW_REQUIRED`;
3. otherwise, any remaining actionable Finding → `PASS_WITH_FINDINGS`;
4. otherwise → `PASS`.

Represented material-claim coverage is sufficient only when every represented claim is `SUPPORTED` or `CONTRADICTED`; any `UNSUPPORTED`, `AMBIGUOUS`, or `CONFLICTING_EVIDENCE` claim makes represented coverage insufficient. Blocker precedence remains intact when a separate unresolved Human Review matter exists.

The semantic layer MUST NOT manufacture inputs to force a preferred Verdict and MUST NOT override the validator's derived result.

## Human Review and limitations

Human Review must correspond to a genuine unresolved material matter and use the approved reason and request policy. Limitations that materially affect interpretation MUST remain visible, including inaccessible sources, material reliance on `DERIVED` evidence, cross-language limits, unavailable optional checks, and unassessable areas.

A limitation does not independently change Verdict unless it is reflected through Run Status, represented coverage, Human Review, or another gate rule defined here. MUST NOT hide limitations because the result is `PASS`, and MUST NOT flood output with irrelevant technical detail.

## Contract validation boundary

Canonical JSON MUST satisfy the bundled schema and invariant validator before it is treated as a successful result. Semantic judgment supplies claims, statuses, Findings, Materiality, Severity, Human Review, and recommendations; deterministic validation checks mechanical consistency. Neither layer may impersonate or silently rewrite the other.

Contract validation proves structural and represented-state consistency. It does not prove semantic correctness, material-claim extraction completeness, evidence sufficiency, or professional judgment quality.
