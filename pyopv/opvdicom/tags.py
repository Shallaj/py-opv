
import pandas as pd

def check_missing_ags(dicom_file_path: str) -> tuple:
    # Read the required tags from nema_opv_dicom.csv and store them in a DataFrame
    nema_opv_dicom = pd.read_csv('qc/opv_dcm.csv')
    
    # Read the DICOM file
    ds = pydicom.dcmread(dicom_file_path)
    
    # Check if the SOP Class UID is correct
    if ds.SOPClassUID != '1.2.840.10008.5.1.4.1.1.80.1':
        print(f'SOP Class UID is incorrect in {dicom_file_path}: {ds.SOPClassUID}')
        print(f'Expected SOP Class UID: 1.2.840.10008.5.1.4.1.1.80.1')

    # Store the complete ds as a string in a variable
    ds_str = str(ds)
    
    # Initialize an empty DataFrame to store missing tags
    missing_tags = pd.DataFrame(columns=nema_opv_dicom.columns)
   
    # Check if each tag in nema_opv_dicom is present in ds_str
    for _, row in nema_opv_dicom.iterrows():
        if row['tag'] not in ds_str:
            missing_tags = pd.concat([missing_tags, pd.DataFrame([row])], ignore_index=True)
    
    # Return the count of missing tags and the DataFrame of missing tags
    return len(missing_tags), missing_tags