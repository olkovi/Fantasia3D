import json
import os
from collections import defaultdict

# Replace with your actual directory path
json_directory = './ok'

# Dictionary to store out_dir and associated files
out_dir_dict = defaultdict(list)

# Loop through all the files in the directory
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(json_directory, filename)
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Extract out_dir if it exists
            if 'out_dir' in data:
                out_dir_value = data['out_dir']
                out_dir_dict[out_dir_value].append(filename)

# Check for duplicate out_dir values
duplicates = {out_dir: files for out_dir, files in out_dir_dict.items() if len(files) > 1}

# Print results
if duplicates:
    print("Files with the same 'out_dir':")
    for out_dir, files in duplicates.items():
        print(f"out_dir: {out_dir} -> Files: {', '.join(files)}")
else:
    print("No files have the same 'out_dir'.")
