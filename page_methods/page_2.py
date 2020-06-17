import numpy as np
from analysis_module.const import *
from analysis_module.utils import *


def str_col(df):
    """
    Convert all columns in dataframe in string
    :param
    (Dataframe Pandas) df:

    :return
    (Dataframe Pandas) df: Dataframe with all columns with type String
    """
    for col in df.columns:
        df[col] = df[col].apply(lambda x: str(x))
    return df


def filter_table(df, filter):
    """
    Filter Dataframe by string

    :param
    (Dataframe Pandas) df:
    (Dictionary) filter:
    :return:
    (Dataframe Pandas) df: Dataframe filter.
    """
    list_result = []
    if 'search' in filter:
        list_col = df.columns
        for col in list_col:
            list_result.append(df[df[col].str.contains(filter['search'], na=False)])
        result_df = pd.concat(list_result)
        return result_df.drop_duplicates()
    return df


def status_invoices(df):
    """
    Number the invoice by status(not_analyse, backoffice or customer)

    :param
    (Dataframe Pandas) df:

    :return
    (Int) to_analyze: Number invoice in not analyse
    (Int) sent_customers: Number invoice in customer
    (Int) sent_backoffice: Number invoice in backoffice
    """
    to_analyze = df[df['status'] == 0].shape[0]
    sent_customers = df[df['status'] == 2].shape[0]
    sent_backoffice = df[df['status'] == 1].shape[0]

    return to_analyze, sent_customers, sent_backoffice


def plot_methods(df, table, all_params):
    """
    Make List of Dictionary with the risk method and percentage with total invoice
    :param
    (Dataframe Pandas) df:
    (Dataframe Pandas) table:
    (Dictionary) all_params:

    :return:
    (List of Dictionary) list_result: Method rick order by percentage in desc
    """
    total_invoice_in_risck = \
    table[(table['month'] == int(all_params['month'])) & (table['year'] == int(all_params['year']))][
        ID_ACCOUNT_COL].drop_duplicates().count() * 1.0
    df_mod = pd.read_csv(PATH_METHODS_STATUS)
    list_filter = list(df_mod[['name', 'status']][df_mod['status'] == True]['name'].values)
    list_result = [{'type': method,
                    'label': method.replace(' ', '_'),
                    'desc': dic_desc[method],
                    'value': round(
                        100 * (make_query(df, dic_input[method])[
                                   ID_ACCOUNT_COL].count() / total_invoice_in_risck),
                        2),
                    'rule': dic_ml[method]}
                   for method in list_filter]
    list_result = sorted(list_result, key=lambda i: i['value'], reverse=True)

    return list_result


def filter_status(df, status):
    """
    Filter invoice by status

    :param
    (Dataframe Pandas) df:
    (Int)status:

    :return
    (Dataframe Pandas): Filter dataframe
    """
    return df[df[STATUS_COL] == status]


def query_by_methods(df, label):
    """
    Filter invoice by method risk

    :param
    (Dataframe Pandas) df:
    (String) label:

    :return
    (Dataframe Pandas) result: Filter dataframe by method risk
    """
    result = df
    if len(label) > 1:
        result = make_query(df, dic_input[label])
    return result


def generate_new_table(intput_list_row, intput_list_col, size_col):
    """
    Generate a table to frontend
    :param
    (Object Array) intput_list_row:
    (String Array) intput_list_col:
    (Int) size_col:

    :return
    (Dictionary) dic_result: Elements of dataframe
    """
    dic_result = {'columns': list(np.vectorize(make_col)(intput_list_col, size_col)),
                  'items': list(map(pass_list, np.vectorize(pass_row)(intput_list_row, size_col)))}
    return dic_result
