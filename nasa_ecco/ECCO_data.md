# ECCO Data
## ECCO input data to run the model

The forcing and other input files are stored on Release 4’s data server at  
https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/  
The total size of the forcing and other input files is about 200GB.   
All forcing and input files are necessary to reproduce Release 4.  
* Input forcing: https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_forcing   
[Input Forcing Readme](https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_forcing/README)
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
* Input ecco: https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_ecco   
 
While the requested time of 24 hours is usually sufficient
to finish V4r4’s 26-year model integration time period on [Pleiades Supercomputer](https://www.nas.nasa.gov/hecc/resources/pleiades.html), with the
provided [data.diagnostics files](https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_init/NAMELIST/data.diagnostics), one may have to increase the time if to run the
job on a different machine or to output significantly more model diagnostics. 

reference: [V4r4 Reproduction Guide](https://ecco-group.org/docs/v4r4_reproduction_howto.pdf)
## ECCO output data
