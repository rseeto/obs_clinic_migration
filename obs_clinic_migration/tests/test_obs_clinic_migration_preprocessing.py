import pandas as pd
import obs_clinic_migration_preprocessing
import pytest
import numpy as np

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
      df = test_df  
    )

    expected_df = pd.DataFrame(# expected df
        {
            'df_label_col': ['coded_1', 'coded_2', 'other', 'other'],
            'df_code_col': ['1', '2', '99', '99'],
            'new_specify_col': [np.NaN, np.NaN, 'uncoded', 'uncoded']
        }
    )
    # does not check data type due to np.NaN == np.NaN returning false
    for col_name in actual_df.columns.values.tolist():
        assert all(
            actual_df[col_name].astype('str') == (
                expected_df[col_name].astype('str')
            )
        )