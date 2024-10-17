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

<table style="display: inline-block; vertical-align: top; margin-right: 20px;">
    <tr>
        <th>Key</th>
        <th>Shape</th>
        <th>Dimensions</th>
    </tr>
    <tr>
        <td>PROCESSOR_ID</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>STATE_ID</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>WEIGHT</td>
        <td>(31875, 2)</td>
        <td>2</td>
    </tr>
    <tr>
        <td>ANTENNA1</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>FLAG_CATEGORY</td>
        <td>(31875, 1, 1024, 2)</td>
        <td>4</td>
    </tr>
    <tr>
        <td>INTERVAL</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>ARRAY_ID</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>FIELD_ID</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>FEED2</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
</table>

<table style="display: inline-block; vertical-align: top;">
    <tr>
        <th>Key</th>
        <th>Shape</th>
        <th>Dimensions</th>
    </tr>
    <tr>
        <td>WEIGHT_SPECTRUM</td>
        <td>(31875, 1024, 2)</td>
        <td>3</td>
    </tr>
    <tr>
        <td>OBSERVATION_ID</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>DATA_DESC_ID</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>UVW</td>
        <td>(31875, 3)</td>
        <td>2</td>
    </tr>
    <tr>
        <td>FLAG_ROW</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>EXPOSURE</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>IMAGING_WEIGHT</td>
        <td>(31875, 1024)</td>
        <td>2</td>
    </tr>
    <tr>
        <td>DATA</td>
        <td>(31875, 1024, 2)</td>
        <td>3</td>
    </tr>
    <tr>
        <td>FLAG</td>
        <td>(31875, 1024, 2)</td>
        <td>3</td>
    </tr>
    <tr>
        <td>SIGMA</td>
        <td>(31875, 2)</td>
        <td>2</td>
    </tr>
    <tr>
        <td>TIME</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>ANTENNA2</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>FEED1</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>TIME_CENTROID</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
    <tr>
        <td>SCAN_NUMBER</td>
        <td>(31875,)</td>
        <td>1</td>
    </tr>
</table>
