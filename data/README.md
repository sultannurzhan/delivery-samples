# CSV cleanup demonstration

This is an original synthetic ability sample, created with AI assistance. The ten craft-supply rows are fictional. No customer, personal, financial, or health data is included. It is not prior client work.

**Result:** 10 input rows become 4 cleaned records representing 5 source rows, plus 5 quarantined rows. One duplicate row is collapsed. Every source ID remains traceable. No source row is silently discarded.

## Rules used

- This single inventory snapshot treats `item_code` as the record key. It must match `KIT-000` after trimming surrounding spaces and uppercasing. Leading zeros in item codes are preserved. Source IDs stay unchanged and must be unique.
- Item names have surrounding and repeated whitespace removed. Their case is preserved. Colors have whitespace normalized and are lowercased. There is no fuzzy matching, synonym guessing, or title-casing.
- Quantity is an optional nonnegative whole count. Accept only ASCII digits after trimming. Leading zeros are removed from counts only. Blank means unknown: output quantity stays blank with `quantity_state=missing`. An explicit `0` has `quantity_state=present`. Neither is substituted for the other.
- Dates must be real calendar dates in `YYYY-MM-DD` form after trimming. An ambiguous slash date is quarantined; no locale is assumed. Impossible dates, missing dates, and other date formats are also held for review.
- Same-key records collapse only if all normalized business fields match, including missing/present state. All original IDs appear in `source_ids`, separated by `|`. The lowest source ID is the retained representative for the disposition report.
- Any different normalized value under the same key quarantines **every** row in that group. No latest/first value wins and quantities are never added. If any group member is invalid, the whole key is held. Exceptions preserve all raw business-field values, including their original whitespace.

## Where every row went

| Source ID | Disposition | Destination or reason |
| --- | --- | --- |
| R001 | Kept | CLEAN-001; whitespace, case, and `012` normalized |
| R002 | Duplicate collapsed | CLEAN-001; source IDs `R001|R002` retained |
| R003 | Kept | CLEAN-002; quantity remains explicit zero |
| R004 | Kept | CLEAN-003; quantity remains missing |
| R005 | Quarantined | KIT-004 conflicts with R006: quantity 8 versus 10 |
| R006 | Quarantined | KIT-004 conflicts with R005: quantity 10 versus 8 |
| R007 | Quarantined | `ten` is not a permitted whole-number quantity |
| R008 | Quarantined | `09/10/2026` has an ambiguous day/month order |
| R009 | Quarantined | `2026-02-30` is not a calendar date |
| R010 | Kept | CLEAN-004; surrounding spaces removed |

Reconciliation: **4 retained source rows + 1 collapsed duplicate + 5 quarantined rows = 10 input rows**. The 4 cleaned records reference 5 distinct source IDs. Those 5 IDs and the 5 exception IDs form a disjoint, complete set of the original IDs.

## Files and reproduction

`input.csv` is the unchanged source. `cleaned.csv` contains accepted normalized records. `exceptions.csv` contains raw values and reason codes for manual resolution. `row-disposition.csv` records each source row's destination. `verification.json` records executed checks.

Run `python cleanup.py` with Python 3.9 or later, without optimization flags. Only the Python standard library is required. The script uses files beside itself and recreates the three output CSVs, verification report, and compact shareable ZIP. It does not change `input.csv`.

Assertions cover source-row reconciliation, duplicate lineage, both conflict records, blank versus zero, invalid numerics, ambiguous/impossible dates, leap-year boundaries, invalid siblings under the same key, duplicate source IDs, input-order independence, and saved CSV round-trips. The ZIP contains only this note, the four CSVs, the script, and verification evidence.

These are explicit demo rules. A real assignment would first confirm the customer's record key, permitted formats, and missing-data policy. Quarantined rows require a source correction or a confirmed rule before they can enter the cleaned output. This sample does not measure performance on large files.
