# Human review of the AI-assisted test design

## Reviewed proposal

The original generated defaults were Load 50 VU, Stress 200 VU, Spike 200 VU
and Soak 40 VU. They were inherited from a different machine and an assumed
38 iterations/s baseline. The generator correctly warned that those values were
not measurements of this target.

## Corrections

| AI-generated issue | Human-reviewed correction | Why the AI missed it |
|---|---|---|
| Load default 50 VU was not traceable to this laptop | Use 34 VU from `13.16 × 2.5304` | Default profile was frozen from another baseline |
| Stress default was initially described as a linear ramp | Use four accumulating +33 VU stages | A linear ramp cannot attribute the first failed threshold to a stable stage |
| Spike default 200 VU was a round number | Use 168 burst VU plus 16 baseline VU | Required conversion from measured workflow capacity and think time |
| Soak default 40 VU exceeded the chosen moderate level | Use 27 VU at 32.5% estimated capacity | The default represented another hardware/data set |
| A 600-second Load duration was treated as a 600-second hold | Use 668 seconds total: 68 ramp + 600 stable | Standard Thread Group duration includes ramp time |
| CSV paths could become machine-specific | Keep `${__P(data.dir,data)}` and override at runtime | A generated plan can run locally while silently losing portability |
| Process selection could choose the wrong Node process | Require explicit backend PID | Process name alone cannot distinguish backend from frontend tooling |
| Status-only success could accept empty product bodies | Assert token, product `id` and checkout `orderId` | HTTP 200 is not sufficient for functional success |

## Remaining human responsibility

The calculations make the plan defensible, not automatically correct. The real
capacity is the measured Stress knee. The student must review GUI screenshots,
raw JTL rows, resource trends, reset evidence and narration, and must not change
criteria after seeing an inconvenient failure.

