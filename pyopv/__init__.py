from typing import List
import pydicom
import os
import requests
import pandas as pd
from pydicom.dataelem import DataElement_from_raw
from pydicom.dataelem import RawDataElement
from pydicom.sequence import Sequence

from .opvdicom import OPVDicom, OPVDicomSet

def read_dicom(path: str) -> OPVDicom:
    """Read a single DICOM file and return a PyOPVDicom object"""

    ds = pydicom.dcmread(path)

    assert isinstance(ds, pydicom.dataset.FileDataset), f"Expected pydicom.dataset.FileDataset, got {type(ds)}"

    return OPVDicom(ds, filename=path.split('/')[-1])

def read_dicom_directory(directory: str, file_extension: str = '') -> OPVDicomSet:
    """Read a directory of DICOM files and return a list of PyOPVDicom objects"""

    opvdicoms = []

    # Loop through each . file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(file_extension):
            file_path = os.path.join(directory, filename)
            opvdicom = read_dicom(file_path)
            opvdicoms.append(opvdicom)

    return OPVDicomSet(opvdicoms)

def refresh_dicom_definitions() -> None:
    """Refresh the DICOM definitions used by PyOPV"""

    pass

def get_dicom_standard():
        # getting most recent version of the parsed DICOM standard
        attributes = requests.get('https://raw.githubusercontent.com/innolitics/dicom-standard/master/standard/attributes.json').json()
        sops = requests.get('https://raw.githubusercontent.com/innolitics/dicom-standard/master/standard/sops.json').json()
        ciod_to_func_group_macros = requests.get('https://raw.githubusercontent.com/innolitics/dicom-standard/master/standard/ciod_to_func_group_macros.json').json()
        ciod_to_modules = requests.get('https://raw.githubusercontent.com/innolitics/dicom-standard/master/standard/ciod_to_modules.json').json()
        ciods = requests.get('https://raw.githubusercontent.com/innolitics/dicom-standard/master/standard/ciods.json').json()
        macros = requests.get('https://raw.githubusercontent.com/innolitics/dicom-standard/master/standard/macros.json').json()
        macro_to_attributes = requests.get('https://raw.githubusercontent.com/innolitics/dicom-standard/master/standard/macro_to_attributes.json').json()
        modules = requests.get('https://raw.githubusercontent.com/innolitics/dicom-standard/master/standard/modules.json').json()
        module_to_attributes = requests.get('https://raw.githubusercontent.com/innolitics/dicom-standard/master/standard/module_to_attributes.json').json()

        print('Up to date DICOM standard json files successfully extracted.')

        # converting json to df
        sops_df = pd.DataFrame(sops)
        ciod_to_func_group_mactros_df = pd.DataFrame(ciod_to_func_group_macros)
        ciod_to_modules_df = pd.DataFrame(ciod_to_modules)
        ciods_df = pd.DataFrame(ciods)
        macros_df = pd.DataFrame(macros)
        macro_to_attributes_df = pd.DataFrame(macro_to_attributes)
        modules_df = pd.DataFrame(modules)
        module_to_attributes_df = pd.DataFrame(module_to_attributes)
        attributes_df = pd.DataFrame(attributes)


        # find Ophthalmic Visual Field Static Perimetry Measurements in coids_df
        opv_ciod = ciods_df[ciods_df['id'] == 'ophthalmic-visual-field-static-perimetry-measurements']
        opv_ciod_to_modules = ciod_to_modules_df[ciod_to_modules_df['ciodId'] == opv_ciod['id'].values[0]]
        opv_ciod_to_macros = ciod_to_func_group_mactros_df[ciod_to_func_group_mactros_df['ciodId'] == opv_ciod['id'].values[0]]
        opv_modules = modules_df[modules_df['id'].isin(opv_ciod_to_modules['moduleId'])]
        opv_module_to_attributes = module_to_attributes_df[module_to_attributes_df['moduleId'].isin(opv_modules['id'])]
        opv_macros_to_attributes = macro_to_attributes_df[macro_to_attributes_df['macroId'].isin(opv_ciod_to_macros['macroId'])]
        opv_attributes = attributes_df[attributes_df['tag'].isin(opv_module_to_attributes['tag']) | attributes_df['tag'].isin(opv_macros_to_attributes['tag'])]

        print('Up to date DICOM attributes successfully extracted for CIOD: ophthalmic-visual-field-static-perimetry-measurements.')
        # write opv_attributes to a csv file
        opv_attributes.to_csv('ophthalmic-visual-field-static-perimetry-measurements.csv', index=False)
        print('Up to date DICOM attributes successfully written to /ophthalmic-visual-field-static-perimetry-measurements.csv.')
        print('Headers:')
        print(opv_attributes.head())

def pointwise_to_nested_json(file_path):        
        ds=pydicom.dcmread(file_path)
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


def opvdicoms_pointwise_to_nested_json(directory_path):
    dicom_files = []
    file_names = []
    file_paths = []
    
    # Iterate through the files in the specified directory
    for file in os.listdir(directory_path):
        if file.endswith('.dcm'):
            try:
                dicom_file = pydicom.dcmread(os.path.join(directory_path, file))
                # If the file doesn't have necessary DICOM header attributes, an exception will be raised
                dicom_files.append(dicom_file)
                file_names.append(file)
                file_paths.append(os.path.join(directory_path, file))
            except Exception as e:
                print(f"Skipping file {file} due to error: {e}")
    
    nested_json = {}
    for i in range(len(dicom_files)):
        try:
            json_output = pointwise_to_nested_json(file_paths[i])
            # Extract the first key from the JSON output
            first_key = list(json_output.keys())[0]
            # Use the first key as the key in the resulting JSON
            nested_json[first_key] = json_output[first_key]
        except Exception as e:
            print(f"Error processing file {file_paths[i]}: {e}")
    
    return nested_json

def dicom_to_dataframe(file_path):
    """
    Reads a DICOM file and converts it to a Pandas DataFrame with 'name' and 'value' columns,
    including nested tags.

    Parameters:
    file_path (str): The path to the DICOM file.

    Returns:
    pd.DataFrame: A DataFrame with DICOM data elements' names and values, including nested tags.
    """
    def process_element(element, df_list):
        """
        Processes a single data element, appending it to the df_list. If the element is a sequence,
        recursively processes its items.

        Parameters:
        element (DataElement): The DICOM data element to process.
        df_list (list): The list to append processed data elements to.
        """
        if isinstance(element, RawDataElement):
            element = DataElement_from_raw(element)
        df_list.append({'name': element.name, 'value': element.value})

        if isinstance(element.value, Sequence):
            for item in element.value:
                for nested_element in item:
                    process_element(nested_element, df_list)

    # Read the DICOM file
    ds = pydicom.dcmread(file_path)

    # Initialize a list to hold all data elements
    df_list = []

    # Process each data element in the dataset
    for element in ds:
        process_element(element, df_list)

    # Create a DataFrame from the list of data elements
    df = pd.DataFrame(df_list)
    transpose_df = df.T
    return transpose_df




