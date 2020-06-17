# -*- coding: utf-8 -*-
import datetime
import hashlib
import os.path

import numpy as np
from dateutil.relativedelta import relativedelta
from sklearn.metrics.pairwise import euclidean_distances

from .const import *
from .invoice_methods import describe_invoices as di
from .ml_methods import basket as bk
from .ml_methods import dbscan_cluster as dbs
from .ml_methods import general_cluster as gc
from .ml_methods import kmeans_cluster as kcluster
from .utils import *


def total_account_invoice_client(df, **all_params):
    """
    Make a dataframe with amount of account, invoice and client

    :param
    (Dataframe Pandas) df:
    (Dictionary) all_params:

    :return
    (Dataframe Pandas) df_result: Dataframe with new columns
    """
    df_month = (df[(df['month'] == int(all_params['month']))
                   & (df['year'] == int(all_params['year']))])

    dic_result = {'Name': ['account', 'invoice', 'client'], 'Total': [len(df_month['ACCOUNT_ID'].unique()),
                                                                      len(df_month['INV_ID'].unique(
                                                                      )),
                                                                      len(df_month['CLIENT_ID'].unique())]}
    df_result = pd.DataFrame(data=dic_result)
    return df_result


def all_invoice(df, month, year, all_params):
    """
    Select invoice with possible problems in value, using a set of methods
    :param
    (Dataframe Pandas) df:
    (Int) month:
    (Int) year:
    (Dictionary) all_params:

    :return
    (Dataframe Pandas) df_general: Concat all dataframe result of identify error methods in values
    """
    name_col = 'error_name'
    list_df = []

    if 'valGreatOscillation' in all_params:
        if str2bool(all_params['valGreatOscillation']):
            df_expensive = di.expensive_cheap_invoice(df, month, year,
                                                      threshold=int(all_params['maxOscillationPercentage']))
            df_expensive = df_expensive[df_expensive['categority_value'].isin(
                ['High', 'Low'])][GROUP_SELECT]
            df_expensive[name_col] = 'invoice_expensive_cheap'

            list_df.append(df_expensive)

    if 'valSmallestCluster' in all_params:
        if str2bool(all_params['valSmallestCluster']):
            df_lower_cluster = kcluster.rows_in_cluster_lower(df, month, year, gc.invoice_prepare_all)[
                GROUP_SELECT]

            df_lower_cluster[name_col] = 'low_cluster'

            list_df.append(df_lower_cluster)

    if 'valGroupLargeSwings' in all_params:
        if str2bool(all_params['valGroupLargeSwings']):
            df_outliers_kmeans = kcluster.apply_history_kmeans(df, month, year, gc.invoice_prepare_all)[GROUP_SELECT]
            df_outliers_kmeans[name_col] = 'outliers_kmeans'

            list_df.append(df_outliers_kmeans)
    if len(list_df) == 0:
        df_general = pd.DataFrame(columns=GROUP_SELECT)
    else:
        df_general = pd.concat(list_df)
    df_general['have_error'] = 1
    return df_general


def all_service(df, month, year, all_params):
    """
    Select invoice with possible problems in services, using a set of methods
    :param
    (Dataframe Pandas) df:
    (Int) month:
    (Int) year:
    (Dictionary) all_params:

    :return
    (Dataframe Pandas) df_general: Concat all dataframe result of identify error methods in services
    """
    name_col = 'error_name'
    list_df = []

    df_filter = (df[(df['month'] == month)
                    & (df['year'] == year)])[GROUP_SELECT].drop_duplicates()

    if 'serRareServices' in all_params:
        if str2bool(all_params['serRareServices']):
            list_apriori = bk.transform_df_to_basket(df, month, year)
            df_apriori = df_filter[df[ID_INVOICE_COL].isin(
                list_apriori)][GROUP_SELECT]
            df_apriori[name_col] = 'apriori_rare_service'

            list_df.append(df_apriori)

    if 'serNegativeValues' in all_params:
        if str2bool(all_params['serNegativeValues']):
            df_negative = di.invoice_with_service_negative(
                df, month, year)[GROUP_SELECT].drop_duplicates()
            df_negative[name_col] = 'negative_service'

            list_df.append(df_negative)

    if 'serZeroValues' in all_params:
        if str2bool(all_params['serZeroValues']):
            df_zero = di.invoice_with_service_zero(
                df, month, year)[GROUP_SELECT].drop_duplicates()
            df_zero[name_col] = 'zero_service'

            list_df.append(df_zero)

    if 'serSmallestCluster' in all_params:
        if str2bool(all_params['serSmallestCluster']):
            df_lower_cluster = kcluster.rows_in_cluster_lower(df, month, year, gc.service_prepare_all)[
                GROUP_SELECT]
            df_lower_cluster[name_col] = 'service_low_cluster'

            list_df.append(df_lower_cluster)

    if 'serGreatOscillation' in all_params:
        if str2bool(all_params['serGreatOscillation']):
            df_outliers_kmeans = kcluster.apply_history_kmeans(df, month, year,
                                                               gc.service_prepare_all, folder='services')[GROUP_SELECT]
            df_outliers_kmeans[name_col] = 'service_outliers_kmeans'

            list_df.append(df_outliers_kmeans)

    if 'serClusterRareServices' in all_params:
        if str2bool(all_params['serClusterRareServices']):
            try:
                df_service, list_features = gc.service_prepare_all(df_filter)
                df_x = df_service[list_features]
                df_dbscan = dbs.create_dbscan_cluster(df_service, df_x)
                df_dbscan_outlier = dbs.maybe_outliers_dbscan(df_dbscan)[
                    GROUP_SELECT]
                df_dbscan_outlier[name_col] = 'dbscan_serivce_error'
                list_df.append(df_dbscan_outlier)
            except(Exception,):
                pass

    if len(list_df) == 0:
        df_general = pd.DataFrame(columns=GROUP_SELECT)
    else:
        df_general = pd.concat(list_df)
    df_general['have_error'] = 1
    return df_general


def general_errors(df, **all_params):
    """
    Load or save and merge the dataframe result from all_service and all_invoice

    :param
    (Dataframe Pandas) df:
    (Dictionary) all_params:

    :return
    (Dataframe Pandas) df_pivot: Merge the dataframe from all_service and all_invoice, and make a pivot using
    column 'error_name' to make the columns of dataframe, column 'have_error' for make values for the columns
    in pivot, make a grouping using GROUP_SELECT (Set of columns stay in const), add column 'sum_errors' to sum
    all values in 'error_name' columns, add column 'percentage_error' divide 'sum_errors' by 'number of error',
    order by the dataframe in dec by 'percentage_error'.
    """
    all_params_copy = all_params.copy()
    if 'filter' in all_params:
        all_params_copy.pop('filter')
    if 'acc' in all_params:
        all_params_copy.pop('acc')
    if 'label' in all_params:
        all_params_copy.pop('label')
    if 'invoice' in all_params:
        all_params_copy.pop('invoice')
    if 'status' in all_params:
        all_params_copy.pop('status')
    if 'message' in all_params:
        all_params_copy.pop('message')
    if 'listproblems' in all_params:
        all_params_copy.pop('listproblems')
    if 'prev_status_acc' in all_params:
        all_params_copy.pop('prev_status_acc')

    str_params = str(all_params_copy)
    hash_params = hashlib.sha256(str_params.encode('utf-8')).hexdigest()
    hash_params_csv = hash_params + '.csv'
    df_mods = pd.read_csv(PATH_METHODS_STATUS)

    list_all = list(df_mods[['name', 'status']][df_mods['status'] == True]['name'].values)
    list_all_parcial = [dic_input[key] for key in list_all]
    list_all_errors = []
    [make_unit(list_all_parcial[index], list_all_errors) for index in range(len(list_all_parcial))]
    number_errors = len(list_all_errors) * 1.0

    if os.path.exists('../server/analysis_module/data/results/' + hash_params_csv):
        df_pivot = pd.read_csv(
            '../server/analysis_module/data/results/' + hash_params_csv)
        df_pivot[ID_INVOICE_COL] = df_pivot[ID_INVOICE_COL].astype('int32')
        df_pivot = filter_by_active_mods(df_pivot, df_mods)

        df_pivot = df_pivot[GROUP_SELECT + list_all_errors + [STATUS_COL, STATUS_REVIEW, COMMENT] + LIST_STATUS_SWITCH]
        df_pivot = make_sum_errors_add_col_status(df_pivot, list_all_errors, number_errors)
        return df_pivot
    else:
        df_invoice_error = all_invoice(
            df, int(all_params['month']), int(all_params['year']), all_params)
        df_service_error = all_service(
            df, int(all_params['month']), int(all_params['year']), all_params)

        if (df_invoice_error.size == 0) and (df_service_error.size == 0):
            df_general = pd.DataFrame(columns=GROUP_SELECT)
        elif len(df_invoice_error) == 0:
            df_general = df_service_error
        elif len(df_service_error) == 0:
            df_general = df_invoice_error
        else:
            df_general = pd.concat([df_invoice_error, df_service_error])

        df_pivot = (df_general.pivot_table(index=GROUP_SELECT,
                                           columns='error_name',
                                           values='have_error',
                                           aggfunc=np.sum).
                    reset_index().
                    fillna(0))

        df_pivot = filter_by_active_mods(df_pivot, df_mods)
        df_pivot = df_pivot[GROUP_SELECT + list_all_errors]
        df_pivot = make_sum_errors_add_col_status(df_pivot, list_all_errors, number_errors)
        df_pivot[STATUS_REVIEW] = 0
        df_pivot[COMMENT] = ''

        df_pivot = df_pivot[df_pivot['sum_errors']
                            >= int(all_params['minOfMethods'])]
        df_pivot = df_pivot[df_pivot['INV_AMT'] >=
                            float(all_params['minInvoiceAmount'])]
        for key in dic_input.keys():
            df_pivot[key.replace(' ', "_")] = make_seq_switch(df_pivot, dic_input[key])

        df_pivot.to_csv('../server/analysis_module/data/results/' +
                        hash_params_csv, index=False)

        return df_pivot


def make_sum_errors_add_col_status(df_pivot, list_all_errors, number_errors):
    df_pivot['sum_errors'] = df_pivot[list_all_errors].sum(axis=1)
    df_pivot['percentage_error'] = df_pivot['sum_errors'].apply(
        lambda x: round(100 * (x / number_errors), 2))
    df_pivot = df_pivot.sort_values('percentage_error', ascending=False)

    # if STATUS_COL not in df_pivot.columns:
    #     df_pivot[STATUS_COL] = 0
    # else:
    # df_pivot[STATUS_COL] = df_pivot[STATUS_COL]

    df_pivot[ID_INVOICE_COL] = df_pivot[ID_INVOICE_COL].astype('int32')
    return df_pivot


def mean_count_account_all_time(df, account_id):
    """
    Amount invoice of this account and mean invoice of this account

    :param
    (Dataframe Pandas) df:
    (Int) account_id:

    :return
    (Int) total_account_df: Amount invoice of this account all time.
    (Int) mean_account_df: Mean invoice of this account all time.
    """
    total_account_df = (len(
        df
        [df[ID_ACCOUNT_COL] == int(account_id)][GROUP_SELECT].
            drop_duplicates()))
    mean_account_df = (round(df
                             [df[ID_ACCOUNT_COL] == int(account_id)]
                             [GROUP_SELECT].
                             drop_duplicates()
                             [INVOICE_VALUE_COL]
                             .mean(), 2))

    return total_account_df, mean_account_df


def total_invoices_in_month(df, **all_params):
    """
    Total invoice of this month

    :param
    (Dataframe Pandas) df:
    (Dictionary) all_params:

    :return
    (Int) total_invoices: Total invoice of this month.
    """
    df_month = (df[(df['month'] == int(all_params['month']))
                   & (df['year'] == int(all_params['year']))])

    total_invoices = len(df_month['INV_ID'].unique())
    return total_invoices


def sum_amount_invoices_in_month(df, **all_params):
    """
    Sum of invoice in this month
    :param
    (Dataframe Pandas) df:
    (Dictionary) all_params:

    :return
    (Int) sum_amount: Sum invoice of this month.
    """
    df_month = (df[(df['month'] == int(all_params['month']))
                   & (df['year'] == int(all_params['year']))])

    sum_amount = df_month[[INVOICE_VALUE_COL, ID_INVOICE_COL]].drop_duplicates()[INVOICE_VALUE_COL].sum()
    return sum_amount


def change_status_acc(df, id_inv, new_status, all_params):
    """
    Change account status for to customer or backoffice

    :param
    (Dataframe Pandas) df:
    (Int) id_inv:
    (Int) new_status:
    (Dictionary) all_params:

    """
    seach = id_inv
    if type(seach) != list:
        seach = [seach]
    seach = [int(number) for number in seach]

    df.loc[df[ID_INVOICE_COL].isin(seach), STATUS_COL] = new_status

    hash_params_csv = create_hash(all_params)

    df.to_csv('../server/analysis_module/data/results/' +
              hash_params_csv, index=False)


def create_hash(all_params):
    all_params_copy = all_params.copy()
    [all_params_copy.pop(key) for key in ['acc', 'invoice', 'status', 'message', 'listproblems', 'prev_status_acc'] if
     key in all_params_copy]
    str_params = str(all_params_copy)
    hash_params = hashlib.sha256(str_params.encode('utf-8')).hexdigest()
    hash_params_csv = hash_params + '.csv'
    return hash_params_csv


def reset():
    """
    Reset all account for status not analyse.
    """

    path = '../server/analysis_module/data/results/'

    list_files_csv = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.csv')]

    for csv_path in list_files_csv:
        df_csv = pd.read_csv(csv_path)
        df_csv['status'] = 0
        df_csv['comment_col'] = ''
        df_csv.loc[:, LIST_STATUS_SWITCH] = 1
        df_csv.to_csv(csv_path, index=False)


def same_invoice_pattern(data, df_error, all_params):
    """
    Search all invoice in dataframe with the same behavior for the account

    :param
    (Dataframe Pandas) data:
    (Dataframe Pandas) df_error: Just have error invoice.
    (Dictionary) all_params:

    :return
    (Dataframe Pandas) df_result: filter all invoice error with the same behavior for the account, using
    euclidian distance to calculate distance.
    """

    df_data_month = data[(data['month'] == int(all_params['month'])) & ((data['year'] == int(all_params['year'])))]
    df_merge = df_data_month.merge(df_error[ID_INVOICE_COL].to_frame(), on=ID_INVOICE_COL, how='inner')
    df_service, list_service = gc.service_prepare_all(df_merge)

    df_features = df_service[list_service].values
    acc_row = (df_service[
                   df_service[ID_INVOICE_COL] == int(all_params['invoice'])]
               [list_service]
               .values)
    df_service['distance'] = euclidean_distances(df_features, acc_row)

    df_result = (df_service[
        (df_service['distance'] == 0)
        & (df_service[ID_INVOICE_COL] != int(all_params['invoice']))]
    [ID_INVOICE_COL])

    return df_result


def read_past_df(all_params_past):
    """
    Read the past dataframe
    :param
    (Dictionary) all_params_past:

    :return
    (Dataframe Pandas) df_result: Dataframe with the last month.
    """
    hash_params_csv = create_hash(all_params_past)

    df_result = pd.read_csv(
        '../server/analysis_module/data/results/' + hash_params_csv)
    df_result[ID_INVOICE_COL] = df_result[ID_INVOICE_COL].astype('int32')

    return df_result


def df_same_pattern_last_month(data, df_error, df_error_past, status, all_params, all_params_last):
    """
    Search all invoice in dataframe with the same behavior by account in backoffice or customer in last month

    :param
    (Dataframe Pandas) data:
    (Dataframe Pandas) df_error:
    (Dataframe Pandas) df_error_past:
    (Int) status:
    (Dictionary) all_params:
    (Dictionary) all_params_last:

    :return
    (Int List) list_invoice: Filter all invoice error with the same behavior by account in backoffice or customer
    in last month, using euclidian distance to calculate distance.
    """

    df_data_month = data[(data['month'] == int(all_params['month'])) & ((data['year'] == int(all_params['year'])))]

    df_data_last = data[
        (data['month'] == int(all_params_last['month'])) & ((data['year'] == int(all_params_last['year'])))]

    df_merge = df_data_month.merge(df_error[ID_INVOICE_COL].to_frame(), on=ID_INVOICE_COL, how='inner')
    df_status_past = df_error_past[df_error_past['status'] == status]
    df_merge_last = df_data_last.merge(df_status_past[ID_INVOICE_COL].to_frame(), on=ID_INVOICE_COL, how='inner')

    df_service, list_service = gc.service_prepare_all(df_merge)
    df_service_last, list_service_last = gc.service_prepare_all(df_merge_last)

    miss_service_past = list(set(list_service_last) - set(list_service))
    miss_service_present = list(set(list_service) - set(list_service_last))

    for col_past in miss_service_present:
        df_service_last[col_past] = 0.0

    for col_preset in miss_service_past:
        df_service[col_preset] = 0.0

    all_service_list = list_service + list_service_last
    all_service_list = sorted(all_service_list)

    df_features = df_service[all_service_list].values
    set_result = {}

    for inv in list(df_status_past[ID_INVOICE_COL].unique()):
        acc_row = (df_service_last[
                       df_service_last[ID_INVOICE_COL] == int(inv)]
                   [all_service_list]
                   .values)

        df_service['distance'] = euclidean_distances(df_features, acc_row)

        set_result.update(df_service[
                              (df_service['distance'] == 0)
                              & (df_service[ID_INVOICE_COL] != int(inv))]
                          [ID_INVOICE_COL])

    list_invoice = list(set_result.values())
    return list_invoice


def make_all_params_last(all_params):
    """
    Make all_params with month and year of the last date

    :param
    (Dictionary) all_params:

    :return
    (Dictionary) all_params_last: all_params with month and year of the last date
    """

    data_month_present = datetime.datetime(int(all_params['year']), int(all_params['month']), 1)
    last_month_data = data_month_present + relativedelta(months=-1)
    all_params_last = all_params.copy()
    all_params_last['month'] = str(last_month_data.month)
    all_params_last['year'] = str(last_month_data.year)
    return all_params_last


def make_unit(list_input, list_out):
    [list_out.append(i) for i in list_input]


def filter_by_active_mods(df_to_filter, df_with_actives_mod):
    list_mod = list(df_with_actives_mod[['name', 'status']][df_with_actives_mod['status'] == True]['name'].values)
    list_result = []
    list_part = [dic_input[key] for key in list_mod]
    [make_unit(list_part[index], list_result) for index in range(len(list_part))]
    return make_query(df_to_filter, list_result)


def change_coment_acc(df, id_inv, all_params, add_coment):
    """
    Change account status for to customer or backoffice

    :param
    (Dataframe Pandas) df:
    (Int) id_inv:
    (Int) new_status:
    (Dictionary) all_params:

    """
    seach = id_inv
    if type(seach) != list:
        seach = [seach]
    seach = [int(number) for number in seach]

    coment = str(df[df[ID_INVOICE_COL].isin(seach)][COMMENT].values[0])
    if coment == 'nan':
        coment = ''

    df.loc[df[ID_INVOICE_COL].isin(seach), COMMENT] = coment + '<br>' + add_coment

    hash_params_csv = create_hash(all_params)

    df.to_csv('../server/analysis_module/data/results/' +
              hash_params_csv, index=False)


def get_comment_acc(df, account, invoice_id):
    comments = df[(df[ID_ACCOUNT_COL] == int(account)) & (df[ID_INVOICE_COL] == int(invoice_id))][COMMENT].values
    if type(comments[0]) != float:
        comments = comments[0].split('<br>')
    return comments


def set_status_error_acc(df_error, account_id, list_error, all_params):
    element = [(dic['label'], dic['status']) for dic in list_error]
    for elem in element:
        df_error.loc[df_error[ID_ACCOUNT_COL].isin([int(account_id)]), elem[0]] = elem[1]
    hash_params_csv = create_hash(all_params)
    df_error.to_csv('../server/analysis_module/data/results/' +
                    hash_params_csv, index=False)


def same_invoice_pattern_review(data, df_error, all_params):
    """
    Search all invoice in dataframe with the same behavior for the account

    :param
    (Dataframe Pandas) data:
    (Dataframe Pandas) df_error: Just have error invoice.
    (Dictionary) all_params:

    :return
    (Dataframe Pandas) df_result: filter all invoice error with the same behavior for the account, using
    euclidian distance to calculate distance.
    """

    df_data_month = data[(data['month'] == int(all_params['month'])) & (data['year'] == int(all_params['year']))]
    df_merge = df_data_month.merge(df_error[[ID_INVOICE_COL] + LIST_STATUS_SWITCH], on=ID_INVOICE_COL, how='inner')
    df_service, list_service = service_status_prepare_all(df_merge)

    df_features = df_service[list_service].values
    acc_row = (df_service[
                   df_service[ID_INVOICE_COL] == int(all_params['invoice'])]
               [list_service]
               .values)
    df_service['distance'] = euclidean_distances(df_features, acc_row)

    df_result = (df_service[
        (df_service['distance'] == 0)
        & (df_service[ID_INVOICE_COL] != int(all_params['invoice']))]
    [ID_INVOICE_COL])

    return df_result


def service_status_prepare_all(df):
    """
    Prepare the dataframe to user in cluster methods, this focus in invoice have or not this service

    :param
    (Dataframe Pandas) df:
    :return
    (Dataframe Pandas) df_pivot: Make pivot using wirh columns DESCRIPTION_COL (Columns stay in const),
    values with ITEM_PRICE_COL (Columns stay in const) and GROUP_PIVOT (Set of columns stay in const)
     with grouping of this.
    (String List) list_k_means: List with feature
    """
    df = df[GROUP_PIVOT + [DESCRIPTION_COL] + LIST_STATUS_SWITCH].drop_duplicates()
    df['unique'] = 1
    list_index = LIST_STATUS_SWITCH + GROUP_PIVOT
    df_pivot = (df.pivot_table(index=list_index,
                               columns=DESCRIPTION_COL,
                               values='unique',
                               aggfunc=np.sum).
                reset_index().
                fillna(0))

    list_status_service = list(df[DESCRIPTION_COL].unique()) + LIST_STATUS_SWITCH
    return df_pivot, list_status_service
