# Configuration file for wcrp-rx5day analysis (climatology files)

PROJECT_NAME=wcrp-rx5day
ENV_DIR=/g/data/xv83/dbi599/miniconda3/envs/unseen
PROJECT_DIR=/g/data/xv83/unseen-projects/outputs/wcrp-rx5day

## Labels
METRIC=zg500-jul-aug
REGION=asia
TIMESCALE=annual

## Metric calculation
VAR=zg500
UNITS=m
TIME_FREQ=YE-DEC
METRIC_OPTIONS=--variables ${VAR} --lat_bnds -15 65 --lon_bnds 35 165 --months 7 8 --time_freq ${TIME_FREQ} --time_agg mean --input_freq D --time_agg_min_tsteps 59 --units ${VAR}='${UNITS}' 
METRIC_OPTIONS_FCST= --output_chunks lead_time=50

