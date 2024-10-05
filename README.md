
# PyOPV

This package provides functionality for working with the OPV DICOM files provided by various vendors. The package facilitates reading, analyzing, and processing these DICOM files for compliance and data extraction. The primary use case is for handling ophthalmology visual field-related DICOM files and ensuring they meet the latest DICOM standards.

## Installation

1. Install the package from PyPi:

```bash
pip install pyopv
```

Once installed, you can import the package and use its various utilities for DICOM file processing:

```python
import pyopv
```

## Working with PyOPV

### Sample Code Snippet for Processing DICOM Files:

To begin processing, you'll first need the latest SAP DICOM standard. This standard is updated regularly to ensure compliance with industry norms. The package allows you to download the latest version of the SAP DICOM standard in CSV format. Here's a simple example:

```python
from pyopv import get_dicom_standard

# Download and save the latest DICOM standard
get_dicom_standard() # This will create a CSV file in the current working directory
```

### Processing a Single File:

Here’s how you can process a single DICOM file to check compliance and extract relevant data:

```python
# Define the path to the DICOM file
file_path = '/path/to/your/dicom/file'

# Read the DICOM file using PyOPV
m_opvdicom = pyopv.read_dicom(file_path)

# Check if the file meets the DICOM compliance standards
missing_tags_df, incorrect_tags_df = m_opvdicom.check_dicom_compliance()

# Display missing and incorrect tags
display(missing_tags_df)
display(incorrect_tags_df)

# Convert the DICOM data to a pandas DataFrame for further analysis
m_opvdicom_df = m_opvdicom.to_pandas()
display(m_opvdicom_df)

# Extract pointwise data from the DICOM file and convert it to a pandas DataFrame
pointwise_data = m_opvdicom.pointwise_to_pandas()
display(pointwise_data)

# Alternatively, save the pointwise data as a nested JSON structure for more flexible use cases
pointwise_data_json = m_opvdicom.pointwise_to_nested_json()
```

### Bulk Processing OPV DICOM Files:

For scenarios where you need to process multiple DICOM files from a directory, PyOPV provides an efficient bulk processing capability. Here's how to do it:

```python
# Import the necessary class for handling multiple DICOM files
from pyopv import OPVDicomSet

# Specify the directory containing your DICOM files
dicom_directory = '/path/to/your/dicom/files'

# Read all the DICOM files in the specified directory
m_opvdicoms, errors = pyopv.read_dicom_directory(dicom_directory, file_extension='dcm')

# Check for missing tags across all files in the directory
missingtags_df = m_opvdicoms.check_dicom_compliance()
display(missingtags_df)

# Convert all DICOM files to pandas DataFrames, returning a wide DataFrame for analysis
result_df, error_df = m_opvdicoms.to_pandas()
display(result_df)
display(error_df)

# Similarly, extract pointwise data from all files in the directory and convert to DataFrames
pointwise_data, error_df = m_opvdicoms.pointwise_to_pandas()
display(pointwise_data)
display(error_df)

# Optionally, save the pointwise data into a nested JSON structure for each file
nested_json = m_opvdicoms.opvdicoms_pointwise_to_nested_json()
```

With these utilities, PyOPV makes it easy to handle large-scale DICOM datasets while ensuring compliance with industry standards. The ability to extract, analyze, and convert data into user-friendly formats like CSV, pandas DataFrames, and JSON structures helps streamline the workflow for researchers and clinicians working with ophthalmic imaging data.
