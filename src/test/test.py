import re
import datetime

# Input date string
date_str = "/Date(1696957200000)/"

# Extract the timestamp from the string using regular expressions
match = re.search(r'\d+', date_str)

if match:
    timestamp = int(match.group())  # Convert the matched digits to an integer
    # Convert the timestamp to a datetime object
    normal_date = datetime.datetime.fromtimestamp(timestamp / 1000)  # Divide by 1000 to convert from milliseconds to seconds
    print(normal_date)
else:
    print("Invalid date format")

