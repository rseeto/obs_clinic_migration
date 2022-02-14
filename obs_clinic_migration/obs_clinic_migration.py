import pandas as pd
import numpy as np
import obs_data_sets

class RedcapConv:
    """Class used to convert Rave data to REDCap data

    Attributes
    ----------
    data : pandas.dataframe
        Clinical data derived from the Rave database that is being converted to
        the REDCap format
    """
    def __init__(
        self, ravestub_redcap_dict, stub_repeat,
        master_df = obs_data_sets.rave_clinic,
        redcap_data_dict = obs_data_sets.redcap_data_dict,
        recode_long = True
    ):
        """Convert Rave dataframe to REDCap

        Parameters
        ----------
        ravestub_redcap_dict : dict
            Dictionary which maps the Rave stub columns (keys) to the REDCap
            columns (values)
        stub_repeat : int
            Maximum number of repeats expected For example, if
            stub_repeat = 2, expecting column_x_1 and column_x_2 in Rave
            dataframe.
        master_df : pandas.dataframe, optional
            Dataframe containing the Rave data to be manipulated. It is
            expected the dataframe is in the wide format, by default
            obs_data_sets.rave_clinic
        redcap_data_dict : pandas.dataframe, optional
            Finalized project's data dictionary derived from REDCap, by default
            obs_data_sets.redcap_data_dict
        recode_long : bool, optional
            When True, will execute self._recoded_based_redcap_data_dict
            (changes values in df (self.data) columns based on
            variable coding in redcap_data_dict), by default True
        """
        # convert relevant data from wide to long depending on
        # iterations/stub_repeat
        if stub_repeat == 0:
            rave_long = self._rave_single(ravestub_redcap_dict, master_df)
        elif stub_repeat > 0:
            rave_long = self._rave_wide_long(
                ravestub_redcap_dict, stub_repeat, master_df
            )
        # recode values based on REDCap data dictionary
        if recode_long:
            self.data = self._recoded_based_redcap_data_dict(
                data_dict_df = redcap_data_dict, rave_long = rave_long
            )
        else:
            self.data = rave_long

    @staticmethod
    def _rave_wide_long(ravestub_redcap_dict, stub_repeat, master_df):
        """Convert and clean Rave data from wide to long with >1 instances

        Subset Rave dataframe, convert to long, remove blank rows,
        rename columns, and modify columns

        Parameters
        ----------
        ravestub_redcap_dict : dict
            dictionary which maps the Rave stub columns (keys) to the REDCap
            columns (values)
        stub_repeat : int
            Maximum number of repeats expected For example, if
            stub_repeat = 2, expecting column_x_1 and column_x_2 in Rave
            dataframe.
        master_df : pandas.dataframe
             Dataframe containing the Rave data to be manipulated. It is
             expected the dataframe is in the wide format.

        Returns
        -------
        pandas.dataframe
            A long dataframe converted from the wide Rave dataframe. The
            dataframe should only contain the columns in the values of
            ravestub_redcap_dict with the addition of 'obs_id' and
            'redcap_repeat_instance'. Column values are in 'label' format as
            opposed to coded as an 'integer'.
        """
        # create list of column names including iterations of stub
        # (e.g. COL_1, COL_2)
        df_cols = ['Subject']
        for i in range(1, (stub_repeat + 1)):
            for stub_name in ravestub_redcap_dict.keys():
                df_cols.append(stub_name + str(i))

        # subset dataframe
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

        # check to see if manipulated file contains the same number of
        # instances as function argument
        if sub_df['redcap_repeat_instance'].max() != stub_repeat:
            print(
                'max redcap_repeat_instance = '
                 + str(sub_df['redcap_repeat_instance'].max())
                 + '; stub_repeat = ' + str(stub_repeat)
            )

        # modifications
        sub_df.rename(columns = ravestub_redcap_dict, inplace = True)
        sub_df.rename(columns = {'Subject': 'obs_id'}, inplace = True)
        sub_df['redcap_repeat_instance'] = (
            sub_df['redcap_repeat_instance'].astype(str)
        )

        return sub_df

    @staticmethod
    def _rave_single(ravestub_redcap_dict, master_df):
        """Clean Rave data with single instance

        Subset Rave dataframe, rename columns, and modify columns

        Parameters
        ----------
        ravestub_redcap_dict : dict
            dictionary which maps the Rave stub columns (keys) to the REDCap
            columns (values)
        master_df : pandas.dataframe
             Dataframe containing the Rave data to be manipulated. It is
             expected the dataframe is in the wide format.

        Returns
        -------
        pandas.dataframe
            The dataframe should only contain the columns in the values of
            ravestub_redcap_dict with the addition of 'obs_id' and
            'redcap_repeat_instance'.

        Notes
        -----
        Equivalent to self._rave_wide_long, converting Rave data from wide to
        long, with single instance; however, data does not need to be converted
        to a long format if there is only a single instance.
        """
        # change column name for consistency with REDCap
        ravestub_redcap_dict['Subject'] = 'obs_id'

        # create a dataframe with only the columns of interest which are
        # derived from the ravestub_redcap_dict
        sub_df = master_df.loc[:, ravestub_redcap_dict.keys()]
        sub_df.rename(columns = ravestub_redcap_dict, inplace = True)

        return sub_df

    def _recoded_based_redcap_data_dict(
            self, rave_long, data_dict_df = obs_data_sets.redcap_data_dict
    ):
        """Recode Rave long dataframe based on REDCap data dictionary

        Changes values in df (self.data) columns based on variable coding in
        the REDCap data dictionary

        Parameters
        ----------
        rave_long : pandas.dataframe
            dataframe in which values will be changed
        data_dict_df : pandas.dataframe, optional
            data dictionary export from REDCap containing variable coding,
            by default obs_data_sets.redcap_data_dict

        Returns
        -------
        pandas.dataframe
            Rave data set recoded based on REDCap data dictionary

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
                        rave_long[redcap_var_name].astype(str).replace(
                            redcap_data_dict_value_rev
                        )
                    )
                    rave_long_counts = (
                        rave_long[redcap_var_name].value_counts()
                    )
                    # check if any issues
                    for value_count_index in rave_long_counts.index:
                        if not self._isfloat(value_count_index):
                            print(
                                (
                                    f"Column '{redcap_var_name}', "
                                    "variable '{value_count_index}' has an "
                                    "issue."
                                )
                            )

                except Exception as ex:
                    template = (
                        "An exception of type {0} occurred. Arguments:\n{1!r}"
                    )
                    message = template.format(type(ex).__name__, ex.args)
                    print('\n')
                    print (redcap_var_name)
                    print (message)
        rave_long.replace('nan', np.nan, regex = True, inplace = True)

        return rave_long

    def _isfloat(self, value):
        """Check if value is a 'float' type

        Parameters
        ----------
        value : unknown
            object where type is unknown

        Returns
        -------
        boolean
            Returns True if value is float and False if value is not a float

        Notes
        -----
        Float is used instead of int because 'nan' returns true when cast
        as float

        """
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _redcap_str_dict(self, input_str):
        """Create Python dictionary from REDCap data dictionary string

        Coding for REDCap variables are stored in the 'Choices, Calculations,
        OR Slider Labels' column of the data dictionary. This function converts
        the string to a dictionary.

        Parameters
        ----------
        input_str : string
            A string derived from the REDCap data dictionary which
            indicates the variable coding. It is expected that the coding
            integer and the answer label are separated by a comma and
            entries are separated by a bar (e.g. '1, No | 2, Yes').

        Returns
        -------
        dictionary
            A dict where the key is the answer label (from input_str) and the
            value is the associated integer.

        Notes
        -----
        Function will process commas in answer label correctly; however,
        if the answer label contains a bar (|), this will be interpreted
        as a new entry.
        """
        str_dict = {}
        val_key_lst = input_str.split(' | ')

        for val_key in val_key_lst:
            val_key_split_lst = val_key.split(', ', 1)

            str_dict[
                str(val_key_split_lst[1])
            ] = str(val_key_split_lst[0]).lstrip()

        return str_dict

    def prep_imp(self, event_name, complete_col, repeat_instrument = None):
        """Prepare data file for REDCap import

        Adds columns necessary to import into REDCap and reorganizes columns.

        Parameters
        ----------
        event_name : str
            REDCap divides the project into events. They are roughly equivalent
            to how the Rave data was divided.
        complete_col : string
            Name of REDCap column which indicate the status of the event. A
            value of 2 indicates event is complete.
        repeat_instrument : string, optional
            Name of REDCap column for repeat instances, by default None

        Returns
        -------
        None

        Notes
        -----
        Method is performed after double data check as REDCap does it's own
        data validation. When attempting to import data into REDCap, won't
        be successful if the column names are incorrectly named or ordered.
        """
        self.data['redcap_event_name'] = event_name
        self.data[complete_col] = '2'
        if repeat_instrument is not None:
            self.data['redcap_repeat_instrument'] = repeat_instrument
        # move obs_id column; REDCap import will raise an error if not in the
        # expected order
        obs_col = self.data.pop('obs_id')
        self.data.insert(0, 'obs_id', obs_col)

    def change_str(
        self, spelling_dict, data_dict_df = obs_data_sets.redcap_data_dict
    ):
        """Manually change column values after initilizing data set

        Manually change the values in processed data set (self.data) which
        have altered spellings compared to the REDCap data dictioanry and
        are not automatically updated as a result.

        Parameters
        ----------
        spelling_dict : dictionary of dictionaries
            The key of the outermost dictionary corresponds to a REDCap column
            where the data was not processed successfully due to spelling
            discrepencies between the Rave and REDCap database. The value of
            the outermost dictionary contains a dictionary. The key of the
            innermost dictionary correponds to the Rave answer label spelling
            and the value of the innermost dictionary corresponds to the
            REDcap answer label spelling.
            For example:
            {'redcap_column_w_errors': {
                'rave_spelling_1': 'redcap_spelling_1',
                'rave_spelling_2': 'redcap_spelling_2'
                }
            }
        data_dict_df : dictionary, optional
            REDCap data dictionary that contains REDCap data dictionary string
            (see self._redcap_str_dict), by default
            obs_data_sets.redcap_data_dict

        Returns
        -------
        None

        Example
        -------
        >>>self.data['redcap_column_w_errors'].tolist()
        ['correct_spelling', 'rave_spelling_1', 'rave_spelling_2']
        >>>self.change_str(
            {'redcap_column_w_errors': {
                'rave_spelling_1': 'redcap_spelling_1',
                'rave_spelling_2': 'redcap_spelling_2'
                }
            }
        )
        >>>self.data['redcap_column_w_errors'].tolist()
        ['correct_spelling', 'redcap_spelling_1', 'redcap_spelling_2']

        """
        for key, val in spelling_dict.items():
            redcap_data_dict_value = data_dict_df.loc[
                data_dict_df['Variable / Field Name'] == key,
                'Choices, Calculations, OR Slider Labels'
            ].to_string(index = False)
            redcap_data_dict_value_rev = self._redcap_str_dict(
                redcap_data_dict_value
            )
            try:
                # replace column values with the 'correct' values (values
                # associated with a REDCap dictionary value)
                self.data[key] = self.data[key].astype(str).replace(val)
                self.data[key] = (
                    self.data[key].astype(str).replace(
                        redcap_data_dict_value_rev
                    )
                )
                self.data.replace('nan', np.nan, regex = True, inplace = True)

                print(self.data[key].value_counts())
            except Exception as ex:
                template = (
                    "An exception of type {0} occurred. Arguments:\n{1!r}"
                )
                message = template.format(type(ex).__name__, ex.args)
                print ('\n')
                print (key)
                print (message)

    def compare_conv_dde(self, redcap_dde, additional_ignore_cols = []):
        """Compare converted Rave data to double data entry REDCap

        Parameters
        ----------
        redcap_dde : pandas.dataframe
            Dataframe containing the double data entry REDCap
        additional_ignore_cols : list, optional
            Columns to ignore when compare the converted Rave data (self.data)
            and the double data entry REDCap (redcap_dde), by default []

        Returns
        -------
        pandas.dataframe

        Notes
        -----
        sort first by obs_id and then by dataset (where lower index value
        indiates redcap; higher is rave converted) to easily locate
        # discrepancies
        """
        # aren't concerned with data type, only values
        rave_converted = self.data.astype(str)
        rave_converted[rave_converted.notnull()] = rave_converted.astype(str)
        redcap_dde = redcap_dde.astype(str)

        # from redcap_dde, create dataframe containing the subjects and columns
        # in both rave_converted and redcap_dde
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

        # only investigate intersecting subjects in converted dataframe
        rave_converted_sub = rave_converted.loc[
            rave_converted['obs_id'].isin(subjects_intersect),
            columns_intersect
        ]

        # add 'Source' column so origin of discrepancies can be identified and
        # combine into one dataframe
        rave_converted_sub['Source'] = 'RaveConverted'
        redcap_dde_sub['Source'] = 'REDCapDDE'
        eval_df = redcap_dde_sub.append(
                rave_converted_sub, ignore_index = True
        )

        # columns to ignore in the comparison
        # remove/ignore columns that are free text (i.e. 'text' in 'Field
        # Type' in the REDcap data dictionary)
        ignore_cols = []
        ignore_cols.extend(additional_ignore_cols)
        if ignore_cols:
            eval_df.drop(ignore_cols, axis = 1, inplace = True)

        # drop rows that have the same value between Rave and REDCap
        # (i.e. are correct) ignoring 'Source'; should only have rows with
        # discrepancies
        eval_df.drop_duplicates(
            keep = False,
            inplace = True,
            subset = eval_df.columns.difference(['Source'])
        )

        # sort first by obs_id and then by dataset (where lower index value
        # indiates redcap; higher is rave converted) to easily locate
        # discrepancies
        eval_df['colFromIndex'] = eval_df.index
        eval_df = eval_df.sort_values(by = ['obs_id', 'colFromIndex'])
        eval_df.drop(['colFromIndex'], axis = 1, inplace = True)

        return eval_df

    def remove_na(self):
        """Remove rows that don't contain relevant data

        Removes rows of the processed data frame (self.data), excluding
        'obs_id' and 'redcap_repeat_instance', which contain only NaN, 'nan'
        or '0'

        Returns
        -------
        None
        """
        data_w_na = self.data

        # ignore 'obs_id' and 'redcap_repeat_instance'
        relevant_cols = data_w_na.columns[~data_w_na.columns.isin(
            ['obs_id','redcap_repeat_instance']
        )]

        # remove NaN columns
        data_wo_na = data_w_na.dropna(
            subset = list(relevant_cols), how = 'all'
        )
        data_wo_cols = data_wo_na[relevant_cols]
        # still contains 'nan' strings and '0', convert to 'nan' to '0'
        data_wo_nan = data_wo_na.loc[
            ~(
                data_wo_cols.astype(str).replace({'nan': '0'}) == '0'
            ).all(axis=1)
        ]
        #remove both 'nan' and '0'
        data_wo = data_wo_nan.dropna(subset = list(relevant_cols), how = 'all')

        self.data = data_wo
