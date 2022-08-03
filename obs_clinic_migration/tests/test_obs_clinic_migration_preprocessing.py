"""Tests for obs_clinic_migration_preprocessing"""

import pandas as pd
import obs_clinic_migration_preprocessing
import numpy as np

def test_rave_date_unknown():
    test_df = pd.DataFrame(
        {
            'date_dependency_col_1': ['No', 'Yes'],
            'date_stub_YYYY_1': ['2000', '1900'],
            'date_stub_MM_1': ['1', np.NaN],
            'date_stub_DD_1': ['1', np.NaN],
            'date_dependency_col_2': ['No', 'Yes'],
            'date_stub_YYYY_2': ['2000', '99'],
            'date_stub_MM_2': ['1', np.NaN],
            'date_stub_DD_2': ['1', np.NaN],
            'date_dependency_col_3': ['No', 'Yes'],
            'date_stub_YYYY_3': ['2000', '2000'],
            'date_stub_MM_3': ['1', '1'],
            'date_stub_DD_3': ['1', '1'],
        }
    )
    actual_df = obs_clinic_migration_preprocessing.rave_date_unknown(
        rave_df = test_df,
        date_dependency = 'date_dependency_col_',
        dependency_answer = 'Yes',
        rave_date_stub = 'date_stub_',
        max_occur_num = 3
    )
    expected_df = pd.DataFrame(
        {
            'date_dependency_col_1': ['No', 'Yes'],
            'date_stub_YYYY_1': ['2000', np.NaN],
            'date_stub_MM_1': ['1', np.NaN],
            'date_stub_DD_1': ['1', np.NaN],
            'date_dependency_col_2': ['No', 'Yes'],
            'date_stub_YYYY_2': ['2000', '99'],
            'date_stub_MM_2': ['1', '99'],
            'date_stub_DD_2': ['1', '99'],
            'date_dependency_col_3': ['No', 'Yes'],
            'date_stub_YYYY_3': ['2000', '2000'],
            'date_stub_MM_3': ['1', '1'],
            'date_stub_DD_3': ['1', '1'],
            'date_stub_yn_date_1': ['Yes', 'No'],
            'date_stub_yn_date_2': ['Yes', 'Yes'],
            'date_stub_yn_date_3': ['Yes', 'Yes'],
        }
    )
    assert actual_df.equals(expected_df)

def test_create_specify_col():
    test_df = pd.DataFrame(
        {
            'df_label_col': ['coded_1', 'coded_2', 'uncoded', 'uncoded'],
            'df_code_col': ['1', '2', '99', '99'],
        }
    )

    actual_df = obs_clinic_migration_preprocessing.create_specify_col(
      create_col = 'new_specify_col',
      coded_col = 'df_code_col',
      label_col = 'df_label_col',
      label_code = '99',
      label_ans = 'other',
      rave_df = test_df
    )

    expected_df = pd.DataFrame(# expected df
        {
            'df_label_col': ['coded_1', 'coded_2', 'other', 'other'],
            'df_code_col': ['1', '2', '99', '99'],
            'new_specify_col': [np.NaN, np.NaN, 'uncoded', 'uncoded']
        }
    )
    assert actual_df.equals(expected_df)
