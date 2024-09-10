
import pandas as pd
import pydicom

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
                # Convert tag to a format that can be used to access elements directly
                tag_group, tag_element = row['tag'].strip('()').split(', ')
                tag_tuple = (int(tag_group, 16), int(tag_element, 16))
                
                # Access the tag in the DICOM dataset
                if tag_tuple not in self.ds:
                    # Create a DataFrame for the missing tag row
                    new_row_df = pd.DataFrame([row])
                    
                    # Filter out empty or all-NA rows before concatenation
                    if not new_row_df.empty and not new_row_df.isna().all(axis=None):
                        missing_tags = pd.concat([missing_tags, new_row_df], ignore_index=True)
            except Exception as e:
                print(f"Error processing tag {row['tag']}: {e}")

        # Return the count of missing tags and the DataFrame of missing tags
        return len(missing_tags), missing_tags