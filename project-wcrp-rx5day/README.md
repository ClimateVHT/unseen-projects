## WCRP Rx5day

The [common event attribution and assessment (CEAA) project](https://www.wcrp-climate.org/epesc-wg3/epesc-wg3-ceaa)
of the WCRP Explaining and Predicting Earth System Change (EPESC) Lighthouse Activity
seeks to identify extreme weather and climate events for coordinated study.

This repository contains the analysis related to our submission
to the 2022 Pakistan floods case study (Rx5day metric).
The [guidance note](https://docs.google.com/document/d/1m47XI9k3ew1b7gJPa87wQzh53fMwakEIgukdT1bZ7Yw/)
explains the submission requirements.

### Data processing

Step 1: Calculate the Rx5day metric from observations:  
```
make metric-obs PROJECT_DETAILS=project-wcrp-rx5day/config_rx5day.mk OBS_DETAILS=dataset_makefiles/MSWEP-precipitation_config.mk
```

Step 2: Calculate the Rx5day metric for a model:  
```
make metric-forecast MODEL=CanESM5 PROJECT_DETAILS=project-wcrp-rx5day/config_rx5day.mk MODEL_DETAILS=dataset_makefiles/CanESM5_dcppA-hindcast_config.mk OBS_DETAILS=dataset_makefiles/MSWEP-precipitation_config.mk
```

Step 3: Calculate the annual climatology for a model:  
```
make metric-forecast MODEL=MRI-ESM2-0 PROJECT_DETAILS=project-wcrp-rx5day/config_clim_psl.mk MODEL_DETAILS=dataset_makefiles/MRI-ESM2-0_dcppA-hindcast_config.mk OBS_DETAILS=dataset_makefiles/MSWEP-precipitation_config.mk
```

Step 4: Copy a `rx5day_*.ipynb` notebook and run it for that model.  


### Data availability

The guidance documents ask for the following variables:

- Z500 geopotential height: `z500`
- Mean sea level pressure: `psl`
- Sea surface temperature: `tos`
- Total atmospheric column water vapour: `prw`

The availability of each variable is listed below:  
:green_circle: = data is available on NCI  
:yellow_circle: = data is available on ESGF  
:white_circle: = data not available  

| model | psl | z500 | tos | prw |
| ---   | :-: | :-:  | :-: | :-: |
| BCC-CSM2-MR | :green_circle: | :green_circle: | :green_circle: | :white_circle: |
| CanESM5 | :green_circle: | :green_circle: | :green_circle: | :white_circle: |
| CMCC-CM2-SR5 | :green_circle: | :green_circle: | :green_circle: | :white_circle: |
| EC-Earth3 | :green_circle: | :green_circle: | :green_circle: | :white_circle: |
| IPSL-CM6A-LR | :green_circle: | :green_circle: | :green_circle: | :white_circle: |
| MIROC6 | :green_circle: | :green_circle: (zg) | :green_circle: | :white_circle: |
| MPI-ESM1-2-HR | :green_circle: | :green_circle: | :green_circle: | :white_circle: |
| MRI-ESM2-0 | :green_circle: | :white_circle: | :green_circle: | :white_circle: |
| NorCPM1 | :green_circle: | :green_circle: | :green_circle: | :yellow_circle: |


