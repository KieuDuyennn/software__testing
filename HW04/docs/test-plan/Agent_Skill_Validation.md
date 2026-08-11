# Agent Skill validation evidence

**Skill under test:** `.claude/skills/playwright-automation/`

## Structural validation

Both `.claude/skills/playwright-automation/SKILL.md` and
`.claude/skills/ai-audit-log/SKILL.md` pass the `skill-creator` `quick_validate.py`
frontmatter and naming checks. The primary skill also includes the deterministic
`scripts/validate-feature.ps1` validator.

## Forward use against the three HW04 features

The validator was invoked with explicit spec, data, student ID and final JSON-report
paths. It checks case count, unique `tc_id`, recognizable external-data loading,
forbidden fixed waits, report attribution, ISO timestamps and report entry points.

| Feature | Cases / unique IDs | Report entry points | Validator result | Historical workflow state | Review note |
|---|---:|---:|---|---|---|
| FR-01 | 43 / 43 | 3 | `PASS` | `READY_FOR_REVIEW` | Chromium, Firefox and WebKit metadata are attributable and valid; the historical approval quote/manifest was not retained. |
| FR-11 | 46 / 46 | 3 | `PASS` | `READY_FOR_REVIEW` | Chromium, Firefox and WebKit metadata are attributable and valid; the historical approval quote/manifest was not retained. |
| FR-13 | 50 / 50 | 7 | `PASS_WITH_REVIEW_ITEMS` | `READY_FOR_REVIEW` | All evidence is attributable; preserved warning: Chromium metadata says `Browser: all`, while Firefox/WebKit are split into `tc`/`bva`/`api`. |

The validator never promotes a workflow to `APPROVED_TO_RUN` or `COMPLETE`: those states
require a preserved human quote and a triaged run manifest. The warning is intentionally
not suppressed or edited out of generated evidence.

## Independent forward test

A fresh reviewer applied the skill to FR-13 using only the repository artifacts. It
independently found all 50 unique cases and all seven attributable report entry points,
then correctly kept the workflow at `READY_FOR_REVIEW`. Besides the preserved Chromium
metadata warning, the reviewer found that the historical run evidence does not preserve
the exact human-approval quote, static-gate exit codes, per-run command exit codes, or
raw validator output. The skill therefore refused to relabel historical evidence as
`COMPLETE` or reconstruct facts that were never recorded.

This is the intended safety behavior: the workflow can be reused, produces a concrete
manifest, distinguishes product failures from missing process evidence, and fails
honestly when a required gate cannot be proven. Future runs must preserve those fields
at execution time; they must not be backfilled after the fact.

## Reproduction commands

Run from the HW04 root:

```powershell
& '.claude/skills/playwright-automation/scripts/validate-feature.ps1' `
  -Feature fr01 `
  -SpecPath 'automation/tests/fr01_account_registration/fr01.registration.spec.ts' `
  -DataPath 'automation/data/fr01_registration.csv' `
  -StudentId 23127184 `
  -ReportJsonPaths @(
    'reports/final/json/fr01-chromium.json',
    'reports/final/json/fr01-firefox.json',
    'reports/final/json/fr01-webkit.json'
  )
```

Use the same command contract for FR-11 and FR-13 with their explicit paths; do not let
the validator discover or guess feature-specific inputs.
