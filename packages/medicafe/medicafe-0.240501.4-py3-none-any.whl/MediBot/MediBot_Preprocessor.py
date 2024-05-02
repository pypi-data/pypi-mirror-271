import csv
import os
import re
from datetime import datetime
from collections import OrderedDict # so that the field_mapping stays in order.
from collections import defaultdict
import re
import sys
import argparse
from MediBot_Preprocessor_lib import save_crosswalk, open_csv_for_editing, load_csv_data

# Add parent directory of the project to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_dir)

from MediLink import MediLink_ConfigLoader
from MediLink import MediLink_DataMgmt

"""
Preprocessing Enhancements
- [X] Preprocess Insurance Policy Numbers and Group Numbers to replace '-' with ''.
- [X] De-duplicate entries in the CSV and only entering the px once even if they show up twice in the file.
- [ ] Implement dynamic field combination in CSV pre-processing for flexibility with various CSV formats.
- [ ] Enhance SSN cleaning logic to handle more variations of sensitive data masking.
- [ ] Optimize script startup and CSV loading to reduce initial latency.

Data Integrity and Validation
- [ ] Conduct a thorough CSV integrity check before processing to flag potential issues upfront.
- [ ] Implement a mechanism to confirm the accuracy of entered data, potentially through a verification step or summary report.
- [ ] Explore the possibility of integrating direct database queries for existing patient checks to streamline the process.
- [ ] Automate the replacement of spaces with underscores ('_') in last names for Medicare entries.
- [ ] Enhance CSV integrity checks to identify and report potential issues with data format, especially concerning insurance policy numbers and special character handling.

Known Issues and Bugs
- [ ] Address the handling of '.' and other special characters that may disrupt parsing, especially under Windows XP.
- [ ] Investigate the issue with Excel modifying long policy numbers in the CSV and provide guidance or a workaround.

Future Work
- [X] Check for PatientID number in La Forma Z to link back to Carol's table for mapping Medisoft insurance name to payerID and payer name and address.
- [X] Check for PatientID to Medisoft custom insurance name mapping in MAPAT.
- [ ] Consolidate data from multiple sources (Provider_Notes.csv, Surgery_Schedule.csv, and Carols_CSV.csv) into a single table with Patient ID as the key, ensuring all data elements are aligned and duplicate entries are minimized.
- [ ] Implement logic to verify and match Patient IDs across different files to ensure data integrity before consolidation. (Catching errors between source data)
- [ ] Optimize the preprocessing of surgery dates and diagnosis codes for use in patient billing and scheduling systems.
- [ ] Read Surgery Schedule doc and parse out a Patient ID : Diagnosis Code table.
- [ ] The Minutes & Cancellation data with logic to consolidate into one table in memory.
- [ ] Dynamically list the endpoint for a new Payer ID via API or user interaction to update the crosswalk.json efficiently.
- [ ] Pull listed addresses of insurance from the CSV. (Not really necessary)
- [ ] Retroactively learn Medisoft insurance name and payerID from the provided data sources.

Development Roadmap for crosswalk_update():
- [X] Automation required for updating the crosswalk.json when new Medisoft insurance is discovered.
- [X] New Medisoft insurances are identified based on the payer ID number.
- [X] Check the existence of the payer ID in crosswalk.json under existing endpoints.
- [X] Facilitate grouping of IDs for insurances like CIGNA with multiple addresses but few payer IDs.
- [X] Retroactive learning based on selected insurances in Medisoft 
- [ ] Prompt user via endpoint APIs to add new payer ID to an endpoint if it does not exist.
- [ ] Retain payer IDs without Insurance ID for future assignments.
- [ ] Check for free payer IDs and determine the appropriate endpoint for assignment.
- [ ] Present unrecognized payer IDs with Carol's Insurance Name to users for assignment to Insurance ID. (Try API Call)
- [ ] Integrate API checks to verify payer ID availability and related information.
- [ ] Implement "Fax/Mail or Other" endpoint for unavailable payer IDs.
- [ ] Present user with a list of top insurances for selection based on fuzzy search scores.
- [ ] Establish payer ID to insurance ID relationship based on user selection.
- [ ] Implicitly establish payer ID to endpoint mapping based on user selection.
- [ ] Implement validation mechanisms to prevent incorrect mappings and ensure data integrity.
- [ ] Considerations for extracting insurance addresses (if necessary)
"""
# Load configuration
# Should this also take args? Path for ./MediLink needed to be added for this to resolve
config, crosswalk = MediLink_ConfigLoader.load_configuration()

class InitializationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def initialize(config):
    global AHK_EXECUTABLE, CSV_FILE_PATH, field_mapping, page_end_markers
    
    try:
        AHK_EXECUTABLE = config.get('AHK_EXECUTABLE', "")
    except AttributeError:
        raise InitializationError("Error: 'AHK_EXECUTABLE' not found in config.")
    
    try:
        CSV_FILE_PATH = config.get('CSV_FILE_PATH', "")
    except AttributeError:
        raise InitializationError("Error: 'CSV_FILE_PATH' not found in config.")
    
    try:
        field_mapping = OrderedDict(config.get('field_mapping', {}))
    except AttributeError:
        raise InitializationError("Error: 'field_mapping' not found in config.")
    
    try:
        page_end_markers = config.get('page_end_markers', [])
    except AttributeError:
        raise InitializationError("Error: 'page_end_markers' not found in config.")

def load_insurance_data_from_mains(config):
    """
    Loads insurance data from MAINS and creates a mapping from insurance names to their respective IDs.
    This mapping is critical for the crosswalk update process to correctly associate payer IDs with insurance IDs.

    Args:
        config (dict): Configuration object containing necessary paths and parameters.

    Returns:
        dict: A dictionary mapping insurance names to insurance IDs.
    """
    # Retrieve MAINS path and slicing information from the configuration
    mains_path = config['MAINS_MED_PATH']
    mains_slices = crosswalk['mains_mapping']['slices']
    
    # Initialize the dictionary to hold the insurance to insurance ID mappings
    insurance_to_id = {}
    
    # Read data from MAINS using a provided function to handle fixed-width data
    for record, line_number in MediLink_DataMgmt.read_general_fixed_width_data(mains_path, mains_slices):
        insurance_name = record['MAINSNAME']
        # Assuming line_number gives the correct insurance ID without needing adjustment
        insurance_to_id[insurance_name] = line_number
    
    return insurance_to_id

def load_insurance_data_from_mapat(config, crosswalk):
    """
    Loads insurance data from MAPAT and creates a mapping from patient ID to insurance ID.
    
    Args:
        config (dict): Configuration object containing necessary paths and parameters.
        crosswalk ... ADD HERE.

    Returns:
        dict: A dictionary mapping patient IDs to insurance IDs.
    """
    # Retrieve MAPAT path and slicing information from the configuration
    mapat_path = config['MAPAT_MED_PATH']
    mapat_slices = crosswalk['mapat_mapping']['slices']
    
    # Initialize the dictionary to hold the patient ID to insurance ID mappings
    patient_id_to_insurance_id = {}
    
    # Read data from MAPAT using a provided function to handle fixed-width data
    for record, line_number in MediLink_DataMgmt.read_general_fixed_width_data(mapat_path, mapat_slices):
        patient_id = record['MAPATPXID']
        insurance_id = record['MAPATINID']
        patient_id_to_insurance_id[patient_id] = insurance_id
        
    return patient_id_to_insurance_id

def parse_z_dat(z_dat_path, config):
    """
    Parses the Z.dat file to map Patient IDs to Insurance Names using the provided fixed-width file format.
    
    Args:
        z_dat_path (str): Path to the Z.dat file.
        config (dict): Configuration object containing slicing information and other parameters.
    
    Returns:
        dict: A dictionary mapping Patient IDs to Insurance Names.
    """
    patient_id_to_insurance_name = {}
    
    try:
        # Reading blocks of fixed-width data (3 lines per record: personal, insurance, service)
        for personal_info, insurance_info, service_info in MediLink_DataMgmt.read_fixed_width_data(z_dat_path, config):
            # Parsing the data using slice definitions from the config
            parsed_data = MediLink_DataMgmt.parse_fixed_width_data(personal_info, insurance_info, service_info, config)
        
            # Extract Patient ID and Insurance Name from parsed data
            patient_id = parsed_data.get('PATID')
            insurance_name = parsed_data.get('INAME')
            
            if patient_id and insurance_name:
                patient_id_to_insurance_name[patient_id] = insurance_name
                MediLink_ConfigLoader.log("Mapped Patient ID {} to Insurance Name {}".format(patient_id, insurance_name), config, level="INFO")
    
    except FileNotFoundError:
        MediLink_ConfigLoader.log("File not found: {}".format(z_dat_path), config, level="ERROR")
        raise
    except Exception as e:
        MediLink_ConfigLoader.log("Failed to parse Z.dat: {}".format(str(e)), config, level="ERROR")
        raise

    return patient_id_to_insurance_name

def load_historical_payer_to_patient_mappings(config):
    """
    Loads historical mappings from multiple Carol's CSV files in a specified directory,
    mapping Payer IDs to sets of Patient IDs.

    Args:
        config (dict): Configuration object containing the directory path for Carol's CSV files
                       and other necessary parameters.

    Returns:
        dict: A dictionary where each key is a Payer ID and the value is a set of Patient IDs.
    """
    directory_path = os.path.dirname(config['CSV_FILE_PATH'])
    payer_to_patient_ids = defaultdict(set)

    try:
        # Check if the directory exists
        if not os.path.isdir(directory_path):
            raise FileNotFoundError("Directory '{}' not found.".format(directory_path))

        # Loop through each file in the directory containing Carol's historical CSVs
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if filename.endswith('.csv'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile)
                        found_data = False  # Flag to track if any valid data is found in the CSV
                        for row in reader:
                            if 'Patient ID' not in row:
                                raise ValueError("CSV file '{}' is misformatted or empty.".format(filename))
                            elif not row.get('Patient ID').strip():
                                raise ValueError("CSV file '{}' is misformatted: Missing or empty 'Patient ID' in row {}".format(filename, row))
                            elif not row.get('Ins1 Payer ID').strip():
                                raise ValueError("CSV file '{}' is misformatted: Missing or empty 'Ins1 Payer ID' in row {}".format(filename, row))
                            else:
                                found_data = True
                                payer_id = row['Ins1 Payer ID'].strip()
                                patient_id = row['Patient ID'].strip()
                                payer_to_patient_ids[payer_id].add(patient_id)
                                MediLink_ConfigLoader.log("Found Patient ID {} with Payer ID {}".format(patient_id, payer_id))
                        if not found_data:
                            raise ValueError("CSV file '{}' is empty.".format(filename))
                except Exception as e:
                    print("Error processing file {}: {}".format(filename, e))
    except FileNotFoundError as e:
        print("Error: {}".format(e))

    if not payer_to_patient_ids:
        print("No historical mappings were generated.")
    
    return dict(payer_to_patient_ids)

def initialize_crosswalk_from_mapat(config, crosswalk):
    """
    Input: Historical Carol's CSVs and MAPAT data.

    Process:
        Extract mappings from Carol's old CSVs to identify Payer IDs and associated Patient IDs.
        Use MAPAT to correlate these Patient IDs with Insurance IDs.
        Compile these mappings into the crosswalk, setting Payer IDs as keys and corresponding Insurance IDs as values.

    Output: A fully populated crosswalk.json file that serves as a baseline for future updates.
    """
    payer_id_to_details = {}
    
    # Load historical Patient ID to Insurance ID mappings from MAPAT
    patient_id_to_insurance_id = load_insurance_data_from_mapat(config, crosswalk)

    # Check if patient_id_to_insurance_id is empty
    if not patient_id_to_insurance_id:
        print("Error: Failed to load historical Patient ID to Insurance ID mappings from MAPAT.")
        sys.exit(1)

    # Process historical Carol's CSVs
    payer_id_to_patient_ids = load_historical_payer_to_patient_mappings(config)
    
    # Check if payer_id_to_patient_ids is empty
    if not payer_id_to_patient_ids:
        print("Error: Failed to load historical Carol's CSVs.")
        sys.exit(1)

    # Map Payer IDs to Insurance IDs
    for payer_id, patient_ids in payer_id_to_patient_ids.items():
        medisoft_ids = set()
        for patient_id in patient_ids:
            if patient_id in patient_id_to_insurance_id:
                medisoft_id = patient_id_to_insurance_id[patient_id]
                medisoft_ids.add(medisoft_id)
                MediLink_ConfigLoader.log("Added Medisoft ID {} for Patient ID {} and Payer ID {}".format(medisoft_id, patient_id, payer_id))
            else:
                MediLink_ConfigLoader.log("No matching Insurance ID found for Patient ID {}".format(patient_id))
        if medisoft_ids:
            payer_id_to_details[payer_id] = {
                "endpoint": "OPTUMEDI",  # TODO This should be determined via API or configured
                "medisoft_id": list(medisoft_ids)
            }
    
    # Update the crosswalk for payer IDs only, retaining other mappings
    crosswalk['payer_id'] = payer_id_to_details
    
    # Save the initial crosswalk
    save_crosswalk(config['MediLink_Config']['crosswalkPath'], crosswalk)

    MediLink_ConfigLoader.log("Crosswalk initialized with mappings for {} payers.".format(len(crosswalk.get('payer_id', {}))))
    
    # Return isn't really necessary since its just a one-off run from args.
    return payer_id_to_details

def crosswalk_update(config, crosswalk):
    """
    Updates the `crosswalk.json` file using mappings from MAINS, Z.dat, and Carol's CSV. This function integrates
    user-defined insurance mappings from Z.dat with existing payer-to-insurance mappings in the crosswalk, 
    and validates these mappings using MAINS.

    Steps:
    1. Load mappings from MAINS for translating insurance names to IDs.
    2. Load mappings from the latest Carol's CSV for new patient entries mapping Patient IDs to Payer IDs.
    3. Parse incremental data from Z.dat which contains recent user interactions mapping Patient IDs to Insurance Names.
    4. Update the crosswalk using the loaded and parsed data, ensuring each Payer ID maps to the correct Insurance IDs.
    5. Persist the updated mappings back to the crosswalk file.

    Args:
        config (dict): Configuration dictionary containing paths and other settings.
        crosswalk (dict): Existing crosswalk mapping Payer IDs to sets of Insurance IDs.

    Returns:
        bool: True if the crosswalk was successfully updated and saved, False otherwise.
        
    Example croswalk:
    {
        "payer_id": {
            "123456": {
                "endpoint": "OPTUMEDI",
                "medisoft_id": ["001", "002"]
            },
            "789012": {
                "endpoint": "AVAILITY",
                "medisoft_id": ["003"]
            },
            "345678": {
                "endpoint": "OPTUMEDI",
                "medisoft_id": ["004", "005", "006"]
            }
        },
        "mapat_mapping": {
            "slices": {
                "MAPATPXID": [195,200],
                "MAPATINID": [159,161],
                "MAPATINID2":[163,166]
            }
        },
        "mains_mapping": {
            "slices": {
                "MAINSNAME": [0,30],
                "MAINSADDR": [31,60]
            }
        }
    }

    """    
    # Load insurance mappings from MAINS (Insurance Name to Insurance ID)
    insurance_name_to_id = load_insurance_data_from_mains(config)
    MediLink_ConfigLoader.log("Loaded insurance data from MAINS...")
    
    # Load new Patient ID to Payer ID mappings from Carol's CSV (This is really just a performance increment)
    # patient_id_to_payer_id = load_patient_to_payer_mappings(config)
    
    # TODO this should work for now but can get bogged down in the futrue since we won't need very old CSVs for incremental changes.
    patient_id_to_payer_id = load_historical_payer_to_patient_mappings(config)
    MediLink_ConfigLoader.log("Loaded historical mappings...")
  
    # Load incremental mapping data from Z.dat (Patient ID to Insurance Name)
    # BUG Wouldn't the incremental information also be available in the latest MAPAT? Why do I need to wait until Z.dat to get the 
    # latest update? Seems slower since the initial saving of the patient goes into MAPAT anyway.
    patient_id_to_insurance_name = parse_z_dat(config['MediLink_Config']['Z_DAT_PATH'], config['MediLink_Config'])
    MediLink_ConfigLoader.log("Parsed Z data...")

    # Update the crosswalk with new or revised mappings
    for patient_id, payer_id in patient_id_to_payer_id.items():
        insurance_name = patient_id_to_insurance_name.get(patient_id)
        if insurance_name and insurance_name in insurance_name_to_id:
            insurance_id = insurance_name_to_id[insurance_name]

            # Ensure payer ID is in the crosswalk and initialize if not
            MediLink_ConfigLoader.log("Initializing payer_id key...")
            # BUG OPTUMEDI hardcode should be gathered via API
            if 'payer_id' not in crosswalk:
                crosswalk['payer_id'] = {}
            if payer_id not in crosswalk['payer_id']:
                crosswalk['payer_id'][payer_id] = {'endpoint': 'OPTUMEDI', 'medisoft_id': set()}

            # Update the medisoft_id set, temporarily using a set to avoid duplicates
            crosswalk['payer_id'][payer_id]['medisoft_id'].add(insurance_id)
            MediLink_ConfigLoader.log("Added new insurance ID {} to payer ID {}".format(insurance_id, payer_id))

    # Convert sets to lists just before saving
    for payer_id in crosswalk['payer_id']:
        if isinstance(crosswalk['payer_id'][payer_id]['medisoft_id'], set):
            crosswalk['payer_id'][payer_id]['medisoft_id'] = list(crosswalk['payer_id'][payer_id]['medisoft_id'])

    # Save the updated crosswalk to the specified file
    crosswalk_path = config['MediLink_Config'].get('crosswalkPath')
    if not save_crosswalk(crosswalk_path, crosswalk):
        return False

    return True

# CSV Preprocessor built for Carol
def preprocess_csv_data(csv_data):
    try:
        # Filter out rows without a Patient ID
        csv_data[:] = [row for row in csv_data if row.get('Patient ID', '').strip()]
        
        # Remove Patients (rows) that are Primary Insurance: 'AETNA', 'AETNA MEDICARE', or 'HUMANA MED HMO'.
        csv_data[:] = [row for row in csv_data if row.get('Primary Insurance', '').strip() not in ['AETNA', 'AETNA MEDICARE', 'HUMANA MED HMO']]
                
        # Convert 'Surgery Date' to datetime objects for sorting
        for row in csv_data:
            try:
                row['Surgery Date'] = datetime.strptime(row.get('Surgery Date', ''), '%m/%d/%Y')
            except ValueError:
                # Handle or log the error if the date is invalid
                row['Surgery Date'] = datetime.min  # Assign a minimum datetime value for sorting purposes

        # Initially sort the patients first by 'Surgery Date' and then by 'Patient Last' alphabetically
        csv_data.sort(key=lambda x: (x['Surgery Date'], x.get('Patient Last', '').strip()))
        
        # Deduplicate patient records based on Patient ID, keeping the entry with the earliest surgery date
        unique_patients = {}
        for row in csv_data:
            patient_id = row.get('Patient ID')
            if patient_id not in unique_patients or row['Surgery Date'] < unique_patients[patient_id]['Surgery Date']:
                unique_patients[patient_id] = row
        
        # Update csv_data to only include unique patient records
        csv_data[:] = list(unique_patients.values())

        # Re-sort the csv_data after deduplication to ensure correct order
        csv_data.sort(key=lambda x: (x['Surgery Date'], x.get('Patient Last', '').strip()))
        
        # Maybe make a dataformat_library function for this? csv_data = format_preprocessor(csv_data)?
        for row in csv_data:
            # Convert 'Surgery Date' back to string format if needed for further processing (cleanup)
            row['Surgery Date'] = row['Surgery Date'].strftime('%m/%d/%Y')
            
            # Combine name fields
            first_name = row.get('Patient First', '').strip()
            middle_name = row.get('Patient Middle', '').strip()
            last_name = row.get('Patient Last', '').strip()
            row['Patient Name'] = "{}, {} {}".format(last_name, first_name, middle_name).strip()

            # Combine address fields
            address1 = row.get('Patient Address1', '').strip()
            address2 = row.get('Patient Address2', '').strip()
            row['Patient Street'] = "{} {}".format(address1, address2).strip()
            
            # Probably make a data_format function for this:
            # Define the replacements as a dictionary
            replacements = {
                '777777777': '',  # Replace '777777777' with an empty string
                'RAILROAD MEDICARE': 'RAILROAD',  # Replace 'RAILROAD MEDICARE' with 'RAILROAD'
                'AARP MEDICARE COMPLETE': 'AARP COMPLETE'  # Replace 'AARP MEDICARE COMPLETE' with 'AARP COMPLETE'
            }

            # Iterate over each key-value pair in the replacements dictionary
            for old_value, new_value in replacements.items():
                # Replace the old value with the new value if it exists in the row
                if row.get('Patient SSN', '') == old_value:
                    row['Patient SSN'] = new_value
                elif row.get('Primary Insurance', '') == old_value:
                    row['Primary Insurance'] = new_value

    except Exception as e:
        print("An error occurred while pre-processing CSV data. Please repair the CSV directly and try again:", e)

def check_existing_patients(selected_patient_ids, MAPAT_MED_PATH):
    existing_patients = []
    patients_to_process = list(selected_patient_ids)  # Clone the selected patient IDs list

    try:
        with open(MAPAT_MED_PATH, 'r') as file:
            next(file)  # Skip header row
            for line in file:
                if line.startswith("0"): # 1 is a flag for a deleted record so it would need to be re-entered.
                    patient_id = line[194:202].strip()  # Extract Patient ID (Columns 195-202)
                    patient_name = line[9:39].strip()  # Extract Patient Name (Columns 10-39)
                    
                    if patient_id in selected_patient_ids:
                        existing_patients.append((patient_id, patient_name))
                        # Remove all occurrences of this patient_id from patients_to_process as a filter rather than .remove because 
                        # then it only makes one pass and removes the first instance.
    except FileNotFoundError:
        # Handle the case where MAPAT_MED_PATH is not found
        print("MAPAT.med was not found at location indicated in config file.")
        print("Skipping existing patient check and continuing...")
        
    # Filter out all instances of existing patient IDs
    patients_to_process = [id for id in patients_to_process if id not in [patient[0] for patient in existing_patients]]
    
    return existing_patients, patients_to_process

def intake_scan(csv_headers, field_mapping):
    identified_fields = OrderedDict()
    missing_fields_warnings = []
    required_fields = config["required_fields"]
    
    # Iterate over the Medisoft fields defined in field_mapping
    for medisoft_field in field_mapping.keys():
        for pattern in field_mapping[medisoft_field]:
            matched_headers = [header for header in csv_headers if re.search(pattern, header, re.IGNORECASE)]
            if matched_headers:
                # Assuming the first matched header is the desired one
                identified_fields[matched_headers[0]] = medisoft_field
                break
        else:
            # Check if the missing field is a required field before appending the warning
            if medisoft_field in required_fields:
                missing_fields_warnings.append("WARNING: No matching CSV header found for Medisoft field '{0}'".format(medisoft_field))
   
   #-----------------------
   # CSV Integrity Check
   #-----------------------
   
   # This section needs to be revamped further so that it can interpret the information from here and decide 
   # if it's significant or not.
   # e.g. If the 'Street' value:key is 'Address', then any warnings about City, State, Zip can be ignored. 
   # Insurance Policy Numbers should be all alphanumeric with no other characters. 
   # Make sure that the name field has at least one name under it (basically check for a blank or 
   # partially blank csv with just a header)
      
    # Display the identified fields and missing fields warnings
    #print("The following Medisoft fields have been identified in the CSV:\n")
    #for header, medisoft_field in identified_fields.items():
    #    print("{0} (CSV header: {1})".format(medisoft_field, header))
    
    #if missing_fields_warnings:
    #    print("\nSome required fields could not be matched:")
    #    for warning in missing_fields_warnings:
    #        print(warning)  

    #print("Debug - Identified fields mapping (intake scan):", identified_fields)
    return identified_fields

def main():
    parser = argparse.ArgumentParser(description='Run MediLink Data Management Tasks')
    parser.add_argument('--update-crosswalk', action='store_true',
                        help='Run the crosswalk update independently')
    parser.add_argument('--init-crosswalk', action='store_true',
                        help='Initialize the crosswalk using historical data from MAPAT and Carol’s CSV')
    parser.add_argument('--load-csv', action='store_true',
                        help='Load and process CSV data')
    parser.add_argument('--preprocess-csv', action='store_true',
                        help='Preprocess CSV data based on specific rules')
    parser.add_argument('--open-csv', action='store_true',
                        help='Open CSV for manual editing')

    args = parser.parse_args()

    if args.update_crosswalk:
        print("Updating the crosswalk...")
        crosswalk_update(config, crosswalk)

    if args.init_crosswalk:
        initialize_crosswalk_from_mapat(config, crosswalk)

    if args.load_csv:
        print("Loading CSV data...")
        csv_data = load_csv_data(config['CSV_FILE_PATH'])
        print("Loaded {} records from the CSV.".format(len(csv_data)))

    if args.preprocess_csv:
        if 'csv_data' in locals():
            print("Preprocessing CSV data...")
            preprocess_csv_data(csv_data)
        else:
            print("Error: CSV data needs to be loaded before preprocessing. Use --load-csv.")
    
    if args.open_csv:
        print("Opening CSV for editing...")
        open_csv_for_editing(config['CSV_FILE_PATH'])

if __name__ == '__main__':
    main()