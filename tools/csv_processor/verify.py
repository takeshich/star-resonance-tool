
import csv
import sys

def load_and_sort(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            # Remove empty rows
            rows = [r for r in reader if r]
            # Sort by ID (index 1) which is Mod_XXX.
            rows.sort(key=lambda x: x[1])
            return header, rows
    except Exception as e:
        print(f'Error reading {path}: {e}')
        sys.exit(1)

try:
    file1 = sys.argv[1] if len(sys.argv) > 1 else 'tools/csv_processor/master_data.csv'
    file2 = sys.argv[2] if len(sys.argv) > 2 else 'tools/csv_processor/fortests/master_data_seikai.csv'

    h1, r1 = load_and_sort(file1)
    h2, r2 = load_and_sort(file2)

    # Verify Header
    if h1 != h2:
        print('HEADER MISMATCH')
        print(f'Actual: {h1}')
        print(f'Expected: {h2}')
        sys.exit(0)

    # Verify Row Count
    if len(r1) != len(r2):
        print(f'ROW COUNT MISMATCH: Actual({len(r1)}) vs Expected({len(r2)})')

    # Verify Content
    mismatches = []
    max_len = min(len(r1), len(r2))
    
    for i in range(max_len):
        row_diffs = []
        if r1[i] != r2[i]:
            for j in range(len(r1[i])):
                if r1[i][j] != r2[i][j]:
                    col_name = h1[j] if j < len(h1) else f"Col_{j}"
                    row_diffs.append(f'{col_name}: {r1[i][j]} != {r2[i][j]}')
            
            diff_msg = ", ".join(row_diffs)
            mismatches.append(f'Row {i} (ID {r1[i][1]}): {diff_msg}')

    if mismatches:
        print(f'FAILED: {len(mismatches)} discrepancies found.')
        for m in mismatches:
            print(m)
    else:
        if len(r1) == len(r2):
            print('SUCCESS: No differences found.')

except Exception as e:
    print(f"Script Error: {e}")
