import os
import pydicom
import pandas as pd
from typing import List, Tuple
import requests
from pydicom.errors import InvalidDicomError
from .components import OPVDicomSensitivity
from .dcm_defs import get_nema_opv_dicom
import numpy as np



class OPVDicom:
    """Class representing a single OPV DICOM file."""

    def __init__(self, ds: pydicom.dataset.FileDataset, filename: str = None):
        self.ds = ds
        self.nema_opv_dicom = get_nema_opv_dicom()
        self.filename = filename if filename else "[unnamed file]"

    def check_dicom_compliance(self):
        """
        Check the DICOM file for missing and incorrect tags, searching all nested elements.

        Returns:
        tuple: Two pandas DataFrames, one for missing tags and one for incorrect tags.
        """
        report = {"missing_tags": [], "incorrect_tags": []}

        def find_nested_tag(dataset, tag_tuple):
            """
            Recursively search for a tag in the dataset, including all nested sequences.
            """
            # Base case: If the tag exists in the current dataset
            if tag_tuple in dataset:
                return dataset[tag_tuple]

            # Recursive case: Search within sequences
            for element in dataset:
                if element.VR == "SQ":  # If the element is a sequence
                    for item in element.value:  # Iterate through sequence items
                        if isinstance(item, pydicom.dataset.Dataset):
                            result = find_nested_tag(item, tag_tuple)
                            if result:
                                return result
            return None

        try:
            for tag_str, tag_info in self.nema_opv_dicom.items():
                tag_tuple = tuple(int(part, 16) for part in tag_str.strip("()").split(","))
                element = find_nested_tag(self.ds, tag_tuple)

                # Check if the tag exists
                if element is None:
                    report["missing_tags"].append({
                            "tag": tag_str,
                            "name": tag_info["name"],
                            "description": tag_info["description"],
                            "type": tag_info["type"],
                        })
                else:
                    # Validate the value representation (VR)
                    if element.VR != tag_info["vr"]:
                        report["incorrect_tags"].append({
                            "tag": tag_str,
                            "name": tag_info["name"],
                            "description": tag_info["description"],
                            "expected_vr": tag_info["vr"],
                            "actual_vr": element.VR,
                        })

                    # Validate the value multiplicity (VM)
                    if isinstance(element.value, (list, tuple)):
                        if len(element.value) != int(tag_info["vm"]):
                            report["incorrect_tags"].append({
                                "tag": tag_str,
                                "name": tag_info["name"],
                                "description": tag_info["description"],
                                "error": f"Incorrect VM: {len(element.value)}, expected {tag_info['vm']}",
                            })

        except InvalidDicomError:
            return pd.DataFrame({"error": ["The provided file is not a valid DICOM file."]}), pd.DataFrame()
        except Exception as e:
            return pd.DataFrame({"error": [str(e)]}), pd.DataFrame()

        missing_tags_df = pd.DataFrame(report["missing_tags"])
        incorrect_tags_df = pd.DataFrame(report["incorrect_tags"])

        return missing_tags_df, incorrect_tags_df

    def to_pandas(self):
        # Initialize a list to hold all data elements
        df_list = []
        
        def process_element(element, parent_name=""):
            """
            Processes a single data element, appending it to the df_list. 
            If the element is a sequence, recursively processes its items.

            Parameters:
            element (DataElement): The DICOM data element to process.
            parent_name (str): Name of the parent element, used for nested sequences.
            """
            if isinstance(element, pydicom.dataelem.RawDataElement):
                element = pydicom.dataelem.DataElement_from_raw(element)
            
            element_name = f"{parent_name}.{element.name}" if parent_name else element.name
            df_list.append({'name': element_name, 'value': element.value})

            # Process nested sequences
            if isinstance(element.value, pydicom.sequence.Sequence):
                for idx, item in enumerate(element.value):
                    for nested_element in item:
                        process_element(nested_element, parent_name=element_name + f"[{idx}]")

        # Process each data element in the dataset
        for element in self.ds:
            process_element(element)
        
        # Create a DataFrame from the list of data elements
        df = pd.DataFrame(df_list)
        df.set_index('name', inplace=True)
        transpose_df = df.T
        # transpose_df = transpose_df.iloc[1:]

        return transpose_df
        

    
    def pointwise_to_pandas(self):
        
        # Initialize lists to store data
        person_id = self.ds.PatientID
        sop_instance_uid = self.ds.SOPInstanceUID
        study_instance_uid = self.ds.StudyInstanceUID
        laterality = self.ds[(0x0020, 0x0060)].value if (0x0020, 0x0060) in self.ds else self.ds[(0x0024, 0x0113)].value
        x_coords = []
        y_coords = []
        sensitivity_values = []
        stimulus_result = []
        # part of the sequence
        age_corrected_sensitivity_deviation_values = []
        age_corrected_sensitivity_deviation_probability_values = []
        generalized_defect_corrected_sensitivity_deviation_flag = []
        generalized_defect_corrected_sensitivity_values = []
        generalized_defect_corrected_sensitivity_probability_values = []
        
        # Iterate over the primary sequence
        for item in self.ds[(0x0024, 0x0089)].value:
            x_coords.append(item[(0x0024, 0x0090)].value)
            y_coords.append(item[(0x0024, 0x0091)].value)
            stimulus_result.append(item[(0x0024, 0x0093)].value)
            sensitivity_values.append(item[(0x0024, 0x0094)].value)

            # Access nested sequence
            nested_sequence = item[(0x0024, 0x0097)].value
            if nested_sequence:
                nested_item = nested_sequence[0]
                if (0x0024, 0x0092) in nested_item:
                    age_corrected_sensitivity_deviation_values.append(nested_item[(0x0024, 0x0092)].value)
                else:
                    age_corrected_sensitivity_deviation_values.append('NaN')
                if (0x0024, 0x0100) in nested_item:
                    age_corrected_sensitivity_deviation_probability_values.append(nested_item[(0x0024, 0x0100)].value)
                else:
                    age_corrected_sensitivity_deviation_probability_values.append('NaN')
                if (0x0024, 0x0102) in nested_item:
                    generalized_defect_corrected_sensitivity_deviation_flag.append(nested_item[(0x0024, 0x0102)].value)
                else:
                    generalized_defect_corrected_sensitivity_deviation_flag.append('NaN')
                if (0x0024, 0x0103) in nested_item:
                    generalized_defect_corrected_sensitivity_values.append(nested_item[(0x0024, 0x0103)].value)
                else:
                    generalized_defect_corrected_sensitivity_values.append('NaN')
                if (0x0024, 0x0104) in nested_item:
                    generalized_defect_corrected_sensitivity_probability_values.append(nested_item[(0x0024, 0x0104)].value)
                else:
                    generalized_defect_corrected_sensitivity_probability_values.append('NaN')
            else:
                age_corrected_sensitivity_deviation_values.append('NaN')
                age_corrected_sensitivity_deviation_probability_values.append('NaN')
                generalized_defect_corrected_sensitivity_deviation_flag.append('NaN')
                generalized_defect_corrected_sensitivity_values.append('NaN')
                generalized_defect_corrected_sensitivity_probability_values.append('NaN')
        # Creating a dataframe
        df = pd.DataFrame({'person_id': person_id, 'sop_instance_uid': sop_instance_uid, 'study_instance_uid':study_instance_uid, 'laterality': laterality, 'x_coords': x_coords, 'y_coords': y_coords, 'stimulus_result': stimulus_result ,'sensitivity_values': sensitivity_values,
                    'age_corrected_sensitivity_deviation_values': age_corrected_sensitivity_deviation_values,
                    'age_corrected_sensitivity_deviation_probability_values': age_corrected_sensitivity_deviation_probability_values,
                    'generalized_defect_corrected_sensitivity_deviation_flag': generalized_defect_corrected_sensitivity_deviation_flag,
                    'generalized_defect_corrected_sensitivity_values': generalized_defect_corrected_sensitivity_values,
                    'generalized_defect_corrected_sensitivity_probability_values': generalized_defect_corrected_sensitivity_probability_values})
        
        return df
    
    def pointwise_to_nested_json(self):        
            ds = self.ds
            # Initialize lists to store data
            person_id = ds.PatientID
            sop_instance_uid = ds.SOPInstanceUID
            study_instance_uid = ds.StudyInstanceUID
            laterality = ds[(0x0020, 0x0060)].value if (0x0020, 0x0060) in ds else ds[(0x0024, 0x0113)].value
            x_coords = []
            y_coords = []
            sensitivity_values = []
            stimulus_result = []
            # part of the sequence
            age_corrected_sensitivity_deviation_values = []
            age_corrected_sensitivity_deviation_probability_values = []
            generalized_defect_corrected_sensitivity_deviation_flag = []
            generalized_defect_corrected_sensitivity_values = []
            generalized_defect_corrected_sensitivity_probability_values = []
            
            # Iterate over the primary sequence
            for item in ds[(0x0024, 0x0089)].value:
                x_coords.append(item[(0x0024, 0x0090)].value)
                y_coords.append(item[(0x0024, 0x0091)].value)
                stimulus_result.append(item[(0x0024, 0x0093)].value)
                sensitivity_values.append(item[(0x0024, 0x0094)].value)

                # Access nested sequence
                nested_sequence = item[(0x0024, 0x0097)].value
                if nested_sequence:
                    nested_item = nested_sequence[0]
                    if (0x0024, 0x0092) in nested_item:
                        age_corrected_sensitivity_deviation_values.append(nested_item[(0x0024, 0x0092)].value)
                    else:
                        age_corrected_sensitivity_deviation_values.append('NaN')
                    if (0x0024, 0x0100) in nested_item:
                        age_corrected_sensitivity_deviation_probability_values.append(nested_item[(0x0024, 0x0100)].value)
                    else:
                        age_corrected_sensitivity_deviation_probability_values.append('NaN')
                    if (0x0024, 0x0102) in nested_item:
                        generalized_defect_corrected_sensitivity_deviation_flag.append(nested_item[(0x0024, 0x0102)].value)
                    else:
                        generalized_defect_corrected_sensitivity_deviation_flag.append('NaN')
                    if (0x0024, 0x0103) in nested_item:
                        generalized_defect_corrected_sensitivity_values.append(nested_item[(0x0024, 0x0103)].value)
                    else:
                        generalized_defect_corrected_sensitivity_values.append('NaN')
                    if (0x0024, 0x0104) in nested_item:
                        generalized_defect_corrected_sensitivity_probability_values.append(nested_item[(0x0024, 0x0104)].value)
                    else:
                        generalized_defect_corrected_sensitivity_probability_values.append('NaN')
                else:
                    age_corrected_sensitivity_deviation_values.append('NaN')
                    age_corrected_sensitivity_deviation_probability_values.append('NaN')
                    generalized_defect_corrected_sensitivity_deviation_flag.append('NaN')
                    generalized_defect_corrected_sensitivity_values.append('NaN')
                    generalized_defect_corrected_sensitivity_probability_values.append('NaN')
            # Creating a dataframe
            df = pd.DataFrame({'person_id': person_id, 'sop_instance_uid': sop_instance_uid,'study_instance_uid':study_instance_uid, 'laterality': laterality, 'x_coords': x_coords, 'y_coords': y_coords, 'stimulus_result': stimulus_result ,'sensitivity_values': sensitivity_values,
                        'age_corrected_sensitivity_deviation_values': age_corrected_sensitivity_deviation_values,
                        'age_corrected_sensitivity_deviation_probability_values': age_corrected_sensitivity_deviation_probability_values,
                        'generalized_defect_corrected_sensitivity_deviation_flag': generalized_defect_corrected_sensitivity_deviation_flag,
                        'generalized_defect_corrected_sensitivity_values': generalized_defect_corrected_sensitivity_values,
                        'generalized_defect_corrected_sensitivity_probability_values': generalized_defect_corrected_sensitivity_probability_values})
            result = {}
            for person_id, group in df.groupby('person_id'):
                result[person_id] = {}
                for laterality, sub_group in group.groupby('laterality'):
                    result[person_id][laterality] = {}
                    for sop_instance_uid, sub_sub_group in sub_group.groupby('sop_instance_uid'):
                        result[person_id][laterality][sop_instance_uid] = sub_sub_group.drop(['person_id', 'laterality', 'sop_instance_uid'], axis=1).to_dict(orient='records')
            return result

    

import pandas as pd
from typing import List

class OPVDicomSet:
    """Class representing a set of OPV DICOM files"""
    
    def __init__(self, opvdicoms: List[OPVDicom]):
        self.opvdicoms = opvdicoms
        self.nema_opv_dicom = get_nema_opv_dicom()

    def check_dicom_compliance(self) -> pd.DataFrame:
        """
        Check if the DICOM files contain all the required tags.
        Returns a DataFrame containing the missingness summary for each file.
        """
        # Get the dictionary of required tags from NEMA OPV DICOM definitions
        opv_dcm_dict = get_nema_opv_dicom()

        # Convert the nested dictionary to a DataFrame for easy filtering
        df = pd.DataFrame.from_dict(opv_dcm_dict, orient='index')

        # Filter the rows where the 'type' column contains '1' or '1C' (required or conditionally required)
        required_tags = df[df['type'].str.contains('1|1C', na=False)]

        # Get the total number of required tags for the calculations
        total_required_tags = len(required_tags)

        # Initialize an empty DataFrame to store missing tag information for each DICOM file
        missing_tags_df = pd.DataFrame(columns=[
            'File Name', 
            'Missing tags Count / Missing DICOM Meta Information Header', 
            'Number of Missing Required Tags', 
            'Percentage of Missing Required Tags'
        ])
        
        # Loop through each OPVDicom object in the provided list
        for opvdicom in self.opvdicoms:
            try:
                # Call the OPVDicom's check_dicom_compliance method to get missing tags for the file
                missing_tags_report, incorrect_tags_report = opvdicom.check_dicom_compliance()
                
                # Count the total number of missing tags
                missing_count = missing_tags_report.shape[0]
                
                # Find the number of missing required tags
                missing_required_count = missing_tags_report[missing_tags_report['tag'].isin(required_tags.index)].shape[0]
                
                # Calculate the percentage of missing required tags
                missing_required_percentage = round((missing_required_count / total_required_tags) * 100, 2) if total_required_tags > 0 else 0
                
                # Append the results for this file to the DataFrame
                missing_tags_df = pd.concat([missing_tags_df, pd.DataFrame({
                    'File Name': [opvdicom.filename], 
                    'Missing tags Count / Missing DICOM Meta Information Header': [missing_count], 
                    'Number of Missing Required Tags': [missing_required_count], 
                    'Percentage of Missing Required Tags': [missing_required_percentage]
                })], ignore_index=True)
            except pydicom.errors.InvalidDicomError:
                # If the file is missing the DICOM meta-information header, we assume all required tags are missing
                missing_required_percentage = 100  # All tags are missing in this case
                
                # Append the error results to the DataFrame with 100% missing tags
                missing_tags_df = pd.concat([missing_tags_df, pd.DataFrame({
                    'File Name': [opvdicom.filename], 
                    'Missing tags Count / Missing DICOM Meta Information Header': ['File is missing DICOM Meta Information Header'], 
                    'Number of Missing Required Tags': [total_required_tags],  # All required tags are missing
                    'Percentage of Missing Required Tags': [missing_required_percentage]
                })], ignore_index=True)
            except Exception as e:
                # In case of other errors, calculate the number of missing required tags as all missing
                missing_required_percentage = 100  # Assume all tags are missing in case of an error
                
                # Append the error results to the DataFrame
                missing_tags_df = pd.concat([missing_tags_df, pd.DataFrame({
                    'File Name': [opvdicom.filename], 
                    'Missing tags Count / Missing DICOM Meta Information Header': [str(e)], 
                    'Number of Missing Required Tags': [total_required_tags],  # All required tags are missing
                    'Percentage of Missing Required Tags': [missing_required_percentage]
                })], ignore_index=True)

        return missing_tags_df
    
    def to_pandas(self):
        """Convert the OPV DICOM files to a single Pandas DataFrame containing the extracted data, handling duplicate column names"""
        
        error_files = []  # List to store files with errors
        data_frames = []  # List to store DataFrames
        
        def make_columns_unique(df):
            """Ensure that the DataFrame has unique column names by adding suffixes to duplicates"""
            cols = pd.Series(df.columns)
            
            # Find duplicates and append a suffix to make them unique
            for dup in cols[cols.duplicated()].unique():
                # Create a suffix iterator to append '_1', '_2', etc.
                dup_count = cols[cols == dup].index
                for i, idx in enumerate(dup_count):
                    if i == 0:
                        continue  # Keep the first occurrence as is
                    cols[idx] = f"{dup}_{i+1}"  # Rename subsequent duplicates with suffix
            
            df.columns = cols  # Assign back the modified column names
            return df
        
        all_columns = set()  # Collect the union of all column names
        
        for opvdicom in self.opvdicoms:
            try:
                # Convert individual DICOM to DataFrame, reset the index, and ensure unique column names
                df = opvdicom.to_pandas().reset_index(drop=True)
                df = make_columns_unique(df)  # Ensure columns are unique
                
                # Update the set of all columns
                all_columns.update(df.columns)
                
                data_frames.append(df)
            
            except Exception as e:
                # Record the file name and error message in case of failure
                error_files.append({'file_name': opvdicom.filename, 'error': str(e)})
                continue
        
        # Reindex all DataFrames to match the union of all columns, filling missing ones with NaN
        all_columns = list(all_columns)  # Convert to list for consistent ordering
        
        if data_frames:
            data_frames = [df.reindex(columns=all_columns, fill_value=np.nan) for df in data_frames]
            result_df = pd.concat(data_frames, ignore_index=True)
        else:
            result_df = pd.DataFrame(columns=all_columns)  # Empty DataFrame with all possible columns
        
        # Create a DataFrame for error files, even if no errors occurred
        error_df = pd.DataFrame(error_files, columns=['file_name', 'error'])
        
        return result_df, error_df




    def pointwise_to_pandas(self):
        """Convert the OPV DICOM files to a single Pandas DataFrame containing the extracted data"""

        # Get all DICOM files in the directory
        error_files = []

        # Initialize lists to store data
        data_frames = []
        
        for opvdicom in self.opvdicoms:
            try:
                # Append DataFrame to the list
                data_frames.append(opvdicom.pointwise_to_pandas())
            
            except Exception as e:
                error_files.append({'file_name': opvdicom.filename, 'error': str(e)})
                continue
        
        # Concatenate all DataFrames into a single one
        result_df = pd.concat(data_frames, ignore_index=True)
        
        # Create a DataFrame for error files
        error_df = pd.DataFrame(error_files)
        
        return result_df, error_df
    
    def opvdicoms_pointwise_to_nested_json(self):
        """Convert the OPV DICOM files to a nested JSON structure"""      
        nested_json = {}
        def pointwise_to_nested_json(self):        
            ds = self.ds
            # Initialize lists to store data
            person_id = ds.PatientID
            sop_instance_uid = ds.SOPInstanceUID
            study_instance_uid = ds.StudyInstanceUID
            laterality = ds[(0x0020, 0x0060)].value if (0x0020, 0x0060) in ds else ds[(0x0024, 0x0113)].value
            x_coords = []
            y_coords = []
            sensitivity_values = []
            stimulus_result = []
            # part of the sequence
            age_corrected_sensitivity_deviation_values = []
            age_corrected_sensitivity_deviation_probability_values = []
            generalized_defect_corrected_sensitivity_deviation_flag = []
            generalized_defect_corrected_sensitivity_values = []
            generalized_defect_corrected_sensitivity_probability_values = []
            
            # Iterate over the primary sequence
            for item in ds[(0x0024, 0x0089)].value:
                x_coords.append(item[(0x0024, 0x0090)].value)
                y_coords.append(item[(0x0024, 0x0091)].value)
                stimulus_result.append(item[(0x0024, 0x0093)].value)
                sensitivity_values.append(item[(0x0024, 0x0094)].value)

                # Access nested sequence
                nested_sequence = item[(0x0024, 0x0097)].value
                if nested_sequence:
                    nested_item = nested_sequence[0]
                    if (0x0024, 0x0092) in nested_item:
                        age_corrected_sensitivity_deviation_values.append(nested_item[(0x0024, 0x0092)].value)
                    else:
                        age_corrected_sensitivity_deviation_values.append('NaN')
                    if (0x0024, 0x0100) in nested_item:
                        age_corrected_sensitivity_deviation_probability_values.append(nested_item[(0x0024, 0x0100)].value)
                    else:
                        age_corrected_sensitivity_deviation_probability_values.append('NaN')
                    if (0x0024, 0x0102) in nested_item:
                        generalized_defect_corrected_sensitivity_deviation_flag.append(nested_item[(0x0024, 0x0102)].value)
                    else:
                        generalized_defect_corrected_sensitivity_deviation_flag.append('NaN')
                    if (0x0024, 0x0103) in nested_item:
                        generalized_defect_corrected_sensitivity_values.append(nested_item[(0x0024, 0x0103)].value)
                    else:
                        generalized_defect_corrected_sensitivity_values.append('NaN')
                    if (0x0024, 0x0104) in nested_item:
                        generalized_defect_corrected_sensitivity_probability_values.append(nested_item[(0x0024, 0x0104)].value)
                    else:
                        generalized_defect_corrected_sensitivity_probability_values.append('NaN')
                else:
                    age_corrected_sensitivity_deviation_values.append('NaN')
                    age_corrected_sensitivity_deviation_probability_values.append('NaN')
                    generalized_defect_corrected_sensitivity_deviation_flag.append('NaN')
                    generalized_defect_corrected_sensitivity_values.append('NaN')
                    generalized_defect_corrected_sensitivity_probability_values.append('NaN')
            # Creating a dataframe
            df = pd.DataFrame({'person_id': person_id, 'sop_instance_uid': sop_instance_uid,'study_instance_uid':study_instance_uid, 'laterality': laterality, 'x_coords': x_coords, 'y_coords': y_coords, 'stimulus_result': stimulus_result ,'sensitivity_values': sensitivity_values,
                        'age_corrected_sensitivity_deviation_values': age_corrected_sensitivity_deviation_values,
                        'age_corrected_sensitivity_deviation_probability_values': age_corrected_sensitivity_deviation_probability_values,
                        'generalized_defect_corrected_sensitivity_deviation_flag': generalized_defect_corrected_sensitivity_deviation_flag,
                        'generalized_defect_corrected_sensitivity_values': generalized_defect_corrected_sensitivity_values,
                        'generalized_defect_corrected_sensitivity_probability_values': generalized_defect_corrected_sensitivity_probability_values})
            result = {}
            for person_id, group in df.groupby('person_id'):
                result[person_id] = {}
                for laterality, sub_group in group.groupby('laterality'):
                    result[person_id][laterality] = {}
                    for sop_instance_uid, sub_sub_group in sub_group.groupby('sop_instance_uid'):
                        result[person_id][laterality][sop_instance_uid] = sub_sub_group.drop(['person_id', 'laterality', 'sop_instance_uid'], axis=1).to_dict(orient='records')
            return result
        for opvdicom in self.opvdicoms:
            try:
                json_output = pointwise_to_nested_json(opvdicom)
                # Extract the first key from the JSON output
                first_key = list(json_output.keys())[0]
                # Use the first key as the key in the resulting JSON
                nested_json[first_key] = json_output[first_key]
            except Exception as e:
                print(f"Error processing file {opvdicom.filename}: {e}")
        
        return nested_json
