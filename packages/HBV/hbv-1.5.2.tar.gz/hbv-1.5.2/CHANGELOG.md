### v1.0.0 
- working basic version after various [testing versions](https://test.pypi.org/project/HBV/)
#### v1.0.1 - v1.0.3 
- various bug fixes etc. (last time using live as a dev branch -> bad practice)
### v1.1.0 
- added support for updating memory vector on the fly for Data assimilation.
#### V1.1.1
- bug fix in `T_lag` value: can now only be set an integer larger than 1: otherwise makes no physical sense
- bug fix where wrong types were given, warning messages cleaned up and code attempted to be made more readable
### V1.2.0
- pretty big issue with setting values fixed - won't affect most use but will cause issues for Data Assimilation
- use opportunity to name all HBV packages/naming/images to 1.2.0 
## V1.3.0
- Change `Q_m` to `Q` in order to better integrate data assimilation & just makes more sense. 
### v1.3.1
- Fix bug in time indexing
### v1.3.2
- typo in update updating_dict_var_obj: was getting values wrong 
## V1.4.0
- adding snow reservoir
### V1.4.1
- bug fix in naming of values 
## v1.5.0
- Refactor potential evaporation from `pev` to `evspsblpot` & `tasmean` to `tas` to match convention
### v1.5.1
- Groundwater and overland flow now can no longer be negative   
### v1.5.2
- now loads forcing as xarray and then immediately stores the values as numpy arrays in memory. This might be less 
efficient as xarray takes care of lazy loading in the background. 
But on long runs using data assimilation the lazy loading seemed to cause issues
