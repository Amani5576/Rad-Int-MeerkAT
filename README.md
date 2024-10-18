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

This observation provides essential insights captured by the MeerKAT telescope, although the log and scheduling information were unavailable at the time of release, Long and Short baselines made by different pairs of Antennas gave good insights to regions of RFI when plotting visibility.
"""
