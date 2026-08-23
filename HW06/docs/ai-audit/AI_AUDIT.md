# HW06 - AI Audit Report (Mandatory Appendix)

Student ID: **23127184** · Assignment: **HW06 - API Testing** · AI policy: **Open**

## Declaration

> I use AI tools for the following tasks.

*(If any part of the work was done without AI, say so explicitly for that part
rather than leaving it ambiguous.)*

## Tools declared

| Tool | Model / version | Used for |
|---|---|---|
| Claude Code | Opus 5 | Repository scaffolding, harness scripts, collection skeletons, source reading |
| | | Test-case generation for API 1 |
| | | Test-case generation for API 2 |
| | | Test-case generation for API 3 |
| | | Test-case generation for API 4 |

Non-AI tools used: Postman, Newman + newman-reporter-htmlextra, Node.js,
Python, Git, GitHub Actions.

---

## Interaction log

Every interaction needs: tool name, date and time, the prompt verbatim, and the
AI output. Keep them in order. Long outputs go in
`docs/ai-audit/transcripts/` with a link from the table row.

### AI-001 | Scaffolding the HW06 workspace

- **Tool:** Claude Code (Opus 5)
- **Date/time:** 2026-08-23
- **Prompt:** "đọc yêu cầu hw06 và setup cho mình" (read the HW06 requirements
  and set up the workspace), followed by the API selection FR-01, FR-06, FR-11,
  FR-13 and the decision to use Postman cloud features.
- **Output:** The HW06 directory tree, `package.json` + Newman toolchain, four
  Postman collection skeletons with the `X-Student-Id` pre-request harness,
  Postman environments, data-driven CSV fixtures, the CI workflow and green-gate
  manifest, the phase/audit/critique/CI document skeletons, and a bug report
  seeded from a verified smoke run.
- **My review:** *(record what you checked and what you changed)*

### AI-002 |

- **Tool:**
- **Date/time:**
- **Prompt:**
- **Output:**
- **My review:**

---

## Review discipline applied

For each batch of AI output, record which of these was done:

- [ ] Read every generated test case against `refs/spec/api_specification.md`
- [ ] Checked expected results against the requirement document, not against
      the SUT's observed behaviour
- [ ] Executed the cases rather than trusting the AI's predicted results
- [ ] Corrected or discarded the cases that did not survive review
- [ ] Recorded the corrections in the phase-2 audit documents

## Bloom-AI level evidence

| Level | Where it is evidenced |
|---|---|
| G9.2 Apply | Driving the AI step by step through partitions, state transitions, security and schema — `docs/phases/*/01-generate.md` |
| G9.3 Analyse | VALID / INVALID / INCOMPLETE audit with reasoning — `docs/phases/*/02-audit.md` |
| G9.4 Collaborate | Extension cases and the diagnosis of why the AI missed them — `docs/phases/*/03-extend.md` |
| G9.5 Create | The AI-driven test generator design — `docs/design/GENERATOR_DESIGN.md` and `.claude/skills/` |
