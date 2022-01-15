import pandas as pd
from pathlib import Path
 
rave_clinic = pd.read_csv(
    Path(__file__).parent/"../data/raw/OBS Flat Output 09SEP2019_475.csv",
    encoding = 'mbcs', 
    low_memory = False,
    dtype = str
)

redcap_data_dict = pd.read_csv(
    Path(__file__).parent/"../data/raw/OBSUAT_DataDictionary_2020-05-13.csv",
    low_memory = False,
    dtype = str
) 

redcap_clinic = pd.read_csv(
    Path(__file__).parent/"../data/raw/redcap_double_data_entry.csv",
    encoding = 'mbcs', 
    low_memory = False,
    dtype = str
)