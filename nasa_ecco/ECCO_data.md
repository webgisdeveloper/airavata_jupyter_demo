# ECCO Data
## ECCO input data to run the model

The forcing and other input files are stored on Release 4’s data server at  
https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/  
The total size of the forcing and other input files is about 200GB.   
All forcing and input files are necessary to reproduce Release 4.  
* Input forcing: https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_forcing   
[Input forcing Readme](https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_forcing/README)
```
- This directory contains the 'ECCO version 4, release 4' atmospheric forcing that is the sum of ERA-Interim 
   and atmospheric control adjustment. 
  README                            This file
  eccov4r4_dlw_YYYY                 downward longwave radiation (W/m^2)
  eccov4r4_dsw_YYYY                 downward shortwave radiation (W/m^2)
  eccov4r4_pres_YYYY                air pressure (N/m^2)
  eccov4r4_rain_YYYY                precipitation (m/s)
  eccov4r4_spfh2m_YYYY              near-surface atmospheric specific humidity (kg/kg)
  eccov4r4_tmp2m_degC_YYYY          near-surface air temperature (degC)
  eccov4r4_ustr_YYYY                zonal wind stress (N/m^2)
  eccov4r4_vstr_YYYY                meridional wind stress (N/m^2)
  eccov4r4_wspeed_YYYY              near-surface wind speed (m/s)

- Each forcing file is a yearly file with 6-hourly records (3Z, 9Z, 15Z, and 21Z) on native
   ECCO v4 grid. YYYY is for a particular year from 1992 to 2015. Because wind speed is 
   not part of the control variables, eccov4r4_wspeed_YYYY contains no wind speed 
   control adjustment. 
```
* Input init: https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_init   
[Input init Readme](https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_init/README)  
```
- This directory contains binary files needed to initialize MITgcm to run 'ECCO version 4, release 4':
  README                               This file
  pickup*.data                         initial condition
  bathy_eccollc_90x50_min2pts.bin      bathymetry 
  geothermalFlux.bin                   geothermal heating (time-mean climatology)
  runoff*.bin                          river runoff (monthly climatology)
  smooth*                              settings for MITgcm/pkg/smooth
  fenty_biharmonic_visc_v11.bin        biharmonic viscosity 
  total_diffkr_r009bit11.bin           vert. diff. of release 1 (this field plus xx is the total)
  total_kapgm_r009bit11.bin            Kappa GM of release 1 (this field plus xx is the total)
  total_kapredi_r009bit11.bin          Kappa Redi of release 1 (this field plus xx is the total)
  xx_*.*                               control adjustments 
  NAMELIST                             namelists
  error_weight                         control weights and data errors
```
* Input ecco: https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_ecco   
[Input ecco Readme](https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_ecco/README)
```
- This directory contains the 'ECCO version 4, release 4' observation input:
  README                            This file
  input_bp                          ocean bottom pressure
  input_insitu                      in situ profiles
  input_nsidc                       sea-ice concentration
  input_other                       other observations
  input_sla                         altimetry data
  input_sss                         Aquarius sea surface salinity
  input_sst                         sea surface temperature
```
 
While the requested time of 24 hours is usually sufficient
to finish V4r4’s 26-year model integration time period on [Pleiades Supercomputer](https://www.nas.nasa.gov/hecc/resources/pleiades.html), with the
provided [data.diagnostics files](https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_init/NAMELIST/data.diagnostics), one may have to increase the time if to run the
job on a different machine or to output significantly more model diagnostics. [Available_Diagnostics](https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/doc/available_diagnostics.log)  

reference: [V4r4 Reproduction Guide](https://ecco-group.org/docs/v4r4_reproduction_howto.pdf)
## ECCO output data
