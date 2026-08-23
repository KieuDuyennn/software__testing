# HW06 - Authentic Evidence Capture Checklist

This file contains the remaining actions that must be performed by student
23127184. Do not replace them with generated screenshots or invented URLs.

## 1. Postman Console - mandatory anti-cheat evidence

1. Open Postman Desktop and import the four files in `collections/` plus
   `config/eshop-local.postman_environment.json`.
2. Select the local environment and start the SUT with `npm run sut:start`.
3. Open **View -> Show Postman Console**.
4. Run one request from any collection.
5. Capture one screenshot containing all of:
   - `[HW06] X-Student-Id=23127184`
   - request method and `http://localhost:3000/...` URL
   - Postman UI/Console chrome showing this is a real Postman run.
6. Save as `evidence/screenshots/postman-console-x-student-id.png`.

## 2. Postman cloud features

Create workspace `HW06 - API Testing - 23127184`, import the collections and
environments, then capture:

| Evidence | Filename |
|---|---|
| Workspace with imported collections | `evidence/postman-cloud/workspace.png` |
| Collection Runner summary | `evidence/postman-cloud/runner.png` |
| Completed Monitor run | `evidence/postman-cloud/monitor.png` |
| Mock Server response | `evidence/postman-cloud/mock-server.png` |

For the mock comparison, use product 2: the contract/mock should return numeric
`price`, while the real SUT returns a string (BUG-04).

## 3. GitHub Issues

Issue URLs are now recorded in `docs/bugs/BUG_REPORT.md`, including newly filed
issues #66-#70. Open each issue and attach a screenshot that shows the relevant
Newman failure from the HTML report or Postman response. Do not use one generic
image for unrelated bugs.

Minimum new screenshot set:

| Issue | Failure to show | Suggested filename |
|---|---|---|
| #66 | plaintext password assertion | `bug-02-plaintext-password.png` |
| #67 | confirmPassword accepted | `bug-10-confirm-password.png` |
| #68 | text/plain returns HTTP 500 | `bug-11-http-500.png` |
| #69 | HTML stack trace / `<pre>` | `bug-12-stack-trace.png` |
| #70 | unauthenticated product mutation returns 200 | `bug-13-product-auth.png` |

## 4. GitHub Actions - one green and one red

1. Push the final green-gate commit and run `.github/workflows/hw06-api-tests.yml`.
2. Record commit SHA and Actions URL in `docs/cicd/CI_CD_REPORT.md`; capture the
   green `regression-gate` job and its 0-failure Newman summary.
3. In a new commit, add genuine failing case `A1-DP-071` to
   `config/ci-suite.json -> gate_cases -> API1_FR01_Register`, refresh its gate
   collection, and push.
4. Capture the red job naming `A1-DP-071` and HTTP 500.
5. Revert only that demonstration gate addition in a third commit.

## 5. Self-drawn generator diagram

Draw this yourself in draw.io, Excalidraw, PowerPoint, Figma, or on paper. Use
the exact stage names in `docs/design/GENERATOR_DESIGN.md` and
`generator_pseudocode.py`:

`Inputs -> Parse Contract -> Domain Partitions -> State Transitions -> Security
Model -> Schema Validation -> Static Validator -> Human Review -> Postman +
Excel`

Add a feedback arrow from rejected/INCOMPLETE cases to the stage that produced
them. Label arrows with `EndpointModel`, `CaseDraft[]`, `ReviewQueue`, and
`ApprovedCases`. Put `23127184` on the diagram. Export both editable source and
PNG to `docs/design/diagram/`.

## 6. Narrated demo video

Record one end-to-end API generation flow. Show the spec input, the four
coverage stages, human review labels, generated collection, Newman execution,
and the `X-Student-Id` console line. Narrate in Vietnamese with your own voice.
Upload unlisted and replace the video placeholders in `README.md` and the main
report.

## 7. Final identity fields

- Add the dated group uniqueness confirmation.
- Fill the self-assessed scores only after all evidence above exists.
- Replace `<SelfAssessedGrade>` in the ZIP filename with a three-digit score.
