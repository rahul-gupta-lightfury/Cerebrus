# CsvTools Reference for Cerebrus

Cerebrus relies on Unreal Engine's CsvTools suite to process performance CSVs. This document summarizes how each tool is expected to be used within this project.

The underlying binaries are provided by Unreal Engine and should not be modified. Cerebrus only wraps and orchestrates them.

## Common Path Layout

Example CsvTools root directory (adjust to your environment):

```text
E:/DonE/git/UE57/Engine/Binaries/DotNET/CsvTools/
  CSVCollate.exe
  CsvConvert.exe
  CSVFilter.exe
  CSVSplit.exe
  CsvToSVG.exe
  csvinfo.exe
  PerfreportTool.exe
```

Cerebrus configuration should expose a single `csvtools_root` path, from which each binary path is derived.

## CSVCollate

Purpose: collate multiple CSV files into a single aggregate CSV suitable for summary analysis.

Key arguments typically used by Cerebrus:

- `-csvs <filename or ; separated list>` or `-csvDir <path>`
- `-searchPattern <pattern>`: pattern like `*.csv` when using `-csvDir`
- `-avg`: compute per-frame averages
- `-recurse`: search subdirectories under `-csvDir`
- `-filterOutlierStat <stat>`
- `-filterOutlierThreshold <value>` (default: 1000)
- `-metadataFilter <key=value,...>`
- `-startEvent <event name>`
- `-o <output.csv>`

Cerebrus should provide a high-level API that:
- Accepts a list of CSV paths or a directory and pattern.
- Encodes outlier and metadata filters via configuration.
- Returns the path to the collated CSV.

## CsvConvert

Purpose: convert CSVs between formats (with or without metadata, or to a binary representation).

Typical arguments:

- `-in <filename>` or a direct `<filename>` argument.
- `-outFormat=<csv|bin|csvNoMetadata>`
- `-binCompress=<0|1|2>`
- `-o <output>` or `-inPlace`
- `-force`, `-verify`
- Metadata handling flags such as:
  - `-dontFixMissingID`
  - `-skipIfMetadataMissing`
  - `-setMetadata key0=value0;key1=value1;...`

Cerebrus can:
- Normalize CSVs into a standard format before further processing.
- Inject or override metadata used by PerfReportTool and other workflows.

## CSVFilter

Purpose: filter a CSV down to a subset of statistics.

Key arguments:

- `-csv <filename>`
- `-stats <stat names>` and/or `-defaults`
- `-o <output.csv>`

Cerebrus should allow profiles to define named stat sets (e.g. GPU, CPU, memory) and use CSVFilter to generate focused CSVs.

## csvinfo

Purpose: inspect CSV contents and metadata.

Useful arguments:

- `<csvfilename>` (positional)
- `-showaverages`, `-showmin`, `-showmax`, `-showTotals`
- `-showAllStats`
- `-showEvents`
- `-forceFullRead`
- `-quiet`
- `-toJson <filename>`
- `-statFilters <stat list>`

Cerebrus can use `csvinfo` to:
- Validate that CSVs are structurally sound.
- Extract metadata and summary values for display in the UI or for automated checks.

## CSVSplit

Purpose: split a CSV on a particular stat, optionally with delay or virtual event handling.

Key arguments:

- `-csv <filename>`
- `-splitStat <statname>`
- `-o <output.csv>` (optional)
- `-delay <frame count>`
- `-virtualEvents`

Cerebrus may use this to isolate warm-up vs steady-state segments or specific gameplay phases.

## CsvToSVG

Purpose: generate SVG graphs from CSVs or collated data.

High-level usage patterns:

- `-csvs <list>` or `-csv <list>` or `-csvDir <path>`
- `-o <output.svg>`
- `-stats <stat names>` or `-batchCommands <file>`
- `-mt <threads>` for parallelization
- `-updatesvg <svgFilename>` to regenerate an existing SVG

Selected optional arguments that Cerebrus may expose via configuration:

- Ranges: `-minX`, `-maxX`, `-minY`, `-maxY`
- Filtering: `-filterOutZeros`, `-ignoreStats <list>`, `-noMetadata`
- Events: `-startEvent`, `-endEvent`, `-showEvents <names>`, `-highlightEventRegions <...>`
- Rendering: `-width`, `-height`, `-smooth`, `-stacked`, `-theme <dark|light>`
- Output behavior: `-view`, `-writeErrorsToSVG`, `-nocommandlineEmbed`

Cerebrus responsibilities:

- Normalize the way stats are selected (e.g. via named chart presets).
- Manage output locations for generated SVGs per project/run.
- Expose key options in the UI while keeping advanced flags configurable via profiles.

## Error Handling and Logging

CsvTools wrappers must:

- Surface non-zero exit codes as explicit failures.
- Capture stderr and log it with enough context (tool, arguments, input files).
- Avoid leaking full paths in user-facing errors when unnecessary.

## Integration Patterns

- Prefer pure orchestration modules that:
  - Accept clean data structures from `core` (e.g. lists of runs, device metadata).
  - Call wrapped CsvTools functions.
  - Produce structured artifacts (paths, summaries) for the UI and subsequent processing.
- Keep CLI string assembly inside wrapper functions, not in callers.

This document should be kept in sync with any additional CsvTools usage introduced in the project.
