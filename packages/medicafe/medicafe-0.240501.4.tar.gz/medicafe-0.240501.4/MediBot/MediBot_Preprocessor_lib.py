import subprocess
import json
import os
import csv
import sys

"""
Draft Docstring to move over from Preprocessor.

Data Integrity and Validation
 Implement a mechanism to confirm the accuracy of entered data, potentially through a verification step or summary report.
 Enhance CSV integrity checks to identify and report potential issues with data format, especially concerning insurance policy numbers and special character handling.

Development Roadmap for crosswalk_update()
 Automation required for updating the crosswalk.json when new Medisoft insurance is discovered.
For open_csv_for_editing

Known Issues and Bugs
 Address the handling of '.' and other special characters that may disrupt parsing, especially under Windows XP.

For load_csv_data

Preprocessing Enhancements
 Optimize script startup and CSV loading to reduce initial latency.

Data Integrity and Validation
 Conduct a thorough CSV integrity check before processing to flag potential issues upfront.

Future Work
 Consolidate data from multiple sources (Provider_Notes.csv, Surgery_Schedule.csv, and Carols_CSV.csv) into a single table with Patient ID as the key, ensuring all data elements are aligned and duplicate entries are minimized.
 Implement logic to verify and match Patient IDs across different files to ensure data integrity before consolidation. (Catching errors between source data)
 Optimize the preprocessing of surgery dates and diagnosis codes for use in patient billing and scheduling systems.
"""

def save_crosswalk(crosswalk_path, crosswalk):
    """
    Saves the updated crosswalk to a JSON file.
    Args:
        crosswalk_path (str): Path to the crosswalk.json file.
        crosswalk (dict): The updated crosswalk data.
    Returns:
        bool: True if the file was successfully saved, False otherwise.
    """
    try:
        # Initialize 'payer_id' key if not present
        if 'payer_id' not in crosswalk:
            print("save_crosswalk is initializing 'payer_id' key...")
            crosswalk['payer_id'] = {}

        # Convert all 'medisoft_id' fields from sets to lists if necessary
        for k, v in crosswalk.get('payer_id', {}).items():
            if isinstance(v.get('medisoft_id'), set):
                v['medisoft_id'] = list(v['medisoft_id'])

        with open(crosswalk_path, 'w') as file:
            json.dump(crosswalk, file, indent=4)  # Save the entire dictionary
        return True

    except KeyError as e:
        # Log the KeyError with specific information about what was missing
        print("Key Error: A required key is missing in the crosswalk data -", e)
        return False

    except TypeError as e:
        # Handle data type errors (e.g., non-serializable types)
        print("Type Error: There was a type issue with the data being saved in the crosswalk -", e)
        return False

    except IOError as e:
        # Handle I/O errors related to file operations
        print("I/O Error: An error occurred while writing to the crosswalk file -", e)
        return False

    except Exception as e:
        # A general exception catch to log any other exceptions that may not have been anticipated
        print("Unexpected crosswalk error:", e)
        return False


def open_csv_for_editing(csv_file_path):
    try:
        # Open the CSV file in the default program
        subprocess.run(['open' if os.name == 'posix' else 'start', csv_file_path], check=True, shell=True)
        print("After saving the revised CSV, please re-run MediBot.")
    except subprocess.CalledProcessError as e:
        print("Failed to open CSV file:", e)
        
# Function to load and process CSV data
def load_csv_data(csv_file_path):
    try:
        # Check if the file exists
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError("***Error: CSV file '{}' not found.".format(csv_file_path))
        
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]  # Return a list of dictionaries
    except FileNotFoundError as e:
        print(e)  # Print the informative error message
        print("Hint: Check if CSV file is located in the expected directory or specify a different path in config file.")
        print("Please correct the issue and re-run MediBot.")
        sys.exit(1)  # Halt the script
    except IOError as e:
        print("Error reading CSV file: {}. Please check the file path and permissions.".format(e))
        sys.exit(1)  # Halt the script in case of other IO errors