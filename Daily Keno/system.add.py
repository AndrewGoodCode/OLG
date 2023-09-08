from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    data = request.json
    date = data['date']
    time = data['time']
    numbers = data['numbers']

    json_file_path = "daily_keno_numbers.json"

    # Check if file exists, create if not
    if not os.path.exists(json_file_path):
        with open(json_file_path, 'w') as f:
            json.dump([], f)

    # Read existing data
    with open(json_file_path, 'r') as f:
        existing_data = json.load(f)

    # Check for duplicate date and time
    for entry in existing_data:
        if entry['date'] == date and entry['time'] == time:
            return jsonify({"status": "error", "message": "Entry for this date and time already exists."}), 400

    # Append new entry
    new_entry = {"date": date, "time": time, "numbers": numbers}
    existing_data.append(new_entry)

    # Write back to file
    with open(json_file_path, 'w') as f:
        json.dump(existing_data, f)

    return jsonify({"status": "success", "message": "Entry added successfully."})

if __name__ == '__main__':
    app.run(debug=True)
