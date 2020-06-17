import pandas as pd
import numpy as np

def slice_df(df, month, year):
    """
    Filter dataframe by month and year

    :param
    (Dataframe Pandas) df:
    (Int) month:
    (Int) year:

    :return
    (Dataframe Pandas) df_result: filtered dataframe
    """
    df_result = (df[(df['month'] == month)
                    & (df['year'] == year)])

    return df_result

def str2bool(v):
    """
    Convert string to boolean
    :param
    (String) v:

    :return
    (Boolean)
    """
    return v.lower() in ('true', '1')

def pass_row(list_input, size_row):
    """
    Make a dictionary

    :param
    (String List) list_input:
    (Int) size_row:

    :return:
    (Dictionary)
    """
    return {'id': size_row, 'content': list_input}


def make_col(intput_list_col, size_col):
    """
    Make a dictionary

    :param
    (String List) intput_list_col:
    (Int) size_col:

    :return:
    (Dictionary)
    """
    return {'id': size_col, 'content': intput_list_col}


def pass_list(array):
    """
    Convert array to list

    :param
    (String Array)array:

    :return:
    (List)
    """
    return list(array)

def make_query(df, list_input):
    """
    Make a condition with the list and filter dataframe by the condition.

    :param
    (Dataframe Pandas) df:
    (String List) list_input:

    :return
    (Dataframe Pandas) result: filtered dataframe
    """
    result = pd.DataFrame(columns=df.columns)
    str_search = ('|').join([col + ' ==1' for col in list_input if col in df.columns])
    if len(str_search) > 0:
        result = df.query(str_search)

    return result

def make_dic_desc_value(list_desc_value):
    """
    Make List Dictionary for frontend

    :param
    (List) list_desc_value:

    :return
    (List Dictionary)
    """
    return [{'content': list_desc_value[0], 'id': 1}, {'content': list_desc_value[1], 'id': 2}]


def pretty_number(number):
    """
    Make number in USA format

    :param
    (Float) number:

    :return
    (String)
    """
    return "{:,}".format(number)


def make_seq_switch(df, cols_select):
    list_data_col = list(df.columns)
    columns_select = [col for col in list_data_col if col in cols_select]
    result_array = np.sum(df[columns_select].values, 1)
    return np.where(result_array >= 1, 1, result_array)
