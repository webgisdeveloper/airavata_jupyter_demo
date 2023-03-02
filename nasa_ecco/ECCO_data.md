# ECCO Data
## ECCO input data to run the model

The forcing and other input files are stored on Release 4’s data server at  
https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/  
The total size of the forcing and other input files is about 200GB.   
All forcing and input files are necessary to reproduce Release 4.  
* Input forcing: https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_forcing 
* Input init: https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_init 
* Input ecco: https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_ecco   
 
While the requested time of 24 hours is usually sufficient
to finish V4r4’s 26-year model integration time period on [Pleiades Supercomputer](https://www.nas.nasa.gov/hecc/resources/pleiades.html), with the
provided [data.diagnostics files](https://ecco.jpl.nasa.gov/drive/files/Version4/Release4/input_init/NAMELIST/data.diagnostics), one may have to increase the time if to run the
job on a different machine or to output significantly more model diagnostics. 

reference: [V4r4 Reproduction Guide](https://ecco-group.org/docs/v4r4_reproduction_howto.pdf)
## ECCO output data
