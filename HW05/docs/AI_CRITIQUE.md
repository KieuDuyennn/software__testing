# AI Critique (281 words)

Working with AI helped me build the JMeter plans faster, especially when I had
to repeat the same workflow for Load, Stress and Spike. However, I also noticed
that some of its first conclusions sounded convincing even though they were not
fully supported by the test data. For example, AI treated the single-user result
of 32.9 journeys per second as a prediction of the system's capacity. The Stress
test later reached about 52 complete journeys per second at 132 VU and still did
not show a clear breaking point. This showed me that the baseline was useful for
choosing an initial load, but not for declaring the final capacity.

AI also counted successful Transaction Controller rows as complete purchases.
When I compared the five endpoint labels, I found 18,797 successful controllers
but only 18,775 complete journeys in the Stress run. Some journeys had been cut
off when the scheduler stopped. Another issue was memory: the final value was
higher than the starting value, so it was easy to call this a memory leak.
However, memory dropped from about 170 MB to 68 MB during the Soak test, which
looked more like garbage collection. The cart not being cleared after checkout
is still a real risk, but the current run is not enough to prove a leak.

Some optimization suggestions also sounded reasonable but did not match the
actual code, such as adding a connection pool or using a normal index for
`LIKE '%keyword%'`. From this assignment, I learned that AI output should be
treated as a suggestion to verify, not as the final answer. Important claims
must be checked against raw logs, test phases and the source code.
