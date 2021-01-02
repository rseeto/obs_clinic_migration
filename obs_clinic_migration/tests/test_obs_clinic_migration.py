# import code to be tested
import pandas as pd
import obs_clinic_migration
import pytest

param_RedcapCov_init = [
    (# stub_repeat = 0; recode_long = True
        {
            'col1': 'incl_main_ga', 
            'col2': 'incl_main_eng'
        },
        0,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002', '10100003', '10100004'],
                'col1': ['Yes', 'Yes', 'No', 'No'], 
                'col2': ['No', 'No', 'Yes', 'Yes']
            }
        ),
        True,
        pd.DataFrame(# expected df
            {
                'obs_id': ['10100001', '10100002', '10100003', '10100004'],
                'incl_main_ga': ['2', '2', '1', '1'], 
                'incl_main_eng': ['1', '1', '2', '2']
            }
        )
    ),
    ( # stub_repeat = 0; recode_long = False
        {
            'col1': 'incl_main_ga', 
            'col2': 'incl_main_eng'
        },
        0,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002', '10100003', '10100004'],
                'col1': ['Yes', 'Yes', 'No', 'No'], 
                'col2': ['No', 'No', 'Yes', 'Yes']
            }
        ),
        False,
        pd.DataFrame(# expected df
            {
                'obs_id': ['10100001', '10100002', '10100003', '10100004'],
                'incl_main_ga': ['Yes', 'Yes', 'No', 'No'], 
                'incl_main_eng': ['No', 'No', 'Yes', 'Yes']
            }
        )
    ),
    (# stub_repeat = 2; recode_long = True
        {
            'col1_': 'incl_main_ga'
        },
        2,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002'],
                'col1_1': ['Yes', 'No'], 
                'col1_2': ['Yes', 'No']
            }
        ),
        True,
        pd.DataFrame(# expected df
            {
                'obs_id': ['10100001', '10100002', '10100001', '10100002'],
                'redcap_repeat_instance': ['1', '1', '2', '2'],
                'incl_main_ga': ['2', '1', '2', '1']
            }
        )
    ),
    (# stub_repeat = 2; recode_long = True
        {
            'col1_': 'incl_main_ga'
        },
        2,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002'],
                'col1_1': ['Yes', 'No'], 
                'col1_2': ['Yes', 'No']
            }
        ),
        False,
        pd.DataFrame(# expected df
            {
                'obs_id': ['10100001', '10100002', '10100001', '10100002'],
                'redcap_repeat_instance': ['1', '1', '2', '2'],
                'incl_main_ga': ['Yes', 'No', 'Yes', 'No']
            }
        )
    ),
]

@pytest.mark.parametrize(
    'ref_dict_1, stub_repeat_1, sample_raw_df_1, recode_bool_1, expected_df_1', 
    param_RedcapCov_init
)

def test_RedcapConv_init_param(
    ref_dict_1, stub_repeat_1, sample_raw_df_1, recode_bool_1, expected_df_1
):
    actual_df = obs_clinic_migration.RedcapConv(
        ravestub_redcap_dict = ref_dict_1, 
        stub_repeat = stub_repeat_1, 
        master_df = sample_raw_df_1,
        recode_long = recode_bool_1
    ).data

    for col_name in actual_df.columns.values.tolist():
        assert all(actual_df[col_name] == expected_df_1[col_name])








def test_pytest_imp():
    assert True






def test_prep_imp():
    assert True

def test_change_str():
    assert True

def test_compare_conv_dde():
    assert True

def test_remove_na():
    assert True

def test_find_cols_issue():
    assert True