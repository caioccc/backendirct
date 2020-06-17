import warnings

import pandas as pd
from sklearn import preprocessing
from sklearn.metrics.pairwise import euclidean_distances

from ..const import *

warnings.filterwarnings("ignore")


def scale_features_df(df_features):
    """
    Apply Standard Scale in the columns in dataframe

    :param
    (Dataframe Pandas) df_features:

    :return
    (Dataframe Pandas) scaled_df: Columns with Standard Scale
    """

    names = df_features.columns
    scaler = preprocessing.StandardScaler()
    scaled_df = scaler.fit_transform(df_features)
    scaled_df = pd.DataFrame(scaled_df, columns=names)

    return scaled_df


def new_dbscan(df_features, min_distance=0.3, min_samples=10):
    """
    Verify of the euclidian distance between the one invoice and other in dataframe, if the distance is small or like
    the mim_distance this invoice stay the group, if the lenght of this group is like or bigger the min_samples this is
    a valid cluster , if small this stay in outliers cluster.

    :param
    (Dataframe Pandas) df_features:
    (Int) min_distance: Default 3
    (Int) min_samples: Default 10

    :return
    (Dataframe Pandas) df_final: Dataframe feature with column k_cluster
    """

    cluster = 0  # numero do cluster incial
    list_df = []  # lista de dataframe com os cluster validos
    list_out = []  # lista de dataframe com os cluster outliers

    df_try = df_features  # dataframe
    columns = df_try.columns
    while (len(df_try) > 0):  # verifica se ainda tem elementos no dataframe

        row = df_try.head(1).values  # pega uma linha do dataframe
        df_try['distance'] = euclidean_distances(df_try, row)

        df_cluster = df_try[df_try[
                                'distance'] <= min_distance]  # verifica quais estão no paramento do min_distance definido na entrada no algoritmo

        if (len(df_cluster) >= min_samples):  # verifica se o tamanho do cluster e valido
            df_cluster[CLUSTER_NUMBER_COL] = cluster  # define o cluster, com o valor do cluster atual
            list_df.append(df_cluster)
            df_try = df_try.drop(
                index=list(df_cluster.index))  # Retira do dataframe os dados ja encaixado em algum grupo.
            cluster = cluster + 1

        else:
            df_cluster[CLUSTER_NUMBER_COL] = -1  # coloca essas linhas no cluster outliers
            list_out.append(df_cluster)
            df_try = df_try.drop(
                index=list(df_cluster.index))  # Retira do dataframe os dados ja encaixado em algum grupo.

    df_final = pd.concat(list_df + list_out)  # junta todos os dataframe elementos em um só dataframe

    return df_final


def create_dbscan_cluster(df, df_features, threshold=0.075):
    """
    Try to find the better size of cluster in dbscan

    :param
    (Dataframe Pandas) df:
    (Dataframe Pandas) df_features:
    (Int)threshold: Default 0.075

    :return
    (Dataframe Pandas) df_final: Dataframe with column k_cluster
    """
    scaled_df = scale_features_df(df_features)
    total_lenght = len(df) * 1.0
    min_lenght_cluster = int(total_lenght * 0.01)
    tr = threshold
    error_percentage = 1.0

    while error_percentage >= tr:
        hdb = (new_dbscan(scaled_df, min_samples=min_lenght_cluster))

        df_result = df
        df_result[CLUSTER_NUMBER_COL] = hdb[CLUSTER_NUMBER_COL]
        error_percentage_step = (len(df_result
                                     [df_result[CLUSTER_NUMBER_COL] == DBSCAN_CLUSTER_OUTLIERS]) /
                                 total_lenght)

        min_lenght_cluster = int(min_lenght_cluster / 2)
        error_percentage = error_percentage_step

    return df_result


def maybe_outliers_dbscan(df):
    """
    Filter the outliers cluster in dbscan

    :param
    (Dataframe Pandas) df:

    :return
    (Dataframe Pandas) df_outlier: Just have the outliers invoice
    """
    df_outlier = df[df[CLUSTER_NUMBER_COL] == DBSCAN_CLUSTER_OUTLIERS]

    return df_outlier
