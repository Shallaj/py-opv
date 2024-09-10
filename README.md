# PyOPV

This package provides functionality for working with the OPV DICOM files provided by various vendors.

## Installation

TODO: Instructions for installing from GitHub / PyPi

```python
import pyopv
```

## Example usage

Loading files

```python
m_opvdicom = pyopv.read_dicom('data/example_opv.dcm')   # Loads one file
m_opvdicoms = pyopv.read_dicom_directory('data')        # Load all files in directory
```

Checking missing tags
```python
missing_count, missingtag_df = m_opvdicom.check_missing_tags()
```

Getting pointwise data

```python
pointwise_data = m_opvdicom.to_pandas()
```

## Contact

Email: shallaj\[at\]health.ucsd.edu
