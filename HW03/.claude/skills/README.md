# GUI & Usability Testing skill suite

Seven skills that together cover an end-to-end GUI/usability testing engagement on a web
application. Each directory is self-contained and installs on its own; used in sequence they form
a pipeline where each stage consumes the previous stage's artefact.

`evidence-discipline.md` is the one document two skills share, so `gui-checklist-execution` carries
a vendored copy of it. Edit both or neither.

```
web-ui-survey ──► gui-checklist-design ──► gui-checklist-execution ──┐
                                                                     ├──► findings-log
                          usability-test-study ──────────────────────┤
                          cross-platform-matrix ────────────────────-┘

ai-audit-log runs alongside every stage above.
```

| Skill | Answers | Produces |
| --- | --- | --- |
| `web-ui-survey` | What does this application actually contain? | Widget inventory + URL map |
| `gui-checklist-design` | What should we check, and on what authority? | Traceable checklist |
| `gui-checklist-execution` | Does this screen pass? | Per-screen Pass/Fail/N/A + evidence |
| `usability-test-study` | Can real people accomplish their goal? | Usability report, SUS/UEQ-S, ranked findings |
| `cross-platform-matrix` | Does it hold up across OS / browser / device? | Compatibility matrix + evidence |
| `findings-log` | What did we find, all of it, in one place? | Normalised findings log |
| `ai-audit-log` | How was AI used, verifiably? | Verbatim interaction log |

## Design principles shared across the suite

**Instruments and results stay separate.** A checklist says how to check; an execution report says
what happened. Mixing them makes both untrustworthy — a defect written into the instrument was
never observed, and a shared instrument carrying results forces everyone who uses it to inherit
findings they did not make.

**A negative result is a statement about the instrument.** "The selector matched nothing" is not
"the product lacks the widget". Claims of absence need a second, differently-shaped instrument
before they are recorded. `web-ui-survey/references/evidence-discipline.md` is the long form of
this and is the most reusable document in the suite.

**Some evidence cannot be produced by an agent, and pretending otherwise is fabrication.** Real
participants, real-device screenshots, whether a QR code physically scans, what a screen reader
announces. Each skill names its own boundary and stops there rather than generating something
plausible.

**Generation and verification are separate passes with different grounding.** An agent checking
its own output looks through the same instrument that produced the error. Verification needs
evidence the agent did not create.

## Provenance — read this before cloning

The suite was written while running a real GUI/usability engagement on one web application, under
a brief that fixed some parameters. Where a number or a rule came from that brief rather than from
the method, it is called out in place. The ones to check against your own context:

- **Five usability participants.** A reasonable default for formative discovery on a single user
  group, and wrong for measurement, for multiple user groups, or for regulated summative
  evaluation. `usability-test-study` has a table of when to use what.
- **The coverage floor in `cross-platform-matrix`** (3 OS × 5 browsers × 3 device classes) was a
  brief's requirement. Real risk concentrates by *rendering engine*, not by brand count — the skill
  says so and the script warns when a matrix has only one engine.
- **Four interface aspects** (general UI / forms / navigation / feedback-and-state) in
  `gui-checklist-design` are a serviceable default, not a standard. Substitute whatever taxonomy
  your engagement defines and the conformance-map technique still works.
- **Checklist size (~50 items)** was chosen so one person could execute it across several screens
  in the time available. Scale it to your own budget; the reduction guidance matters more than the
  number.
- **Severity scales** are Nielsen 0–4 for usability and a five-level functional scale for bugs. If
  your tracker imposes its own, use that and keep the two scales distinct.

Nothing in the suite depends on the application it was developed against. The lessons in
`web-ui-survey/references/evidence-discipline.md`, however, are all drawn from real mistakes made
during that engagement, which is why they are specific.

## Where these live

Developed in-project under `.claude/skills/` so they ship with the work that exercised them.
To reuse them elsewhere, copy the directories into a marketplace repository:

```
claude-skills/
├── .claude-plugin/marketplace.json   # one plugin entry listing ./skills/*
└── skills/<copy these directories>
```

Then `/plugin marketplace add <owner>/claude-skills` once, and every project has them. Prefer
this over a git submodule: a submodule needs a per-project pin and exports as an empty directory
when the project is archived.
