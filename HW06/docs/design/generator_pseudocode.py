"""
HW06 - AI-driven API test generator: PSEUDOCODE.

This is a design artefact, not a runnable program. It exists to make the stage
boundaries and the data passed between them concrete enough to draw.

Stage names match docs/design/GENERATOR_DESIGN.md and the editable diagram.
The submitted version requires student review of every design decision.
"""

# =============================================================================
# INPUTS  (decision D1)
# =============================================================================
#
#   api_spec        api_specification.md - endpoints, request bodies, responses
#   requirements    FR-01..FR-19 and SEC-01..SEC-07 from the SUT README
#   target          which endpoint to generate for, e.g. "POST /api/register"
#   student_id      "23127184" - baked into every generated request
#
# Why requirements are a separate input, not an optional extra: the specification
# documents happy paths. Every critical defect confirmed in this assignment
# (plaintext passwords, IDOR, missing role check) is a violation of a SEC rule
# that the specification does not mention at all. A generator fed only the spec
# cannot produce a case that finds them.


def generate_test_suite(api_spec, requirements, target, student_id):
    # -------------------------------------------------------------------------
    # STAGE 0 - Parse the contract
    # -------------------------------------------------------------------------
    # Turn prose into a structure the later stages can iterate over, so no
    # stage has to re-read the Markdown.
    endpoint = parse_endpoint(api_spec, target)
    #   endpoint.method, endpoint.path
    #   endpoint.params      -> [{name, location, type, required, constraints}]
    #   endpoint.responses   -> {status_code: schema}
    #   endpoint.auth        -> none | bearer | bearer+admin

    rules = select_applicable_rules(requirements, endpoint)
    #   Every FR and SEC id that constrains this endpoint. Carried through to
    #   the end so each generated case can name the rule it enforces - a case
    #   that cannot name one is a case with no oracle.

    # -------------------------------------------------------------------------
    # STAGE 1 - Domain partitions        (one case per class and boundary)
    # -------------------------------------------------------------------------
    partition_cases = []
    for param in endpoint.params:
        classes = ai_derive_equivalence_classes(param, rules)
        #   valid classes, invalid classes, and the boundaries between them.
        #   Constraints come from `rules`, NOT from the SUT: FR-01 states the
        #   password policy that POST /api/register fails to implement, so the
        #   policy has to come from the requirement text or the generated case
        #   would assert the defect as correct.
        for cls in classes + boundaries_of(classes):
            partition_cases.append(
                build_case(
                    dimension="domain",
                    param=param,
                    value=cls.representative_value,
                    expected=cls.expected_outcome,   # from the rule, not the SUT
                    rule=cls.source_rule,
                )
            )

    # -------------------------------------------------------------------------
    # STAGE 2 - State transitions
    # -------------------------------------------------------------------------
    machine = ai_extract_state_machine(rules)
    #   e.g. FR-10: pending -> confirmed -> shipping -> delivered,
    #                pending|confirmed -> canceled
    transition_cases = []
    for state in machine.states:
        for event in machine.events:
            legal = machine.is_legal(state, event)
            transition_cases.append(
                build_case(
                    dimension="state",
                    setup=path_to_reach(machine, state),   # how to get there
                    action=event,
                    expected="accepted" if legal else "rejected",
                    rule=machine.rule_id,
                )
            )
    #   Generating the ILLEGAL transitions is the point. `canceled -> delivered`
    #   is a defect precisely because nobody thought to try it.

    # -------------------------------------------------------------------------
    # STAGE 3 - Security                 (SEC-01..SEC-07)
    # -------------------------------------------------------------------------
    security_cases = []
    for sec_rule in rules.security:
        if not applies_to(sec_rule, endpoint):
            record_not_applicable(sec_rule, endpoint, reason="...")
            continue
        for attack in attack_patterns_for(sec_rule):
            #   SEC-02 -> no token / expired token / forged token
            #   SEC-03 -> non-admin token on an admin route
            #   SEC-05 -> SQL injection in every string parameter
            #   SEC-06 -> inject a privileged field the client must not control
            security_cases.append(
                build_case(
                    dimension="security",
                    actors=attack.actors,   # >= 2 actors for IDOR / ownership
                    payload=attack.payload,
                    expected=attack.must_be_refused,
                    rule=sec_rule.id,
                )
            )
    #   Multi-actor setup is what a single-endpoint prompt never produces. IDOR
    #   is undetectable with one user, so the actor model belongs in the
    #   generator, not in the prompt.

    # -------------------------------------------------------------------------
    # STAGE 4 - Schema validation
    # -------------------------------------------------------------------------
    schema_cases = []
    for status, schema in endpoint.responses.items():
        schema_cases.append(
            build_case(
                dimension="schema",
                expected_status=status,
                assertion=json_schema_assertion(schema, strict=True),
                rule="spec conformance",
            )
        )
    #   strict=True matters: additionalProperties=false catches fields the SUT
    #   leaks that the spec never promised - which is how the login response
    #   returning the whole users row shows up as a schema failure.
    #
    #   Run schema cases across EVERY id partition, not just one: BUG-04's price
    #   type depends on the id's parity, so a single-id schema check misses it.

    # -------------------------------------------------------------------------
    # STAGE 5 - Validate the generated cases    (decision D6)
    # -------------------------------------------------------------------------
    all_cases = partition_cases + transition_cases + security_cases + schema_cases
    validated, rejected = [], []
    for case in all_cases:
        problems = []
        if not case.rule:
            problems.append("no requirement id - the case has no oracle")
        if case.expected_derived_from_sut_response:
            problems.append("oracle taken from observed behaviour, not the spec")
        if duplicates(case, validated):
            problems.append("duplicate of an existing case")
        if case.needs_setup and not case.setup:
            problems.append("precondition not reachable")

        (rejected if problems else validated).append((case, problems))

    # -------------------------------------------------------------------------
    # STAGE 6 - Human review checkpoint     (decision D3)
    # -------------------------------------------------------------------------
    # The brief is explicit: raw AI output is not acceptable, and the student is
    # responsible for correctness. So the generator STOPS here and emits a
    # review queue - it does not publish a collection on its own authority.
    reviewed = human_review(
        validated,
        labels=["VALID", "INVALID", "INCOMPLETE"],
        require_reason=True,
    )

    # -------------------------------------------------------------------------
    # STAGE 7 - Emit artefacts              (decision D4)
    # -------------------------------------------------------------------------
    collection = to_postman_collection(
        [c for c in reviewed if c.label == "VALID"],
        pre_request_script=inject_student_id_header(student_id),  # non-negotiable
        folders_by="dimension",
    )
    excel = to_excel_testcases(reviewed)

    return collection, excel, rejected


# =============================================================================
# FEEDBACK PATH
# =============================================================================
#
# Cases rejected at stage 5, and cases labelled INVALID or INCOMPLETE at stage
# 6, go back to the stage that produced them together with the reason. The
# reason is the useful part: it names a systematic weakness in the generation
# prompt, which is what gets fixed. Draw this arrow on the diagram - a
# generator without it produces the same wrong case forever.
