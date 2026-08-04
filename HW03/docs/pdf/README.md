# docs/pdf — generated PDF deliverables

§15 of the assignment requires the reports in **both Markdown and PDF**. This folder holds the
PDF half. **The Markdown files are the source of truth; every `.pdf` here is a generated
artefact.** Never edit a PDF directly — edit the Markdown and rebuild.

## Rebuild

```
python docs/pdf/build_pdf.py
```

Run it from the HW03 repository root, after any edit to a source `.md`. Requires Python 3.8+,
`markdown` (`pip install --user markdown`) and Google Chrome (auto-detected). Chrome is driven
headless with `--print-to-pdf`; no pandoc, LaTeX or admin rights involved.

## Contents

| PDF | Built from |
| --- | --- |
| `00_Main_Report.pdf` | `README.md` |
| `01_Task1A_Shared_GUI_Checklist.pdf` | `docs/01_Task1A_Shared_GUI_Checklist.md` |
| `02_Task1B_Execution_Report_ScenarioD.pdf` | `docs/02_Task1B_Execution_Report_ScenarioD.md` |
| `05_Bug_Usability_Findings_Log.pdf` | `docs/05_Bug_Usability_Findings_Log.md` |
| `06_AI_Audit_Report.pdf` | `docs/06_AI_Audit_Report.md` |
| `07_AI_Critique.pdf` | `docs/07_AI_Critique.md` |

Output is A4 with 2 cm margins; evidence screenshots are embedded in the PDF, and tables of nine
or more columns are placed on landscape pages so no column is cut off.
