import csv
import re
import json

# Read the CSV
rows = []
with open('/home/user/attachments/vcs-and-angels.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    all_rows = list(reader)
    # Extract rows 501-600 (0-indexed: 500-599)
    rows = all_rows[500:600]

print(f"Total rows in CSV: {len(all_rows)}")
print(f"Extracted rows: {len(rows)}")
print(f"Columns: {list(all_rows[0].keys())}")

# Email validation regex (RFC 5322 simplified)
email_pattern = re.compile(
    r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
)

def validate_email(email):
    if not email or email.strip() == '':
        return {"valid": False, "reason": "missing"}
    email = email.strip()
    if email_pattern.match(email):
        return {"valid": True, "reason": None}
    else:
        return {"valid": False, "reason": "invalid_format"}

# Parse and structure all rows
parsed = []
valid_count = 0
invalid_count = 0
missing_count = 0

for i, row in enumerate(rows):
    row_num = 501 + i
    # Clean up keys (handle trailing empty column from trailing comma)
    name = (row.get('name') or '').strip()
    city = (row.get('city') or '').strip()
    contact = (row.get('contact') or '').strip()
    email_raw = (row.get('email') or '').strip()

    email_check = validate_email(email_raw)
    if email_check["valid"]:
        valid_count += 1
        email_status = "valid"
    elif email_check["reason"] == "missing":
        missing_count += 1
        email_status = "missing"
    else:
        invalid_count += 1
        email_status = "invalid_format"

    # Determine sub-chunk
    if row_num <= 520:
        chunk = 1
        chunk_label = "Chunk 1 (Rows 501-520)"
    elif row_num <= 540:
        chunk = 2
        chunk_label = "Chunk 2 (Rows 521-540)"
    elif row_num <= 560:
        chunk = 3
        chunk_label = "Chunk 3 (Rows 541-560)"
    elif row_num <= 580:
        chunk = 4
        chunk_label = "Chunk 4 (Rows 561-580)"
    else:
        chunk = 5
        chunk_label = "Chunk 5 (Rows 581-600)"

    entry = {
        "row_number": row_num,
        "firm": name,
        "city": city,
        "contact_name": contact,
        "email": email_raw if email_raw else None,
        "email_status": email_status,
        "sub_chunk": chunk,
        "sub_chunk_label": chunk_label
    }
    parsed.append(entry)

# Build the final structured output
chunks = {}
for i in range(1, 6):
    chunk_entries = [e for e in parsed if e["sub_chunk"] == i]
    start = 501 + (i-1)*20
    end = 500 + i*20
    chunks[f"chunk_{i}"] = {
        "label": f"Rows {start}-{end}",
        "count": len(chunk_entries),
        "contacts": chunk_entries
    }

output = {
    "metadata": {
        "source_file": "vcs-and-angels.csv",
        "columns_available": ["name (firm)", "city", "contact (person name)", "email"],
        "columns_not_available": ["title", "investment_focus"],
        "note": "The CSV only contains firm name, city, contact name, and email. Title and investment focus columns are not present in this dataset.",
        "total_extracted": len(parsed),
        "row_range": "501-600",
        "email_validation_summary": {
            "valid_emails": valid_count,
            "invalid_emails": invalid_count,
            "missing_emails": missing_count,
            "total": len(parsed)
        }
    },
    "full_parsed_data": parsed,
    "sub_chunks": chunks
}

# Write JSON output
with open('/home/user/output/angels_rows_501_600.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nEmail Validation Summary:")
print(f"  Valid: {valid_count}")
print(f"  Invalid format: {invalid_count}")
print(f"  Missing: {missing_count}")
print(f"\nSub-chunk breakdown:")
for i in range(1, 6):
    chunk_entries = [e for e in parsed if e["sub_chunk"] == i]
    start = 501 + (i-1)*20
    end = 500 + i*20
    print(f"  Chunk {i} (Rows {start}-{end}): {len(chunk_entries)} contacts")

print(f"\nJSON output written to /home/user/output/angels_rows_501_600.json")
