# Configuration file for Makefile workflows

OBS_DATASET=CPC
OBS_DATA := $(sort $(wildcard /g/data/xv83/dbi599/cpc/precip.*.nc))
OBS_CONFIG=/home/599/dbi599/unseen-projects/dataset_config/dataset_cpc_daily.yml
OBS_TIME_PERIOD=1979-2025
