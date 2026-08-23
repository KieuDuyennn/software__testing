# HW06 - AI-Driven API Test Generator (Design)

Section 7 of the brief, Bloom-AI level **G9.5 (Create)** — worth 10 points.

**Goal:** given the API specification, produce test cases automatically.

**Deliverables:** a self-drawn diagram, pseudocode, and (encouraged) a working
Agent Skill plus a YouTube demo of it generating tests for one API.

---

## ⚠ The diagram must be self-drawn

Section 11 lists the diagram as one of three items TAs verify as **not
AI-generated**:

> *"The AI test-generator diagram, which must be self-drawn — designed by you,
> not generated directly by an AI."*

So this file deliberately contains **no diagram**. It contains the design
decisions you need to make, phrased as questions. Answer them, then draw the
result yourself — draw.io, Excalidraw, Figma, PowerPoint, or pen and paper
photographed are all fine; the tool does not matter, the authorship does.

Save it to `docs/design/diagram/` as PNG (plus the editable source).

---

## Design decisions to make

Write your answer under each. These answers *are* the design — the diagram is
just their picture.

### D1. What does the generator take as input?

Options: the Markdown spec as free text · an OpenAPI conversion · the spec plus
the requirement document (FR/SEC ids) · the spec plus the live SUT.

Consider: the six defects already confirmed in `docs/bugs/BUG_REPORT.md` were
**not** discoverable from `api_specification.md` alone. BUG-06 is invisible
unless the generator also reads SEC-03. That is an argument about input, and
it belongs in your design.

> **Your answer:**

### D2. What are the stages, and what does each one hand to the next?

The four coverage dimensions the brief mandates — domain partitions, state
transitions, security, schema validation — suggest one stage each. Decide
whether they run in sequence or in parallel, and what the shared intermediate
representation is (a parameter model? an endpoint model? a state machine?).

> **Your answer:**

### D3. Where does the human sit in the loop?

You audited every AI-generated case by hand in phase 2. Does the generator
automate that, ask for approval at a checkpoint, or emit a review queue?

> **Your answer:**

### D4. What is the output artefact?

A Postman collection JSON? An Excel test-case table? Both? If it is a
collection, it must carry the `X-Student-Id` pre-request script — that is a
hard requirement of this assignment and therefore a hard requirement of the
generator.

> **Your answer:**

### D5. How does it avoid the failure you actually observed?

Your extension phase will document why the AI missed certain cases. Whatever
that reason turns out to be, the generator has to have an answer for it. If the
cause is "the AI asserts observed behaviour instead of specified behaviour",
then something in the pipeline must ban the SUT's own responses as an oracle.

> **Your answer:**

### D6. How is a generated case validated before it is trusted?

Executable? Deterministic? Independent of run order? Does it clean up after
itself? Who decides — a schema check, a dry run, an LLM judge, you?

> **Your answer:**

---

## Diagram checklist

Once drawn, the diagram should show:

- [ ] Inputs, with their sources
- [ ] Each stage as a distinct box, in order
- [ ] What flows along each arrow (not just that an arrow exists)
- [ ] The human review checkpoint
- [ ] The output artefacts
- [ ] The feedback path — what happens to a case that fails validation
- [ ] Your name or student ID somewhere on the drawing

---

## Pseudocode

Lives in `docs/design/generator_pseudocode.py`. Keep it aligned with the
diagram: same stage names, same order. Pseudocode that contradicts the diagram
reads as though one of the two was produced by someone else.

## Implementation

The reusable Agent Skill scaffold is in `.claude/skills/api-test-generator/`.
Section 7 makes the implementation *encouraged*, not required — the diagram and
pseudocode are the graded parts.

If you record the demo video, show it generating tests for **one** API end to
end, and put the YouTube link in `README.md`.
