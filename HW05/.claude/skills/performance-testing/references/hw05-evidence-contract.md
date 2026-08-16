# HW05 evidence contract

Use this checklist only for HW05-style coursework. It extends the reusable
performance workflow with attribution and submission gates; it does not replace
the official brief.

## Before execution

- Confirm the student ID and the non-duplicated end-to-end workflow.
- Preserve step-by-step AI prompts and outputs with tool name and timestamp.
- Record hostname, hardware screenshot, tool versions, seeded volume,
  rate-limiter setting, backend PID and reset procedure.
- Measure the single-user baseline before choosing thread counts.
- Validate every CSV against the live target; do not invent credentials or IDs.
- Name plans `{StudentID}_{ScenarioType}_{YYYYMMDD}.jmx`.

## Per scenario

For Load, Stress and Spike, retain together:

- the final `.jmx` and human-review notes showing what AI got wrong;
- the complete unedited `.jtl`, HTML report, `jmeter.log` and `run.md`;
- `resources.csv` for the explicitly selected backend PID;
- a screenshot with JMeter and backend resources in the same frame;
- the assigned distinct listener: Summary, Aggregate or Results Tree;
- the reset record before the next run.

Run Soak for 10–15 minutes and report maximum sustained RPS, p95/error-rate
verdict, memory start/peak/end and the co-located setup's limitations.

## AI analysis and human review

Keep the AI analysis unchanged as an attributed artifact. Review it separately:

1. List each claim being checked.
2. Cite the recomputed value from the raw `.jtl` and name the method.
3. Explain the misinterpretation instead of silently replacing the value.
4. Classify each optimisation as supported, plausible but unverified, or
   unfounded after inspecting the relevant code path.
5. Write the required 200–300 word critique in the student's reviewed voice.

## Final submission gate

- Main report in Markdown and PDF.
- Three plans, raw logs, HTML reports, data files and execution evidence.
- Soak/endurance result with concrete threshold numbers.
- Public repository and genuine GitHub Issues when findings exist.
- Unlisted video of at least six minutes with the student's Vietnamese narration.
- Skill demo showing one complete endpoint workflow end to end.
- AI Audit Report in Markdown and PDF.
- Continuous-performance proposal with commit trigger, p95 regression decision,
  flow chart, cost and false-alarm trade-offs.
- Commit per meaningful step and exported text commit log.
- README with self-assessment and test summary.
- Final ZIP name and contents checked against the official brief.

Never fabricate screenshots, video, logs, issue reports, timestamps, hostnames,
commit history or measured values. Missing evidence is a task to perform, not a
blank for an AI to fill.
