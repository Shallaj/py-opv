import os
import pydicom
import pandas as pd
from typing import List, Tuple
import requests

from .components import OPVDicomSensitivity
from .dcm_defs import get_nema_opv_dicom

class OPVDicom:
    """Class representing a single OPV DICOM file"""

    def __init__(self, ds: pydicom.dataset.FileDataset, filename: str = None):
        self.ds = pydicom.dcmread(self)
        self.nema_opv_dicom = get_nema_opv_dicom()
        self.filename = filename if filename is not None else '[unnamed file]'

    def check_missing_tags(self) -> Tuple[int, pd.DataFrame]:
        """Check if the DICOM file contains all the required tags, returns number of missing tags and dataframe containing missing tags"""

        # Check if the SOP Class UID is correct
        if self.ds.SOPClassUID != '1.2.840.10008.5.1.4.1.1.80.1':
            print(f'SOP Class UID is incorrect in {self.filename}: {self.ds.SOPClassUID}')
            print(f'Expected SOP Class UID: 1.2.840.10008.5.1.4.1.1.80.1')

            # Initialize an empty DataFrame to store missing tags
            missing_tags = pd.DataFrame(columns=self.nema_opv_dicom.columns)

            # Check if each tag in nema_opv_dicom is present in the DICOM dataset
            for _, row in self.nema_opv_dicom.iterrows():
                try:
                    # Convert self.ds to a string
                    ds_str = str(self.ds)
                    tag = row['tag']

                    # search the long ds_str for the exact tag
                    if tag not in ds_str:
                        missing_tags = missing_tags.append(row)

                except ValueError as ve:
                    print(f"Tag parsing error for {row['tag']}: {ve}")
                except KeyError:
                    print(f"Tag not found: {row['tag']}")
                except Exception as e:
                    print(f"Error processing tag {row['tag']}: {e}")

        # Return the count of missing tags and the DataFrame of missing tags
        return len(missing_tags), missing_tags



    def as_dict(self) -> dict:
        return {
            'status': 'not implemented'
        }
    
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

class OPVDicomSet:
    """Class representing a set of OPV DICOM files"""
    
    def __init__(self, opvdicoms: List[OPVDicom]):
        self.opvdicoms = opvdicoms
        self.nema_opv_dicom = get_nema_opv_dicom()
        pass

    def check_missing_tags(self) -> pd.DataFrame:
        """Check if the DICOM files contain all the required tags, returns Dataframe containing missingness summary for each file"""
        # Filter the required tags (type contains 1)
        required_tags = self.nema_opv_dicom[self.nema_opv_dicom['type'].astype(str).str.contains('1')]['tag'].tolist()

        # Create an empty DataFrame to store the number of missing tags for each File Name
        missing_tags_df = pd.DataFrame(columns=['File Name', 'Missing tags Count / Missing DICOM Meta Information Header', 'Number of Missing Required Tags', 'Percentage of Missing Required Tags'])
        
        # Loop through each .dcm file in the directory
        for opvdicom in self.opvdicoms:
            try:
                # Get the count and list of missing tags
                missing_count, missing_tags_report = opvdicom.check_missing_tags()
                
                # Find the missing required tags
                missing_required_count = missing_tags_report[missing_tags_report['tag'].isin(required_tags)].shape[0]
                
                # Calculate the percentage of missing required tags
                if len(required_tags) > 0:
                    missing_required_percentage = round((missing_required_count / len(required_tags)) * 100, 0)
                else:
                    missing_required_percentage = 0
                
                # Append the results to the DataFrame
                missing_tags_df = pd.concat([missing_tags_df, pd.DataFrame({'File Name': [opvdicom.filename], 
                                                        'Missing tags Count / Missing DICOM Meta Information Header': [missing_count], 
                                                        'Number of Missing Required Tags': [missing_required_count], 
                                                        'Percentage of Missing Required Tags': [missing_required_percentage]})], ignore_index=True)
            except pydicom.errors.InvalidDicomError:
                # Handle the case where DICOM file is missing meta-information header
                missing_tags_df = pd.concat([missing_tags_df, pd.DataFrame({'File Name': [opvdicom.filename], 
                                                        'Missing tags Count / Missing DICOM Meta Information Header': ['File is missing DICOM Meta Information Header'], 
                                                        'Number of Missing Required Tags': [None], 
                                                        'Percentage of Missing Required Tags': [None]})], ignore_index=True)
            except Exception as e:
                # Handle any other exceptions
                missing_tags_df = pd.concat([missing_tags_df, pd.DataFrame({'File Name': [opvdicom.filename], 
                                                        'Missing tags Count / Missing DICOM Meta Information Header': [str(e)], 
                                                        'Number of Missing Required Tags': [None], 
                                                        'Percentage of Missing Required Tags': [None]})], ignore_index=True)
        
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