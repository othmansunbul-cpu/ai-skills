"""Validate PR Release Gatekeeper result JSON against the Phase 7A contract."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator


SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "result.schema.json"

FINDING_TYPE_DOMAINS = {
    "CLAIM_CONTRADICTED_BY_EVIDENCE": "FACTUAL_INTEGRITY",
    "INTERNAL_CONTRADICTION": "FACTUAL_INTEGRITY",
    "QUOTE_INTEGRITY_MISMATCH": "FACTUAL_INTEGRITY",
    "ATTRIBUTION_ERROR": "FACTUAL_INTEGRITY",
    "MATERIAL_CLAIM_UNSUPPORTED": "EVIDENCE_SUFFICIENCY",
    "MATERIAL_CONTEXT_OMISSION": "EVIDENCE_SUFFICIENCY",
    "UNRESOLVED_EVIDENCE_CONFLICT": "EVIDENCE_SUFFICIENCY",
    "APPROVED_MESSAGING_MISALIGNMENT": "MESSAGING_ALIGNMENT",
    "KEY_MESSAGE_OMISSION": "MESSAGING_ALIGNMENT",
    "MATERIAL_AMBIGUITY": "EDITORIAL_USABILITY",
    "UNCLEAR_ATTRIBUTION": "EDITORIAL_USABILITY",
    "HEADLINE_BODY_MISMATCH": "EDITORIAL_USABILITY",
    "PRESS_RELEASE_USABILITY_ISSUE": "EDITORIAL_USABILITY",
    "STYLE_GUIDE_VIOLATION": "STYLE_COMPLIANCE",
    "OVERSTATEMENT_RISK": "COMMUNICATIONS_RISK",
    "MATERIAL_COMMUNICATIONS_RISK": "COMMUNICATIONS_RISK",
}

BLOCKER_ELIGIBLE_TYPES = {
    "CLAIM_CONTRADICTED_BY_EVIDENCE",
    "INTERNAL_CONTRADICTION",
    "QUOTE_INTEGRITY_MISMATCH",
    "ATTRIBUTION_ERROR",
    "MATERIAL_CONTEXT_OMISSION",
    "APPROVED_MESSAGING_MISALIGNMENT",
    "KEY_MESSAGE_OMISSION",
    "HEADLINE_BODY_MISMATCH",
}

CRITICAL_ALLOWED_TYPES = {
    "CLAIM_CONTRADICTED_BY_EVIDENCE",
    "INTERNAL_CONTRADICTION",
    "QUOTE_INTEGRITY_MISMATCH",
    "ATTRIBUTION_ERROR",
    "MATERIAL_CLAIM_UNSUPPORTED",
    "MATERIAL_CONTEXT_OMISSION",
    "UNRESOLVED_EVIDENCE_CONFLICT",
    "APPROVED_MESSAGING_MISALIGNMENT",
    "MATERIAL_AMBIGUITY",
}

MAX_HIGH_TYPES = {
    "KEY_MESSAGE_OMISSION",
    "UNCLEAR_ATTRIBUTION",
    "HEADLINE_BODY_MISMATCH",
    "OVERSTATEMENT_RISK",
    "MATERIAL_COMMUNICATIONS_RISK",
}

MAX_MEDIUM_TYPES = {
    "PRESS_RELEASE_USABILITY_ISSUE",
    "STYLE_GUIDE_VIOLATION",
}

REQUIRED_MATERIALITY = {
    "MATERIAL_CLAIM_UNSUPPORTED": "MATERIAL",
    "MATERIAL_CONTEXT_OMISSION": "MATERIAL",
    "MATERIAL_AMBIGUITY": "MATERIAL",
    "MATERIAL_COMMUNICATIONS_RISK": "MATERIAL",
}

MATERIALITY_SEVERITIES = {
    "MATERIAL": {"MEDIUM", "HIGH", "CRITICAL"},
    "NON_MATERIAL": {"LOW", "MEDIUM"},
    "UNCERTAIN": {"MEDIUM", "HIGH"},
}

SEVERITY_RANK = {
    "LOW": 0,
    "MEDIUM": 1,
    "HIGH": 2,
    "CRITICAL": 3,
}

VERIFICATION_SUFFICIENT_EVIDENCE_STATUSES = {
    "SUPPORTED",
    "CONTRADICTED",
}

NON_SUPPORTED_EVIDENCE_STATUSES = {
    "CONTRADICTED",
    "UNSUPPORTED",
    "AMBIGUOUS",
    "CONFLICTING_EVIDENCE",
}

MATERIAL_CLAIM_MINIMUM_EVIDENCE_REFS = {
    "SUPPORTED": 1,
    "CONTRADICTED": 1,
    "UNSUPPORTED": 0,
    "AMBIGUOUS": 1,
    "CONFLICTING_EVIDENCE": 2,
}


def load_schema(path: Path | None = None) -> dict[str, Any]:
    """Load the canonical schema as UTF-8 JSON."""
    schema_path = path or SCHEMA_PATH
    with schema_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def check_schema(schema: dict[str, Any] | None = None) -> None:
    """Raise if the canonical schema is not valid Draft 2020-12."""
    Draft202012Validator.check_schema(schema or load_schema())


def _json_path(parts: Iterable[Any]) -> str:
    path = "$"
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return path


def validate_schema_instance(
    result: Any, schema: dict[str, Any] | None = None
) -> list[str]:
    """Return all JSON Schema validation errors in a stable readable order."""
    active_schema = schema or load_schema()
    Draft202012Validator.check_schema(active_schema)
    validator = Draft202012Validator(active_schema)
    errors = sorted(
        validator.iter_errors(result),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    return [
        f"schema: {_json_path(error.absolute_path)}: {error.message}"
        for error in errors
    ]


def derive_is_blocker(finding: dict[str, Any]) -> bool:
    """Derive blocker status only from the approved deterministic conditions."""
    return (
        finding["finding_type"] in BLOCKER_ELIGIBLE_TYPES
        and finding["materiality"] == "MATERIAL"
        and finding["severity"] in {"HIGH", "CRITICAL"}
        and finding["human_review_required"] is False
    )


def derive_material_claims_sufficient(result: dict[str, Any]) -> bool:
    """Derive represented material-claim coverage from Evidence Statuses."""
    return all(
        claim["evidence_status"]
        in VERIFICATION_SUFFICIENT_EVIDENCE_STATUSES
        for claim in result["material_claims"]
    )


def derive_verdict(result: dict[str, Any]) -> str | None:
    """Derive the verdict for an eligible Full Gate result."""
    if (
        result["run_status"] != "COMPLETED"
        or result["review_type"] != "FULL_GATE_REVIEW"
    ):
        return None
    if any(finding["is_blocker"] for finding in result["findings"]):
        return "NOT_READY_FOR_PUBLICATION"
    if (
        any(
            finding["human_review_required"]
            for finding in result["findings"]
        )
        or result["coverage"]["material_claims_sufficient"] is False
    ):
        return "HUMAN_REVIEW_REQUIRED"
    if result["findings"]:
        return "PASS_WITH_FINDINGS"
    return "PASS"


def _duplicate_values(values: Iterable[str]) -> set[str]:
    return {value for value, count in Counter(values).items() if count > 1}


def validate_invariants(result: dict[str, Any]) -> list[str]:
    """Validate deterministic cross-field and cross-object product invariants."""
    issues: list[str] = []
    sources = result["sources"]
    material_claims = result["material_claims"]
    findings = result["findings"]
    human_review = result["human_review"]

    source_ids = [source["source_id"] for source in sources]
    duplicate_source_ids = sorted(_duplicate_values(source_ids))
    for source_id in duplicate_source_ids:
        issues.append(f"invariant: duplicate source_id {source_id!r}")

    finding_ids = [finding["finding_id"] for finding in findings]
    duplicate_finding_ids = sorted(_duplicate_values(finding_ids))
    for finding_id in duplicate_finding_ids:
        issues.append(f"invariant: duplicate finding_id {finding_id!r}")

    claim_ids = [claim["claim_id"] for claim in material_claims]
    duplicate_claim_ids = sorted(_duplicate_values(claim_ids))
    for claim_id in duplicate_claim_ids:
        issues.append(f"invariant: duplicate claim_id {claim_id!r}")

    source_id_set = set(source_ids)
    source_by_id = {source["source_id"]: source for source in sources}
    claim_id_set = set(claim_ids)
    finding_by_id = {finding["finding_id"]: finding for finding in findings}
    findings_by_claim_id: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for claim in material_claims:
        claim_id = claim["claim_id"]
        minimum_references = MATERIAL_CLAIM_MINIMUM_EVIDENCE_REFS[
            claim["evidence_status"]
        ]
        if len(claim["evidence_refs"]) < minimum_references:
            issues.append(
                f"invariant: material claim {claim_id!r} with Evidence Status "
                f"{claim['evidence_status']} requires at least "
                f"{minimum_references} evidence_refs"
            )
        for reference in claim["evidence_refs"]:
            if reference["source_id"] not in source_id_set:
                issues.append(
                    "invariant: material claim "
                    f"{claim_id!r} references unknown source_id "
                    f"{reference['source_id']!r}"
                )
            elif source_by_id[reference["source_id"]]["usable"] is False:
                issues.append(
                    "invariant: material claim "
                    f"{claim_id!r} references unusable source_id "
                    f"{reference['source_id']!r}"
                )

    for finding in findings:
        finding_id = finding["finding_id"]
        for claim_id in finding["material_claim_ids"]:
            if claim_id not in claim_id_set:
                issues.append(
                    f"invariant: finding {finding_id!r} references unknown "
                    f"material claim_id {claim_id!r}"
                )
            else:
                findings_by_claim_id[claim_id].append(finding)
        for reference in finding["evidence_refs"]:
            if reference["source_id"] not in source_id_set:
                issues.append(
                    "invariant: finding "
                    f"{finding_id!r} references unknown source_id "
                    f"{reference['source_id']!r}"
                )
            elif source_by_id[reference["source_id"]]["usable"] is False:
                issues.append(
                    "invariant: finding "
                    f"{finding_id!r} references unusable source_id "
                    f"{reference['source_id']!r}"
                )

    summaries_by_finding: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for summary in human_review:
        finding_id = summary["finding_id"]
        summaries_by_finding[finding_id].append(summary)
        if finding_id not in finding_by_id:
            issues.append(
                "invariant: human_review references unknown finding_id "
                f"{finding_id!r}"
            )

    for finding_id, summaries in sorted(summaries_by_finding.items()):
        if len(summaries) > 1:
            issues.append(
                "invariant: duplicate human_review entries for finding_id "
                f"{finding_id!r}"
            )

    for finding in findings:
        finding_id = finding["finding_id"]
        requires_review = finding["human_review_required"]
        reason = finding["human_review_reason"]
        request = finding["human_review_request"]
        summaries = summaries_by_finding.get(finding_id, [])

        if requires_review:
            if finding["materiality"] == "NON_MATERIAL":
                issues.append(
                    f"invariant: finding {finding_id!r} with NON_MATERIAL "
                    "Materiality must not require Human Review"
                )
            if reason is None:
                issues.append(
                    f"invariant: finding {finding_id!r} requires a "
                    "human_review_reason"
                )
            if not isinstance(request, str) or not request.strip():
                issues.append(
                    f"invariant: finding {finding_id!r} requires a non-empty "
                    "human_review_request"
                )
            if len(summaries) != 1:
                issues.append(
                    f"invariant: finding {finding_id!r} requiring Human Review "
                    "must have exactly one human_review summary"
                )
            elif (
                summaries[0]["reason"] != reason
                or summaries[0]["request"] != request
            ):
                issues.append(
                    f"invariant: human_review summary for finding {finding_id!r} "
                    "must match its reason and request"
                )
        else:
            if reason is not None:
                issues.append(
                    f"invariant: finding {finding_id!r} not requiring Human "
                    "Review must have null human_review_reason"
                )
            if request is not None:
                issues.append(
                    f"invariant: finding {finding_id!r} not requiring Human "
                    "Review must have null human_review_request"
                )
            if summaries:
                issues.append(
                    f"invariant: finding {finding_id!r} not requiring Human "
                    "Review must not appear in human_review"
                )

        expected_domain = FINDING_TYPE_DOMAINS[finding["finding_type"]]
        if finding["primary_domain"] != expected_domain:
            issues.append(
                f"invariant: finding {finding_id!r} type "
                f"{finding['finding_type']} requires primary_domain "
                f"{expected_domain}"
            )

        allowed_severities = MATERIALITY_SEVERITIES[finding["materiality"]]
        if finding["severity"] not in allowed_severities:
            issues.append(
                f"invariant: finding {finding_id!r} has invalid "
                f"{finding['materiality']} + {finding['severity']} combination"
            )

        finding_type = finding["finding_type"]
        if finding_type in CRITICAL_ALLOWED_TYPES:
            maximum = "CRITICAL"
        elif finding_type in MAX_HIGH_TYPES:
            maximum = "HIGH"
        elif finding_type in MAX_MEDIUM_TYPES:
            maximum = "MEDIUM"
        else:
            raise AssertionError(
                f"No severity cap configured for Finding Type {finding_type}"
            )
        if SEVERITY_RANK[finding["severity"]] > SEVERITY_RANK[maximum]:
            issues.append(
                f"invariant: finding {finding_id!r} type {finding_type} "
                f"has maximum Severity {maximum}"
            )

        required_materiality = REQUIRED_MATERIALITY.get(finding_type)
        if (
            required_materiality is not None
            and finding["materiality"] != required_materiality
        ):
            issues.append(
                f"invariant: finding {finding_id!r} type {finding_type} "
                f"requires Materiality {required_materiality}"
            )

        if (
            finding_type in {"QUOTE_INTEGRITY_MISMATCH", "ATTRIBUTION_ERROR"}
            and finding["severity"] == "LOW"
        ):
            issues.append(
                f"invariant: finding {finding_id!r} type {finding_type} "
                "must not have LOW Severity"
            )

        expected_blocker = derive_is_blocker(finding)
        if finding["is_blocker"] is not expected_blocker:
            issues.append(
                f"invariant: finding {finding_id!r} is_blocker must be "
                f"{str(expected_blocker).lower()}"
            )

    for claim in material_claims:
        claim_id = claim["claim_id"]
        evidence_status = claim["evidence_status"]
        if evidence_status not in NON_SUPPORTED_EVIDENCE_STATUSES:
            continue
        qualifying_findings = [
            finding
            for finding in findings_by_claim_id.get(claim_id, [])
            if finding["materiality"] == "MATERIAL"
            and finding["evidence_status"] == evidence_status
        ]
        if not qualifying_findings:
            issues.append(
                f"invariant: non-supported material claim {claim_id!r} with "
                f"Evidence Status {evidence_status} requires at least one "
                "linked MATERIAL Finding with matching Evidence Status"
            )

    run_status = result["run_status"]
    review_type = result["review_type"]
    verdict = result["verdict"]

    if (
        run_status == "COMPLETED"
        and review_type == "FULL_GATE_REVIEW"
        and not any(source["usable"] for source in sources)
    ):
        issues.append(
            "invariant: COMPLETED FULL_GATE_REVIEW requires at least one "
            "usable supporting source"
        )

    if run_status == "COMPLETED" and review_type == "FULL_GATE_REVIEW":
        expected_coverage = derive_material_claims_sufficient(result)
        actual_coverage = result["coverage"]["material_claims_sufficient"]
        if actual_coverage is not expected_coverage:
            issues.append(
                "invariant: coverage.material_claims_sufficient must be "
                f"{str(expected_coverage).lower()} based on material_claims, "
                f"got {str(actual_coverage).lower()}"
            )

    if run_status != "COMPLETED" and verdict is not None:
        issues.append(
            "invariant: verdict must be null when run_status is not COMPLETED"
        )
    if review_type == "FOCUSED_REVIEW" and verdict is not None:
        issues.append(
            "invariant: verdict must be null for FOCUSED_REVIEW"
        )
    if (
        run_status == "COMPLETED"
        and review_type == "FULL_GATE_REVIEW"
        and verdict is None
    ):
        issues.append(
            "invariant: COMPLETED FULL_GATE_REVIEW requires a verdict"
        )

    if run_status == "COMPLETED" and review_type == "FULL_GATE_REVIEW":
        expected_verdict = derive_verdict(result)
        if verdict != expected_verdict:
            issues.append(
                f"invariant: verdict must be {expected_verdict}, got {verdict}"
            )

    if (
        result["coverage"]["material_claims_sufficient"] is False
        and verdict in {"PASS", "PASS_WITH_FINDINGS"}
    ):
        issues.append(
            "invariant: insufficient material-claim coverage cannot coexist "
            f"with {verdict}"
        )

    return issues


def validate_result_data(
    result: Any, schema: dict[str, Any] | None = None
) -> list[str]:
    """Return schema errors, or deterministic invariant errors when structural."""
    active_schema = schema or load_schema()
    schema_issues = validate_schema_instance(result, active_schema)
    if schema_issues:
        return schema_issues
    return validate_invariants(result)


def _load_result(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a PR Release Gatekeeper result JSON file."
    )
    parser.add_argument("result", type=Path, help="Path to UTF-8 result JSON")
    args = parser.parse_args(argv)

    try:
        result = _load_result(args.result)
        issues = validate_result_data(result)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print("INVALID")
        print(f"- input: {error}")
        return 1

    if issues:
        print("INVALID")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())
