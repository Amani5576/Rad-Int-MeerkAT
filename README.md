# Rad-Int-MeerkAT
Using MeerKat Radio interferometry data to analyse and understand Regions of Radio Interferance with ```daskms```

# **Observation Summary**

This document provides an overview of the observational data collected with the **MeerKAT** telescope. Below are the key details of the observation and its metadata:

---

## **Project Information**
- **Project ID**: `20190131-0012`
- **Observer**: `Lindsay`

---

## **Observation Details**
- **Telescope Name**: MeerKAT  
- **Total Number of Antennas Used**: 50  
- **Release Date**: `5055656390 s` (from epoch)  
- **Time Range**:
  - **Start**: `5055656170 s` (from epoch)  
  - **End**: `5055656390 s` (from epoch)

---

## **Data Statistics**
- **Interval Table Shape**: `(31,875,)`  
  *(Number of intervals recorded during the observation)*  
- **Dump Rate**: `7.9966 s`  
  *(Time between data dumps)*

---

This observation provides essential insights captured by the MeerKAT telescope, although the log and scheduling information were unavailable at the time of release, Long and Short baselines made by different pairs of Antennas gave good insights to regions of RFI when plotting visibility.
"""

# Overview of Tables in the Script

The script utilizes the **`daskms`** package to handle Measurement Set (MS) data from radio interferometry. This package is highly efficient for working with large observational datasets.

## Tables being accessed:

- **ANTENNA table**: Contains information about the antennas used in the observation.
- **FEED table**: Includes data on the feed systems, such as the receptor angles.
- **FIELD table**: Provides information on the observed fields, like the target's sky coordinates.
- **OBSERVATION table**: Contains metadata about the observation session, like start and end times.
- **POLARIZATION table**: Details polarization products available in the dataset.
- **PROCESSOR table**: Information about processing steps applied to the data.
- **SOURCE table**: Includes details about the sources being observed.
- **SPECTRAL_WINDOW table**: Describes the frequency channels and bandwidth of the observation.
- **STATE table**: Keeps track of the state of the observation, such as calibrator or science target identifiers.
"""

# Data Structure Overview

The following table summarizes the shapes and dimensions of each item in the 1548939342.ms dataset file:

| **Key**                | **Shape**            | **Dim**       |
|-----------------------|----------------------|----------------|
| PROCESSOR_ID          | (31875,)             | 1              |
| STATE_ID              | (31875,)             | 1              |
| WEIGHT                | (31875, 2)           | 2               |
| ANTENNA1              | (31875,)              | 1               |
| FLAG_CATEGORY         | (31875, 1, 1024, 2)  | 4               |
| INTERVAL              | (31875,)             | 1              |
| ARRAY_ID              | (31875,)             | 1              |
| FIELD_ID              | (31875,)             | 1              |
| FEED2                 | (31875,)              | 1               |
| WEIGHT_SPECTRUM       | (31875, 1024, 2)      | 3               |
| OBSERVATION_ID        | (31875,)             | 1              |
| DATA_DESC_ID          | (31875,)             | 1              |
| UVW                   | (31875, 3)           | 2              |
| FLAG_ROW              | (31875,)             | 1              |
| EXPOSURE              | (31875,)             | 1              |
| IMAGING_WEIGHT        | (31875, 1024)        | 2              |
| DATA                  | (31875, 1024, 2)     | 3              |
| FLAG                  | (31875, 1024, 2)     | 3              |
| SIGMA                 | (31875, 2)           | 2              |
| TIME                  | (31875,)             | 1              |
| ANTENNA2              | (31875,)              | 1               |
| FEED1                 | (31875,)              | 1               |
| TIME_CENTROID         | (31875,)             | 1              |
| SCAN_NUMBER           | (31875,)             | 1              |
