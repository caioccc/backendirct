import os.path
import pickle

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from ..const import *


def __auto_number_cluster(df, threshold=10, random_state=170, max_number_cluster=15):
    """
    Search the best number of cluster to apply in kemans methods.

    :param
    (Dataframe Pandas) df:
    (Int) threshold: Default 10
    (Int) random_state: Default 170
    (Int) max_number_cluster: Default 15

    :return
    (Int) best_number_cluster: Best number to split the dataframe in kmeans cluster
    """
    list_wcss = []
    list_range = range(1, max_number_cluster)
    for number_cluster in list_range:
        kmeans = (KMeans(n_clusters=number_cluster
                         , random_state=random_state))
        kmeans.fit(df)
        list_wcss.append(kmeans.inertia_)

    max_wcss = list_wcss[0]
    dic = {'number_cluster': list_range, 'wcss': list_wcss}
    pandas_df = pd.DataFrame(data=dic)
    pandas_df['percentage'] = pandas_df['wcss'] / max_wcss
    pandas_df['diff'] = (100 *
                         (pandas_df['percentage'].shift(1) - pandas_df['percentage']))
    pandas_df = pandas_df.dropna()
    pandas_df = pandas_df[pandas_df['diff'] >= threshold]

    best_number_cluster = (int(
        pandas_df
            .tail(n=1)
        ['number_cluster']))

    return best_number_cluster


def just_kmeans(df_input_kmeans, month, year, random_state=170, folder ='invoices', save=True):
    """
    Apply and save Kmeans model

    :param
    (Dataframe Pandas) df_input_kmeans:
    (Int) month:
    (Int) year:
    (Int) random_state: Default 170
    (String) folder: Default'invoice'
    (Boolean) save: Default True
    :return
    (Model Kmeans) kmeans: Model kmeans
    """

    kmeans = (KMeans(n_clusters=__auto_number_cluster(df_input_kmeans)
                     , random_state=random_state
                     , algorithm='full'))

    kmeans.fit(df_input_kmeans)

    if (save):
        path = PATH_KMEANS + str(folder)
        filename = path + '\\' + str(month) + '_' + str(year) + '.sav'
        pickle.dump(kmeans, open(filename, 'wb'))

    return kmeans


def apply_kmeans(df, df_input_kmeans, random_state=170):
    """
    Apply model Kmeans in daframe

    :param
    (Dataframe Pandas) df:
    (Dataframe Pandas) df_input_kmeans:
    (Int) random_state: Default 170

    :return
    (Dataframe Pandas) df: Add column CLUSTER_NUMBER_COL(Columns stay in const)
    (Array List) kmeans.cluster_centers_: Have Centroid of clusters
    """
    kmeans = just_kmeans(df_input_kmeans, random_state = random_state)

    df[CLUSTER_NUMBER_COL] = kmeans.fit_predict(df_input_kmeans)
    return df, kmeans.cluster_centers_


def rows_in_cluster_lower(df, month, year, method_use):
    """
    Return all row in low cluster in kmeans

    :param
    (Dataframe Pandas) df:
    (Int) month:
    (Int) year:
    (Method) method_use: Select method between invoice_prepare_all or service_prepare_all in (general_cluster)

    :return
    (Dataframe Pandas) df_result: Have just low cluster rows.
    """
    df_current = (df[(df['month'] == month)
                     & (df['year'] == year)])

    df_current_prepare, list_service_current = method_use(df_current)

    df_current_prepare_input_low = df_current_prepare[list_service_current]

    df_current_prepare_low = df_current_prepare.copy()

    kmens_current = just_kmeans(df_current_prepare_input_low, month, year, random_state=170, save=False)

    df_current_prepare_low[CLUSTER_NUMBER_COL] = kmens_current.fit_predict(df_current_prepare_input_low)

    df_group = df_current_prepare_low.groupby(CLUSTER_NUMBER_COL)[ID_CLIENT_COL].count().reset_index(name='count')
    lower_cluster = int(df_group.sort_values('count')[CLUSTER_NUMBER_COL].head(1))
    df_result = df_current_prepare_low[df_current_prepare_low[CLUSTER_NUMBER_COL] == lower_cluster][GROUP_SELECT]

    return df_result


def __norm_linalf(centroid, element):
    """
    Return euclidian distance between features of kmeans and center of cluster

    :param
    (List) centroid:
    (List) element:

    :return
    (Float) np.linalg.norm(centroid - element): euclidian distance
    """
    return np.linalg.norm(centroid - element)


def maybe_outliers_cluster_general(df, list_col_features, list_centroid, multiply_theta=2):
    """
    Select outliers in kmeans cluster, using confidence interval of 95%

    :param
    (Dataframe Pandas) df:
    (String list) list_col_features:
    (Array List) list_centroid:
    (Int) multiply_theta: Default 2, Number of standard deviation

    :return
    (Dataframe Pandas) df_result: outliers in kmeans cluster
    """
    df['list_element'] = list(df[list_col_features].values)
    df['center_this_cluster'] = df[CLUSTER_NUMBER_COL].apply(lambda x: list_centroid[x])
    df['distance'] = (np.vectorize(__norm_linalf)(df['center_this_cluster'],
                                                  df['list_element']))
    median = float(df['distance'].mean())
    std = float(df['distance'].std())
    cut = median + (multiply_theta * std)

    df_result = (df[df['distance'] >= cut][GROUP_SELECT + [CLUSTER_NUMBER_COL]])
    return df_result


def maybe_outliers_by_cluster(df, list_col_features, list_centroid, multiply_theta=2):
    """
    Select outliers by cluster in kmeans cluster, using confidence interval of 95%

    :param
    (Dataframe Pandas) df:
    (String list) list_col_features:
    (Array List) list_centroid:
    (Int) multiply_theta: Default 2, Number of standard deviation

    :return
    (Dataframe Pandas) df_result: outliers by cluster in kmeans cluster
    """
    df['list_element'] = list(df[list_col_features].values)
    df['center_this_cluster'] = df[CLUSTER_NUMBER_COL].apply(lambda x: list_centroid[x])
    df['distance'] = (np.vectorize(__norm_linalf)(df['center_this_cluster'],
                                                  df['list_element']))
    list_unique_cluster = list(df[CLUSTER_NUMBER_COL]
                               .unique())
    list_cluster = ([df[
                         df[CLUSTER_NUMBER_COL] == cluster]
                     for cluster in
                     list_unique_cluster])
    list_result = []

    for cluster in list_unique_cluster:
        if len(list_cluster[cluster]) > 5:
            median = float(list_cluster[cluster]['distance'].mean())
            std = float(list_cluster[cluster]['distance'].std())
            cut = median + (multiply_theta * std)

            list_result.append((list_cluster[cluster]
            [list_cluster[cluster]['distance'] >= cut]
            [GROUP_SELECT + [CLUSTER_NUMBER_COL]]))

    df_result = pd.concat(list_result)
    return df_result


def apply_history_kmeans(df, month, year, method_use, folder ='invoices'):
    """
    Apply,save and select outliers in  kmeans model in historical data

    :param
    (Dataframe Pandas) df:
    (Int) month:
    (Int) year:
    (Method) method_use: Select method between invoice_prepare_all or service_prepare_all in (general_cluster)
    (String) folder: Default 'invoices'

    :return
    (Dataframe Pandas) maybe_outliers_by_cluster: outliers by cluster in kmeans cluster
    """
    path = PATH_KMEANS + str(folder)
    filename = path + '/' + str(month) + '_' + str(year) + '.sav'

    df_history = (df[(df['year'] < year)
                     | ((df['year'] == year)
                        & (df['month'] < month))])

    df_current = (df[(df['month'] == month)
                     & (df['year'] == year)])

    if len(df_history) <= 0:
        df_history = df_current

    df_history_prepare, list_service_all = method_use(df_history)
    df_current_prepare, list_service_current = method_use(df_current)
    diff_list_service_general = list(set(list_service_all) - set(list_service_current))
    diff_list_service_current = list(set(list_service_current) - set(list_service_all))
    list_service_all = list_service_all + diff_list_service_current

    for col in diff_list_service_general:
        df_current_prepare[col] = 0.0

    for col in diff_list_service_current:
        df_history_prepare[col] = 0.0

    df_history_prepare_input = df_history_prepare[list_service_all]

    if (os.path.isfile(filename)):

        kmens_history = pickle.load(open(filename, 'rb'))

        centers_history = kmens_history.cluster_centers_

    else:

        kmens_history = just_kmeans(df_history_prepare_input, month, year, random_state=170, paste = folder)

        centers_history = kmens_history.cluster_centers_

    df_current_prepare_input = df_current_prepare[list_service_all]

    df_current_prepare[CLUSTER_NUMBER_COL] = kmens_history.fit_predict(df_current_prepare_input)

    return maybe_outliers_by_cluster(df_current_prepare, list_service_all, centers_history,
                                     multiply_theta=2)
