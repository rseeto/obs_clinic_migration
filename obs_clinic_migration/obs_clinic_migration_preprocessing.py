"""Functions to preprocess data before calling obs_clinic_migration"""

import numpy as np

def rave_date_unknown(
    rave_df, date_dependency, dependency_answer, rave_date_stub, max_occur_num,
    year_suffix = 'YYYY_', month_suffix = 'MM_', day_suffix = 'DD_'
):
    """Add 'date unavailabe' column to RAVE dataframe.

    The new REDCap database has a column which indicates if date was available
    for some variables. An equivalent column may not exist in the RAVE
    database.

    Parameters
    ----------
    rave_df : pandas.dataframe
        the rave dataframe to be altered
    date_dependency : str
        name of column which can conditionally determine if a date field is
        needed. For example, if the 'MEDHX_NY_' stub (i.e. the date_dependency
        field) is a 'Yes' (i.e. dependency_answer), the subject should have
        values for the associated dates (e.g. date medication started).
        Alternatively, if the subject answers 'No' (i.e. did not take any
        medication), then associated date fields are needed.
    dependency_answer : str
        answer to the date_depencency which will result in the date fields
        needing to be completed.
    rave_date_stub : str
        name of column which which contains the date stub field portion without
        the associated date specifics and iteration. For example, the
        date_dependency field 'MEDHX_NY_' is associated with 'ONSET_YR_'
        (i.e. rave_date_stub). 'ONSET_YR_' will be concatenated with
        year_suffix, month_suffix, or day_suffix, and iterable
        (<= max_occur_num) to determine the associated date field - 'MEDH_NY_1'
        is associated with 'ONSET_YR_YYYY_1', 'ONSET_YR_MM_1', and
        'ONSET_YR_DD_1', respectively.
    max_occur_num : int
        maximum number of occurences of the date_dependency in rave_df
    year_suffix : str, optional
        year suffix that is appended to rave_date_stub, by default 'YYYY_'
    month_suffix : str, optional
        month suffix that is appended to rave_date_stub, by default 'MM_'
    day_suffix : str, optional
        day suffix that is appended to rave_date_stub, by default 'DD_'

    Returns
    -------
    pandas.dataframe
        The rave_df dataframe with modified dates to accomidate the REDCap
        format and the REDCapConversion class. New column called
        (rave_date_stub + '_yn_date_' + iteration) will indicate if data is
        available

    Notes
    -----
    Assumes '99' is the 'don't know' response and a year of '1900' was used to
    signify date unknown

    """

    rave_date_known_col_name = rave_date_stub + 'yn_date_'
    rave_date_year = rave_date_stub + year_suffix
    rave_date_month = rave_date_stub + month_suffix
    rave_date_day = rave_date_stub + day_suffix

    for occur_num in range(1, (max_occur_num + 1)):
        # indicate 'Yes' in the rave_date_known column for instances where a
        # date is available
        rave_df.loc[
            (
                (
                    (rave_df[rave_date_year + str(occur_num)] != '1900')
                    & (rave_df[rave_date_year + str(occur_num)].notna())
                )
                | (rave_df[rave_date_month + str(occur_num)].notna())
                | (rave_df[rave_date_day + str(occur_num)].notna())
            ), (rave_date_known_col_name + str(occur_num))
        ] = 'Yes'
        # indicate 'No' in the rave_date_known column for instances where a
        # date is unavailable
        rave_df.loc[
            (
                (
                    rave_df[
                        date_dependency + str(occur_num)
                    ] == dependency_answer
                )
                & (rave_df[date_dependency + str(occur_num)].notna())
                & (rave_df[rave_date_known_col_name + str(occur_num)].isna())
            ), (rave_date_known_col_name + str(occur_num))
        ] = 'No'
        # indicate '99' (i.e.no data availble) in the rave_date_year column for
        # instances where the year is listed as 1900
        rave_df.loc[
            (
                (rave_df[rave_date_known_col_name + str(occur_num)] == 'Yes')
                & (rave_df[rave_date_year + str(occur_num)] == '1900')
            ), (rave_date_year + str(occur_num))
        ] = '99'
        # np.NaN in the rave_date_year column for instances where the
        # no year data is availble
        rave_df.loc[
            (
                (rave_df[rave_date_known_col_name + str(occur_num)] == 'No')
                & (rave_df[rave_date_year + str(occur_num)] == '1900')
            ), (rave_date_year + str(occur_num))
        ] = np.NaN
        # indicate '99' (i.e.no data availble) in the rave_date_month or
        # rave_date_day column for instances where the data is unavailable
        for date_val in [rave_date_month, rave_date_day]:

            rave_df.loc[
                (
                    (rave_df
                        [
                            rave_date_known_col_name + str(occur_num)
                        ] == 'Yes'
                    )
                    & (rave_df[date_val + str(occur_num)].isna())
                ), (date_val + str(occur_num))
            ] = '99'

    return rave_df


def create_specify_col(
    create_col, coded_col, label_col, label_code, label_ans, rave_df
):
    """Add 'please specify' column to RAVE dataframe

    The new REDCap database has a separate column for 'please specify'. In the
    RAVE database 'please specify' is intermingled in a column with the
    associated labelled data. This function separates the 'please specify'
    answer into a unique column based on the coded column.

    Parameters
    ----------
    create_col : str
        Name of new column created in df.
    coded_col : str
        Name of column containing the coded values.
    label_col : str
        Name of column containing the label values.
    label_code : str
        Coded value that corresponds to the 'please specify' value
    label_ans : str
        Corrected label associated with the 'please specify' value. This value
        will replace the 'please specify' value in the column with the label
        values (label_col). It is expected that the label will have a
        corresponding coded value in the REDCap data dictionary.
    df : pandas.dataframe
        Dataframe the function will be performed on.

    Returns
    -------
    pandas.dataframe
        original pandas.dataframe with a new column (create_col) containing
        relevant data from the original column (label_col); original column
        (label_col) is overwritten with expected value
    """
    # initialize new empty column
    rave_df[create_col] = np.NaN
    # transfer relevant data from the old column (label_col) to the new
    # one (create_col)
    rave_df.loc[rave_df[coded_col] == label_code, create_col] = (
        rave_df[label_col][rave_df[coded_col] == label_code]
    )
    # overwrite data in old column with expected 'please specify' value
    rave_df.loc[rave_df[coded_col] == label_code, label_col] = label_ans

    return rave_df
   