import json
import os

# Define the path for the JSON file
define_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'analyze.daily_keno.json')

# Check if the JSON file exists
if not os.path.exists(define_json_path):
    # Create the JSON file with an empty list
    with open(define_json_path, 'w') as f:
        json.dump([], f)
        print('analyze.daily_keno.json file created.')
else:
    print('analyze.daily_keno.json file already exists.')