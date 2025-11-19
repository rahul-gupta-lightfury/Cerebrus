# PerfReportTool Reference for Cerebrus

PerfReportTool is used to generate HTML and CSV-based performance reports from profiling CSV or PRC data. Cerebrus orchestrates PerfReportTool but does not modify it.

## Typical Invocation

Base pattern:

```text
PerfreportTool.exe -csv <file> -reportType <type> -o <output_dir> [options...]
```

or, for bulk processing:

```text
PerfreportTool.exe -csvdir <directory> -recurse -o <output_dir> [options...]
```

Examples of inputs:

- Single CSV:
  - `-csv <filename>`
- Directory of CSVs:
  - `-csvdir <directory path>`
- Summary table cache:
  - `-summaryTableCacheIn <directory path>`
- Explicit CSV or PRC lists:
  - `-csvList <comma separated>`
  - `-prcList <comma separated>`

`-o <dir name>` specifies the output directory and will be created if necessary.

## Report Types and Profiles

PerfReportTool supports different `-reportType` values, such as:

- `flythrough`
- `playthrough`
- `playthroughmemory`
- `default` / engine-specific profiles (e.g. `Default60fps`)

Cerebrus should map its own profiling profiles to these report types, so the UI can present friendly names while the tool receives the correct argument.

Optional supporting arguments include:

- `-reportTypeCompatCheck` to validate compatibility when specifying a report type.
- `-graphXML <xmlfilename>`
- `-reportXML <xmlfilename>`
- `-reportxmlbasedir <folder>`

## Output and Summary Tables

Useful options for generating structured outputs:

- `-writeSummaryCsv` to generate a CSV with summary information (non-bulk mode).
- `-summaryTableXML <XML filename>`
- `-summaryTable <name>` and `-condensedSummaryTable <name>`
- `-summaryTableFilename <name>`
- `-csvTable` to output the summary table in CSV format.
- `-emailTable` to generate condensed, email-friendly tables.

JSON serialization:

- `-summaryTableToJson <path>`
- `-summaryTableToJsonSeparateFiles`
- `-summaryTableToJsonFastMode`
- `-summaryTableToJsonWriteAllElementData`
- `-summaryTableToJsonMetadataOnly`
- `-summaryTableToJsonFileStream`
- `-summaryTableToJsonNoIndent`
- `-jsonToPrcs <json filename>`

Cerebrus should provide configuration for:

- Whether to write HTML, CSV, JSON, or combinations.
- Where to place report directories per project and per run.

## Bulk Mode and Caching

For batch processing:

- Use bulk args with `-csvdir`, `-summaryTableCacheIn`, `-csvList`, or `-prcList`.
- Common options:
  - `-recurse`
  - `-searchpattern <pattern>` (e.g. `csvprofile*`)
  - `-customTable <fields>`
  - `-customTableSort <fields>`
  - `-noDetailedReports`
  - `-noReports`
  - `-collateTable` / `-collateTableOnly`
  - `-reverseTable`, `-scrollableTable`, `-colorizeTable <off|budget|auto>`

Summary table cache and performance options:

- `-summaryTableCache <dir>` to cache summary table data.
- `-summaryTableCacheInvalidate`, `-summaryTableCacheReadOnly`, `-summaryTableCachePurgeInvalid`
- `-precacheCount <n>`, `-precacheThreads <n>`
- `-noCsvCacheFiles` to disable `.csv.cache` usage.

Cerebrus should manage cache directories per project and offer a way to purge or rebuild caches from the UI.

## Data Filtering

To truncate or filter the source data:

- `-minx <frameNumber>`
- `-maxx <frameNumber>`
- `-beginEvent <event>`
- `-endEvent <event>`
- `-noStripEvents`

Metadata and file selection:

- `-metadataFilter <query or key=value,...>`
- `-listFiles` to only list files that pass the metadata query.
- `-requireMetadata`
- `-minFrameCount <n>`
- `-maxFileAgeDays <n>`

These options are good candidates for higher-level presets controlled by profiling profiles.

## Diff and Regression Analysis

PerfReportTool supports diff and regression-focused behaviors:

- Diff rows:
  - `-addDiffRows`
  - `-sortColumnsByDiff`
  - `-columnDiffDisplayThreshold <value>`
  - `-diffRowsAlternating 0|1`
  - `-showOnlyDiffRows`
- Regression filtering:
  - `-onlyShowRegressedColumns`
  - `-regressionJoinRowsByName <statName>`
  - `-regressionStdDevThreshold <n>`
  - `-regressionOutlierStdDevThreshold <n>`

Cerebrus may expose “comparison runs” in the UI that leverage these options to show regressions between builds or device profiles.

## Performance and Parallelism

Performance-related arguments:

- `-perfLog` for performance logging.
- `-graphThreads <n>`
- `-csvToSvgSequential`
- `-useEmbeddedGraphUrl`
- `-embeddedGraphUrlRoot <url>`

Cerebrus should allow configuration of sensible defaults (e.g. number of graph threads) based on machine capabilities.

## Error Handling and Diagnostics

PerfReportTool wrappers must:

- Log the full command line (or a sanitized version) when failures occur.
- Capture exit codes and stderr output.
- Provide user-facing error messages that:
  - Indicate which input files failed.
  - Suggest likely causes (missing metadata, incompatible report type, corrupt CSVs).
  - Offer actionable next steps (e.g. rerun with a different profile or regenerate CSVs).

## Integration Guidelines

- Treat PerfReportTool as an external, versioned dependency.
- When Unreal Engine is upgraded:
  - Validate that existing profiles and report types still behave correctly.
  - Update this document if arguments or behaviors change.
- Avoid relying on undocumented behavior; prefer explicit, documented arguments.

This document should be kept in sync with any new PerfReportTool-based workflows implemented in Cerebrus.
