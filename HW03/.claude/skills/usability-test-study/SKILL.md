---
name: usability-test-study
description: Design, run and analyse a usability study with real human participants — task scenarios, moderator script, think-aloud sessions, task success and time-on-task, SUS or UEQ-S, and a report that clusters session observations into its own severity-ranked findings. Use to observe people using a product, build or score a participant questionnaire, write recruiting criteria, or turn fresh session notes from a study just run into that study's ranked findings. Trigger on "usability testing", "test với người dùng thật", "kiểm thử người dùng", "bảng khảo sát cho người dùng", "SUS", "UEQ", "chấm SUS", "think aloud", "task scenario", "moderator script", "bao nhiêu người tham gia", "usability report", "trong buổi test này người dùng gặp lỗi gì". Do NOT use with no users involved (web-ui-survey, gui-checklist-execution), or to re-rate findings already sitting in a consolidated log (findings-log). Never invent participants, sessions, quotes or scores.
---

# Usability test study

Heuristic review tells you what violates a principle. A usability study tells you what actually
stops a person from getting their goal done — which is often not the same list, and is the reason
to run one rather than assume.

The output is a report with three parts that must agree: **metrics** (what happened), **findings**
(what it means, ranked), and **recommendations** (what to change). Findings not traceable to
observed behaviour are opinions; observations never turned into ranked findings are notes.

## What an agent can and cannot do here

Be exact about this before starting, because the boundary is not negotiable:

**An agent can** design task scenarios, write the moderator script and consent framing, build the
note template and the questionnaire, score responses, compute metrics, cluster observations, rank
severity, draft the report.

**An agent cannot** be a participant, recruit participants, or supply session data. If asked to
generate participants, sessions, quotes or scores, decline and say why: fabricated study data
misrepresents real people's behaviour, and every downstream conclusion inherits the fabrication.
Where a study is verified by contacting participants, invented ones are also detected. Offer the
recruiting criteria and screener instead.

## Phase 1 — Design

### Task scenarios: give a goal, not a click path

A scenario that lists steps tests whether someone can follow instructions. A scenario that states
a goal tests whether the product is usable.

| | |
| --- | --- |
| Weak | "Click Events, then click the first event, then click Register, then select Student." |
| Strong | "You heard there's a workshop next week you'd like to attend. Sign yourself up, and show me the check-in code you'd bring on the day." |

The strong version names an outcome the participant can recognise as achieved, and stays silent
about the route — so a bad route becomes visible instead of being prescribed away. Keep the
product's own vocabulary out of the wording where you can: if the scenario says "register" and the
button says "Register", you have tested nothing about findability.

Write 2–4 scenarios covering the screens under study, each completable in roughly 3–8 minutes, and
define **in advance** what counts as complete. Deciding afterwards is where success rates become
unreliable.

### Metrics

| Metric | How to capture |
| --- | --- |
| Task success | Complete / partial / fail, against the criterion written in advance |
| Time on task | Start when they begin acting, stop at the success criterion. Note if you intervened. |
| Errors | Wrong action requiring recovery. Count them, don't just note them. |
| Hesitations | Pauses > ~3 s, backtracks, re-reads. The richest signal in think-aloud. |
| Post-task attitude | **SUS** (10 items, general and comparable) or **UEQ-S** (8 items, faster, splits pragmatic from hedonic). Pick one and use it for everyone. |
| Open probes | Clarity, error recovery, speed, trust — 3–5 questions, same wording each time |

### Recruit and pilot

Participants must match the real user profile — the study measures nothing if the wrong people take
it. Record verifiable contact details, and mask them in the report (middle digits of a phone
number, local part of an email) so the report can be shared without exposing anyone.

**Run a pilot with one extra person.** It always finds something: a task nobody understands, a
broken flow, a scenario that takes triple the estimate. Fix, then start counting. Pilot data does
not go in the results.

### How many participants

The examples in this skill assume around **five**, which is the right default for a *formative,
moderated, discovery* study on one user group. It comes from Nielsen and Landauer's cost-benefit
curve: five users surface about 85 % of the problems findable in a homogeneous group, and three
rounds of five beat one round of fifteen, because each round gets to test the fixes.

**That 85 % is a mean, and the spread around it is large.** Faulkner (2003) resampled from 60 users
and found individual five-user samples ranging from 55 % to nearly 100 % of the known problem set;
ten users raised the *floor* to 80 %, twenty to 95 %. So the honest reading of the five-user result
is not "five is enough" but "five is the cheapest useful round" — the variance is the argument for
iterating, not for stopping. If you get one shot with no second round, five is thin and you should
say so in Limitations.

Five is a default, not a rule. Adjust deliberately:

| Situation | Participants | Why |
| --- | --- | --- |
| Formative discovery, one user group | ~5 | The curve flattens; further sessions mostly repeat findings |
| Several distinct user groups (e.g. administrator vs end user, novice vs expert) | ~5 **per group** | Different mental models produce different problems; one pool of five hides this |
| You need to *measure* — compare two versions, track a score over releases | 20+ | Small samples give a SUS number with a confidence interval too wide to act on |
| Summative or regulated evaluation (e.g. medical-device human factors) | 15+ per group, per the applicable standard | The requirement is external; the curve is irrelevant |
| Unmoderated remote testing | Larger | No moderator, no think-aloud, so less signal per session |

Two consequences worth stating in a report. **Five supports discovery, not measurement** — report
task counts and severity-ranked findings, not statistics. And **a fixed number set by a brief is a
constraint, not a methodological finding**: if you were told to run five, say so in Limitations,
rather than implying five was chosen from the curve.

## Phase 2 — Run the sessions

**Frame it, every time, in the same words.** "I'm testing the product, not you. If something is
confusing, that's information I need. Please say what you're thinking out loud as you go."

**Observe neutrally.** No leading ("did you see the button at the top?"), no rescuing at the first
sign of struggle — struggle is the data. Intervene only when they are fully stuck and the session
would otherwise end, and record that you intervened, because it changes the task result.

**Take structured notes**, not prose. Prose notes cannot be counted across five sessions:

| Time | Task | Type | What happened / said (verbatim where possible) |
| 02:14 | T1 | hesitation | Scrolled past the Register block twice; "where do I actually sign up?" |
| 03:02 | T1 | error | Clicked the category filter expecting a detail page |

Types worth distinguishing: hesitation · error · workaround · verbalisation · request for help ·
expression of frustration. Record participants' words verbatim where you can — a quote carries a
finding further than a paraphrase.

Close each session with the questionnaire, then the probes. That order matters: probing first
contaminates the questionnaire.

## Phase 3 — Analyse

**Score the questionnaires with the script**, because hand-scoring SUS gets the reverse-scored
items wrong often enough to matter:

```bash
python .claude/skills/usability-test-study/scripts/score_sus.py responses.csv --instrument sus
python .claude/skills/usability-test-study/scripts/score_sus.py responses.csv --instrument ueq-s
```

Report the individual scores alongside the mean. A mean of 68 from five scores of 68 and a mean of
68 from 40/50/68/90/92 are different products, and only the spread shows it.

**Tabulate the task metrics** — success rate, mean time, error count per task. At small n, report
counts (`3/5 completed`) rather than percentages that imply precision you do not have.

**Cluster observations into findings.** Group by *cause*, not by symptom: three participants
hesitating in three different places for the same reason is one finding. Then separate the two kinds:

- **Individual slip** — one participant, once, no structural explanation. Report it as an
  observation, not a finding.
- **Systemic design problem** — appears in **2 or more of 5 sessions**, or once with a structural
  cause you can name (a control below the fold, a label that means something else in the domain,
  no feedback after an action).

**Rank severity 0–4** (Nielsen), judging **frequency, impact and persistence together** — Nielsen
asks for a combined judgement, not a product of three scores, and he adds market impact as a fourth
consideration where commercial appeal is at stake. Persistence is the one people forget: a problem
that keeps costing users after they have learned the workaround outranks a dramatic one-off.

| | |
| --- | --- |
| 0 | Not a usability problem |
| 1 | Cosmetic — fix if time permits |
| 2 | Minor |
| 3 | Major — high priority |
| 4 | Catastrophe — fix before release |

## The report

```markdown
# Usability report — <product / scope>
Method: moderated think-aloud, <n> participants, <dates>, <remote|in person>
Screens under test: <list>   Instrument: SUS | UEQ-S

## Task scenarios
Goal wording, and the success criterion defined in advance.

## Participants
| P | Profile | Contact (masked) | Date | Notes |

## Metrics
| Task | Complete | Partial | Fail | Mean time | Errors |
| Participant | SUS/UEQ-S | Notes |
Mean, spread, and individual scores.

## Findings, ranked by severity
For each: severity · what happened · how many participants · evidence (quote, timestamp,
screenshot) · why it happens · recommendation.

## Recommendations, prioritised
Concrete changes, ordered by severity then by cost.

## Limitations
Sample size, environment, tasks not covered, anything that constrains the conclusions.
```

**Interpret honestly.** A small formative sample surfaces most of the *findable* problems, but
supports no statistical claim — no significance, no confidence intervals, no comparison against an
industry benchmark as if it were measured. Say "3 of 5 participants", give the questionnaire mean
alongside the individual scores, and let the severity ranking carry the argument. See *How many
participants* above for when the number needs to be larger.

## Handing off

Real defects go to `findings-log` with the usability severity scale. If AI assisted with design,
scoring or drafting, log it with `ai-audit-log` — and record explicitly that the sessions and
participants were not AI-produced.
