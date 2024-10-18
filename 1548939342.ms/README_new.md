
# Overview of Tables

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

# Measurement Set Tables and their associative Keys
## Antenna Table
- MOUNT, TYPE, NAME, DISH_DIAMETER, POSITION, STATION, OFFSET, FLAG_ROW

## Feed Table
- BEAM_ID, SPECTRAL_WINDOW_ID, ANTENNA_ID, TIME, INTERVAL, POL_RESPONSE, RECEPTOR_ANGLE, FEED_ID, POSITION, NUM_RECEPTORS, POLARIZATION_TYPE, BEAM_OFFSET

## Field Table
- DELAY_DIR, NUM_POLY, SOURCE_ID, TIME, NAME, CODE, PHASE_DIR, REFERENCE_DIR, FLAG_ROW

## Observation Table
- PROJECT, SCHEDULE_TYPE, RELEASE_DATE, TIME_RANGE, LOG, TELESCOPE_NAME, SCHEDULE, OBSERVER, FLAG_ROW

## Polarization Table
- CORR_PRODUCT, NUM_CORR, CORR_TYPE, FLAG_ROW

## Processor Table
- TYPE, MODE_ID, TYPE_ID, SUB_TYPE, FLAG_ROW

## Source Table
- SOURCE_ID, SPECTRAL_WINDOW_ID, REST_FREQUENCY, TIME, DIRECTION, INTERVAL, NAME, CALIBRATION_GROUP, PROPER_MOTION, NUM_LINES, CODE

## Spectral Window Table
- FREQ_GROUP, TOTAL_BANDWIDTH, IF_CONV_CHAIN, NUM_CHAN, NAME, NET_SIDEBAND, FLAG_ROW, MEAS_FREQ_REF, REF_FREQUENCY, CHAN_WIDTH, FREQ_GROUP_NAME, EFFECTIVE_BW, RESOLUTION, CHAN_FREQ

## State Table
- OBS_MODE, REF, CAL, LOAD, SIG, SUB_SCAN, FLAG_ROW
