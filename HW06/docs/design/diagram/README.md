# Generator diagram

Section 11 of the brief: the test-generator diagram is one of three items the
TAs verify as **not AI-generated**. It must be self-drawn.

## What to save here

| File | What it is |
|---|---|
| `generator-design.png` | Exported diagram used in the report |
| `generator-design.mmd` | Editable Mermaid source; import it with **Insert > Advanced > Mermaid** in draw.io |
| `generator-design.svg` | Editable vector layout used to create the readable report PNG |

The checked-in files are an editable draft. The final submitted diagram must
reflect the student's reviewed design decisions.

## Before editing

The source implements D1-D6 in `../GENERATOR_DESIGN.md`. Before submission,
open it in draw.io, review every label, and make any needed changes before the
demo. Mermaid import may become draw.io shapes or
an SVG depending on the draw.io version; keep this `.mmd` as the editable source.

## Checklist

- [ ] Inputs and where they come from
- [ ] One box per stage, in order, named as in the pseudocode
- [ ] What flows along each arrow
- [ ] The human review checkpoint
- [ ] Output artefacts
- [ ] The feedback path for rejected cases
- [ ] Your student ID on the drawing
