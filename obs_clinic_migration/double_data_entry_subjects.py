from itertools import compress
import obs_data_sets

NUM_MIN_NA_SUBJECTS = 40

clinic_temp = obs_data_sets.rave_clinic
clinic_temp = clinic_temp.loc[clinic_temp['Subject'].astype(int) <= 91299999]

# only review columns with data in them
col_names = [
    col_name for col_name in list(clinic_temp.columns.values)
    if clinic_temp[col_name].notnull().astype(int).sum() > 0
]

# min_na_subjects will contain OBS IDs of relevant subjects (i.e. minimum
# number of NAs)
min_na_subjects = []

# loop will find the OBS ID with the lowest number of columns with missing
# data; add it to the list; remove the OBS ID; and repeat according to
# NUM_MIN_NA_SUBJECTS

for _ in range(1, (NUM_MIN_NA_SUBJECTS + 1)):

    # create a column, 'sum_na', which counts the number of NA's (i.e. empty
    # column values) the subject has
    clinic_temp['sum_na'] = 0
    for col_name in col_names:
        clinic_temp['sum_na'] = (clinic_temp['sum_na']
                                + clinic_temp[col_name].isnull().astype(int))
    print(clinic_temp['sum_na'].min())

    # find the subject with the lowest number of NA's
    min_na_subject = clinic_temp['Subject'].loc[
        clinic_temp['sum_na'] == clinic_temp['sum_na'].min()
    ].iloc[0]

    # find which columns which have NA's for the min_na_subject
    col_names = list(compress(col_names, clinic_temp[
        clinic_temp['Subject'] == min_na_subject
    ].isnull().iloc[0].tolist()))
    # need to keep 'Subject' column to track subjects
    col_names.append('Subject')

    print(col_names[0:10])
    # create new dataframe which excludes min_na_subject and has the
    # appropriate column names
    clinic_temp = clinic_temp.loc[
        clinic_temp['Subject'] != min_na_subject, col_names
    ]

    min_na_subjects.append(min_na_subject)

print(min_na_subjects)
