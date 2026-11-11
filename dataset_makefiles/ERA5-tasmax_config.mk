# Configuration file for Makefile workflows

OBS_DATASET=ERA5
OBS_DATA := $(sort $(wildcard /g/data/xv83/unseen-projects/outputs/bias/data/era5/tasmax_ERA5_day_gn_*.nc))
OBS_CONFIG=/home/599/dbi599/unseen-projects/dataset_config/dataset_era5_daily.yml
OBS_TIME_PERIOD=1940-2025
