import pandas as pd

def get_nema_opv_dicom():
   opv_dcm_dict = {
        "(0024, 0306)": {
            "name": "DataSetName",
            "description": "The name assigned to the data set.",
            "type": "1",
            "vm": 1.0,
            "vr": "LO"
        },
        "(0024, 0307)": {
            "name": "DataSetVersion",
            "description": "The software version identifier assigned to the data set.",
            "type": "1",
            "vm": 1.0,
            "vr": "LO"
        },
        "(0024, 0308)": {
            "name": "DataSetSource",
            "description": "Source of the data set e.g. the name of the manufacturer, researcher, university, etc.",
            "type": "1",
            "vm": 1.0,
            "vr": "LO"
        },
        "(0024, 0309)": {
            "name": "DataSetDescription",
            "description": "Description of the data set.",
            "type": "3",
            "vm": 1.0,
            "vr": "LO"
        },
        "(0066, 002F)": {
            "name": "AlgorithmFamilyCodeSequence",
            "description": "The family of algorithm(s) that best describes the software algorithm used. \nOnly one item shall be permitted in the sequence.",
            "type": "1",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0066, 0030)": {
            "name": "AlgorithmNameCodeSequence",
            "description": "The code assigned by a manufacturer to a specific software algorithm. \nOnly one item shall be permitted in the sequence.",
            "type": "3",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0066, 0036)": {
            "name": "AlgorithmName",
            "description": "The name assigned by a manufacturer to a specific software algorithm.",
            "type": "1",
            "vm": 1.0,
            "vr": "LO"
        },
        "(0066, 0031)": {
            "name": "AlgorithmVersion",
            "description": "The software version identifier assigned by a manufacturer to a specific software algorithm.",
            "type": "1",
            "vm": 1.0,
            "vr": "LO"
        },
        "(0066, 0032)": {
            "name": "AlgorithmParameters",
            "description": "The input parameters used by a manufacturer to configure the behavior of a specific software algorithm.",
            "type": "3",
            "vm": 1.0,
            "vr": "LT"
        },
        "(0024, 0202)": {
            "name": "AlgorithmSource",
            "description": "Source of the algorithm, e.g., the name of the manufacturer, researcher, university, etc.",
            "type": "3",
            "vm": 1.0,
            "vr": "LO"
        },
        "(0020, 0060)": {
            "name": "Laterality",
            "description": "Laterality of (paired) body part examined. Required if the body part examined is a paired structure and Image Laterality (0020, 0062) or Frame Laterality (0020, 9072) are not sent. Enumerated Values:\nR = right\nL = left\nNote: Some IODs support Image Laterality (0020, 0062) at the Image level or Frame Laterality (0020, 9072) at the Frame level in the Frame Anatomy functional group macro or Measurement Laterality (0024, 0113) at the Measurement level, which can provide a more comprehensive mechanism for specifying the laterality of the body part(s) being examined.",
            "type": "2C",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0008, 0060)": {
            "name": "Modality",
            "description": "Type of equipment that originally acquired the data used to create the measurements in this Series.\nEnumerated Values:\nOPV\nSee section C.7.3.1.1.1 for further explanation.",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0008, 1111)": {
            "name": "ReferencedPerformedProcedureStepSequence",
            "description": "Uniquely identifies the Performed Procedure Step SOP Instance to which the Series is related (e.g. a Modality or General-Purpose Performed Procedure Step SOP Instance).\nOnly a single Item shall be permitted in this sequence.\nRequired if the Modality Performed Procedure Step SOP Class, or General Purpose Performed Procedure Step SOP Class is supported.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0040, 0275)": {
            "name": "RequestAttributesSequence",
            "description": "Sequence that contains attributes from the Imaging Service Request.\nThe sequence may have one or more Items.",
            "type": "3",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0010)": {
            "name": "VisualFieldHorizontalExtent",
            "description": "The maximum horizontal angular subtend (diameter or width) of the tested visual field, in degrees.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0011)": {
            "name": "VisualFieldVerticalExtent",
            "description": "The maximum vertical angular subtend (diameter or height) of the tested visual field, in degrees.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0012)": {
            "name": "VisualFieldShape",
            "description": "The shape of the visual field tested.\nDefined Terms:\nRECTANGLE\nCIRCLE\nELLIPSE",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0016)": {
            "name": "ScreeningTestModeCodeSequence",
            "description": "Mode used to determine how the starting luminance values and expected thresholds are chosen.\nRequired if Content Item Modifier Sequence (0040, 0441) within Performed Protocol Code Sequence (0040, 0260) contains an item with the value (R-42453, SRT, \u00d2Screening\u00d3). May be present otherwise.\nOnly a single Item shall be permitted in this sequence.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0018)": {
            "name": "MaximumStimulusLuminance",
            "description": "Maximum luminance of stimulus, in candelas per square meter (cd/m_).",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0020)": {
            "name": "BackgroundLuminance",
            "description": "Background luminance of the device, in candelas per square meter (cd/m_). \nNote: This value is easily convertible to apostilb, which is used only in perimetry and is not a standardized unit.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0021)": {
            "name": "StimulusColorCodeSequence",
            "description": "Color of light stimulus presented to the patient.\nOnly a single Item shall be permitted in this sequence.",
            "type": "1",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0024)": {
            "name": "BackgroundIlluminationColorCodeSequence",
            "description": "Color of the background illumination of the visual field device.\nOnly a single Item shall be permitted in this sequence.",
            "type": "1",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0025)": {
            "name": "StimulusArea",
            "description": "Area of light stimulus presented to the patient, in degrees squared.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0028)": {
            "name": "StimulusPresentationTime",
            "description": "The duration of time that a light stimulus is presented to a patient per each individual test point, in milliseconds.\nNote: This time is the same for each stimulus presentation.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0032)": {
            "name": "FixationSequence",
            "description": "The patient's gaze stability information during the visual field test.\nOnly a single Item shall be permitted in this sequence.",
            "type": "1",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0033)": {
            "name": "FixationMonitoringCodeSequence",
            "description": "The device strategy used to monitor the patient's fixation.\nOne or more Items shall be included in this sequence.",
            "type": "1",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0035)": {
            "name": "FixationCheckedQuantity",
            "description": "The number of times that the patient's gaze fixation is checked.\nRequired if Fixation Monitoring Code Sequence (0024, 0033) contains an item with the value (111844, DCM, \u00d2Blind Spot Monitoring\u00d3) or (111845, DCM, \u00d2Macular Fixation Testing\u00d3). May be present otherwise.",
            "type": "1C",
            "vm": 1.0,
            "vr": "US"
        },
        "(0024, 0036)": {
            "name": "PatientNotProperlyFixatedQuantity",
            "description": "The number of times the patient's gaze is not properly fixated.\nRequired if Fixation Monitoring Code Sequence (0024, 0033) contains an item with the value (111844, DCM, \u00d2Blind Spot Monitoring\u00d3) or (111845, DCM, \u00d2Macular Fixation Testing\u00d3). May be present otherwise.",
            "type": "1C",
            "vm": 1.0,
            "vr": "US"
        },
        "(0024, 0039)": {
            "name": "ExcessiveFixationLossesDataFlag",
            "description": "Whether the device was able to determine excessive fixation losses.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0040)": {
            "name": "ExcessiveFixationLosses",
            "description": "The number of fixation losses is outside of implementation-specific limits.\nEnumerated Values:\nYES\nNO\nRequired if Excessive Fixation Losses Data Flag (0024, 0039) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0034)": {
            "name": "VisualFieldCatchTrialSequence",
            "description": "The reliability of the patient's responses to the visual field test.\nOnly a single Item shall be permitted in this sequence.",
            "type": "1",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0055)": {
            "name": "CatchTrialsDataFlag",
            "description": "Whether catch trials data were performed.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0048)": {
            "name": "NegativeCatchTrialsQuantity",
            "description": "Total number of times the patient's visual attention was tested using stimuli brighter than previously seen luminance (negative catch trials).\nRequired if Catch Trials Data Flag (0024, 0055) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "US"
        },
        "(0024, 0050)": {
            "name": "FalseNegativesQuantity",
            "description": "Total number of stimuli that were not seen by the patient but were previously seen at a lower luminance earlier in the visual field test (false negatives).\nRequired if Catch Trials Data Flag (0024, 0055) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "US"
        },
        "(0024, 0045)": {
            "name": "FalseNegativesEstimateFlag",
            "description": "Whether the device was able to estimates false negatives.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0046)": {
            "name": "FalseNegativesEstimate",
            "description": "Estimated percentage of all stimuli that were not seen by the patient but were previously seen at a lower luminance earlier in the visual field test (false negative responses), as percent.\nRequired if False Negatives Estimate Flag (0024, 0045) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0051)": {
            "name": "ExcessiveFalseNegativesDataFlag",
            "description": "Whether the device was able to determine excessive false negatives.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0052)": {
            "name": "ExcessiveFalseNegatives",
            "description": "The false negative estimate is outside of implementation-specific limits.\nEnumerated Values:\nYES\nNO\nRequired if Excessive False Negatives Data Flag (0024, 0051) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0056)": {
            "name": "PositiveCatchTrialsQuantity",
            "description": "The total number of times the device behaved as if it was going to present a visual stimulus but did not actually present the stimulus (positive catch trials).\nRequired if Catch Trials Data Flag (0024, 0055) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "US"
        },
        "(0024, 0060)": {
            "name": "FalsePositivesQuantity",
            "description": "The total number of patient responses that occurred at a time when no visual stimulus was present (false positive responses).\nRequired if Catch Trials Data Flag (0024, 0055) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "US"
        },
        "(0024, 0053)": {
            "name": "FalsePositivesEstimateFlag",
            "description": "Whether the device was able to estimate false positives.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0054)": {
            "name": "FalsePositivesEstimate",
            "description": "Estimated percentage of all patient responses that occurred at a time when no visual stimulus was present (false positive responses), as percent.\nRequired if False Positives Estimate Flag (0024, 0053) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0061)": {
            "name": "ExcessiveFalsePositivesDataFlag",
            "description": "Whether the device was able to determine excessive false positives.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0062)": {
            "name": "ExcessiveFalsePositives",
            "description": "The false positive estimate is outside of implementation-specific limit.\nEnumerated Values:\nYES\nNO\nRequired if Excessive False Positives Data Flag (0024, 0061) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0042)": {
            "name": "StimuliRetestingQuantity",
            "description": "Total number of times in the course of a visual field exam that any location had to be retested at the same magnitude.\nNote: An example is that the patient received 20 stimuli and blinked twice, therefore need to present the stimuli two additional times in which case the value is 2.",
            "type": "3",
            "vm": 1.0,
            "vr": "US"
        },
        "(0024, 0069)": {
            "name": "PatientReliabilityIndicator",
            "description": "Vendor implementation specific text to provide an analysis and/or summary of patient reliability indicator/indices.",
            "type": "3",
            "vm": 1.0,
            "vr": "LO"
        },
        "(0024, 0044)": {
            "name": "CommentsOnPatientPerformanceOfVisualField",
            "description": "Operator's (test administrator) subjective comment on patient's performance.",
            "type": "3",
            "vm": 1.0,
            "vr": "LT"
        },
        "(0024, 0317)": {
            "name": "VisualFieldTestReliabilityGlobalIndexSequence",
            "description": "Information about various visual field indices related to test reliability.\nOne or more items may be present.",
            "type": "3",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0325)": {
            "name": "DataObservationSequence",
            "description": "Information about various visual field global indexes.\nOnly a single Item shall be permitted in this sequence.",
            "type": "1",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0338)": {
            "name": "IndexNormalsFlag",
            "description": "Whether normative data exists for this index.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0344)": {
            "name": "IndexProbabilitySequence",
            "description": "Probability value and software algorithm used to provide the index.\nRequired if Index Normals Flag (0024, 0338) is YES.\nOnly a single Item shall be permitted in this sequence.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0341)": {
            "name": "IndexProbability",
            "description": "Probability for the index value within the normal population, in percent.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0113)": {
            "name": "MeasurementLaterality",
            "description": "Laterality of body part (eye) examined. See section C.8.X.4.1.1 for further explanation. Enumerated Values: R = right L = left B = both left and right together Note: This Attribute is mandatory, in order to ensure that measurements may be positioned correctly relative to one another for display. Note: Laterality (0020, 0060) is a Series level Attribute and must be the same for all Measurements in the Series, hence it must be absent if multiple instances from different eyes are encoded.",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0037)": {
            "name": "PresentedVisualStimuliDataFlag",
            "description": "Whether the device was able to determine presented visual stimuli.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0038)": {
            "name": "NumberOfVisualStimuli",
            "description": "The total number of visual stimuli presented to the patient. This includes the number of stimuli repetitions.\nRequired if Presented Visual Stimuli Data Flag (0024, 0037) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "US"
        },
        "(0024, 0088)": {
            "name": "VisualFieldTestDuration",
            "description": "Total time the visual field machine was actively presenting visual stimuli to patient, in seconds.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0086)": {
            "name": "FovealSensitivityMeasured",
            "description": "Whether foveal sensitivity was measured.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0087)": {
            "name": "FovealSensitivity",
            "description": "Foveal Sensitivity is the reciprocal of foveal threshold (1/foveal threshold), in dB.\nFoveal Threshold is the minimum amount of luminance increment on a uniform background that can be detected by the patient at coordinates 0, 0 (relative to the center of the patient's fixation).\nSee section C.8.X.4.1.2 for further explanation.\nRequired if the value for Foveal Sensitivity Measured (0024, 0086) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0117)": {
            "name": "FovealPointNormativeDataFlag",
            "description": "Existence of normative data base for the foveal point sensitivity.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0118)": {
            "name": "FovealPointProbabilityValue",
            "description": "The percentile of the foveal point sensitivity within an age corrected normal visual field, in percent.\nRequired if the value for Foveal Sensitivity Measured (0024, 0086) is YES and Foveal Point Normative Data Flag (0024, 0117) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0120)": {
            "name": "ScreeningBaselineMeasured",
            "description": "Whether visual field screening baseline was measured.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0122)": {
            "name": "ScreeningBaselineMeasuredSequence",
            "description": "Information about the starting luminance screening values.\nRequired if the value for Screening Baseline Measured (0024, 0120) is YES.\nOne or more items may be present.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0124)": {
            "name": "ScreeningBaselineType",
            "description": "Method used to determine starting luminance screening values.\nEnumerated Values:\nCENTRAL\nPERIPHERAL",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0126)": {
            "name": "ScreeningBaselineValue",
            "description": "Visual Field screening baseline value, in dB.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0106)": {
            "name": "BlindSpotLocalized",
            "description": "Whether the blind spot was measured.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0107)": {
            "name": "BlindSpotXCoordinate",
            "description": "The horizontal coordinate of the patient's blind spot relative to the center of the patient's fixation, in degrees, such that toward the right is positive.\nRequired if the value for Blind Spot Localized (0024, 0106) is YES.\nSee section C.8.X.4.1.3 for further explanation.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0108)": {
            "name": "BlindSpotYCoordinate",
            "description": "The vertical coordinate of the patient's blind spot relative to the center of the patient fixation, in degrees, such that up is positive.\nRequired if the value for Blind Spot Localized (0024, 0106) is YES.\nSee section C.8.X.4.1.3 for further explanation.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0105)": {
            "name": "MinimumSensitivityValue",
            "description": "The minimum sensitivity value generated by the equipment used for this visual field test, in dB.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0057)": {
            "name": "TestPointNormalsDataFlag",
            "description": "Existence of normative data base for this set of test points.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0058)": {
            "name": "TestPointNormalsSequence",
            "description": "Normative data base used for this test sequence.\nRequired if Test Point Normals Data Flag (0024, 0057) is YES.\nOnly a single Item shall be permitted in this sequence.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0065)": {
            "name": "AgeCorrectedSensitivityDeviationAlgorithmSequence",
            "description": "Software algorithm used to provide the probability that the age corrected sensitivity deviation values at each test point belong to a normal visual field.\nRequired if Test Point Normals Data Flag (0024, 0057) is YES.\nOnly a single Item shall be permitted in this sequence.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0067)": {
            "name": "GeneralizedDefectSensitivityDeviationAlgorithmSequence",
            "description": "Software algorithm used to provide the probability that the sensitivity deviation values at each test point belong to a normal visual field.\nRequired if Test Point Normals Data Flag (0024, 0057) is YES.\nOnly a single Item shall be permitted in this sequence.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0089)": {
            "name": "VisualFieldTestPointSequence",
            "description": "Information for each test point in the visual field.\nOne or more items shall be present.",
            "type": "1",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0090)": {
            "name": "VisualFieldTestPointXCoordinate",
            "description": "The horizontal coordinate of a single test point relative to the center of the patient fixation, in degrees, such that toward the right is positive.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0091)": {
            "name": "VisualFieldTestPointYCoordinate",
            "description": "The vertical coordinate of a single test point relative to the center of the patient fixation, in degrees, such that up is positive.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0093)": {
            "name": "StimulusResults",
            "description": "Whether the patient saw a stimulus presented at a luminance other than maximum, a presentation at maximum luminance, or did not see any presented stimulus.\nEnumerated Values:\nSEEN = stimulus seen at a luminance value less than maximum\nNOT SEEN = stimulus not seen\nSEEN AT MAX = stimulus seen at the maximum luminance possible for the instrument \nNote: SEEN AT MAX is a value only relevant to Screening tests.",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0094)": {
            "name": "SensitivityValue",
            "description": "If Stimulus Results (0024, 0093) is SEEN then this value is the sensitivity, in dB.\nRequired if Content Item Modifier Sequence (0040, 0441) within Performed Protocol Code Sequence (0040, 0260) contains an item with the value (R-408C3, SRT, \u00d2Diagnostic\u00d3). May be present otherwise.\nNote: If this is not present, refer to the Minimum Sensitivity Value (0024, 0105).",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0095)": {
            "name": "RetestStimulusSeen",
            "description": "Whether the retested stimulus presented was seen by the patient.\nEnumerated Values:\nYES\nNO",
            "type": "3",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0096)": {
            "name": "RetestSensitivityValue",
            "description": "If the Retest Stimulus Seen (0024, 0095) is YES, then this value is the sensitivity, in dB.\nNote: If this is not present, refer to the Minimum Sensitivity Value (0024, 0105).",
            "type": "3",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0098)": {
            "name": "QuantifiedDefect",
            "description": "Difference between the expected and the determined sensitivity, each in dB.\nNote: This field is only useful when the sensitivity is quantified. Some examples include Test Strategy Code Sequence (0024, 0015) with items providing values such as Quantity-Defects, 2LT-Dynamic, 2LT-Normal.",
            "type": "3",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0097)": {
            "name": "VisualFieldTestPointNormalsSequence",
            "description": "Information about normal values for each visual field test point.\nRequired if Test Point Normals Data Flag (0024, 0057) is YES.\nOne or more items shall be present.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0092)": {
            "name": "AgeCorrectedSensitivityDeviationValue",
            "description": "Difference between the patient's local sensitivity and the age corrected normal sensitivity, in dB.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0100)": {
            "name": "AgeCorrectedSensitivityDeviationProbabilityValue",
            "description": "The percentile of the age corrected sensitivity deviation within the normal population of visual field, in percent.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0102)": {
            "name": "GeneralizedDefectCorrectedSensitivityDeviationFlag",
            "description": "Whether generalized defect corrected data are available for this point.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0103)": {
            "name": "GeneralizedDefectCorrectedSensitivityDeviationValue",
            "description": "The age corrected sensitivity deviation after correction for the Generalized Defect, in dB. Generalized defect is proportional to the loss in sensitivity shared by all points in the visual field.\nRequired if Generalized Defect Corrected Sensitivity Deviation Flag (0024, 0102) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0104)": {
            "name": "GeneralizedDefectCorrectedSensitivityDeviationProbabilityValue",
            "description": "The percentile of the generalized defect corrected sensitivity deviation within the normal population of visual field, in percent. \nRequired if Generalized Defect Corrected Sensitivity Deviation Flag (0024, 0102) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0070)": {
            "name": "VisualFieldMeanSensitivity",
            "description": "Average sensitivity of the test points of the visual field, in dB.\nRequired if Content Item Modifier Sequence (0040, 0441) within the Performed Protocol Code Sequence (0040, 0260) contains an item with the value (R-408C3, SRT, \u00d2Diagnostic\u00d3). May be present otherwise.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0063)": {
            "name": "VisualFieldTestNormalsFlag",
            "description": "Whether normals exist for this patient's results.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0064)": {
            "name": "ResultsNormalsSequence",
            "description": "Information that represents the statistically normal results for patients from a referenced data base.\nRequired if Visual Field Test Normals Flag (0024, 0063) is YES.\nOnly a single Item shall be permitted in this sequence.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0066)": {
            "name": "GlobalDeviationFromNormal",
            "description": "Weighted average deviation from the age corrected normal field, in dB.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0059)": {
            "name": "GlobalDeviationProbabilityNormalsFlag",
            "description": "Whether normals exist for the global deviation probability.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0083)": {
            "name": "GlobalDeviationProbabilitySequence",
            "description": "Probability value and software algorithm used to provide the normality for the global deviation.\nOnly a single Item shall be permitted in this sequence.\nRequired if Global Deviation Probability Normals Flag (0024, 0059) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0071)": {
            "name": "GlobalDeviationProbability",
            "description": "The percentile of the Global Deviation from Normal (0024, 0066) value within the normal population, in percent.0024",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0068)": {
            "name": "LocalizedDeviationFromNormal",
            "description": "Weighted square root of loss variance, in dB.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0072)": {
            "name": "LocalDeviationProbabilityNormalsFlag",
            "description": "Whether normals exist for the local deviation probability.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0085)": {
            "name": "LocalizedDeviationProbabilitySequence",
            "description": "Probability value and software algorithm used to provide the normality for the local deviation.\nOnly a single Item shall be permitted in this sequence.\nRequired if Local Deviation Probability Normals Flag (0024, 0072) is YES..",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0073)": {
            "name": "LocalizedDeviationProbability",
            "description": "The0024 percentile of the Localized Deviation from Normal (0024, 0068) value within the normal population, in percent.0024",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0074)": {
            "name": "ShortTermFluctuationCalculated",
            "description": "Whether the short term fluctuation was calculated.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0075)": {
            "name": "ShortTermFluctuation",
            "description": "Average deviation of sensitivity for the repeated test locations, in dB. This is used to determine the consistency of the patient's responses.\nRequired if Short Term Fluctuation Calculated (0024, 0074) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0076)": {
            "name": "ShortTermFluctuationProbabilityCalculated",
            "description": "Whether the short term fluctuation probability was calculated.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0077)": {
            "name": "ShortTermFluctuationProbability",
            "description": "The percentile of the Short Term Fluctuation (0024, 0075) value within the normal population, in percent.\nRequired if Short Term Fluctuation Probability Calculated (0024, 0076) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0078)": {
            "name": "CorrectedLocalizedDeviationFromNormalCalculated",
            "description": "Whether the corrected localized deviation from normal was calculated.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0079)": {
            "name": "CorrectedLocalizedDeviationFromNormal",
            "description": "Weighted square root of loss variance corrected for short term fluctuation, in dB. \nRequired if Corrected Localized Deviation From Normal Calculated (0024, 0078) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0080)": {
            "name": "CorrectedLocalizedDeviationFromNormalProbabilityCalculated",
            "description": "Whether the corrected localized deviation from Normal probability was calculated.\nEnumerated Values:\nYES\nNO",
            "type": "1",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0024, 0081)": {
            "name": "CorrectedLocalizedDeviationFromNormalProbability",
            "description": "The percentile of the Corrected Localized Deviation From Normal (0024, 0079) value within the normal population, in percent.\nRequired if Corrected Localized Deviation From Normal Probability Calculated (0024, 0080) is YES.",
            "type": "1C",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0320)": {
            "name": "VisualFieldGlobalResultsIndexSequence",
            "description": "Information about various visual field indexes related to test results.\nOne or more items may be present.",
            "type": "3",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0114)": {
            "name": "OphthalmicPatientClinicalInformationLeftEyeSequence",
            "description": "Information used to represent a patient's clinical parameters during an ophthalmic test. \nOnly a single Item shall be permitted in this sequence.\nRequired if Measurement Laterality (0024, 0113) is L or B.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0115)": {
            "name": "OphthalmicPatientClinicalInformationRightEyeSequence",
            "description": "Information used to represent a patient's clinical parameters during an ophthalmic test. \nOnly a single Item shall be permitted in this sequence.\nRequired if Measurement Laterality (0024, 0113) is R or B.",
            "type": "1C",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0024, 0112)": {
            "name": "RefractiveParametersUsedOnPatientSequence",
            "description": "Refractive parameters used when performing visual field test. Zero or one Item shall be permitted.",
            "type": "2",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0022, 0007)": {
            "name": "SphericalLensPower",
            "description": "Sphere value in diopters.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0022, 0008)": {
            "name": "CylinderLensPower",
            "description": "Cylinder value in diopters.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0022, 0009)": {
            "name": "CylinderAxis",
            "description": "Axis value in degrees.",
            "type": "1",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0046, 0044)": {
            "name": "PupilSize",
            "description": "The horizontal diameter measurement of the pupil, in mm.",
            "type": "2",
            "vm": 1.0,
            "vr": "FD"
        },
        "(0022, 000D)": {
            "name": "PupilDilated",
            "description": "The patient's pupils were pharmacologically dilated for this acquisition.\nEnumerated Values:\nYES\nNO\nIf this tag is empty, no information is available.",
            "type": "2",
            "vm": 1.0,
            "vr": "CS"
        },
        "(0022, 000B)": {
            "name": "IntraOcularPressure",
            "description": "Value of intraocular pressure in mmHg.",
            "type": "3",
            "vm": 1.0,
            "vr": "FL"
        },
        "(0024, 0110)": {
            "name": "VisualAcuityMeasurementSequence",
            "description": "Measurements of a patient's visual acuity.",
            "type": "3",
            "vm": 1.0,
            "vr": "SQ"
        },
        "(0020, 000d)": {
            "name": "Study Instance Unique Identifier",
            "description": "Study Instance Unique Identifier",
            "type": "1",
            "vm": 1.0,
            "vr": "UI"
        },
        "(0020, 000e)": {
            "name": "Series Instance Unique Identifier",
            "description": "Series Instance Unique Identifier",
            "type": "1",
            "vm": 1.0,
            "vr": "UI"
        },
        "(0008, 1090)": {
            "name": "ManufacturerModelName",
            "description": "Manufacturer's Model Name",
            "type": "1",
            "vm": 1.0,
            "vr": "LO"
        },
        "(0008, 0070)": {
            "name": "Manufacturer",
            "description": "Manufacturer",
            "type": "1",
            "vm": 1.0,
            "vr": "LO"
        },
        "(0008, 0104)": {
            "name": "CodeMeaning",
            "description": "Test Strategy",
            "type": "1",
            "vm": 1.0,
            "vr": "LO"
        }
    }
   return opv_dcm_dict