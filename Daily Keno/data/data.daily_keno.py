import json
from collections import Counter

# Load the analysis data from the JSON file
analysis_file_path = 'data.daily_keno.json'  # Updated path
with open(analysis_file_path, 'r') as f:
    analysis_data = json.load(f)

# Check if the upcoming draw is in the morning (you can replace 'morning' with your actual logic)
upcoming_draw_is_morning = True  # Update this with your logic

# Get the frequency dictionary based on the time of day
if upcoming_draw_is_morning:
    frequency_dict = analysis_data['frequency_morning']
    draw_time = "m"
else:
    frequency_dict = analysis_data['frequency_evening']
    draw_time = "e"

# Select the 20 numbers with the highest frequency
most_likely_numbers = dict(sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True)[:20])

# Select the 20 numbers with the lowest frequency (least likely)
least_likely_numbers = dict(sorted(frequency_dict.items(), key=lambda item: item[1])[:20])

# Attach draw date and time to the suggested numbers
most_likely_numbers_with_time = {number: {"frequency": frequency, "draw_time": draw_time} for number, frequency in most_likely_numbers.items()}
least_likely_numbers_with_time = {number: {"frequency": frequency, "draw_time": draw_time} for number, frequency in least_likely_numbers.items()}

# Save the most likely and least likely numbers with date and time to a JSON file
output_file_path = 'output.daily_keno.json'  # Specify the path for the output file
with open(output_file_path, 'w') as output_file:
    output_data = {
        "most_likely_numbers": most_likely_numbers_with_time,
        "least_likely_numbers": least_likely_numbers_with_time,
    }
    json.dump(output_data, output_file, indent=4)

# Load the Daily Keno numbers data from the JSON file
daily_keno_numbers_file_path = '../daily_keno_numbers.json'  # Specify the path for the Daily Keno numbers data
with open(daily_keno_numbers_file_path, 'r') as daily_keno_file:
    daily_keno_data = json.load(daily_keno_file)

# Analyze the most and least frequent numbers for the day
day_frequency = Counter()

for entry in daily_keno_data:
    numbers = entry['numbers']
    day_frequency.update(numbers)

# Select the 20 most frequent numbers for the day
most_frequent_day_numbers = dict(day_frequency.most_common(20))

# Select the 20 least frequent numbers for the day
least_frequent_day_numbers = dict(sorted(day_frequency.items(), key=lambda item: item[1])[:20])

# Append the most and least frequent numbers for the day to the same output file
with open(output_file_path, 'a') as output_file:
    output_data = {
        "most_frequent_day_numbers": most_frequent_day_numbers,
        "least_frequent_day_numbers": least_frequent_day_numbers,
    }
    json.dump(output_data, output_file, indent=4)

# Print the results for the day
print("\nMost frequent numbers for the day:")
for number, frequency in most_frequent_day_numbers.items():
    print(f"Number: {number}, Frequency: {frequency}")

print("\nLeast frequent numbers for the day:")
for number, frequency in least_frequent_day_numbers.items():
    print(f"Number: {number}, Frequency: {frequency}")

print("\nData saved to output.daily_keno.json.")
