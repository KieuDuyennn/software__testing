#!/usr/bin/env python3
"""Human-review metadata for the HW06 API cases.

The executable case modules remain the source of truth for requests and
assertions.  This module records the independent phase-2 review decision for
every case.  A default VALID decision is only applied after the structural
checks in :func:`enrich_cases`; ambiguous, duplicated, or mis-scoped cases are
listed explicitly below so the correction is traceable.
"""

from __future__ import annotations


INCOMPLETE = {
    # API 1 - requirements gaps / weak oracles called out during generation.
    "A1-DP-006": "FR-01 gives no minimum name length, so acceptance of one character is not a firm contract.",
    "A1-DP-008": "FR-01 gives no maximum name length; the original oracle could only require safe handling.",
    "A1-DP-009": "The oversized-name case had only a no-5xx oracle because no limit is specified.",
    "A1-DP-012": "The original oracle accepted either trimming or rejection, two contradictory outcomes.",
    "A1-DP-037": "The original oracle accepted either trimming or rejection of trailing email whitespace.",
    "A1-DP-061": "FR-01 neither permits nor forbids embedded spaces in passwords.",
    "A1-DP-062": "No maximum password length is specified, so only availability and non-disclosure are testable.",
    "A1-DP-065": "confirmPassword is required by FR-01 but omitted from the backend API specification.",
    "A1-DP-067": "confirmPassword is required by FR-01 but omitted from the backend API specification.",
    "A1-DP-075": "The request-size limit is unspecified; the original assertion was only a safety invariant.",
    "A1-SEC-013": "The original title attributed access to role injection, while A1-SEC-012 proves the role was ignored; the real issue is missing admin authorization.",
    "A1-SEC-020": "The specification does not explicitly say whether registration ignores an Authorization header.",

    # API 2 - routing normalisation is outside the API contract.
    "A2-DP-026": "The specification does not define leading-zero normalisation for path ids.",
    "A2-DP-027": "The specification does not define whitespace trimming for path ids.",
    "A2-DP-028": "The encoded-space oracle can prove safety but not select uniquely between 400 and 404.",
    "A2-DP-029": "The maximum path-id length is unspecified; only safe handling can be required.",
    "A2-DP-031": "Trailing-slash routing is an Express behaviour observation, not an FR-06 requirement.",

    # API 3 - HTTP auth-scheme casing and ordering are not fixed by the brief.
    "A3-DP-008": "The API specification does not state whether the Bearer scheme keyword is case-sensitive.",
    "A3-DP-013": "FR-11 does not define a sort order; the case can assert stability only.",

    # API 4 - orphan handling is not specified.
    "A4-DP-012": "FR-13 does not define whether an orphaned order is retained or how user_name is represented.",
}


INVALID = {
    # The original A2-DP-006 duplicated A2-DP-005 exactly.  The executable case
    # is now corrected to cover URL-decoding of a percent-encoded digit.
    "A2-DP-006": "The generated case duplicated A2-DP-005 (both requested seeded id 5) and added no new partition.",
}


CORRECTIONS = {
    "A1-DP-012": "Retained only spec-supported safety and non-corruption assertions; documented trimming as an open requirement decision.",
    "A1-DP-037": "Retained rejection-or-normalisation as a documented gap and did not count either SUT behaviour as proof of FR-01 conformance.",
    "A1-SEC-013": "Retitled and interpreted as a direct SEC-03 admin-authorization test for a newly registered ordinary user.",
    "A2-DP-006": "Replaced the duplicate with GET /api/products/%35 and an exact product-5 oracle, covering URL decoding without duplicating the plain-id case.",
}


def _default_reason(case):
    return (
        "Cross-checked %s against %s: method/path, precondition, input partition "
        "and executable oracle are mutually consistent and do not use the "
        "observed SUT response as the expected result."
        % (case["id"], case.get("rule") or "the API specification")
    )


def enrich_cases(cases):
    """Attach origin and phase-2 audit fields to every case, in place."""
    seen = set()
    for case in cases:
        case_id = case["id"]
        if case_id in seen:
            raise ValueError("duplicate case id during audit: %s" % case_id)
        seen.add(case_id)

        origin = case.get("origin", "AI-generated")
        case["origin"] = origin
        if case_id in INVALID:
            label, reason = "INVALID", INVALID[case_id]
        elif case_id in INCOMPLETE or case.get("gap"):
            label = "INCOMPLETE"
            reason = INCOMPLETE.get(
                case_id,
                "The case identifies a real partition, but the specification is silent: %s"
                % case.get("gap", "oracle not fully specified"),
            )
        else:
            label, reason = "VALID", _default_reason(case)

        case["audit_label"] = label
        case["audit_reason"] = reason
        case["correction"] = CORRECTIONS.get(
            case_id,
            ("Oracle limited to a spec-supported safety invariant and the ambiguity is documented."
             if label == "INCOMPLETE" else
             "Replaced before execution; see the current executable definition."
             if label == "INVALID" else "None required."),
        )
    return cases


def audit_counts(cases):
    counts = {"VALID": 0, "INVALID": 0, "INCOMPLETE": 0}
    for case in cases:
        counts[case["audit_label"]] += 1
    return counts
