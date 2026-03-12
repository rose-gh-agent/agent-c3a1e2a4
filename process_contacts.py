#!/usr/bin/env python3
"""
Extract rows 301-400 (1-indexed data rows, excluding header) from vcs-and-angels.csv.
Validate emails, split valid-email contacts into 5 batches, and output JSON.
"""

import csv
import json
import re
import math

INPUT_FILE = "/home/user/attachments/vcs-and-angels.csv"
OUTPUT_FILE = "/home/user/output/contacts_rows_301_400.json"

# Basic email format validation
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

def validate_email(email: str) -> bool:
    if not email or not email.strip():
        return False
    return bool(EMAIL_RE.match(email.strip()))

def main():
    # Read CSV
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        # Clean up fieldnames (trailing comma creates an empty-string key)
        fieldnames = [fn for fn in fieldnames if fn.strip()]
        all_rows = list(reader)

    # Rows 301-400 (1-indexed data rows → Python 0-indexed 300-399)
    start_idx = 300  # 0-indexed
    end_idx = 400     # exclusive
    selected = all_rows[start_idx:end_idx]

    # Identify the "core" columns vs "other" columns
    core_cols = {"name", "city", "contact", "email"}
    other_cols = [c for c in fieldnames if c not in core_cols]

    contacts = []
    invalid_email_list = []
    valid_email_contacts = []

    for i, row in enumerate(selected):
        data_row_number = start_idx + i + 1  # 1-indexed data row number
        name = (row.get("name") or "").strip()
        firm = (row.get("name") or "").strip()   # 'name' column is actually the firm name
        contact_name = (row.get("contact") or "").strip()
        city = (row.get("city") or "").strip()
        email = (row.get("email") or "").strip()

        email_valid = validate_email(email)

        # Build other_columns dict
        all_other = {}
        for col in fieldnames:
            if col not in {"contact", "email"}:
                val = (row.get(col) or "").strip()
                if val:
                    all_other[col] = val

        contact_record = {
            "name": contact_name,
            "firm": firm,
            "city": city,
            "email": email,
            "email_valid": email_valid,
            "row_number": data_row_number,
            "all_other_columns": all_other
        }

        contacts.append(contact_record)

        if email_valid:
            valid_email_contacts.append(contact_record)
        else:
            invalid_email_list.append({
                "name": contact_name,
                "firm": firm,
                "email": email if email else "(empty)",
                "row_number": data_row_number,
                "reason": "empty email" if not email else "invalid format"
            })

    # Split valid-email contacts into 5 roughly equal batches
    n = len(valid_email_contacts)
    batch_size = math.ceil(n / 5)
    batches = {}
    for b in range(5):
        batch_start = b * batch_size
        batch_end = min((b + 1) * batch_size, n)
        batch_contacts = valid_email_contacts[batch_start:batch_end]
        # Remove email_valid from batch output (redundant—all valid)
        clean = []
        for c in batch_contacts:
            rec = {k: v for k, v in c.items() if k != "email_valid"}
            clean.append(rec)
        batches[f"batch{b + 1}"] = clean

    # Build full contact list for summary (all 100 rows)
    all_contacts_summary = []
    for c in contacts:
        rec = {k: v for k, v in c.items()}
        all_contacts_summary.append(rec)

    # Assemble output
    output = {
        "chunk_definition": {
            "description": "Data rows 301-400 (1-indexed, excluding header row). "
                           "Row 301 is the 302nd line of the CSV file (line 1 = header). "
                           "Row 400 is the 401st line of the CSV file.",
            "start_data_row": 301,
            "end_data_row": 400,
            "file_line_range": "lines 302-401 of the CSV (header is line 1)",
            "assumptions": [
                "Row numbering is 1-indexed starting from the first data row after the header.",
                "The CSV column 'name' represents the firm/fund name.",
                "The CSV column 'contact' represents the person's name.",
                "Email validation uses a basic regex format check (user@domain.tld).",
                "Batches are divided as evenly as possible (larger batches first if uneven)."
            ]
        },
        "total_rows": len(contacts),
        "valid_email_count": len(valid_email_contacts),
        "invalid_email_count": len(invalid_email_list),
        "invalid_email_list": invalid_email_list,
        "batches_summary": {
            f"batch{b+1}": len(batches[f"batch{b+1}"]) for b in range(5)
        },
        "batch1": batches["batch1"],
        "batch2": batches["batch2"],
        "batch3": batches["batch3"],
        "batch4": batches["batch4"],
        "batch5": batches["batch5"],
        "all_contacts": all_contacts_summary
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"Total rows extracted: {len(contacts)}")
    print(f"Valid emails: {len(valid_email_contacts)}")
    print(f"Invalid emails: {len(invalid_email_list)}")
    sizes = [f"batch{b+1}={len(batches[f'batch{b+1}'])}" for b in range(5)]
    print(f"Batch sizes: {', '.join(sizes)}")
    if invalid_email_list:
        print("\nInvalid email entries:")
        for inv in invalid_email_list:
            print(f"  Row {inv['row_number']}: {inv['name']} ({inv['firm']}) - {inv['email']} [{inv['reason']}]")
    print(f"\nOutput written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
