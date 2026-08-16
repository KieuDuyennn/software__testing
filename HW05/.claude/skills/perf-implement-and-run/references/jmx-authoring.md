# Authoring JMeter .jmx by hand or by generator

JMeter's file format is XStream-serialised Java objects. It loads happily with
values that mean something other than what they look like, so the failure mode is
usually a plan that runs and reports nonsense rather than one that refuses to
start. These are the traps worth knowing, each of which has cost a real debugging
session.

## Contents

- [File-level traps](#file-level-traps)
- [Thread groups](#thread-groups)
- [HTTP samplers](#http-samplers)
- [Extractors and correlation](#extractors-and-correlation)
- [Assertions](#assertions)
- [CSV data sets](#csv-data-sets)
- [Listeners](#listeners)
- [Reading the .jtl afterwards](#reading-the-jtl-afterwards)

## File-level traps

**A byte-order mark stops the parser.** JMeter fails with
`com.thoughtworks.xstream.io.StreamException` and no useful detail. Windows
PowerShell 5.1 writes a BOM with `Out-File -Encoding utf8`, so generated plans
need `[System.IO.File]::WriteAllText` with `UTF8Encoding($false)`.

**`--` cannot appear inside an XML comment.** The parser reports
`in comment after two dashes (--) next character must be > not \n`, pointing at
the position where the comment *opened*, not where the offending dashes are.

**A template must not document its own placeholders literally.** If the header
comment of a template lists `{{THREAD_GROUPS}}`, the generator substitutes there
too, injecting a thread group into a comment and breaking the file. Name
placeholders without their delimiters in documentation.

**Reading with the wrong encoding corrupts non-ASCII silently.** PowerShell 5.1's
`Get-Content` defaults to the ANSI codepage; an em dash becomes `â€"` and stays
that way in every generated file.

## Thread groups

Duration is controlled by the scheduler, not by a loop count:

```xml
<elementProp name="ThreadGroup.main_controller" elementType="LoopController" ...>
  <boolProp name="LoopController.continue_forever">false</boolProp>
  <intProp name="LoopController.loops">-1</intProp>
</elementProp>
<stringProp name="ThreadGroup.num_threads">50</stringProp>
<stringProp name="ThreadGroup.ramp_time">100</stringProp>
<boolProp name="ThreadGroup.scheduler">true</boolProp>
<stringProp name="ThreadGroup.duration">600</stringProp>
<stringProp name="ThreadGroup.delay">0</stringProp>
```

`loops = -1` with `continue_forever = false` means "iterate until the scheduler
stops you". A fixed loop count makes run length depend on how fast the system
responds, which is precisely the variable under test — a degraded system would
run *longer*, confusing every time-based comparison.

`ThreadGroup.delay` is what builds a spike: a second thread group with a delay
starts its burst partway through the run of the first.

**Sharing a workflow between thread groups.** A Module Controller resolves its
target by node path at load time and breaks quietly when the plan is
restructured. In a generated file, duplicating the workflow into each thread
group is free and cannot break.

## HTTP samplers

For a JSON body, raw post-body mode is required — otherwise the body is sent as
form parameters and the server sees an empty object:

```xml
<boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
<elementProp name="HTTPsampler.Arguments" elementType="Arguments">
  <collectionProp name="Arguments.arguments">
    <elementProp name="" elementType="HTTPArgument">
      <boolProp name="HTTPArgument.always_encode">false</boolProp>
      <stringProp name="Argument.value">{"email":"${email}"}</stringProp>
      <stringProp name="Argument.metadata">=</stringProp>
    </elementProp>
  </collectionProp>
</elementProp>
```

The argument's `name` must be empty in raw mode. A named argument in raw mode
produces a body of `name=value`.

For query parameters, use named arguments with `always_encode` true rather than
appending to the path — a keyword containing a space or an ampersand otherwise
builds a malformed URL, and the resulting error looks like a server fault.

## Extractors and correlation

```xml
<JSONPostProcessor ...>
  <stringProp name="JSONPostProcessor.referenceNames">authToken</stringProp>
  <stringProp name="JSONPostProcessor.jsonPathExprs">$.token</stringProp>
  <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
  <stringProp name="JSONPostProcessor.defaultValues">TOKEN_NOT_FOUND</stringProp>
</JSONPostProcessor>
```

Always set a default value. Without one, a failed extraction leaves the variable
*unset*, so `${authToken}` is sent literally as the string `${authToken}` and the
failure surfaces far from its cause. A marker like `TOKEN_NOT_FOUND` in the
request headers of a failed sample names the problem immediately.

Extractors are children of the sampler they read, so they must sit inside that
sampler's own `hashTree`.

## Assertions

`Assertion.test_type` is a bit field, and the numbers are not self-explanatory:

| Value | Meaning |
|---|---|
| 1 | Matches (regex, whole field) |
| 2 | Contains (substring or regex) |
| 8 | Equals (exact) |
| 16 | Substring (literal, no regex) |

Combine with the field under test:

```xml
<stringProp name="Assertion.test_field">Assertion.response_code</stringProp>  <!-- status -->
<stringProp name="Assertion.test_field">Assertion.response_data</stringProp>  <!-- body -->
```

Assert on the body wherever a `200` is not proof of success. An endpoint that
answers `200 {}` for a missing record will otherwise be recorded as a success and
the error rate will flatter the system.

Note the misspelling in JMeter's own schema: the collection is
`Asserion.test_strings`, with one `t`. Spelling it correctly produces an
assertion that checks nothing and always passes.

## CSV data sets

```xml
<stringProp name="variableNames"></stringProp>
<boolProp name="quotedData">true</boolProp>
<boolProp name="recycle">true</boolProp>
<stringProp name="shareMode">shareMode.all</stringProp>
```

Leaving `variableNames` empty makes JMeter read column names from the header row,
so the file stays self-describing and a reordered column does not silently shift
every value.

`quotedData` is required whenever a field can contain the delimiter — an address
like `"1 Le Loi, Q1, TP.HCM"` shifts every later column without it.

`shareMode.all` means one shared cursor across threads, so N threads read N
different rows. Per-thread mode gives every thread its own copy starting at row
one, which is almost never what a load test wants.

`recycle = true` wraps around at end of file; `stopThread = true` instead ends
threads when data runs out, which is the right choice when each row must be used
exactly once.

## Listeners

```xml
<ResultCollector guiclass="SummaryReport" testclass="ResultCollector" testname="Summary Report">
  <boolProp name="ResultCollector.error_logging">false</boolProp>
  <stringProp name="filename"></stringProp>
</ResultCollector>
```

`guiclass` selects the view: `SummaryReport`, `StatVisualizer` (Aggregate
Report), `ViewResultsFullVisualizer` (View Results Tree), `GraphVisualizer`.

`error_logging = true` means *errors only*, not "log errors as well". For a
results tree during a high-thread burst this is the difference between a usable
file and one larger than the run itself.

Leave `filename` empty in the plan and pass `-l` on the command line, so the
output path belongs to the run rather than to the plan.

## Reading the .jtl afterwards

The `.jtl` is CSV with a header row, and **fields can contain commas inside
quotes**. Transaction controller rows carry a message like
`"Number of samples in transaction : 5, number of failing samples : 0"`, so
splitting on commas shifts every later column and reports transactions as
failures when they succeeded.

Use a real CSV parser. This is not a hypothetical: it is the single most common
way an analysis of a healthy run concludes that everything failed.
