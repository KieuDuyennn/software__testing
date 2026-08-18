# HW05 submission status

Checked on 2026-08-18 against `refs/requirements/ver2.md` and the repository's
HW05 evidence contract.

## Complete

- Student ID, unique workflow and endpoint-group mapping.
- Four named JMeter plans: Load, Stress, Spike and supporting Soak.
- Three 240-row data-driven CSV pools.
- Distinct required listener views across Load, Stress and Spike.
- Four official raw JTL, HTML dashboard, JMeter log, resource log and run record
  sets.
- Genuine hardware and same-frame JMeter/Task Manager screenshots.
- Load, Stress, Spike and 15-minute Soak analyses with raw-value corrections.
- Concrete endurance threshold: at least 54.5 request/s at 27 VU, request p95
  no higher than 12 ms in full stable buckets, 0% errors and 172.0 MB backend
  working-set ceiling.
- Human-review notes, AI misinterpretation hunt, optimisation classification,
  continuous-performance proposal and flow chart.
- Reusable Agent Skills.
- Main Markdown report, 272-word AI Critique and AI Audit Markdown.
- Rendered and visually checked main-report and AI-Audit PDFs.
- Public GitHub repository verified; branch `hw5` pushed and the raw HW05 README was readable without authentication.

## Must be done by the student

- Record/upload an unlisted YouTube video of at least six minutes with the
  student's own Vietnamese narration. Use `docs/VIDEO_DEMO_GUIDE_VI.md`.
- Ensure the video shows JMeter and backend resource monitoring in the same
  frame during genuine execution. If no recording from the official runs was
  retained, rerun the scenarios while recording; do not animate screenshots.
- Read and approve/revise `docs/AI_CRITIQUE.md` in the student's own voice.
- Replace `VIDEO_URL_PENDING` by running the packaging command below.

```powershell
powershell -File scripts/package-submission.ps1 -VideoUrl "https://youtu.be/..."
```

The script refuses to make a final ZIP when the video URL is absent, rebuilds
the PDFs after inserting the URL, exports the commit log, packages the required
artifacts and reopens the ZIP to verify its entries.

## Optional, not a submission blocker

- The prepared 198-VU Stress retest can narrow the capacity lower bound on a
  clean host with at least 2 GB free RAM. The completed official Stress run is
  already valid and shows that the knee lies above 132 VU.