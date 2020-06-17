import math as math
from datetime import datetime, timedelta

import numpy as np

from ..const import *


def top_5_invoice_values(df, month, year, boolean_asc=False):
    '''
    Seleciona os top 5 faturas com seus respectivos valores
    Podendo selecionar a forma de ordenacao (ASC ou DESC)
    :param df: DataFrame pandas
    :param month: Integer
    :param year: Integer
    :param boolean_asc: Boolean
    :return: Um pandas dataFrame contendo os top 5 faturas e seus respectivos precos
    '''

    top_5_df = (df[(df['month'] == month)
                   & (df['year'] == year)]
                [GROUP_VALUE_INVOICE].
                drop_duplicates().
                sort_values(INVOICE_VALUE_COL, ascending=boolean_asc).
                head(5))

    return top_5_df


def describe_invoice_values(df, month, year):
    '''
    Mostra os dados estatisticos do dataFrame dos valores das invoices
    Exemplo: Mediana, Min, Max, Quatis, Media...
    :param df: DataFrame pandas
    :param month: Integer
    :param year: Integer
    :return: pandas DataFrame contendo os dados estatisticos
    '''

    describe_df = (df
                   [(df['month'] == month)
                    & (df['year'] == year)]
                   [[INVOICE_VALUE_COL]].describe())

    return describe_df


def invoice_with_outliers_values(df, month, year, whisker=1.5):
    '''
    Mostra os outliers contidos no DataFrame das invoices
    :param df: DataFrame pandas
    :param month: Integer
    :param year: Integer
    :param whisker: Integer
    :return: PandasDataframe contendo os possiveis outliers
    '''

    quantile_3 = (df[(df['month'] == month)
                     & (df['year'] == year)]
                  [INVOICE_VALUE_COL]
                  .quantile(.75))

    quantile_1 = (df[(df['month'] == month)
                     & (df['year'] == year)]
                  [INVOICE_VALUE_COL]
                  .quantile(.25))

    iqr = quantile_3 - quantile_1

    lower_whisker = quantile_1 - whisker * iqr

    high_whisker = quantile_3 + whisker * iqr

    outliers_df = (df[(df['month'] == month)
                      & (df['year'] == year)
                      & ((df[INVOICE_VALUE_COL] < lower_whisker)
                         | (df[INVOICE_VALUE_COL] > high_whisker))]
                   [GROUP_VALUE_INVOICE]
                   .drop_duplicates())

    return outliers_df


def invoice_with_service_negative(df, month, year):
    '''
    Mostra as invoices que contem servicos negativos
    :param df: Pandas DataFrame
    :param month: Integer
    :param year: Integer
    :return: Pandas DataFrame
    '''
    df_invoice_service_negative = (df[(df['month'] == month)
                                      & (df['year'] == year) & (df[ITEM_PRICE_COL] < 0)])

    return df_invoice_service_negative


def invoice_negative(df, month, year):
    '''
    Mostra as invoices com valores negativos
    :param df: Pandas DataFrame
    :param month: Integer
    :param year: Integer
    :return: Pandas DataFrame com as invoices negativas
    '''
    df_invoice_negative = (df[(df['month'] == month)
                              & (df['year'] == year) & (df[INVOICE_VALUE_COL] < 0)])

    return df_invoice_negative


def invoice_with_service_zero(df, month, year):
    '''
    Mostra as invoices com servicos zerados
    :param df: Pandas DataFrame
    :param month: Integer
    :param year: Integer
    :return: Pandas DataFrame com as invoices com servicos zerados
    '''
    df_invoice_price_zero = (df[(df['month'] == month)
                                & (df['year'] == year) & (df[INVOICE_VALUE_COL] == 0)])

    return df_invoice_price_zero


def select_invoice(df, month, year, inv_id):
    '''
    Mostra os dados de uma invoice selecionada
    :param df: Pandas DataFrame
    :param month: Integer
    :param year: Integer
    :param inv_id: Integer
    :return: Pandas DataFrame com a invoice selecionada
    '''

    selected_invoice_df = (df[(df['month'] == month)
                              & (df['year'] == year)
                              & (df[ID_INVOICE_COL] == inv_id)])

    return selected_invoice_df


def more_than_59_day(df, month_begin, year_begin, months_before=6):
    '''
    Apresenta os clientes que passaram 60 dias ou mais sem gerar faturas
    considerando os ultimos 6 meses
    :param df: Pandas DataFrame
    :param month_begin: Integer
    :param year_begin: Integer
    :param months_before: Integer
    :return: Pandas DataFrame com os clientes
    '''

    day_start = datetime.datetime(year_begin, month_begin, 1)

    days_before = day_start + timedelta(days=- 30 * months_before)

    month_before, year_before = days_before.month, days_before.year

    year_diff = year_begin - year_before

    if (year_diff == 0):
        df_filter = (df[(df['year'].between(year_before, year_begin)) &
                        (df['month'].between(month_before, month_begin))])

    else:

        df_filter = (df[
            ((df['year'] == year_before)
             & (df['month'] >= month_before)) |
            ((df['year'] == year_begin)
             & (df['month'] <= month_begin))])

    slice_df = (df_filter[GROUP_ACCOUNT_INVOICE].
                drop_duplicates().
                sort_values(by=[DATE_COL]))

    slice_df['shift'] = slice_df.groupby(ID_ACCOUNT_COL)[DATE_COL].shift(1)

    slice_df = slice_df.dropna()
    slice_df['diff_days'] = (slice_df[DATE_COL] - slice_df['shift']) / np.timedelta64(1, 'D')
    return (slice_df[(slice_df['diff_days'] > 59)
                     & (slice_df['month'] == month_begin)
                     & (slice_df['year'] == year_begin)])


def expensive_cheap_invoice(df, month, year, threshold=30):
    '''
    Mostra os clientes que passaram a ter uma fatura muito alta ou baixa
    de um mes para o outro
    :param df: Pandas DataFrame
    :param month: Integer
    :param year: Integer
    :param threshold: Integer (limiar para considerar alto ou baixo)
    :return: Pandas DataFrame com os clientes que tiveram oscilacao
    '''

    months_before = 1
    day_start = datetime(year, month, 28)
    days_before = day_start + timedelta(days=- (30 * months_before))
    month_before, year_before = days_before.month, days_before.year
    year_diff = year - year_before

    if year_diff == 0:
        df_filter = (df[(df['year'].between(year_before, year)) &
                        (df['month'].between(month_before, month))])
    else:
        df_filter = (df[
            ((df['year'] == year_before)
             & (df['month'] >= month_before)) |
            ((df['year'] == year)
             & (df['month'] <= month))])

    df_shift = (df_filter
                [GROUP_ACCOUNT_VALUES].
                drop_duplicates().
                sort_values(by=[DATE_COL]))

    df_shift['past_value'] = (df_shift
                              .groupby(ID_ACCOUNT_COL)
                              [INVOICE_VALUE_COL]
                              .transform('shift'))

    df_shift = df_shift.dropna()
    df_shift['percentage_change'] = ((df_shift[INVOICE_VALUE_COL]
                                      / df_shift['past_value'])
                                     * 100) - 100

    df_shift['categority_value'] = (df_shift['percentage_change'].apply(lambda x: 'Normal'

    if x <= threshold and x >= -threshold
       or math.isnan(x)
    else ('High' if x > threshold
          else 'Low')))

    return df_shift


def expensive_cheap_invoice_roll_windows(df, month, year, threshold=30, months_before=5):
    '''
    Mostra os clientes que passaram a ter uma fatura muito alta ou baixa
    de um mes para o outro utilizando uma media movel dos ultimos
    :param df: Pandas DataFrame
    :param month: Integer
    :param year: Integer
    :param threshold:  Integer
    :param months_before: Integer
    :return: Pandas DataFrame com os clientes que tiveram oscilacao
    '''

    day_start = datetime(year, month, 1)
    days_before = day_start + timedelta(days=- (30 * months_before))
    month_before, year_before = days_before.month, days_before.year
    year_diff = year - year_before

    if year_diff == 0:

        df_filter_between = (df[(df['year'].between(year_before, year)) &
                                (df['month'].between(month_before, month))])
    else:
        df_filter_between = (df[
            ((df['year'] == year_before)
             & (df['month'] >= month_before)) |
            ((df['year'] == year)
             & (df['month'] <= month))])

    df_filter = (df[(df['month'] == month)
                    & (df['year'] == year)]
                 [GROUP_ACCOUNT_VALUES].
                 drop_duplicates())

    df_filter['last_value'] = df_filter[ID_INVOICE_COL]
    df_filter = df_filter[[ID_ACCOUNT_COL, 'last_value']]
    df_join = df_filter.merge(df_filter_between, how='inner')

    df_result = (df_join
                 [[ID_ACCOUNT_COL, 'month', 'year', ID_INVOICE_COL, INVOICE_VALUE_COL, 'last_value']].
                 drop_duplicates().
                 sort_values(by=['month', 'year'], ascending=[True, True]))

    df_result = (df_result
                 .groupby([ID_ACCOUNT_COL, 'last_value'])
                 [INVOICE_VALUE_COL]
                 .rolling(months_before)
                 .mean()
                 .dropna()
                 .reset_index(name='mean'))

    df_result['percentage_change'] = ((df_result['last_value']
                                       / df_result['mean'])
                                      * 100) - 100
    df_result = (df_result.groupby(['ACCOUNT_ID']).
                 tail(1))
    df_result['categority_value'] = (df_result['percentage_change'].apply(lambda x: 'Normal'

    if x <= threshold and x >= -threshold
       or math.isnan(x)
    else ('high' if x > threshold
          else 'Low')))

    return df_result
