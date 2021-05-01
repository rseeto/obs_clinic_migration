import pandas as pd
from pathlib import Path


# # https://stackoverflow.com/questions/40416072/reading-file-using-relative-path-in-python-project/40416154
# path = Path(__file__).parent / "../data/test.csv"
# print(path)
  
rave_clinic = pd.read_csv(
    #'D:/Downloads/WorkFromHome/OBS Flat Output 09SEP2019_475.csv', 
    Path(__file__).parent/"../../data/raw/OBS Flat Output 09SEP2019_475.csv",
    encoding = 'mbcs', 
    low_memory = False,
    dtype = str # temporary addition, see if this is causing issues
)


redcap_data_dict = pd.read_csv(
    # (
    #     'D:/Downloads/WorkFromHome/obs_data_migration/clinic/data/'
    #      #'OBS_DataDictionary_2019-08-20.csv'
    #      'OBSUAT_DataDictionary_2020-05-13.csv'
    # ),
    
    Path(__file__).parent/"../../data/raw/OBSUAT_DataDictionary_2020-05-13.csv", 
    #encoding = 'mbcs', 
    low_memory = False,
    dtype = str,
    #sep = ',',
    #quotechar='"'
) 

redcap_clinic = pd.read_csv(
    Path(__file__).parent/"../../data/raw/redcap_double_data_entry.csv",
    encoding = 'mbcs', 
    low_memory = False,
    dtype = str # temporary addition, see if this is causing issues
)