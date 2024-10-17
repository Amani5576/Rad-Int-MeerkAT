# Rad-Int-MeerkAT
Using MeerKat Radio interferometry data to analyse and understand Regions of Radio Interferance

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
