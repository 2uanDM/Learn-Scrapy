data = '3.298,86'

# Remove non-numeric characters
cleaned_data = data.replace(',', '')

# Convert to float
parsed_float = float(cleaned_data)

print(parsed_float)  # Output: 3298.86
