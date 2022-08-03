"""Tests for obs_clinic_migration"""

import pandas as pd
import pytest
import numpy as np
import obs_clinic_migration

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

def test_RedcapConv_init(
    ref_dict_1, stub_repeat_1, sample_raw_df_1, recode_bool_1, expected_df_1
):
    actual_df = obs_clinic_migration.RedcapConv(
        ravestub_redcap_dict = ref_dict_1,
        stub_repeat = stub_repeat_1,
        main_df = sample_raw_df_1,
        recode_long = recode_bool_1
    ).data

    for col_name in actual_df.columns.values.tolist():
        assert all(actual_df[col_name] == expected_df_1[col_name])

def test_change_str():
    actual = obs_clinic_migration.RedcapConv(
        ravestub_redcap_dict = {
            'col1': 'incl_main_ga',
            'col2': 'incl_main_eng'
        },
        stub_repeat = 0,
        main_df = pd.DataFrame(
            {
                'Subject': ['10100001', '10100002', '10100003', '10100004'],
                'col1': ['Yes', 'Yes', 'NO', 'Noo'],
                'col2': ['No', 'No', 'Yes', 'YES']
            }
        ),
        recode_long = True
    )
    expected_unchanged_df = pd.DataFrame(
        {
            'obs_id': ['10100001', '10100002', '10100003', '10100004'],
            'incl_main_ga': ['2', '2', 'NO', 'Noo'],
            'incl_main_eng': ['1', '1', '2', 'YES']
        }
    )
    # check that data is initially incorrect
    for col_name in actual.data.columns.values.tolist():
        assert all(actual.data[col_name] == expected_unchanged_df[col_name])
    actual.change_str({
        'incl_main_ga': {
            'Noo': 'No',
            'NO': 'No'
        },
        'incl_main_eng': {
            'YES': 'Yes'
        }
    })
    expected_changed_df = pd.DataFrame(
        {
            'obs_id': ['10100001', '10100002', '10100003', '10100004'],
            'incl_main_ga': ['2', '2', '1', '1'],
            'incl_main_eng': ['1', '1', '2', '2']
        }
    )
    # check that data is corrected
    for col_name in actual.data.columns.values.tolist():
        assert all(actual.data[col_name] == expected_changed_df[col_name])

param_remove_na = [
    (# replace np.NaN
        {
            'col1': 'incl_main_ga',
            'col2': 'incl_main_eng'
        },
        0,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002', '10100003', '10100004'],
                'col1': ['Yes', 'Yes', 'No', np.NaN],
                'col2': ['No', 'No', 'Yes', np.NaN]
            }
        ),
        True,
        pd.DataFrame(# expected df
            {
                'obs_id': ['10100001', '10100002', '10100003'],
                'incl_main_ga': ['2', '2', '1'],
                'incl_main_eng': ['1', '1', '2']
            }
        )
    ),
    (# replace '0'
        {
            'col1': 'incl_main_ga',
            'col2': 'incl_main_eng'
        },
        0,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002', '10100003', '10100004'],
                'col1': ['Yes', 'Yes', 'No', '0'],
                'col2': ['No', 'No', 'Yes', '0']
            }
        ),
        True,
        pd.DataFrame(# expected df
            {
                'obs_id': ['10100001', '10100002', '10100003'],
                'incl_main_ga': ['2', '2', '1'],
                'incl_main_eng': ['1', '1', '2']
            }
        )
    ),
    (# replace np.NaN and '0'
        {
            'col1': 'incl_main_ga',
            'col2': 'incl_main_eng'
        },
        0,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002', '10100003', '10100004'],
                'col1': ['Yes', 'Yes', 'No', np.NaN],
                'col2': ['No', 'No', 'Yes', '0']
            }
        ),
        True,
        pd.DataFrame(# expected df
            {
                'obs_id': ['10100001', '10100002', '10100003'],
                'incl_main_ga': ['2', '2', '1'],
                'incl_main_eng': ['1', '1', '2']
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
                'col1_2': ['Yes', np.NaN]
            }
        ),
        True,
        pd.DataFrame(# expected df
            {
                'obs_id': ['10100001', '10100002', '10100001'],
                'redcap_repeat_instance': ['1', '1', '2'],
                'incl_main_ga': ['2', '1', '2']
            }
        )
    )
]

@pytest.mark.parametrize(
    'ref_dict_2, stub_repeat_2, sample_raw_df_2, recode_bool_2, expected_df_2',
    param_remove_na
)

def test_remove_na(
    ref_dict_2, stub_repeat_2, sample_raw_df_2, recode_bool_2, expected_df_2
):
    actual = obs_clinic_migration.RedcapConv(
        ravestub_redcap_dict = ref_dict_2,
        stub_repeat = stub_repeat_2,
        main_df = sample_raw_df_2,
        recode_long = recode_bool_2
    )
    actual.remove_na()
    actual_df = actual.data

    for col_name in actual_df.columns.values.tolist():
        assert all(actual_df[col_name] == expected_df_2[col_name])

param_compare_conv_dde = [
    (# successful conversion, no columns ignored
        {
            'col1': 'incl_main_ga',
            'col2': 'incl_main_eng',
            'col3': 'incl_main_age',
        },
        0,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002', '10100003', '10100004'],
                'col1': ['Yes', 'Yes', 'No', 'No'],
                'col2': ['No', 'No', 'Yes', 'Yes'],
                'col3': ['Yes', 'No', 'Yes', 'Yes']
            }
        ),
        True,
        pd.DataFrame(# redcap double data entry
            {
                'obs_id': ['10100001', '10100002', '10100003', '10100004'],
                'incl_main_ga': ['2', '2', '1', '1'],
                'incl_main_eng': ['1', '1', '2', '2'],
                'incl_main_age': ['2', '1', '2', '2']
            }
        ),
        [],
        pd.DataFrame(# expected df
            {
                'obs_id': [],
                'incl_main_ga': [],
                'incl_main_eng': [],
                'incl_main_age': [],
                'Source': []
            }
        )
    ),
    (# successful conversion, 2 columns ignored
        {
            'col1': 'incl_main_ga',
            'col2': 'incl_main_eng',
            'col3': 'incl_main_age',
        },
        0,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002', '10100003', '10100004'],
                'col1': ['Yes', 'Yes', 'No', 'No'],
                'col2': ['No', 'No', 'Yes', 'Yes'],
                'col3': ['Yes', 'No', 'Yes', 'Yes']
            }
        ),
        True,
        pd.DataFrame(# redcap double data entry
            {
                'obs_id': ['10100001', '10100002', '10100003', '10100004'],
                'incl_main_ga': ['2', '2', '1', '1'],
                'incl_main_eng': ['1', '1', '2', '2'],
                'incl_main_age': ['2', '1', '2', '2']
            }
        ),
        ['incl_main_eng', 'incl_main_age'],
        pd.DataFrame(# expected df
            {
                'obs_id': [],
                'incl_main_ga': [],
                'Source': []
            }
        )
    ),
    (# successful conversion after ignoring column
        {
            'col1': 'incl_main_ga',
            'col2': 'incl_main_eng',
            'col3': 'incl_main_age',
        },
        0,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002', '10100003', '10100004'],
                'col1': ['Yes', 'Yes', 'No', 'No'],
                'col2': ['No', 'No', 'Yes', 'Yes'],
                'col3': ['Yes', 'No', 'Yes', 'Yes']
            }
        ),
        True,
        pd.DataFrame(# redcap double data entry
            {
                'obs_id': ['10100001', '10100002', '10100003', '10100004'],
                'incl_main_ga': ['2', '2', '1', '1'],
                'incl_main_eng': ['1', '1', '2', '2'],
                'incl_main_age': ['2', '1', '2', '1'] # different last value
            }
        ),
        ['incl_main_age'],
        pd.DataFrame(# expected df
            {
                'obs_id': [],
                'incl_main_ga': [],
                'incl_main_eng': [],
                'Source': []
            }
        )
    ),
    (# unsuccessful conversion, no columns ignored
        {
            'col1': 'incl_main_ga',
            'col2': 'incl_main_eng',
            'col3': 'incl_main_age',
        },
        0,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002', '10100003', '10100004'],
                'col1': ['Yes', 'Yes', 'No', 'No'],
                'col2': ['No', 'No', 'Yes', 'Yes'],
                'col3': ['Yes', 'No', 'Yes', 'Yes']
            }
        ),
        True,
        pd.DataFrame(# redcap double data entry
            {
                'obs_id': ['10100001', '10100002', '10100003', '10100004'],
                'incl_main_ga': ['2', '2', '1', '1'],
                'incl_main_eng': ['1', '1', '2', '2'],
                'incl_main_age': ['2', '1', '2', '1'] # different last value
            }
        ),
        [],
        pd.DataFrame(# expected df
            {
                'obs_id': ['10100004', '10100004'],
                'incl_main_ga': ['1', '1'],
                'incl_main_eng': ['2', '2'],
                'incl_main_age': ['1', '2'], # different last value
                'Source': ['REDCapDDE', 'RaveConverted']
            }
        )
    ),
    (# unsuccessful conversion, columns ignored
        {
            'col1': 'incl_main_ga',
            'col2': 'incl_main_eng',
            'col3': 'incl_main_age',
        },
        0,
        pd.DataFrame(# pandas sample raw df
            {
                'Subject': ['10100001', '10100002', '10100003', '10100004'],
                'col1': ['Yes', 'Yes', 'No', 'No'],
                'col2': ['No', 'No', 'Yes', 'Yes'],
                'col3': ['Yes', 'No', 'Yes', 'Yes']
            }
        ),
        True,
        pd.DataFrame(# redcap double data entry
            {
                'obs_id': ['10100001', '10100002', '10100003', '10100004'],
                'incl_main_ga': ['2', '2', '1', '1'],
                'incl_main_eng': ['1', '1', '2', '2'],
                'incl_main_age': ['2', '1', '2', '1'] # different last value
            }
        ),
        ['incl_main_eng'],
        pd.DataFrame(# expected df
            {
                'obs_id': ['10100004', '10100004'],
                'incl_main_ga': ['1', '1'],
                'incl_main_age': ['1', '2'], # different last value
                'Source': ['REDCapDDE', 'RaveConverted']
            }
        )
    ),
]

@pytest.mark.parametrize(
    (
        'ref_dict_3, stub_repeat_3, sample_raw_df_3, recode_bool_3, '
        'redcap_dde_3, additional_ignore_cols_3, expected_df_3'
    ), param_compare_conv_dde
)

def test_compare_conv_dde(
    ref_dict_3, stub_repeat_3, sample_raw_df_3, recode_bool_3, redcap_dde_3,
    additional_ignore_cols_3, expected_df_3
):
    initialized_class = obs_clinic_migration.RedcapConv(
        ravestub_redcap_dict = ref_dict_3,
        stub_repeat = stub_repeat_3,
        main_df = sample_raw_df_3,
        recode_long = recode_bool_3
    )
    actual_df = initialized_class.compare_conv_dde(
        redcap_dde = redcap_dde_3,
        additional_ignore_cols = additional_ignore_cols_3
    )
    # don't care about index
    actual_df.reset_index(drop=True, inplace=True)

    for col_name in actual_df.columns.values.tolist():
        assert all(actual_df[col_name] == expected_df_3[col_name])

param_prep_imp = [
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
        'test_event_name',
        'test_complete_col',
        None,
        pd.DataFrame(# expected df
            {
                'redcap_event_name': ['test_event_name'] * 4,
                'test_complete_col': ['2'] * 4,
            }
        ),
        [ # expected columns
            'obs_id', 'incl_main_ga', 'incl_main_eng',
            'redcap_event_name', 'test_complete_col'
        ]
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
        'test_event_name',
        'test_complete_col',
        'test_repeat_instrument',
        pd.DataFrame(# expected df
            {
                'redcap_event_name': ['test_event_name'] * 4,
                'test_complete_col': ['2'] * 4,
                'redcap_repeat_instrument': ['test_repeat_instrument'] * 4
            }
        ),
        [ # expected columns
            'obs_id', 'redcap_repeat_instance', 'incl_main_ga',
            'redcap_event_name', 'test_complete_col',
            'redcap_repeat_instrument'
        ]
    )
]

@pytest.mark.parametrize(
    (
        'ref_dict_4, stub_repeat_4, sample_raw_df_4, recode_bool_4, '
        'event_name_4, complete_col_4, repeat_instrument_4, expected_df_4, '
        'expected_cols_4'
    ), param_prep_imp
)

def test_prep_imp(
    ref_dict_4, stub_repeat_4, sample_raw_df_4, recode_bool_4, event_name_4,
    complete_col_4, repeat_instrument_4, expected_df_4, expected_cols_4
):
    actual = obs_clinic_migration.RedcapConv(
        ravestub_redcap_dict = ref_dict_4,
        stub_repeat = stub_repeat_4,
        main_df = sample_raw_df_4,
        recode_long = recode_bool_4
    )
    actual.prep_imp(
        event_name = event_name_4,
        complete_col = complete_col_4,
        repeat_instrument = repeat_instrument_4
    )
    actual_df = actual.data

    for col_name in expected_df_4.columns.values.tolist():
        assert all(actual_df[col_name] == expected_df_4[col_name])
    assert actual_df.columns.tolist() == expected_cols_4
