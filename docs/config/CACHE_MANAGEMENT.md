# Cache Management

Cerebrus caches intermediate data to speed up report generation.

## Cache Types

- **Summary tables** produced by PerfReportTool.
- **Collated CSVs** produced by CSVCollate.
- **SVG graphs** that can be regenerated or reused.

## Layout

Typical layout:

```text
<ProjectRoot>/
  cache/
    perfreport/
    csv_collate/
    svg/
```

Or under a shared cache root defined in configuration.

## Purging Cache

- Cerebrus should provide:
  - UI option to clear cache per project.
  - CLI or script option for bulk clean-up.
- Cache purges should:
  - Remove intermediate files.
  - Preserve raw captures and final reports.

## When to Rebuild

- After upgrading Unreal Engine or CsvTools/PerfReportTool.
- After changing profiles or metadata filters.
- When encountering inconsistent or stale data.

Proper cache management helps keep report generation fast while avoiding inconsistent results.
