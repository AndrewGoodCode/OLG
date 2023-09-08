import json
import os
from collections import Counter

# Print the current working directory for debugging
print("Current Working Directory:", os.getcwd())

# Define the file paths
analysis_file_path = os.path.join(os.getcwd(), 'data.daily_keno.json')
daily_keno_numbers_file_path = os.path.join(os.getcwd(), 'daily_keno_numbers.json')
output_file_path = os.path.join(os.getcwd(), 'output.daily_keno.json')

# Check if the analysis file exists
if not os.path.exists(analysis_file_path):
    print(f"Analysis file {analysis_file_path} not found. Exiting.")
    exit(1)

# Load the analysis data from the JSON file
with open(analysis_file_path, 'r') as f:
    analysis_data = json.load(f)

# Determine if the upcoming draw is in the morning or evening
upcoming_draw_is_morning = True  # Replace with your actual logic
draw_time = 'm' if upcoming_draw_is_morning else 'e'

# Check if the frequency key exists in the analysis data
key = f'frequency_{draw_time}'
if key not in analysis_data:
    print(f"Key {key} not found in analysis data. Exiting.")
    exit(1)

# Get the frequency dictionary based on the time of day
frequency_dict = analysis_data[key]

# Select the 20 numbers with the highest frequency
most_likely_numbers = dict(sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)[:20])

# Select the 20 numbers with the lowest frequency
least_likely_numbers = dict(sorted(frequency_dict.items(), key=lambda item: item[1])[:20])

# Attach draw date and time to the suggested numbers
most_likely_numbers_with_time = {number: {'frequency': frequency, 'draw_time': draw_time} for number, frequency in most_likely_numbers.items()}
least_likely_numbers_with_time = {number: {'frequency': frequency, 'draw_time': draw_time} for number, frequency in least_likely_numbers.items()}

# Save the most likely and least likely numbers with date and time to a JSON file
with open(output_file_path, 'w') as output_file:
    output_data = {
        'most_likely_numbers': most_likely_numbers_with_time,
        'least_likely_numbers': least_likely_numbers_with_time,
    }
    json.dump(output_data, output_file, indent=4)

# Check if the daily keno numbers file exists
if not os.path.exists(daily_keno_numbers_file_path):
    print(f"Daily Keno numbers file {daily_keno_numbers_file_path} not found. Exiting.")
    exit(1)

# Load the Daily Keno numbers data from the JSON file
with open(daily_keno_numbers_file_path, 'r') as daily_keno_file:
    daily_keno_data = json.load(daily_keno_file)

# Analyze the most and least frequent numbers for the day
day_frequency = Counter()
for entry in daily_keno_data:
    numbers = entry['numbers']
    day_frequency.update(numbers)

# Select the 20 most and least frequent numbers for the day
most_frequent_day_numbers = dict(day_frequency.most_common(20))
least_frequent_day_numbers = dict(sorted(day_frequency.items(), key=lambda item: item[1])[:20])

# Append the most and least frequent numbers for the day to the same output file
with open(output_file_path, 'a') as output_file:
    output_data = {
        'most_frequent_day_numbers': most_frequent_day_numbers,
        'least_frequent_day_numbers': least_frequent_day_numbers,
    }
    json.dump(output_data, output_file, indent=4)

print("Data saved to output.daily_keno.json.")
