# Screenshot evidence manifest

## Primary evidence

| Scope | File | What is visible |
|---|---|---|
| Hardware | `23127184_hardware_dxdiag_20260817.png` | Hostname `KIEUDUYEN`, Windows, Intel i7-10510U and 8192 MB RAM |
| Load | `23127184_Load_stable_20260817-222900.png` | JMeter non-GUI summary at 34 VU and Task Manager CPU/memory in the same frame |
| Stress | `23127184_Stress_peak132_20260817-224530.png` | 132 active VU, about 259-261 req/s, 0 errors and Task Manager in the same frame |
| Spike burst | `23127184_Spike_burst185_20260817-225015.png` | 185 active VU, burst throughput and Task Manager in the same frame |
| Spike recovery | `23127184_Spike_recovery_performance_20260817-225145.png` | Burst threads finished and throughput returned to baseline with Task Manager visible |
| Soak start | `23127184_Soak_stable_start_20260817-225615.png` | Early 27-VU stable window and Task Manager |
| Soak late | `23127184_Soak_late_stable_20260817-230830.png` | Late 27-VU stable window, 0 errors and Task Manager |

## Supporting captures

The remaining Load/Stress/Spike images are genuine captures retained for audit.
Some early Stress captures show the JMeter console clearly but Task Manager was
behind another window; they are not used as the primary same-frame proof.

Screenshots supplement, but do not replace, each run's raw JTL, HTML report,
resource CSV, JMeter log and run record.
