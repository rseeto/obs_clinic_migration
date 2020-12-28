  import pandas as pd         

def rave_date_unknown(
    rave_df,
    date_dependency,
    dependency_answer,
    rave_date_stub,
    max_occur_num,
    year_suffix = 'YYYY_',
    month_suffix = 'MM_',
    day_suffix = 'DD_',
      
):
    """Add 'date unavailabe' column to RAVE dataframe.
    
    The new REDCap database has a column which indicates if date was available 
    for some variables. An equivalent column may not exist in the RAVE 
    database.
    
    Args:
        rave_df: the rave dataframe to be altered
        date_dependency: the answer to a previous question may dictate if the 
            associateddate fields are completed; date_dependency indicates 
            this field
        dependency_answer: answer to the date_depencency which will result in 
            the date fields needing to be completed. For example, if the 
            'MEDHX_NY_' stub (i.e. the date_dependency field) is a 'Yes' (i.e. 
            dependency_answer), the subject should have values for the 
            associated dates
        rave_date_stub: variable name which contains the date stub field 
            portion without the associated date specifics and iteration. For
            example, the date_ependency field 'MEDHX_NY_' is associated with 
            'ONSET_YR_' (i.e. rave_date_stub). 'ONSET_YR_' will be concatenated
            with year_suffix, month_suffix, or day_suffix, and iterable 
            (<= max_occur_num) to determine the associated date field - 
            'MEDH_NY_1' is associated with 'ONSET_YR_YYYY_1', 'ONSET_YR_MM_1', 
            and 'ONSET_YR_DD_1', respectively.
        max_occur_num: maximum number of occurences for the particular 
        year_suffix: year suffix that is appended to rave_date_stub
        month_suffix: month suffix that is appended to rave_date_stub
        day_suffix: day suffix that is appended to rave_date_stub
    
    Returns:
        The rave_df dataframe with modified dates to accomidate the REDCap 
        format and the REDCapConversion class. New column called 
        (rave_date_stub + '_yn_date_' + iteration) will indicate if data 
        is available
    
    Notes:
        Assumes a year of '1900' was used to signify date unknown
        Assumes '99' is the 'don't know' response
    
    """
    
    rave_date_known_col_name = rave_date_stub + 'yn_date_'
    rave_date_year = rave_date_stub + year_suffix
    rave_date_month = rave_date_stub + month_suffix
    rave_date_day = rave_date_stub + day_suffix
    
    
    
    for occur_num in range(1, (max_occur_num + 1)):
        rave_df.loc[
            (
                (
                    (rave_df[rave_date_year + str(occur_num)] != '1900')
                    & (rave_df[rave_date_year + str(occur_num)].notna())
                )
                | (rave_df[rave_date_month + str(occur_num)].notna())
                | (rave_df[rave_date_day + str(occur_num)].notna())
            ),
            (rave_date_known_col_name + str(occur_num))     
        ] = 'Yes'
        
        
        rave_df.loc[
            (
                (rave_df[date_dependency + str(occur_num)] == dependency_answer)
                & (rave_df[date_dependency + str(occur_num)].notna())
                & (rave_df[rave_date_known_col_name + str(occur_num)].isna())
            ),
            (rave_date_known_col_name + str(occur_num))     
        ] = 'No'
        
        
        rave_df.loc[
            (
                (
                    (rave_df[rave_date_known_col_name + str(occur_num)] == 'Yes')
                    & (rave_df[rave_date_year + str(occur_num)] == '1900')
                )
            ),
            (rave_date_year + str(occur_num))
        ] = '99'
        
        rave_df.loc[
            (
                (
                    (rave_df[rave_date_known_col_name + str(occur_num)] == 'No')
                    & (rave_df[rave_date_year + str(occur_num)] == '1900')
                )
            ),
            (rave_date_year + str(occur_num))
        ] = np.NaN
    
        for date_val in [rave_date_month, rave_date_day]:
                rave_df.loc[
                    (
                        (
                            (rave_df[rave_date_known_col_name + str(occur_num)] == 'Yes')
                            & (rave_df[date_val + str(occur_num)].isna())
                        )
                    ),
                    (date_val + str(occur_num))
                ] = '99'
    
    return rave_df
            
            
            # for obs_id in compare_df['obs_id'].unique():
            #     redcap_clinic_sub_id = redcap_clinic.loc[
            #         redcap_clinic['obs_id'].isin([obs_id]),
            #     ]
                

            #     for eval_col in eval_cols:
            #         eval_ignore_cols = ignore_cols + [eval_col]
                    
            #         if self.compare_conv_dde(
            #             redcap_clinic_sub_id, 
            #             eval_ignore_cols
            #         ).empty:
                        
                        
            #             print(str(obs_id), ": ", str(eval_col))
            #             print("Subject '{}' has an issue with the column '{}'.".format(obs_id, eval_col))



def create_specify_col(
        create_col, coded_col, label_col, label_code, label_ans,
        df = rave_clinic
):
    '''
    Add 'please specify' column to RAVE dataframe
    
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
        Coded value that corresponds to the'please specify' value
    label_ans : str
        Corrected label associated with the 'please specify' value. This value 
        will replace the 'please specify' value in the column with the label 
        values (label_col). It is expected that the label will have a 
        corresponding coded value in the REDCap data dictionary.
    df : pandas.dataframe, optional
        Dataframe the function will be performed on. The default is 
        rave_clinic.

    Returns
    -------
    None.

    '''
    
    # try:
    #     df[create_col] = np.where(
    #         df[coded_col] == label_code, 
    #         df.loc[
    #             df[coded_col] == label_code, 
    #             label_col
    #         ], 
    #         np.NaN
    #     )
    #     df.loc[
    #         df[coded_col] == label_code,
    #         label_col
    #     ] = label_ans
    # except:
    #     df[create_col] = np.NaN
        
    df[create_col] = np.NaN
    df.loc[
        df[coded_col] == label_code,
        create_col
    ] = df[label_col][
        df[coded_col] == label_code
    ]
        
    df.loc[
        df[coded_col] == label_code,
        label_col
    ] = label_ans
    
    return df
   