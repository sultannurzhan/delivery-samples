"""Synthetic CSV cleanup proof. Python 3.9+, standard library only.

Run: python cleanup.py
Reads input.csv beside this script. Recreates only the named outputs beside it.
This is a deliberately small demonstration, not a general-purpose import system.
"""
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
import csv
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parent
FIELDS = ["source_id", "item_code", "item_name", "color", "quantity", "checked_date"]
NORMAL_FIELDS = ["item_code", "item_name", "color", "quantity", "quantity_state", "checked_date"]
CLEAN_FIELDS = ["output_id", "source_ids"] + NORMAL_FIELDS
ERROR_FIELDS = ["source_id", "normalized_key", "reason_codes", "conflicting_fields"] + [f + "_raw" for f in FIELDS[1:]]
DISPOSITION_FIELDS = ["source_id", "disposition", "destination", "reason"]

def normalize(raw):
    """Return normalized values and errors without replacing invalid data."""
    n = {"item_code": raw["item_code"].strip().upper(),
         "item_name": " ".join(raw["item_name"].split()),
         "color": " ".join(raw["color"].split()).lower()}
    errors = []
    if not re.fullmatch(r"KIT-[0-9]{3}", n["item_code"]):
        errors.append("INVALID_ITEM_CODE")
    if not n["item_name"]:
        errors.append("MISSING_ITEM_NAME")
    if not n["color"]:
        errors.append("MISSING_COLOR")
    quantity = raw["quantity"].strip()
    if quantity == "":
        n.update(quantity="", quantity_state="missing")
    elif re.fullmatch(r"[0-9]+", quantity):
        n.update(quantity=str(int(quantity)), quantity_state="present")
    else:
        n.update(quantity="", quantity_state="invalid")
        errors.append("INVALID_QUANTITY")
    checked = raw["checked_date"].strip()
    n["checked_date"] = checked
    if not checked:
        errors.append("MISSING_DATE")
    elif re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", checked):
        try:
            date.fromisoformat(checked)
        except ValueError:
            errors.append("INVALID_DATE")
    else:
        slash = re.fullmatch(r"([0-9]{1,2})/([0-9]{1,2})/[0-9]{4}", checked)
        ambiguous = slash and 1 <= int(slash[1]) <= 12 and 1 <= int(slash[2]) <= 12 and int(slash[1]) != int(slash[2])
        errors.append("AMBIGUOUS_DATE" if ambiguous else "NON_ISO_DATE")
    return n, errors

def transform(rows):
    ids = [row["source_id"] for row in rows]
    if any(not re.fullmatch(r"R[0-9]{3}", value) for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("Source IDs must be unique and use the demo R000 format; refusing an untraceable run.")
    groups = defaultdict(list)
    for raw in rows:
        n, errors = normalize(raw)
        groups[n["item_code"]].append((raw, n, errors))
    clean, exceptions, dispositions = [], [], []
    for key in sorted(groups):
        group = sorted(groups[key], key=lambda entry: entry[0]["source_id"])
        bad_group = any(errors for _, _, errors in group)
        # With invalid values, their meaning is unknown; hold the whole key.
        conflicts = [] if bad_group else [field for field in NORMAL_FIELDS
                                         if len({n[field] for _, n, _ in group}) > 1]
        if bad_group or conflicts:
            for raw, n, own_errors in group:
                reasons = list(own_errors)
                if bad_group and len(group) > 1:
                    reasons.append("KEY_GROUP_HAS_INVALID_ROW")
                if conflicts:
                    reasons.append("CONFLICTING_KEY")
                exceptions.append({"source_id": raw["source_id"], "normalized_key": key,
                                   "reason_codes": ";".join(reasons), "conflicting_fields": ";".join(conflicts),
                                   **{f + "_raw": raw[f] for f in FIELDS[1:]}})
                dispositions.append({"source_id": raw["source_id"], "disposition": "quarantined",
                                     "destination": "exceptions.csv:" + raw["source_id"], "reason": ";".join(reasons)})
        else:
            output_id = f"CLEAN-{len(clean)+1:03d}"
            clean.append({"output_id": output_id, "source_ids": "|".join(raw["source_id"] for raw, _, _ in group), **group[0][1]})
            for index, (raw, _, _) in enumerate(group):
                dispositions.append({"source_id": raw["source_id"],
                                     "disposition": "kept" if index == 0 else "duplicate_collapsed",
                                     "destination": "cleaned.csv:" + output_id,
                                     "reason": "Normalized duplicate; all source IDs retained" if index else "Validated under the documented rules"})
    return clean, sorted(exceptions, key=lambda x: x["source_id"]), sorted(dispositions, key=lambda x: x["source_id"])

def write_csv(name, fields, rows):
    with (ROOT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

def read_csv(name, expected_fields):
    with (ROOT / name).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected_fields:
            raise ValueError(f"Unexpected columns in {name}")
        rows = list(reader)
        if any(None in row or any(value is None for value in row.values()) for row in rows):
            raise ValueError(f"Ragged CSV row in {name}")
        return rows

def verify(rows, clean, exceptions, dispositions):
    """Expected outcomes plus failure-mode tests, not implementation snapshots."""
    by_key = {row["item_code"]: row for row in clean}
    by_source = {row["source_id"]: row for row in exceptions}
    assert len(rows) == 10 and len(clean) == 4 and len(exceptions) == 5
    assert by_key["KIT-001"]["source_ids"] == "R001|R002"
    assert by_key["KIT-001"]["quantity"] == "12" and by_key["KIT-001"]["item_name"] == "Paper Kite Kit"
    assert (by_key["KIT-002"]["quantity"], by_key["KIT-002"]["quantity_state"]) == ("0", "present")
    assert (by_key["KIT-003"]["quantity"], by_key["KIT-003"]["quantity_state"]) == ("", "missing")
    assert "KIT-004" not in by_key
    assert all(by_source[s]["reason_codes"] == "CONFLICTING_KEY" for s in ("R005", "R006"))
    assert {by_source[s]["quantity_raw"] for s in ("R005", "R006")} == {"8", "10"}
    assert by_source["R007"]["reason_codes"] == "INVALID_QUANTITY" and by_source["R007"]["quantity_raw"] == "ten"
    assert by_source["R008"]["reason_codes"] == "AMBIGUOUS_DATE" and by_source["R008"]["checked_date_raw"] == "09/10/2026"
    assert by_source["R009"]["reason_codes"] == "INVALID_DATE"
    represented = [s for row in clean for s in row["source_ids"].split("|")] + [row["source_id"] for row in exceptions]
    assert Counter(represented) == Counter(row["source_id"] for row in rows)
    assert Counter(row["source_id"] for row in dispositions) == Counter(represented)
    assert Counter(row["disposition"] for row in dispositions) == {"kept": 4, "duplicate_collapsed": 1, "quarantined": 5}
    assert transform(list(reversed(rows))) == (clean, exceptions, dispositions)
    checks = ["All 10 source IDs accounted for exactly once", "Normalized duplicate collapsed with both IDs retained",
              "Missing quantity stays blank and explicit zero stays zero", "Both conflicting records quarantined with raw values",
              "Invalid quantity, ambiguous date, and impossible date flagged", "Results independent of input row order"]
    base = {"source_id": "R101", "item_code": "KIT-901", "item_name": "Test Item", "color": "blue", "quantity": "", "checked_date": "2026-09-18"}
    # Blank versus zero under the SAME key must conflict, not be deduplicated.
    c, e, _ = transform([base, {**base, "source_id": "R102", "quantity": "0"}])
    assert not c and len(e) == 2 and all(row["reason_codes"] == "CONFLICTING_KEY" for row in e)
    checks.append("Same-key missing versus zero quarantined as a conflict")
    # A valid sibling cannot hide another row's invalid numeric value.
    c, e, _ = transform([{**base, "quantity": "3"}, {**base, "source_id": "R102", "quantity": "oops"}])
    assert not c and len(e) == 2 and all("KEY_GROUP_HAS_INVALID_ROW" in row["reason_codes"] for row in e)
    checks.append("Entire key held when a sibling row is invalid")
    for value in ("-1", "1.5", "1,000", "1e3", "NaN"):
        c, e, _ = transform([{**base, "quantity": value}])
        assert not c and e[0]["reason_codes"] == "INVALID_QUANTITY"
    checks.append("Negative, decimal, grouped, scientific, and NaN quantities rejected")
    for value, expected in (("2024-02-29", []), ("2026-02-29", ["INVALID_DATE"]), ("2026-9-18", ["NON_ISO_DATE"]), ("09/9/2026", ["NON_ISO_DATE"]), ("", ["MISSING_DATE"])):
        _, errors = normalize({**base, "checked_date": value})
        assert errors == expected
    checks.append("Leap-year, strict ISO format, and missing-date boundaries checked")
    try:
        transform([base, base])
    except ValueError:
        pass
    else:
        raise AssertionError("Duplicate source IDs were accepted")
    checks.append("Duplicate source IDs rejected before output")
    return checks

def main():
    rows = read_csv("input.csv", FIELDS)
    source_hash = hashlib.sha256((ROOT / "input.csv").read_bytes()).hexdigest()
    clean, exceptions, dispositions = transform(rows)
    checks = verify(rows, clean, exceptions, dispositions)
    write_csv("cleaned.csv", CLEAN_FIELDS, clean)
    write_csv("exceptions.csv", ERROR_FIELDS, exceptions)
    write_csv("row-disposition.csv", DISPOSITION_FIELDS, dispositions)
    # Verify exported CSV round-trips, including empty quantity and raw spaces.
    assert read_csv("cleaned.csv", CLEAN_FIELDS) == clean
    assert read_csv("exceptions.csv", ERROR_FIELDS) == exceptions
    assert read_csv("row-disposition.csv", DISPOSITION_FIELDS) == dispositions
    assert hashlib.sha256((ROOT / "input.csv").read_bytes()).hexdigest() == source_hash
    checks.append("Exported CSV round-trip verified; source file unchanged")
    report = {"sample": "Original synthetic demonstration; not client work", "input_rows": len(rows),
              "cleaned_records": len(clean), "source_rows_represented_in_cleaned": 5,
              "duplicate_rows_collapsed": 1, "quarantined_rows": len(exceptions),
              "unaccounted_source_rows": 0, "checks_passed": checks, "input_sha256": source_hash}
    (ROOT / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    names = ["README.md", "input.csv", "cleaned.csv", "exceptions.csv", "row-disposition.csv", "cleanup.py", "verification.json"]
    archive_path = ROOT / "astra-csv-cleanup-proof.zip"
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in names:
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 19, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (ROOT / name).read_bytes())
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None and archive.namelist() == names
    assert archive_path.stat().st_size < 30000
    print(json.dumps({**report, "zip_bytes": archive_path.stat().st_size}, indent=2))

if __name__ == "__main__":
    main()
