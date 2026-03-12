import csv
import json

rows = []
with open('/home/user/attachments/vcs-and-angels.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)  # skip header
    for i, row in enumerate(reader, start=1):
        if 101 <= i <= 200:
            rows.append({
                "row_number": i,
                "firm_name": row[0].strip(),
                "city": row[1].strip(),
                "contact_name": row[2].strip(),
                "email": row[3].strip()
            })

# Split into 5 chunks of 20
chunks = [
    rows[0:20],    # rows 101-120
    rows[20:40],   # rows 121-140
    rows[40:60],   # rows 141-160
    rows[60:80],   # rows 161-180
    rows[80:100],  # rows 181-200
]

chunk_labels = [
    "Chunk 1: Rows 101-120",
    "Chunk 2: Rows 121-140",
    "Chunk 3: Rows 141-160",
    "Chunk 4: Rows 161-180",
    "Chunk 5: Rows 181-200",
]

# Print each chunk clearly labeled
for label, chunk in zip(chunk_labels, chunks):
    print(f"\n{'='*80}")
    print(f"  {label}")
    print(f"{'='*80}")
    print(f"{'Row':<6} {'Firm Name':<45} {'City':<20} {'Contact Name':<35} {'Email'}")
    print(f"{'-'*6} {'-'*45} {'-'*20} {'-'*35} {'-'*40}")
    for r in chunk:
        print(f"{r['row_number']:<6} {r['firm_name']:<45} {r['city']:<20} {r['contact_name']:<35} {r['email']}")

# Output JSON
print(f"\n\n{'='*80}")
print("  JSON OUTPUT")
print(f"{'='*80}")
json_output = json.dumps(chunks, indent=2, ensure_ascii=False)
print(json_output)

# Save JSON to files
with open('/home/user/agent-c3a1e2a4/vcs_rows_101_200.json', 'w', encoding='utf-8') as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

with open('/home/user/output/vcs_rows_101_200.json', 'w', encoding='utf-8') as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print(f"\nJSON saved to vcs_rows_101_200.json")
print(f"Total rows extracted: {len(rows)}")
print(f"Chunks: {len(chunks)}, each with {[len(c) for c in chunks]} rows")
