from analysis_module.const import *
from analysis_module.utils import *
import numpy as np
import pandas as pd


def error_account(df_error, account_id):
    """
    Select method error activate in this account

    :param
    (Dataframe Pandas) df_error:
    (String) account_id:

    :return
    (Dictionary List): Have all method error of this account
    """
    df_error_account = df_error[df_error[ID_ACCOUNT_COL] == int(account_id)]

    list_description_result = []
    for key in dic_input.keys():
        if (make_seq_switch(df_error_account, dic_input[key]) == 1):
            list_description_result.append({'title': key,
                                            'description': dic_desc[key],
                                            'label': key.replace(' ', '_'),
                                            'status': int(df_error_account[key.replace(' ', '_')])
                                            })
    return list_description_result


def mean_by_month(df):
    """
    Make grouping using columns (month, year,ID_INVOICE_COL and INVOICE_VALUE_COL (Columns stay in const)) to
    make mean by month

    :param
    (Dataframe Pandas) df:

    :return
    (Dataframe Pandas) result_df: Grouping Dataframe with columns (month, year,ID_INVOICE_COL and INVOICE_VALUE_COL
    (Columns stay in const)) and add column  mean_month_invoice.
    """
    result_df = (df[['month', 'year', ID_INVOICE_COL, INVOICE_VALUE_COL]].
                 drop_duplicates().
                 groupby(['month', 'year'])
                 [INVOICE_VALUE_COL].
                 mean().
                 reset_index(name='mean_month_invoice').
                 sort_values(['year', 'month']))
    result_df['mean_month_invoice'] = result_df['mean_month_invoice'].apply(lambda x: int(x))
    return result_df


def plot_values_invoice_time(df, account_id):
    """
    Make elemento to chart line

    :param
    (Dataframe Pandas) df:
    (String) account_id:

    :return
    (Dictionary List): Elements to chart line by time.
    """
    df_acc = (df
              [df[ID_ACCOUNT_COL] == int(account_id)]
              .sort_values(by=['year', 'month'])
              [[DATE_COL, INVOICE_VALUE_COL, 'year', 'month']]
              .drop_duplicates())
    df_mean = mean_by_month(df)
    df_merge = df_acc.merge(df_mean, on=['year', 'month'], how='inner')
    df_merge = df_merge[[DATE_COL, INVOICE_VALUE_COL, 'mean_month_invoice']]
    df_merge[DATE_COL] = pd.to_datetime(df_merge[DATE_COL], format="%Y/%m/%d")
    df_merge[DATE_COL] = df_merge[DATE_COL].apply(
        lambda x: x.timestamp() * 1000)
    return [{'name': 'Invoice Value',
             'data': (df_merge
                      [[DATE_COL, INVOICE_VALUE_COL]].
                      as_matrix().
                      tolist())},
            {'name': 'Average invoice amount per bill cycle',
             'data': (df_merge
                      [[DATE_COL, 'mean_month_invoice']].
                      as_matrix().
                      tolist())}]


def transform_to_highchart_ts_line(data):
    """
    Generate line chart with service by time

    :param
    (Dictionary) data:

    :return
    (Dictionary) dict: Generate line chart by time
    """
    dict = {
        "data": {
            "colors": [
                '#0672CE',
                '#7C3F98',
                '#962B3F',
                '#DB9806',
                '#277859',
                '#BD2B34',
                '#C5621B',

            ],
            "chart": {
                "backgroundColor": '#242424',
                "type": "line"
            },
            "xAxis": {
                "labels": {
                    "style": {
                        "color": "#fff"
                    }
                }
            },
            "yAxis": {
                "gridLineColor": "#ffffff"
            },
            "title": {
                "text": ""
            },
            "dateTimeLabelFormats": {
                "day": "%d of %b",
            },
            "subtitle": {
                "text": 'Click and drag in the plot area to zoom in'
            },
            "tooltip": {
                "pointFormat": '<span style="color:#333333">{series.name}</span>: <b>{point.y}</b><br/>',
                "valueDecimals": 2,
                "split": "true"
            },
            "credits": {"enabled": "false"},
            "legend": {"enabled": "true",
                       "itemStyle": {
                           "color": '#fff'
                       },
                       "itemHoverStyle": {"color": "#0082f0"}
                       },
            "series": list(data)
        }
    }
    return dict


def transform_to_highchart_ts_stacked(data):
    """
    Generate bar stacked chart with service  by time

    :param
    (Dictionary) data:

    :return
    (Dictionary) dict: Generate bar stacked chart with service  by time
    """
    dict = {
        "data": {
            "colors": [
                '#0672CE',
                '#7C3F98',
                '#962B3F',
                '#DB9806',
                '#277859',
                '#BD2B34',
                '#C5621B',

            ],
            "chart": {
                "backgroundColor": '#242424',
                "type": "column"
            },
            "xAxis": {
                "labels": {
                    "style": {
                        "color": "#fff"
                    }
                }
            },
            "plotOptions": {
                "column": {
                    "stacking": 'normal',
                    "dataLabels": {
                        "enabled": "true"
                    }
                },
                "series": {
                    "borderColor": "#242424"
                }
            },
            "yAxis": {
                "gridLineColor": "#ffffff"
            },
            "title": {
                "text": ""
            },
            "dateTimeLabelFormats": {
                "day": "%d of %b",
            },
            "subtitle": {
                "text": 'Click and drag in the plot area to zoom in'
            },
            "tooltip": {
                "pointFormat": '<span style="color:#333333">{series.name}</span>: <b>{point.y}</b><br/>',
                "valueDecimals": 2,
                "split": "true"
            },
            "credits": {"enabled": "false"},
            "legend": {"enabled": "true",
                       "itemStyle": {
                           "color": '#fff'
                       },
                       "itemHoverStyle": {"color": "#0082f0"}
                       },
            "series": list(data)
        }
    }
    return dict


def service_by_time_invoice_line_plot(df, account_id):
    """
        Elements to chart line with service  by time.

        :param
        (Dataframe Pandas) df:
        (String) account_id:

        :return
        (Dictionary List): Elements to chart line with service  by time.
        """

    df_services = (df
                   [df[ID_ACCOUNT_COL] == int(account_id)]
                   [[DATE_COL, ITEM_PRICE_COL, DESCRIPTION_COL, 'year', 'month']]
                   .groupby([DATE_COL, DESCRIPTION_COL, 'year', 'month'])
                   [ITEM_PRICE_COL]
                   .sum()
                   .reset_index(name='sum')
                   .sort_values(by=['year', 'month']))
    df_services[DATE_COL] = pd.to_datetime(
        df_services[DATE_COL], format="%Y/%m/%d")
    df_services['sum'] = (df_services['sum'].
                          apply((lambda x: round(x, 2))))
    df_services[DATE_COL] = df_services[DATE_COL].apply(
        lambda x: x.timestamp() * 1000)

    list_service = list(df_services[DESCRIPTION_COL].unique())
    list_date = list(df_services[DATE_COL].unique())
    list_df_date = [df_services[df_services[DATE_COL] == time] for time in list_date]

    list_df_new_rows = [put_miss_service(df, list_service) for df in list_df_date]

    df_result = pd.concat(list_df_new_rows)

    list_result = ([{'name': service,
                     'data': df_result[(df_result[DESCRIPTION_COL] == service)]
                     [[DATE_COL, 'sum']]
                         .as_matrix()
                         .tolist()
                     }
                    for service in list_service])
    return list_result


def service_by_time_invoice(df, account_id):
    """
        Elements to chart line with service  by time.

        :param
        (Dataframe Pandas) df:
        (String) account_id:

        :return
        (Dictionary List): Elements to chart line with service  by time.
        """
    df_services = (df
                   [df[ID_ACCOUNT_COL] == int(account_id)]
                   [[DATE_COL, ITEM_PRICE_COL, DESCRIPTION_COL, 'year', 'month']]
                   # .drop_duplicates()
                   .groupby([DATE_COL, DESCRIPTION_COL, 'year', 'month'])
                   [ITEM_PRICE_COL]
                   .sum()
                   .reset_index(name='sum')
                   .sort_values(by=['year', 'month']))
    df_services[DATE_COL] = pd.to_datetime(
        df_services[DATE_COL], format="%Y/%m/%d")
    df_services['sum'] = (df_services['sum'].
                          apply((lambda x: round(x, 2))))
    df_services[DATE_COL] = df_services[DATE_COL].apply(
        lambda x: x.timestamp() * 1000)
    list_service = list(df_services[DESCRIPTION_COL].unique())
    list_result = ([{'name': service,
                     'data': df_services[(df_services[DESCRIPTION_COL] == service)]
                     [[DATE_COL, 'sum']]
                         .as_matrix()
                         .tolist()
                     }
                    for service in list_service])
    return list_result


def make_pretty_number(list_dict):
    """
    Transform int in string and apply USA format in string

    :param
    (Dictionary List) list_dict:

    :return
    (Dictionary List) list_dict
    """
    return [list_dict[0], {'content': "$ " + pretty_number(list_dict[1]['content']), 'id': 2}]


def list_service_value_inv(id_inv, data):
    """
    Transform int in string and apply USA format in string by service in account

    :param
    (String) id_inv:
    (Dataframe Pandas) data:

    :return
    (Dictionary List) list_dict
    """

    df_inv_service = list(data[data[ID_INVOICE_COL] == id_inv][[DESCRIPTION_COL, ITEM_PRICE_COL]].values)

    list_service = list(map(make_dic_desc_value, df_inv_service))
    list_result = list_service + [[{'content': 'Total', 'id': 1},
                                   {'content': sum(map(lambda x: x[1]['content'], list_service)), 'id': 2}]]

    return list(map(make_pretty_number, list_result))


def put_miss_service(df, list_service):
    """
    Put the missing service.

    :param
    (Dataframe Pandas) df:
    (Sting List) list_service:

    :return
    (Dataframe Pandas) df_result: Dataframe with the missing services.
    """
    list_present_service = list(df[DESCRIPTION_COL].unique())
    df_result = df
    list_diff = list(set(list_service) - set(list_present_service))

    if (len(list_diff) > 0):
        array_var = df[['ENTDATE', 'year', 'month']].drop_duplicates().values[0]
        list_append = [pd.Series([array_var[0], item, array_var[1], array_var[2], 0], index=df.columns) for item in
                       list_diff]
        df_result = df.append(list_append)

    return df_result
