# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:41:45 2020

@author: Ryan Seeto
"""

# import requests
# import io
# import re
# import glob
# import os
# import pyodbc
import pandas as pd
import numpy as np


class RedcapConv:
    
    def __init__(
        self, ravestub_redcap_dict, stub_repeat, master_df = rave_clinic, 
        redcap_data_dict = redcap_data_dict, recode_long = True
    ):
        """Apply criteria to data set
        [summary]

        Args:
            ravestub_redcap_dict ([type]): [description]
            stub_repeat ([type]): [description]
            master_df ([type], optional): [description]. Defaults to rave_clinic.
            redcap_data_dict ([type], optional): [description]. Defaults to redcap_data_dict.
            recode_long (bool, optional): [description]. Defaults to True.
        """
        if stub_repeat == 0:
            rave_long = self._rave_single(ravestub_redcap_dict, master_df)
        elif stub_repeat > 0:
            rave_long = self._rave_wide_long(
                ravestub_redcap_dict, stub_repeat, master_df
            )
 
        if recode_long:
            self.data = self._recoded_based_redcap_data_dict(
    #            ravestub_redcap_dict.values(), 
                data_dict_df = redcap_data_dict, 
                rave_long = rave_long
            )
        else:
            self.data = rave_long

# use 'where' method to modify 'redcap_data_access_group'??? maybe another method
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.where.html


        
    @staticmethod
    def _rave_wide_long(ravestub_redcap_dict, stub_repeat, master_df ):
        """Convert RAVE dataframe from wide to long with 2 or more occurences
        
        
        LONGER DESCRIPTION
        
        
        
        
        Args:
            ravestub_redcap_dict: dictionary which maps the RAVE stub columns 
                (keys) to the REDCap columns (values)
            stub_repeat: Maximum number of repeats expected For example, if 
                stub_repeat = 2, expecting column_x_1 and column_x_2 in RAVE
                dataframe.
            master_df: Dataframe containing the RAVE data to be manipulated.
                It is expected the dataframe is in the wide format.
        
        Returns:
            A long dataframe converted from the wide RAVE dataframe. The 
            dataframe should only contain the columns in the VALUES ARGUMENT 
            with the addition of 'obs_id' and 'redcap_repeat_instance'. Column
            values are in 'label' format as opposed to coded as an 'integer'.
        
        Comments:
        # https://stackoverflow.com/questions/50087135/convert-dataframe-from-wide-to-long-pandas
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.wide_to_long.html
        
        # used the 'labels' fields, as opposed to the 'raw/coded' fields to minimize 
        # errors in transcription
        """
     
        # create list of column names including iterations of stub 
        # (e.g. COL_1, COL_2)
        df_cols = ['Subject']
        for i in range(1, (stub_repeat + 1)):
            for stub_name in ravestub_redcap_dict.keys():
                df_cols.append(stub_name + str(i))
                
        sub_df = master_df.loc[:, df_cols]
        sub_df = (pd.wide_to_long(
            sub_df, 
            stubnames = ravestub_redcap_dict.keys(), 
            i = 'Subject', 
            j = 'redcap_repeat_instance'
        ).reset_index())
        
        
        # remove blank rows after ignoring 'Subject', and 
        # 'redcap_repeat_instance'
        sub_df_cols = [
            col_name 
            for col_name in list(sub_df)
            if col_name not in ['Subject', 'redcap_repeat_instance']
        ]
        sub_df.dropna(subset = sub_df_cols, thresh = 1, inplace = True) 

        # check to see if manipulated file contains the same number of instances 
        # as function argument
        if (sub_df['redcap_repeat_instance'].max() != stub_repeat):
            
            # insert warning instead of exception
            
            # throw exception???? if issue with stubs and number of repeats
            print(
                'max redcap_repeat_instance = ' 
                 + str(sub_df['redcap_repeat_instance'].max())
                 + '; stub_repeat = ' + str(stub_repeat))

        sub_df.rename(columns = ravestub_redcap_dict, inplace = True)
        sub_df.rename(columns = {'Subject': 'obs_id'}, inplace = True)
        
        return sub_df
    
    
# separating redcap and rave columns instead of in one dictionary    
#    @staticmethod
#    def _rave_single(stubnames, redcapnames, master_df):
#        """Single instance RAVE conversion
#        
#        """
#        
#        '''
#        convert RAVE data containing only a single instance
#        '''
#        
#        rave_cols = ['Subject']
#        rave_cols.extend(stubnames)
#         
#        sub_df = master_df.loc[:, rave_cols]
#        
#        redcap_cols = ['obs_id']
#        redcap_cols.extend(redcapnames)
#        
#        rename_dict = dict(zip(rave_cols, redcap_cols))
#        
#        sub_df.rename(columns = rename_dict, inplace = True)
#        
#        return rename_dict, sub_df


    @staticmethod
    def _rave_single(ravestub_redcap_dict, master_df):
        """Single instance RAVE conversion
        
        obtains associated RAVE columns
        does not record them????
        
        """
        
        '''
        convert RAVE data containing only a single instance
        '''
        ravestub_redcap_dict['Subject'] = 'obs_id'
#        rave_cols = ['Subject']
#        rave_cols.extend(ravestub_redcap_dict.keys())
#         
        sub_df = master_df.loc[:, ravestub_redcap_dict.keys()]
#        
#        redcap_cols = ['obs_id']
#        redcap_cols.extend(redcapnames)
#        
#        rename_dict = dict(zip(rave_cols, redcap_cols))
        
        sub_df.rename(columns = ravestub_redcap_dict, inplace = True)

#        return rename_dict, sub_df        
        return sub_df

                

    
    
    
    
    
     
        
        
        
        
        # can I remove 'redcapnames' and just derive it from rave_long.columns.values.to_list()?
    def _recoded_based_redcap_data_dict(
            self, rave_long, data_dict_df = redcap_data_dict
    ):
        """Recode RAVE long dataframe based on REDcap data dictionary
        
        
        changes values in df (self.data) columns based on variable coding in the REDCap data dictionary
        
        Args:
            
        Notes: 
            Known issue with '.to_string' method, need to set max_colwidth
            https://github.com/pandas-dev/pandas/issues/9784 
        """
        
        
        redcap_var_names = [
            col_name 
            for col_name in rave_long.columns.values.tolist()
            if col_name not in ['obs_id', 'redcap_repeat_instance']
        ]

        for redcap_var_name in redcap_var_names:


            # get REDCap coding info from data dictionary
            redcap_data_dict_value = data_dict_df.loc[
                data_dict_df['Variable / Field Name'] == redcap_var_name, 
                'Choices, Calculations, OR Slider Labels'
            ]

            # if coding info is avaiable, convert to Python dict
            if not redcap_data_dict_value.isna().bool():
                redcap_data_dict_value_rev = self._redcap_str_dict(
                    redcap_data_dict_value.to_string(index = False)
                )

            
            
            
            
            # only prints value counts if there is a REDCap coding information
                try:
                    rave_long[redcap_var_name] = (
                        rave_long[redcap_var_name].astype(str).replace(redcap_data_dict_value_rev)
                    )
                    
                    
                    rave_long_counts = rave_long[redcap_var_name].value_counts()
                    
                    
                    
                    
                    
                    # print(rave_long_counts)
                    for value_count_index in rave_long_counts.index:
                        #if not self._isint(value_count_index):
                        if not self._isfloat(value_count_index):
                        #if not isinstance(value_count_index, int):
                            #print(redcap_var_name, ': ', value_count_index)
                            print("Column '{}' has an issue with the variable '{}'.".format(redcap_var_name, value_count_index))

                except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print('\n')
                    print (redcap_var_name)
                    print (message)
            
        
        # temp
        rave_long.replace('nan', np.nan, regex = True, inplace = True)
        # temp testing
        
        return rave_long  
          
            
    # def _isint(self, value):
    #     try:
    #         int(value)
    #         return True
    #     except ValueError:
    #         return False
    def _isfloat(self, value):
        """
        Comments:
            float is used instead of int because 'nan' returns true when cast 
            as float
        """
        try:
            float(value)
            return True
        except ValueError:
            return False
    
#    def _check_if_col_only_has_integers(
#            self, redcapnames, rave_long, data_dict_df = redcap_data_dict
#    ):
#        """Recode RAVE long dataframe based on REDcap data dictionary
#        
#        Args:
#            
#        
#        
#        """
#        
#        
#        '''
#        
#        changes values in df (self.data) columns based on variable coding in the REDCap data dictionary
#        '''
#        for redcapname in redcapnames:
##            print(redcapname)
#            
#            
#            
#            redcap_data_dict_value = data_dict_df.loc[
#                data_dict_df['Variable / Field Name'] == redcapname, 
#                'Choices, Calculations, OR Slider Labels'
#            ]
#            
#            if not redcap_data_dict_value.isna().bool():
#                redcap_data_dict_value_rev = self._redcap_str_dict(
#                    redcap_data_dict_value.to_string(index = False)
#                )    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            
            
#            # check to see if there is a value for
#            if not (data_dict_df.loc[
#                data_dict_df['Variable / Field Name'] == redcapname, 
#                'Choices, Calculations, OR Slider Labels'
#                ]
#                .isna().bool()
#            ):
#                redcap_data_dict_value = data_dict_df.loc[
#                        data_dict_df['Variable / Field Name'] == redcapname, 
#                        'Choices, Calculations, OR Slider Labels'].to_string(index = False)
#                redcap_data_dict_value_rev = self._redcap_str_dict(redcap_data_dict_value)
#                
#                # only prints value counts if there is a REDCap coding information
#                try:
#                    self.data[redcapname] = self.data[redcapname].astype(str).replace(redcap_data_dict_value_rev)
#                    print(self.data[redcapname].value_counts())
#                except Exception as ex:
#                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#                    message = template.format(type(ex).__name__, ex.args)
#                    print('\n')
#                    print (redcapname)
#                    print (message)
##                except TypeError:
##                    print('TypeError for: ' + redcapname)
##                else:
##                    print(str(NameError))

    def _redcap_str_dict2(self, input_str):
        
        """Reverse REDCap Data Dictionary string
        
        Coding for REDCap variables are stored in the 'Choices, Calculations, 
        OR Slider Labels' column of the data dictionary. This function reverses
        the variable coding. 

    
        Args:
            input_str: A string derived from the REDCap data dictionary which 
                indicates the variable coding. It is expected that the coding 
                integer and the answer label are separated by a comma and 
                entries are separated by a bar (e.g. '1, No | 2, Yes').
        
        Returns:
            A dict where the key is the answer label (from input_str) and the 
            value is the associated integer.
            
        Comments:
            Function will process commas in answer label correctly; however,
            if the answer label contains a bar (|), this will be interpreted
            as a new entry.

        """

        str_dict = {}
       
        val_key_lst = input_str.split(' | ')
        
        for val_key in val_key_lst:
            val_key_split_lst = val_key.split(', ', 1)
            
            str_dict[str(val_key_split_lst[1])] = str(val_key_split_lst[0])
            
           
        return(str_dict)
    
    def _redcap_str_dict(self, input_str):
        
        """Reverse REDCap Data Dictionary string
        
        Coding for REDCap variables are stored in the 'Choices, Calculations, 
        OR Slider Labels' column of the data dictionary. This function reverses
        the variable coding. 

    
        Args:
            input_str: A string derived from the REDCap data dictionary which 
                indicates the variable coding. It is expected that the coding 
                integer and the answer label are separated by a comma and 
                entries are separated by a bar (e.g. '1, No | 2, Yes').
        
        Returns:
            A dict where the key is the answer label (from input_str) and the 
            value is the associated integer.
            
        Comments:
            Function will process commas in answer label correctly; however,
            if the answer label contains a bar (|), this will be interpreted
            as a new entry.

        """
        str_dict = {}
       
        dict_val = ""
        dict_key = ""
        
        # when value flag is true, loop will add character to dict_val;
        # when value flage is false, loop will add character to dict_key
        val_flag = True
        
        for char in input_str:
            if char != '|':
                if val_flag:
                    if char != ',':
                        dict_val = dict_val + char
                    else:
                        val_flag = False
                else:
                        dict_key = dict_key + char                    
            else:
                dict_key = dict_key.strip()
                dict_val = dict_val.strip()
                
                str_dict[dict_key] = dict_val
                
                dict_key = ""
                dict_val = ""
                val_flag = True
        
        # last key, value pair is not proceeded by a '|' (bar)
        dict_key = dict_key.strip()
        dict_val = dict_val.strip()
        str_dict[dict_key] = dict_val
        
        
        return(str_dict)
        
    

    
    #     # str_dict = {}
       
    #     # val_key_lst = input_str.split(' |')
        
    #     # for val_key in val_key_lst:
    #     #     val_key_split_lst = val_key.split(', ', 1)
            
    #     #     str_dict[val_key_split_lst[1]] = val_key_split_lst[0]
            
    #     #     # dict_val = val_key.split(', ', 1)[0]
    #     #     # dict_key = val_key.split(', ', 1)[1]
            
    #     #     # str_dict[dict_key] = dict_val
           
    #     #return(str_dict)
    
    def prep_imp(self, event_name, 
                 
                 #access_group, 
                 complete_col, 
                 #import_temp
                 repeat_instrument = None
    ):
        self.data['redcap_event_name'] = event_name
        #self.data['redcap_data_access_group'] = access_group
        self.data[complete_col] = '2'
        if repeat_instrument is not None:
            self.data['redcap_repeat_instrument'] = repeat_instrument
       
        
        obs_col = self.data.pop('obs_id')
        self.data.insert(0, 'obs_id', obs_col)
        # self.final_df = pd.concat(
        #     [import_temp, self.data], 
        #     axis = 1, ignore_index = True, sort = False)
    def change_str(self, # should be change_str_val
                   #df_to_be_modified, # add this instead of self reference
                   spelling_dict, data_dict_df = redcap_data_dict):
        """Manually change initilized data set
        
        
        changes the values in processed data set (self.data) which have altered spellings compared to the redcap data dictioanry
        
        
        Manually change the values in processed data set (self.data) which 
        have altered spellings compared to the REDCap data dictioanry and 
        are not automatically updated as a result.
        
        
        Args:
            spelling_dict: A dictionary of dictionaries. The key of the 
                outermost dictionary corresponds to a REDCap column where the 
                data was not processed successfully due to spelling 
                discrepencies between the RAVE and REDCap database. The value
                of the outermost dictionary contains a dictionary. The key of
                thge innermost dictionary correponds to the RAVE answer label
                spelling and the value of the innermost dictionary corresponds 
                to the REDcap answer label spelling.
                For example:
                {'redcap_column_w_errors': {
                    'rave_spelling_1': 'redcap_spelling_1',
                    'rave_spelling_2': 'redcap_spelling_2'
                    }
                }
        
        Returns:
            Data frame is modified but nothing is returned

        """
        
        
        
        
        #df_to_be_modified = self.data
        
        
        
        
        
        for key, val in spelling_dict.items():
            redcap_data_dict_value = data_dict_df.loc[
                data_dict_df['Variable / Field Name'] == key, 
                'Choices, Calculations, OR Slider Labels'
            ].to_string(index = False)
            redcap_data_dict_value_rev = self._redcap_str_dict(
                redcap_data_dict_value
            )
            try:
                # replace column values with the 'correct' values (values associated with a REDCap dictionary value)
                self.data[key] = self.data[key].astype(str).replace(val)
                self.data[key] = self.data[key].astype(str).replace(redcap_data_dict_value_rev)
#                    self.data[redcapname] = self.data[redcapname].replace(redcap_data_dict_value_rev)
                self.data.replace('nan', np.nan, regex = True, inplace = True)
                
                print(self.data[key].value_counts())
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print ('\n')
                print (key)
                print (message)
                
    def compare_conv_dde(self, redcap_dde,   
                          #selected_subjects #probably don't need this; used to identify subjects with minized NA but will use the converted clinic dataframe to subset redcap dataframe
                          additional_ignore_cols = [],
                          data_dict_df = redcap_data_dict,
                          remove_text_cols = False):
        """Compare converted RAVE data to double data entry REDCap

            Comment:
                sort first by obs_id and then by dataset (where lower index value indiates redcap; higher is rave converted)
        
        """
        
        # https://docs.python-guide.org/writing/gotchas/
        # Python’s default arguments are evaluated once when the function is defined, not each time the function is called (like it is in say, Ruby). This means that if you use a mutable default argument and mutate it, you will and have mutated that object for all future calls to the function as well.
   
        ignore_cols = []
        ignore_cols.extend(additional_ignore_cols)
        
        # there's probably a better way to do this
        rave_converted = self.data.astype(str)
        
        
        
        
        #https://stackoverflow.com/questions/43125729/python-pandas-series-convert-float-to-string-preserving-nulls
        #redcap_dde[redcap_dde.notnull()] = redcap_dde.astype(str)
        redcap_dde = redcap_dde.astype(str)
        
        # int has trailing zeros
        #this is the easiest solution to fix, 
        # I should investigate why some integers receive trailing zeros ans dome don't
        #redcap_dde[redcap_dde.notnull()] = redcap_dde.str.place('.0', '')

        
        
        # I am not sure why I am having issues with the following
        rave_converted[rave_converted.notnull()] = rave_converted.astype(str)
        # the following should work though
        #rave_converted = rave_converted.astype(str)
        
        
        subjects_intersect = [
            subject 
            for subject in list(rave_converted['obs_id'])
            if subject in list(redcap_dde['obs_id'])
        ]
        columns_intersect = [
            column 
            for column in list(redcap_dde.columns.values) 
            if column in list(rave_converted.columns.values)
        ]
        
        
        redcap_dde_sub = redcap_dde.loc[
            redcap_dde['obs_id'].isin(subjects_intersect), 
            columns_intersect
        ]

        
        
        # remove rows which don't have data in them (after excluding 'obs_id')
        
        # converts Nan to a string of 'nan'; need to change it back
        # maybe change to string type later instead of immediately 
        redcap_dde_sub.replace('nan', np.nan, regex = True, inplace = True)

        redcap_dde_sub = redcap_dde_sub.dropna(
            subset = [
                column
                for column in columns_intersect
                if column not in ['obs_id', 'redcap_repeat_instance']
            ],
            thresh = 1,
            inplace = False 
        )
        redcap_dde_sub = redcap_dde_sub.astype(str)
        
        rave_converted_sub = rave_converted.loc[
            rave_converted['obs_id'].isin(subjects_intersect), 
            columns_intersect
        ]
        
        rave_converted_sub['Source'] = 'RaveConverted'
        
        redcap_dde_sub['Source'] = 'REDCapDDE'
        eval_df = redcap_dde_sub.append(
                rave_converted_sub, ignore_index = True
        )
       
        # remove/ignore columns that are free text (i.e. 'text' in 'Field 
        # Type' in the REDcap data dictionary)
        
        
        
        
        
        
        
        
        
        
        # if remove_text_cols:
            
        #     eval_cols = [eval_col for eval_col in eval_df.columns.values if eval_col not in ['obs_id', 'redcap_repeat_instance']]
            

        #     for eval_col in eval_cols:

                
        #         if (

        #           ((data_dict_df.loc[data_dict_df['Variable / Field Name'] == eval_col, 'Field Type'] == 'text').bool()
        #           | (data_dict_df.loc[data_dict_df['Variable / Field Name'] == eval_col, 'Field Type'] == 'notes').bool()
        #           )
        #         & (data_dict_df.loc[data_dict_df['Variable / Field Name'] == eval_col, 'Text Validation Type OR Show Slider Number'].isna().bool())):
        #             ignore_cols.append(eval_col)
                    










        if ignore_cols:
            eval_df.drop(ignore_cols, axis = 1, inplace = True)

        eval_df.drop_duplicates(
            keep = False, 
            inplace = True, 
            subset = eval_df.columns.difference(['Source'])
        )
        
        # sort first by obs_id and then by dataset (where lower index value indiates redcap; higher is rave converted)
        eval_df['colFromIndex'] = eval_df.index
        eval_df = eval_df.sort_values(by = ['obs_id', 'colFromIndex'])
        eval_df.drop(['colFromIndex'], axis = 1, inplace = True)
        
        return eval_df
    def remove_na(self):
        """Remove rows that don't contain relevant data
        
        # https://stackoverflow.com/questions/40659212/futurewarning-elementwise-comparison-failed-returning-scalar-but-in-the-futur
        """
        data_w_na = self.data
        # remove columns not expected to have 0s/nas
       
        relevant_cols = data_w_na.columns[~data_w_na.columns.isin([
            'obs_id','redcap_repeat_instance'
        ])]
        
        
        data_wo_na = data_w_na.dropna(subset = list(relevant_cols), how = 'all')

        
        data_wo_cols = data_wo_na[relevant_cols]
        data_wo_0 = data_wo_na.loc[~(data_wo_cols.astype(str).replace({'nan': '0'}) == '0').all(axis=1)]
        
        #data_wo_0 = data_w_na.loc[((data_wo_cols != '0')).any(axis=1)]
        
        data_wo = data_wo_0.dropna(subset = list(relevant_cols), how = 'all')
        #data_wo = data_wo_0.replace({'nan': np.nan}).dropna(subset = list(relevant_cols), how = 'all')
        
        
        self.data = data_wo
        
        
    def find_cols_issue(self, redcap_clinic,   # shouldn't this be redcap_clinic instead of redcap_dde
                        ignore_cols = []):

        """Identify the columns with issues after running compare_conv_dde
        
        
        """
        compare_df = self.compare_conv_dde(redcap_clinic, ignore_cols)
        
        eval_cols = [
            eval_col 
            for eval_col in compare_df.columns.values 
            if eval_col not in ignore_cols
            if eval_col not in 'obs_id'
        ]
        
        if not compare_df.empty:
            for obs_id in compare_df['obs_id'].unique():
                for eval_col in eval_cols:
                
                
                    redcap_clinic_sub_id = redcap_clinic.loc[
                        redcap_clinic['obs_id'].isin([obs_id]),
                        ['obs_id', eval_col]
                    ]

                    if not self.compare_conv_dde(
                        redcap_clinic_sub_id, 
                        ignore_cols
                    ).empty:
                        
                        
                        #print(str(obs_id), ": ", str(eval_col))
                        print("Subject '{}' has an issue with the column '{}'.".format(obs_id, eval_col))
            
            

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
    """Add 'date unavailabe' column to RAVE dataframe
    
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
            

#%% Rave coding to label

rave_entries = pd.read_excel(
    (
        'D:/Downloads/WorkFromHome/obs_data_migration/clinic/data/'
        'OBS_V2 4_Data Dictionary.xlsx'
    ),
    sheet_name = 'DataDictionaryEntries',
    encoding = 'mbcs', 
    dtype = str # temporary addition, see if this is causing issues
)


rave_fields = pd.read_excel(
    (
        'D:/Downloads/WorkFromHome/obs_data_migration/clinic/data/'
        'OBS_V2 4_Data Dictionary.xlsx'
    ),
    sheet_name = 'Fields',
    encoding = 'mbcs', 
    dtype = str # temporary addition, see if this is causing issues
)






def rave_code_label_dict(data_dict_name, data_dict_entries_df = rave_entries):
    '''Dictionary with RAVE coded (key) and label (value) values
    
    Args:
        data_dict_name: name associated with the RAVE coded/label value 
        (e.g. "noyes" should return a dictionary with No and Yes values)
        data_dict_entries_df: dataframe containing the both the coded and 
        labeled info; this should be derived from the RAVE data dictionary 
        received from AHRC
    
    Notes:
        The "fields" derived from the RAVE data dictionary received from AHRC 
        contains two columns with numeric values: "CodedData" and "Ordinal".
        The "CodedData" column was designed as the coded value because the 
        "OBS Flat Output 09SEP2019.csv" has "TYPEOFTWIN_1" coded with "9" 
        corresponding to "Not applicable" and "URINE_DIPSTICK_1" coded with
        "9" corresponding to "Not recorded".
    '''
    
    sub_data_dict_entried_df = data_dict_entries_df.loc[
        data_dict_entries_df['DataDictionaryName'] == data_dict_name,
        ['CodedData', 'UserDataString']
    ]
    final_dict = sub_data_dict_entried_df.set_index(
        'CodedData'
    )['UserDataString'].to_dict()
    
    return final_dict
           

def rave_convert_code_label(
        clinic_ser,
        data_dict_var,
        data_dict_fields_df = rave_fields
):
    '''RAVE coded column to labelled column
    
    Args:
        data_dict_name: name associated with the RAVE coded/label value 
        (e.g. "noyes" should return a dictionary with No and Yes values)
        data_dict_entries_df: dataframe containing the both the coded and 
        labeled info; this should be derived from the RAVE data dictionary 
        received from AHRC
    
    Notes:
        The "fields" derived from the RAVE data dictionary received from AHRC 
        contains two columns with numeric values: "CodedData" and "Ordinal".
        The "CodedData" column was designed as the coded value because the 
        "OBS Flat Output 09SEP2019.csv" has "TYPEOFTWIN_1" coded with "9" 
        corresponding to "Not applicable"
    '''
    
    
    datadictionaryname = data_dict_fields_df.loc[
        data_dict_fields_df['VariableOID'] == data_dict_var,
        'DataDictionaryName'
    ].astype(str)
    
    recoded_ser = clinic_ser.replace(rave_code_label_dict(datadictionaryname))
    
    return recoded_ser