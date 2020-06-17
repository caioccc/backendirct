import numpy as np
import pandas as pd

from ..const import *


def invoice_prepare_all(df):
    """
    Prepare the dataframe to user in cluster methods, this focus in invoice price services

    :param
    (Dataframe Pandas) df:
    :return
    (Dataframe Pandas) df_pivot: Make pivot using wirh columns DESCRIPTION_COL (Columns stay in const),
    values with ITEM_PRICE_COL (Columns stay in const) and GROUP_PIVOT (Set of columns stay in const)
     with grouping of this.
    (String List) list_k_means: List with feature
    """
    df_pivot = (df.pivot_table(index=GROUP_PIVOT,
                               columns=DESCRIPTION_COL,
                               values=ITEM_PRICE_COL,
                               aggfunc=np.sum).
                reset_index().
                fillna(0))

    list_k_means = list(df[DESCRIPTION_COL].unique())

    return df_pivot, list_k_means


def service_prepare_all(df):
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
    df = df[GROUP_PIVOT + [DESCRIPTION_COL]].drop_duplicates()
    df['unique'] = 1
    df_pivot = (df.pivot_table(index=GROUP_PIVOT,
                               columns=DESCRIPTION_COL,
                               values='unique',
                               aggfunc=np.sum).
                reset_index().
                fillna(0))

    list_k_means = list(df[DESCRIPTION_COL].unique())
    return df_pivot, list_k_means

def __same_outliers_cluster(df_kmens_outliers, df_dbscan_outliers):
    """
    Verify the cluster methods have the same invoice

    :param
    (Dataframe Pandas) df_kmens_outliers:
    (Dataframe Pandas) df_dbscan_outliers:

    :return
    (Dataframe Pandas) df_same: Select column with GROUP_SELECT (Set of columns stay in const)
    """
    df_same = (df_dbscan_outliers
    [df_dbscan_outliers[ID_INVOICE_COL].
            isin((df_kmens_outliers
        [ID_INVOICE_COL]).
                 unique())])

    return df_same[GROUP_SELECT]


def __diff_to_invoice_df(df_1, df_2):
    """
    Verify the dataframe  have the difference invoice

    :param
    (Dataframe Pandas) df_1:
    (Dataframe Pandas) df_2:

    :return
    (Dataframe Pandas) df_same: Select column with GROUP_SELECT (Set of columns stay in const)
    """
    df_result = (df_1
    [~df_1[ID_INVOICE_COL].
            isin((df_2
        [ID_INVOICE_COL]).
                 unique())])

    return df_result[GROUP_SELECT]


def __diff_outliers_cluster(df_kmens_outliers, df_dbscan_outliers):
    """
    Concat the dataframes with the outliers invoice with just have in Kmeans cluster or dbscan.

    :param
    (Dataframe Pandas) df_kmens_outliers:
    (Dataframe Pandas) df_dbscan_outliers:

    :return
    (Dataframe Pandas) df_general_diff: Contcat dataframe with invoice outliers
    """
    df_diff_dbscan = __diff_to_invoice_df(df_dbscan_outliers, df_kmens_outliers)
    df_diff_kmens = __diff_to_invoice_df(df_kmens_outliers, df_dbscan_outliers)
    df_general_diff = pd.concat([df_diff_dbscan, df_diff_kmens])
    return df_general_diff


def maybe_outliers_general(df_kmens_outliers, df_dbscan_outliers):
    """
    Concat a general outliers invoice in cluster methods in dataframe

    :param
    (Dataframe Pandas)df_kmens_outliers:
    (Dataframe Pandas)df_dbscan_outliers:

    :return
    (Dataframe Pandas) df_result: Concat outliers invoice
    """
    df_same = __same_outliers_cluster(df_kmens_outliers, df_dbscan_outliers)
    df_diff = __diff_outliers_cluster(df_kmens_outliers, df_dbscan_outliers)
    df_result = pd.concat([df_same, df_diff])
    return df_result
