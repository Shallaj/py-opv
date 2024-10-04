import os
import pydicom
import pandas as pd
from typing import List, Tuple
import requests
from pydicom.errors import InvalidDicomError
from .components import OPVDicomSensitivity
from .dcm_defs import get_nema_opv_dicom

class OPVDicom:
    """Class representing a single OPV DICOM file"""

    def __init__(self, ds: pydicom.dataset.FileDataset, filename: str = None):
        self.ds = ds
        self.nema_opv_dicom = get_nema_opv_dicom()  # Assuming this function provides the DICOM tag dictionary
        self.filename = filename if filename is not None else '[unnamed file]'

    def check_dicom_compliance(self):
        """
        Check the DICOM file for missing and incorrect tags from the instance's dataset.

        Returns:
        tuple: Two pandas DataFrames, one for missing tags and one for incorrect tags.
        """
        report = {"missing_tags": [], "incorrect_tags": []}

        try:
            # Iterate through the expected tags in the dictionary
            for tag_str, tag_info in self.nema_opv_dicom.items():
                tag_tuple = tuple(int(part, 16) for part in tag_str.strip("()").split(","))
                
                # Check if the tag is present in the DICOM dataset
                if tag_tuple not in self.ds:
                    tag_info['tag'] = tag_str
                    report["missing_tags"].append(tag_info)
                else:
                    # Validate the tag's value representation (vr)
                    element = self.ds[tag_tuple]
                    if element.VR != tag_info["vr"]:
                        report["incorrect_tags"].append({
                            "tag": tag_str,
                            "name": tag_info["name"],
                            "expected_vr": tag_info["vr"],
                            "actual_vr": element.VR,
                            "description": tag_info["description"]
                        })

                    # Check the value multiplicity (vm), only for list-like objects
                    if tag_info["vm"] and isinstance(element.value, (list, tuple)):
                        if len(element.value) != int(tag_info["vm"]):
                            report["incorrect_tags"].append({
                                "tag": tag_str,
                                "name": tag_info["name"],
                                "error": f"Incorrect VM: {len(element.value)}, expected {tag_info['vm']}",
                                "description": tag_info["description"]
                            })

        except InvalidDicomError:
            return pd.DataFrame({"error": ["The provided file is not a valid DICOM file."]})
        except Exception as e:
            return pd.DataFrame({"error": [str(e)]})

        # Convert missing tags to DataFrame with all details
        missing_tags_df = pd.DataFrame(report["missing_tags"])

        # Convert incorrect tags to DataFrame
        incorrect_tags_df = pd.DataFrame(report["incorrect_tags"])

        return missing_tags_df, incorrect_tags_df

    
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