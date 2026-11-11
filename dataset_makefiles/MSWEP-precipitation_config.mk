# Configuration file for Makefile workflows

OBS_DATASET=MSWEP
OBS_DATA := $(sort $(wildcard /g/data/jt48/aus-ref-clim-data-nci/mswep/data/MSWEP_V316/day/mswep_v316_day_*.nc))
OBS_CONFIG=/home/599/dbi599/unseen-projects/dataset_config/dataset_mswep_daily.yml
OBS_TIME_PERIOD=1979-2025
