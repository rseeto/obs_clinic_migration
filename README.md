# Ontario Birth Study Clinic Data Migration
#### -- Project Status: [Completed]

## Project Organization

    ├── LICENSE
    ├── README.md
    ├── data
    │   ├── processed
    │   └── raw
    ├── notebooks
    │   ├── 01_data_migration_overview.ipynb
    |   ├── 02_specific_form_changes.ipynb
    │   └── figures
    |       └── data-import-warning.png
    ├── requirements.txt
    └── obs_clinic_migration
        ├── __init__.py
        ├── double_data_entry_subjects.py
        ├── obs_clinic_migration_preprocessing.py
        ├── obs_clinic_migration.py
        ├── obs_data_sets.py
        └── tests
            ├── __init__.py
            ├── test_obs_clinic_migration_preprocessing.py
            ├── test_obs_clinic_migration.py
            └── test_results.xml

## Project Description

At the inception of the [Ontario Birth Study](http://www.ontariobirthstudy.ca) in 2013, clinical data was stored on  
a [Medidata Rave](https://www.medidata.com/en/products/edc/) database.  Medidata Rave was used as it was believed that the  
Ontario Birth Study data  would be associated with the [Ontario Health Study](https://www.ontariohealthstudy.ca/) on  
an ongoing basis. Since the Ontario Birth Study is no longer associated with the  
Ontario Health Study and there were significant limitations with the Medidata  
Rave database, the Ontario Birth Study decided to move the clinical database  
from Medidata Rave to [REDCap](https://www.project-redcap.org/) in late 2019. This project documents the process  
of migrating data from one electronic data  capture (Medidata Rave) system to  
another (Research Electronic Data Capture; REDCap).  

## Technologies
* Python
    * pandas, numpy, pytest
* Jupyter notebooks
* Medidata Rave
* REDCap

## Featured Notebooks/Analysis/Deliverables
* [notebooks/01_data_migration_overview.ipynb](notebooks/01_data_migration_overview.ipynb): 
    * outlines a broad, comprehensive overview of the process including data  
    manipulation, data cleaning, integration testing, and data verification.
* [notebooks/02_specific_form_changes.ipynb](notebooks/02_specific_form_changes.ipynb): 
    * outlines the specific steps associated with modifying Rave data into a  
    format suitable for REDCap. 

## Contact
* Feel free to contact me for questions regarding this specific project.
* For information about how to access Ontario Birth Study data, you can contact  
them through their [website](http://www.ontariobirthstudy.ca).
