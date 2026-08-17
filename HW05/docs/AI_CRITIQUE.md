# AI Critique (student review draft)

The AI was useful for generating a repeatable JMeter workflow, but several of
its early conclusions were too confident. First, it treated the single-user
baseline capacity of 32.9 journeys per second as if it predicted multi-user
capacity. The Stress run later reached about 52 complete journeys per second at
132 VU without a knee, showing that the baseline value was only a sizing
heuristic. Second, the initial analyzer trusted successful Transaction
Controller rows. Manual comparison of the five endpoint-label counts showed
that scheduler shutdown produced partial journeys: for example, Stress had
18,797 successful controller rows but only 18,775 endpoint-complete journeys.
The analyzer was corrected to report the conservative lower bound. Third, an
automatic warning described end memory above start as a possible accumulation
signal. That warning was reasonable, but calling it a leak would have been
wrong: the Soak trace fell from about 170 MB to 68 MB during garbage collection
and ended at 89.6 MB. Source inspection instead found a specific risk: checkout
does not clear the in-memory cart. Finally, generic recommendations such as a
connection pool or a B-tree index for `LIKE '%keyword%'` sounded plausible but
did not match this implementation. It uses one shared SQLite handle, and a
leading wildcard prevents a normal prefix index from serving the query. These
misses occurred because the model initially reasoned from common performance
patterns before it had raw label counts, phase-specific timelines, and source
code. I learned to treat AI output as a testable hypothesis: pre-register
criteria, preserve raw evidence, recompute every important number, inspect the
actual code path, and make capacity or leak claims only within the measured
scope.

> Student action before submission: read this draft, revise it into your own
> reviewed voice if needed, and record that approval in the AI Audit Report.
