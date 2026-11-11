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
    'BCC-CSM2-MR': 36, #bc
#    'CanESM5': ,
#    'CMCC-CM2-SR5': ,
    'EC-Earth3': 33, #bc
    'IPSL-CM6A-LR': 122, #bc
#    'MIROC6': ,
    'MPI-ESM1-2-HR': 22, #bc
    'MRI-ESM2-0': 47, #bc
    'NorCPM1': 30, #raw
}
rp_dict['mswep'] = {
    'BCC-CSM2-MR': 35, #bc
#    'CanESM5': ,
    'CMCC-CM2-SR5': 15, #bc
    'EC-Earth3': 32, #bc
    'IPSL-CM6A-LR': 117, #bc
    'MIROC6': 23, #bc
    'MPI-ESM1-2-HR': 21,  #bc
    'MRI-ESM2-0': 43, #bc
    'NorCPM1': 38, #raw
}
rp_dict['cpc'] = {
    'BCC-CSM2-MR': 371, #raw
#    'CanESM5': ,
    'CMCC-CM2-SR5': 100, #bc
    'EC-Earth3': 2250, #raw
    'IPSL-CM6A-LR': 72119, #bc
    'MIROC6': 184, #raw
    'MPI-ESM1-2-HR': 310, #bc
    'MRI-ESM2-0': 1607, #bc
    'NorCPM1': 19459, #bc
}

percentiles = [5, 16, 84, 95]
rp_bnds_dict = {}
rp_bnds_dict['era5'] = {
    'BCC-CSM2-MR': (32, 33, 39, 41),
#    'CanESM5': (),
#    'CMCC-CM2-SR5': (),
    'EC-Earth3': (28, 31, 34, 36),
    'IPSL-CM6A-LR': (103, 110, 137, 151),
#    'MIROC6': (),
    'MPI-ESM1-2-HR': (18, 20, 23, 24),
    'MRI-ESM2-0': (41, 43, 51, 55),
    'NorCPM1': (27, 29, 31, 33),
}
rp_bnds_dict['mswep'] = {
    'BCC-CSM2-MR': (31, 33, 38, 39),
#    'CanESM5': (),
    'CMCC-CM2-SR5': (14, 15, 16, 17),
    'EC-Earth3': (24, 30, 33, 34),
    'IPSL-CM6A-LR': (99, 106, 131, 142),
    'MIROC6': (22, 22, 25, 25),
    'MPI-ESM1-2-HR': (15, 20, 22, 23),
    'MRI-ESM2-0': (37, 40, 47, 50),
    'NorCPM1': (31, 36, 40, 41),
}
rp_bnds_dict['cpc'] = {
    'BCC-CSM2-MR': (286, 314, 443, 494),
#    'CanESM5': (),
    'CMCC-CM2-SR5': (86, 91, 109, 118),
    'EC-Earth3': (1525, 1785, 2810, 3326),
    'IPSL-CM6A-LR': (31768, 41735, 139294, 213667),
    'MIROC6': (156, 165, 203, 220),
    'MPI-ESM1-2-HR': (245, 269, 356, 395),
    'MRI-ESM2-0': (1009, 1213, 2176, 2751),
    'NorCPM1': (10834, 41704, 14083, 29483),
}

sample_size_dict = {
    'BCC-CSM2-MR': 4320,
    'CanESM5': 10260,
    'CMCC-CM2-SR5': 5400,
    'EC-Earth3': 7830,
    'IPSL-CM6A-LR': 5130,
    'MIROC6': 5900,
    'MPI-ESM1-2-HR': 5900,
    'MRI-ESM2-0': 3000,
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

code_url = 'https://github.com/ClimateVHT/unseen-projects/tree/master/project-wcrp-rx5day'
history_log = cmdprov.new_log(code_url=code_url)
global_attrs = {
    'institution': 'CSIRO',
    'method': 'UNSEEN',
    'event': 'Pakistan Floods (short timescale)',
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
        'mswep': '86.1 mm',
        'cpc': '118.3 mm',
        'era5': '83.0 mm',
    }
    
    event = event_dict[obs]
    obs_dataset = obs_dataset_dict[obs]
    intro = f'Extreme value analysis was conducted to calculate the return period (rp) for the 2022 Rx5day value of {event} observed in the {obs_dataset} dataset.'
    rp1 = 'This involved fitting a generalised extreme value (GEV) distribution to the model data using maximum likelihood estimation.'
    rp2 = f'The cumulative distribution function corresponding to the fitted GEV distribution was then used to calculate rp.'
    uncert1 = 'The uncertainty bounds (rp_bnds) were determined by parametric bootstrapping, whereby the GEV distribution was repeatedly randomly sampled (with the same sample size as the model data) to obtain 1000 estimates of rp.'
    uncert2 = 'From these 1000 estimates the 5-95 percentile and 16-84 percentile uncertainty ranges could be calculated.'

    description = f'{intro} {rp1} {rp2} {uncert1} {uncert2}'
    
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

    outdir = f'/g/data/xv83/unseen-projects/outputs/wcrp-rx5day/data'
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
