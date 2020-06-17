from datetime import datetime, timedelta

import numpy as np

from ..const import *


def __make_set_service(df):

    """
    Grouping the dataframe using GROUP_DESCRIPTION_INVOICE (Set of columns stay in const), add column in dataframe
    with list of services in this group of columns with name services_string.

    :param
    (Dataframe Pandas) df:

    :return:
    (Dataframe Pandas) df_result: Dataframe with grouping and new col services_string.
    """
    df_result = (df
                 [GROUP_DESCRIPTION_INVOICE]
                 .drop_duplicates().
                 sort_values(DESCRIPTION_COL, ascending=True).
                 groupby(GROUP_VALUE_INVOICE)
                 [DESCRIPTION_COL]
                 .apply(lambda x: x.values.tolist())
                 .reset_index(name='list_name'))

    df_result['services_string'] = df_result['list_name'].apply(lambda x: ','.join(x))

    return df_result


def __apply_find(services_string, shift):
    """
    Compare the lists and make a sub list with the intersection between this list.

    :param
    (String List) services_string:
    (String List) shift:

    :return
    (String List): Sub list with intersection between this list
    """
    return services_string.find(shift)


def __apply_new_diff_service(df):

    """
    Make a difference between two columns in dataframe.

    :param
    (Dataframe Pandas) df:

    :return
    (String List) list_element: List with the different between two columns, have the new service.
    """
    list_element = list(set(df['part_1']) - set(df['part_2']))
    return list_element


def __apply_miss_diff_service(df):
    """
    Make a difference between two columns in dataframe

    :param
    (Dataframe Pandas) df:

    :return
    (String List) list_element: List with the different between two columns, have the miss service.
    """
    list_element = list(set(df['part_2']) - set(df['part_1']))
    return list_element


def invoice_chance_service(df, month, year, months_before=2):
    """
    Verify with the account have new or miss servie comprare with the last invoice.

    :param
    (Dataframe Pandas) df:
    (Int) month:
    (Int) year:
    (Int) months_before: Default is 2.

    :return
    (Dataframe Pandas) df_shift: Dataframe with columns new_service and miss_service this represent that account
    have miss or new service.
    """
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

    df_set_service = __make_set_service(df_filter)
    df_shift = (df_set_service
                [GROUP_INVOICE_SERVICE_SET].
                drop_duplicates().
                sort_values(by=[DATE_COL]))

    df_shift['shift'] = df_shift.groupby(ID_ACCOUNT_COL)['services_string'].transform('shift')
    df_shift = df_shift.dropna()
    df_shift['difference'] = (np.vectorize(__apply_find)(df_shift['services_string'], df_shift['shift']))
    df_shift['difference2'] = (np.vectorize(__apply_find)(df_shift['shift'], df_shift['services_string']))
    df_shift = df_shift[(df_shift['difference'] == -1) & (df_shift['difference2'] == -1)]
    df_shift['part_1'] = df_shift['services_string'].apply(lambda x: x.split(','))
    df_shift['part_2'] = df_shift['shift'].apply(lambda x: x.split(','))
    df_shift['new_service'] = df_shift.apply(__apply_new_diff_service, axis=1)
    df_shift['miss_service'] = df_shift.apply(__apply_miss_diff_service, axis=1)

    return df_shift


def top_5_services_use(df, month, year, boolean_asc=False):
    """
    Find the top five service most user or not.

    :param
   (Dataframe Pandas) df:
   (Int) month:
   (Int) year:
   (Boolean)  boolean_asc: Default is False

    :return
    (DataFrame Pandas) df_result: Grouping the dataframe using GROUP_DESCRIPTION_INVOICE
    (Set of columns stay in const), adds columns 'count' this represent the number of
    occurrence of this service , order by column count in asc or desc and add column
    'percentage' this represent the percentage of this service by account.
    """
    total_account = (len((df[(df['month'] == month)
                             & (df['year'] == year)]
                          [ID_INVOICE_COL]
                          .drop_duplicates()))) * 1.0

    df_result = (df[(df['month'] == month)
                    & (df['year'] == year)]
                 [GROUP_DESCRIPTION_INVOICE]
                 .drop_duplicates()
                 .groupby(DESCRIPTION_COL)
                 [DESCRIPTION_COL]
                 .count()
                 .reset_index(name='count')
                 .sort_values('count', ascending=boolean_asc))

    df_result['percentage'] = df_result['count'] / total_account

    return df_result.head(5)


def service_negative(df, month, year):
    """
    Find all service with Negative values.

    :param
   (Dataframe Pandas) df:
   (Int) month:
   (Int) year:

    :return
    (Dataframe Pandas) df_service_negative: Grouping the dataframe using DESCRIPTION_COL
    (Columns stay in const), add column 'count' order by the dataframe in desc by him.
    """

    df_service_negative = (df[(df['month'] == month)
                              & (df['year'] == year)
                              & (df[ITEM_PRICE_COL] < 0)])

    return (df_service_negative
            .groupby(DESCRIPTION_COL)
            [ITEM_PRICE_COL]
            .count()
            .reset_index(name='count')
            .sort_values('count', ascending=False))


def service_zero(df, month, year):
    """
    Find all service with Zero values.

    :param
   (Dataframe Pandas) df:
   (Int) month:
   (Int) year:

    :return
    (Dataframe Pandas) df_service_zero: Grouping the dataframe using DESCRIPTION_COL
    (Columns stay in const), add column 'count' order by the dataframe in desc by him.
    """

    df_service_zero = (df[(df['month'] == month)
                          & (df['year'] == year) & (df[ITEM_PRICE_COL] == 0)])

    return (df_service_zero
            .groupby(DESCRIPTION_COL)
            [ITEM_PRICE_COL]
            .count()
            .reset_index(name='count')
            .sort_values('count', ascending=False))


def set_services_group_percentage(df, month, year, boolean_asc=False):
    """
    Find all set of services and order than by occurrence.

    :param
   (Dataframe Pandas) df:
   (Int) month:
   (Int) year:
   (Boolean) boolean_asc: Default False

    :return
    (Dataframe Pandas) df_result: Filter dataframe using GROUP_ACCOUNT_SERVICE_SET (Set of columns stay in const)
    grouping dataframe using 'services_string' , add column 'count' order by the dataframe in desc or asc by him and
    add column 'percentage' this represent the percentage of this set service by occurrence.
    (Dataframe Pandas) df_parcial: Using the method __make_set_service.
    """
    df_filter = (df[(df['month'] == month)
                    & (df['year'] == year)])

    total_account = (len((df_filter
                          [ID_INVOICE_COL]
                          .drop_duplicates()))) * 1.0

    df_parcial = __make_set_service(df_filter)

    df_result = (df_parcial[
                     GROUP_ACCOUNT_SERVICE_SET]
                 .groupby('services_string')
                 ['services_string']
                 .count()
                 .reset_index(name='count')
                 .sort_values('count', ascending = boolean_asc))

    df_result['percentage'] = 100 * (df_result['count'] / total_account)
    return df_result, df_parcial


def top_5_set_services_use(df, month, year, boolean_asc=False):
    """
    Find the top five most or not use of set of services.

    :param
   (Dataframe Pandas) df:
   (Int) month:
   (Int) year:
   (Boolean) boolean_asc: Default False

    :return
    (Dataframe Pandas) df_result: Filter by the 5 set of service.
    """
    df_result, _ = set_services_group_percentage(df, month, year, boolean_asc=boolean_asc)
    return df_result.head(5)


def invoice_with_rare_set_service(df, month, year, threshold=1.0):
    """
    Find all invoice have a rare set of service.

    :param
   (Dataframe Pandas) df:
   (Int) month:
   (Int) year:
   (Float) threshold: Default 1.0

    :return
    (Dataframe Pandas) df_result: Filter by list of rare set service.
    """

    df_percentage, df_parcial = set_services_group_percentage(df, month, year, boolean_asc=False)

    list_rare_set_services = list(df_percentage
                                  [df_percentage['percentage'] <= threshold]
                                  ['services_string'])

    df_result = (df_parcial[
        df_parcial['services_string']
            .isin(list_rare_set_services)]
    [GROUP_VALUE_INVOICE + ['services_string']])

    return df_result
