# Reset before Soak

| Field | Value |
|---|---|
| Timestamp | 2026-08-17 22:54:04 +07:00 |
| Previous Spike backend PID | 6760 |
| New Soak backend PID | 20612 |
| LOADTEST | 1 |
| Products | 5 |
| Generated users | 240 (+ 2 seeded) |
| CSV validation | PASS, 240 rows each |
| API products | HTTP 200 |
| Free RAM before run | 1.97 GB |
| Database/cart state | Fresh process; startup reseeded DB and cleared in-memory carts |

## Final execution gate

- Rechecked after background cleanup at 2026-08-17 22:54:32 +07:00.
- Free RAM: **2.03 GB** — PASS.
- Backend PID/API/data unchanged after the recheck.
