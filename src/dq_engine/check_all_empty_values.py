# Check every entry for empty values

# Method 1: Check for NaN/null values across entire dataset
print("=== NaN/NULL VALUES ===")
print(f"Total NaN values in dataset: {df.isnull().sum().sum()}")
print("NaN values by column:")
print(df.isnull().sum())

# Method 2: Check for empty strings ('')
print("\n=== EMPTY STRINGS ('') ===")
empty_strings = (df == '').sum()
print(f"Total empty strings: {empty_strings.sum()}")
if empty_strings.sum() > 0:
    print("Empty strings by column:")
    print(empty_strings[empty_strings > 0])

# Method 3: Check for empty spaces (' ')
print("\n=== EMPTY SPACES (' ') ===")
empty_spaces = (df == ' ').sum()
print(f"Total empty spaces: {empty_spaces.sum()}")
if empty_spaces.sum() > 0:
    print("Empty spaces by column:")
    print(empty_spaces[empty_spaces > 0])

# Method 4: Check for any whitespace-only values
print("\n=== WHITESPACE-ONLY VALUES ===")
whitespace_count = 0
for col in df.select_dtypes(include=['object']).columns:
    whitespace_in_col = df[col].astype(str).str.strip().eq('').sum()
    if whitespace_in_col > 0:
        print(f"{col}: {whitespace_in_col}")
        whitespace_count += whitespace_in_col
print(f"Total whitespace-only values: {whitespace_count}")

# Method 5: Comprehensive check for all types of "empty"
print("\n=== COMPREHENSIVE EMPTY CHECK ===")
for col in df.columns:
    null_count = df[col].isnull().sum()
    empty_str = (df[col] == '').sum() if df[col].dtype == 'object' else 0
    space_str = (df[col] == ' ').sum() if df[col].dtype == 'object' else 0
    
    total_empty = null_count + empty_str + space_str
    if total_empty > 0:
        print(f"{col}: NaN={null_count}, Empty='{empty_str}, Spaces={space_str}, Total={total_empty}")

# Method 6: One-liner for quick check
print(f"\n=== QUICK SUMMARY ===")
print(f"NaN: {df.isnull().sum().sum()}, Empty strings: {(df == '').sum().sum()}, Spaces: {(df == ' ').sum().sum()}")

# Method 7: Show actual rows with any empty values (sample)
print("\n=== SAMPLE ROWS WITH EMPTY VALUES ===")
# Find rows with any NaN
nan_rows = df[df.isnull().any(axis=1)]
if len(nan_rows) > 0:
    print(f"Sample rows with NaN values ({len(nan_rows)} total):")
    print(nan_rows.head()[['customerID'] + [col for col in df.columns if df[col].isnull().any()]])

# Find rows with empty strings in object columns
for col in df.select_dtypes(include=['object']).columns:
    empty_rows = df[df[col] == '']
    if len(empty_rows) > 0:
        print(f"Rows with empty {col}: {len(empty_rows)}")