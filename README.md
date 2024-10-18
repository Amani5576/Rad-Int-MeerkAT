# Rad-Int-MeerkAT
Using MeerKat Radio interferometry data to analyse and understand Regions of Radio Interferance with ```daskms```

## Reproducing the Environment

To recreate the environment in which this code was run, you can use the `daskms_environment.yml` file provided in this repository. Follow the steps below:

1. Make sure you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed on your system.

2. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

3. Create the conda environment using the `daskms_environment.yml` file:

   ```bash
   conda env create -f daskms_environment.yml
   ```

4. Activate the environment:

   ```bash
   conda activate iraf27
   ```

And you're all set!

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

# Documentation of Functions in PACK_func.py

## Overview

This document describes the key functions defined in `PACK_func.py` and their roles in the data extraction process using `daskms` from `PACK.py` and `main.py`.

## Functions in PACK_func.py

### 1. `argmax_more(num, arr)`
- **Description**: Returns the index of the `num`-th maximum value in the input array.
- **Parameters**:
  - `num`: Integer indicating which maximum to return.
  - `arr`: Numpy array from which to find the maximum.
- **Returns**: Index of the `num`-th maximum value.
- **Usage**:
    ```python
    from PACK_func import argmax_more
    index = argmax_more(0, my_array)  # Getting index of 0th Longest Baseline
    ```

### 2. `argmin_more(num, arr)`
- **Description**: Returns the index of the `num`-th minimum value in the input array.
- **Parameters**:
  - `num`: Integer indicating which minimum to return.
  - `arr`: Numpy array from which to find the minimum.
- **Returns**: Index of the `num`-th minimum value.
- **Usage**:
    ```python
    from PACK_func import argmin_more
    index = argmin_more(0, my_array)  # Getting index of 0th Shortest Baseline
    ```

### 3. `plot_visibility_data(a1, a2, name1, name2, baseline_type, frequencies)`
- **Description**: Plots visibility data for a specified baseline defined by two antennas.
- **Parameters**:
  - `a1`, `a2`: Antenna identifiers.
  - `name1`, `name2`: Names of the antennas.
  - `baseline_type`: Type of baseline (e.g., "short", "long").
  - `frequencies`: Array of frequency values.
- **Returns**: None. Displays a plot.
- **Usage**:
    ```python
    from PACK_func import plot_visibility_data
    plot_visibility_data(1, 2, "Antenna 1", "Antenna 2", "Short", frequency_array)
    ```

### 4. `progressive_rfi_filter(visibility_amplitudes, frequencies, initial_kernel=29, sigma_threshold=1)`
- **Description**: Applies a progressive median filter to detect RFI (Radio Frequency Interference) in visibility data.
- **Parameters**:
  - `visibility_amplitudes`: 2D array containing visibility amplitude data.
  - `frequencies`: 1D array of frequency values.
  - `initial_kernel`: Initial kernel size for the median filter (default is 29).
  - `sigma_threshold`: Standard deviation threshold for RFI detection (default is 1).
- **Returns**: None. Displays plots of the filtering process.
- **Usage**:
    ```python
    from PACK_func import progressive_rfi_filter
    progressive_rfi_filter(visibility_data, frequency_array)
    ```

### 5. `plotting_hists(vis_clean, vis_rfi, xlims, ylims=[0,])`
- **Description**: Plots histograms for clean visibility data and RFI data.
- **Parameters**:
  - `vis_clean`: List of clean visibility data arrays.
  - `vis_rfi`: List of RFI data arrays.
  - `xlims`: Limits for the x-axis.
  - `ylims`: Limits for the y-axis (default is [0,]).
- **Returns**: None. Displays a histogram plot.
- **Usage**:
    ```python
    from PACK_func import plotting_hists
    plotting_hists(clean_data_list, rfi_data_list, x_limits, y_limits)
    ```

## Integration with PACK.py and main.py

### Extraction Process in PACK.py
- The `PACK.py` script utilizes `daskms` to perform data extraction and calls functions from `PACK_func.py` for data processing and visualization.
- **Example**:
    ```python
    from PACK_func import plot_visibility_data
    import daskms

    # Example of extracting data using daskms
    ds = daskms.open("path/to/data.ms")
    visibility_data = ds["DATA"]  # Example extraction

    # Visualizing the extracted data
    plot_visibility_data(1, 2, "Antenna 1", "Antenna 2", "Short", frequency_array)
    ```

### Main Execution in main.py
- The `main.py` script serves as the entry point for the application, orchestrating the extraction and processing of data using functions from both `PACK.py` and `PACK_func.py`.
- **Example**:
    ```python
    from PACK import ds
    from PACK_func import progressive_rfi_filter

    # Main execution flow
    visibility_amplitudes = ds["DATA"]  # Example extraction
    progressive_rfi_filter(visibility_amplitudes, frequency_array)
    ```
This documentation provides an overview of the functions in `PACK_func.py` and their interaction with data extraction processes facilitated by `PACK.py` and `main.py`. Ensure to refer to the specific implementation details within the respective files for further insights.

