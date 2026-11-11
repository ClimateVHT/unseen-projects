"""Script for producing a tier1 data file"""

import argparse
from datetime import datetime, timezone
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import xarray as xr
import cmdline_provenance as cmdprov


rp_dict = {}
rp_dict['era5'] = {
#    'BCC-CSM2-MR': ,
#    'CanESM5': ,
#    'CMCC-CM2-SR5': ,
    'EC-Earth3': 326, #bc
    'IPSL-CM6A-LR': np.inf, #bc
#    'MIROC6': ,
#    'MPI-ESM1-2-HR': 
#    'MRI-ESM2-0': 
    'NorCPM1': 817, #bc
}
rp_dict['mswep'] = {
#    'BCC-CSM2-MR': 
    'CanESM5': 128, #bc
    'CMCC-CM2-SR5': 225, #bc 
    'EC-Earth3': 1566, #bc
#    'IPSL-CM6A-LR': 
#    'MIROC6':
#    'MPI-ESM1-2-HR':
#    'MRI-ESM2-0':
    'NorCPM1': 5310, #bc
}
rp_dict['cpc'] = {
#    'BCC-CSM2-MR':
    'CanESM5': 855, #bc
    'CMCC-CM2-SR5': np.inf, #bc 
    'EC-Earth3': np.inf, #bc
    'IPSL-CM6A-LR': np.inf, #bc 
#    'MIROC6': 
    'MPI-ESM1-2-HR': 738, #bc 
#    'MRI-ESM2-0': 
    'NorCPM1': np.inf, #raw
}

percentiles = [5, 16, 84, 95]
rp_bnds_dict = {}
rp_bnds_dict['era5'] = {
#    'BCC-CSM2-MR': 
#    'CanESM5': (),
#    'CMCC-CM2-SR5': (),
    'EC-Earth3': (237, 270, 412, 489),
    'IPSL-CM6A-LR': (np.inf, np.inf, np.inf, np.inf),
#    'MIROC6': (),
#    'MPI-ESM1-2-HR': 
#    'MRI-ESM2-0': 
    'NorCPM1': (559, 625, 1180, 1517),
}
rp_bnds_dict['mswep'] = {
#    'BCC-CSM2-MR': 
    'CanESM5': (108, 115, 145, 155),
    'CMCC-CM2-SR5': (164, 180, 300, 360), 
    'EC-Earth3': (870, 1119, 2610, 3915),
#    'IPSL-CM6A-LR': 
#    'MIROC6': 
#    'MPI-ESM1-2-HR': 
#    'MRI-ESM2-0': 
    'NorCPM1': (2655, 3540, 10620, np.inf),
}
rp_bnds_dict['cpc'] = {
#    'BCC-CSM2-MR': 
    'CanESM5': (570, 641, 1140, 1466),
    'CMCC-CM2-SR5': (np.inf, np.inf, np.inf, np.inf),
    'EC-Earth3': (np.inf, np.inf, np.inf, np.inf),
    'IPSL-CM6A-LR': (np.inf, np.inf, np.inf, np.inf),
#    'MIROC6': 
    'MPI-ESM1-2-HR': (492, 536, 1180, 1475),
#    'MRI-ESM2-0': 
    'NorCPM1': (np.inf, np.inf, np.inf, np.inf),
}

sample_size_dict = {
    'BCC-CSM2-MR': 3888,
    'CanESM5': 10260,
    'CMCC-CM2-SR5': 3600,
    'EC-Earth3': 7830,
    'IPSL-CM6A-LR': 5130,
    'MIROC6': 3540,
    'MPI-ESM1-2-HR': 5900,
    'MRI-ESM2-0': 2400,
    'NorCPM1': 10620,
}

obs_dataset_dict = {
    'mswep': 'Multi-Source Weighted-Ensemble Precipitation (MSWEP)',
    'cpc': 'Climate Prediction Center (CPC) Global Unified Gauge-Based Analysis of Daily Precipitation',
    'era5': 'ERA5',
}

obs_source_dict = {
    'era5': 'https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview',
    'cpc': 'https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html',
    'mswep': 'https://www.gloh2o.org/',
}

code_url = 'https://github.com/ClimateVHT/unseen-projects/tree/master/project-wcrp-prJA'
history_log = cmdprov.new_log(code_url=code_url)
global_attrs = {
    'institution': 'CSIRO',
    'method': 'UNSEEN',
    'event': 'Pakistan Floods (seasonal timescale)',
    'data_tier': 'tier1',
    'project': 'WCRP Common Event Attribution and Assessment',
    'contact': 'damien.irving@csiro.au',
    'source': 'Decadal Climate Prediction Project (DCPP) models',
    'experiment': 'dcppA-hindcast',
    'references': 'Decadal Climate Prediction Project (DCPP): https://doi.org/10.5194/gmd-9-3751-2016. UNSEEN methodology: https://doi.org/10.1002/met.70118',
    'creation_date': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'history': history_log,
}


def processing_description(obs):
    """Describe the processing for a given observational dataset"""

    event_dict = {
        'mswep': '437.7 mm',
        'cpc': '518.6 mm',
        'era5': '405.3 mm',
    }
    
    event = event_dict[obs]
    obs_dataset = obs_dataset_dict[obs]
    intro = f'Extreme value analysis was conducted to calculate the return period (rp) for the 2022 July-August accumulated rainfall value of {event} observed in the {obs_dataset} dataset.'
    rp = 'This involved calculating the empirical probability of exceeding the observed value in the model data and converting that to a return period in years.'
    uncert1 = 'The uncertainty bounds (rp_bnds) were determined by non-parametric bootstrapping, whereby the model data was repeatedly randomly sampled (with the same sample size as the model data) with replacement to obtain 1000 estimates of rp.'
    uncert2 = 'From these 1000 estimates the 5-95 percentile and 16-84 percentile uncertainty ranges could be calculated.'

    description = f'{intro} {rp} {uncert1} {uncert2}'
    
    return description
    

def get_encoding(ds):
    """Output file encoding."""

    encoding = {}
    ds_vars = list(ds.coords) + list(ds.keys())
    for ds_var in ds_vars:
        encoding[ds_var] = {'_FillValue': None}

    return encoding


def main(args):
    """Run the program"""

    models = list(rp_dict[args.obs].keys())
    rp_values = [rp_dict[args.obs][model] for model in models]
    rp_bnds_values = [rp_bnds_dict[args.obs][model] for model in models]
    ss_values = [sample_size_dict[model] for model in models]

    rp_da = xr.DataArray(
        data=rp_values,
        dims=['model',],
        coords={'model': models,},
        name='rp',
        attrs = {
            'long_name': 'Return period',
            'units': 'years',
        }
    )
    rp_bnds_da = xr.DataArray(
        data=rp_bnds_values,
        dims=['model', 'percentile'],
        coords={'model': models, 'percentile': percentiles},
        name='rp_bnds',
        attrs = {
            'long_name': 'Return period uncertainty bounds',
            'units': 'years'
        }
    )
    ss_da = xr.DataArray(
        data=ss_values,
        dims=['model',],
        coords={'model': models,},
        name='n',
        attrs = {
            'long_name': 'Sample size',
            'units': '1',
        }
    )
    output_ds = xr.merge([rp_da, rp_bnds_da, ss_da])
    output_ds.attrs = global_attrs
    obs_dataset = obs_dataset_dict[args.obs]
    obs_source = obs_source_dict[args.obs]
    output_ds.attrs['references'] = output_ds.attrs['references'] + f'. {obs_dataset}: {obs_source}' 
    output_ds.attrs['processing'] = processing_description(args.obs)
    output_ds['model'].attrs['long_name'] = 'Model name'
    output_ds['percentile'].attrs['long_name'] = 'Percentile'
    output_ds['percentile'].attrs['units'] = '1'

    outdir = f'/g/data/xv83/unseen-projects/outputs/wcrp-prJA/data'
    ob_name = args.obs.upper()
    fpath = f'{outdir}/CSIRO_UNSEEN_tier1_{ob_name}.nc'
    encoding = get_encoding(output_ds)
    output_ds.to_netcdf(fpath, encoding=encoding)
    print(fpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        argument_default=argparse.SUPPRESS,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )                      
    parser.add_argument("obs", type=str, choices=('mswep', 'cpc', 'era5'), help="observational dataset")           
    args = parser.parse_args()
    main(args)
