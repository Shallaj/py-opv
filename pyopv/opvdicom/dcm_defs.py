import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

def get_nema_opv_dicom():
    # Path to a file located in a "data" subdirectory of the script's directory
    data_file_path = os.path.join(script_dir, 'data', 'opv_dcm.csv')

    return pd.read_csv(data_file_path)