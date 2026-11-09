# Official execution checklist — 23127184

## Scope locked

- Workflow: Login → Search product → Product detail → Add to cart → Checkout.
- The student confirmed on 2026-08-17 that this workflow is not duplicated by
  another student/group member.
- Execute in this order: Load → reset → Stress → reset → Spike → reset → Soak.
- The existing pilot is diagnostic evidence only; never present it as an
  official scenario result.

## One-time evidence before the first run

- Capture a visible `dxdiag`/System Information screenshot showing hostname
  `KIEUDUYEN`, CPU and RAM.
- Close browsers, IDE instances, sync tools, launchers and other unnecessary
  applications. Keep at least **2 GB free physical RAM** before every run.
- Use Vietnamese narration and show Student ID `23127184`, the selected workflow,
  tool versions and the four planned profiles.

## Gate before every scenario

Do not start unless every item below is true:

1. The preceding backend is stopped and a fresh backend is started with
   `LOADTEST=1`; record its new PID.
2. `scripts/prepare-performance-data.js` has recreated and verified all three
   240-row CSV files against the fresh SUT.
3. The CSV validator passes and `GET /api/products` returns HTTP 200.
4. Free physical RAM is at least 2 GB and Task Manager shows no unrelated heavy
   CPU/disk activity.
5. Screen recording is active. The same frame visibly contains the JMeter run
   console and Task Manager CPU/memory information.
6. The plan filename, scenario profile and backend PID are spoken or shown.

Run from the HW05 root, replacing `<backend-pid>` with the freshly verified PID:

```powershell
powershell -File .claude/skills/perf-implement-and-run/scripts/run-scenario.ps1 `
  -Plan test-plans/23127184_Load_20260817.jmx `
  -DataDir data -TargetProcessId <backend-pid>
```

For later scenarios, replace `Load` with `Stress`, `Spike` or `Soak`. Never reuse
a backend/database state between scenarios.

## Evidence to capture during and after each run

- Keep the recording continuous through ramp, stable/peak period and completion.
- Capture at least one legible same-frame screenshot while meaningful load is
  active; for Stress/Spike, also capture the highest stage/burst and recovery.
- Preserve the complete timestamped result directory containing:
  `result.jtl`, `report/`, `resources.csv`, `jmeter.log` and `run.md`.
- Record any warning, error, aborted run or unexpected machine activity. Keep
  invalid/failed runs separate; do not overwrite or silently delete them.
- Verify JMeter exit code, JTL existence, non-empty resource samples and HTML
  dashboard generation before resetting the SUT.

Suggested screenshot names:

```text
evidence/screenshots/23127184_<Scenario>_active_<timestamp>.png
evidence/screenshots/23127184_<Scenario>_peak_<timestamp>.png
evidence/screenshots/23127184_<Scenario>_recovery_<timestamp>.png
```

## Stop and invalidate the run when

- free RAM falls below a safe level before launch;
- the monitored PID is not the backend started for this scenario;
- the API/data preflight fails;
- screen recording or same-frame resource evidence is missing;
- unrelated heavy activity starts and materially contaminates the host;
- the JMeter log shows a plan/data/tool failure rather than SUT behaviour.

An invalid run is retained as diagnostic evidence, then repeated from a clean
reset. It is not used for the official verdict.

## Analysis and retest gate

After all valid runs, compute every claim from the raw JTL with all five journey
labels. Report per-scenario SLO verdicts, the Stress knee, Spike recovery,
Soak memory trend, limitations and one controlled retest. Compare transaction
controller rows with endpoint-complete journey counts so scheduler-tail partial
iterations are not counted as passed purchases.

## Submission gate

- Four official JMX plans and four valid result directories are present.
- Screenshots and the unlisted video are genuine, readable and attributable.
- Phase documents, AI audit, source/config/data, analysis and retest evidence are
  included under the exact naming/ZIP rules in the official brief.
- Open the final ZIP once and verify its contents before submission.
