## WCRP prJA

The [common event attribution and assessment (CEAA) project](https://www.wcrp-climate.org/epesc-wg3/epesc-wg3-ceaa)
of the WCRP Explaining and Predicting Earth System Change (EPESC) Lighthouse Activity
seeks to identify extreme weather and climate events for coordinated study.

This repository contains the analysis related to our submission
to the 2022 Pakistan floods case study (July-August accumulated precipitation metric; prJA).
The [guidance note](https://docs.google.com/document/d/1m47XI9k3ew1b7gJPa87wQzh53fMwakEIgukdT1bZ7Yw/)
explains the submission requirements.

### Data processing

Step 1: Calculate the prJA metric from observations:  
```
make metric-obs PROJECT_DETAILS=project-wcrp-prJA/config_prJA.mk OBS_DETAILS=dataset_makefiles/MSWEP-precipitation_config.mk
```

Step 2: Calculate the prJA metric for a model:  
```
make metric-forecast MODEL=CanESM5 PROJECT_DETAILS=project-wcrp-prJA/config_prJA.mk MODEL_DETAILS=dataset_makefiles/CanESM5_dcppA-hindcast_config.mk OBS_DETAILS=dataset_makefiles/MSWEP-precipitation_config.mk
```

Step 3: Calculate the annual climatology for a model:  
```
make metric-forecast MODEL=MRI-ESM2-0 PROJECT_DETAILS=project-wcrp-rx5day/config_clim_psl.mk MODEL_DETAILS=dataset_makefiles/MRI-ESM2-0_dcppA-hindcast_config.mk OBS_DETAILS=dataset_makefiles/MSWEP-precipitation_config.mk
```

Step 4: Copy a `prJA_*.ipynb` notebook and run it for that model.  


### Data availability

See the [`project-wcrp-rx5day` repo](https://github.com/ClimateVHT/unseen-projects/blob/master/project-wcrp-rx5day/README.md#data-availability).


