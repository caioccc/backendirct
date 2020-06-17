import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseNotFound
from django.views.generic import TemplateView

from analysis_module.data import extract_data as ed
from analysis_module.general_methods import *
from page_methods.page_1 import *
from page_methods.page_2 import *
from page_methods.page_3 import *
from pagination import Pagination

extract = ed.ExtractData()
data = extract.extract_data()


class IndexView(TemplateView):
    template_name = 'index.html'


def get_all_params(request):
    """
    This method transform all params in request to dict.


    Parameters:
    request (dict): Request with type GET .

    Returns:
    dict:A request.
    """
    params = request.GET.dict()
    return params


def get_account_id(request):
    """
    This method return an account id informed by frontend in request.


    Parameters:
    request (dict): Request with type GET .

    Returns:
    int:An account id.
    """
    if 'acc' in request.args:
        account_id = int(request.GET.get('acc'))
    else:
        account_id = 0
    return account_id


def get_test(request):
    return JsonResponse({'id': 'deu certo moral'})


def get_value(request):
    """
    This method return a test page to frontend.

    Returns:
    Page Flask:A Page Test.
    """
    all_params = get_all_params(request)
    try:
        result = general_errors(data, **all_params)
        invoices_problems = result.shape[0]
        return JsonResponse({'id': invoices_problems})
    except:
        result = general_errors(data, **all_params)
        invoices_problems = result.shape[0]
        return JsonResponse({'id': invoices_problems})


def get_invoices(request):
    """
    This method return a JSON with total invoices problems.

    Returns:
    json:A dict with total invoices.
    """
    all_params = get_all_params(request)
    try:
        total_invoices = total_account_invoice_client(
            data, **all_params)['Total'][1]
        result = {'total': int(total_invoices)}
    except (Exception,):
        result = {'total': int(0)}

    return JsonResponse(result)


def get_invoices_problems(request):
    """
    This method return a JSON with percent invoices problems.

    Returns:
    json:A dict with percent invoices.
    """
    all_params = get_all_params(request)
    try:
        table = general_errors(data, **all_params)
        invoices_problems = table.shape[0]
        result = {'total': int(invoices_problems)}
    except (Exception,):
        result = {'total': int(0)}
    return JsonResponse(result)


def get_sum_revenue(request):
    """
    This method return a JSON with a sum value of invoices problems.

    Returns:
    json:A dict with a sum value of invoices problems.
    """
    all_params = get_all_params(request)
    try:
        table = general_errors(data, **all_params)
        sum_revenue = table['INV_AMT'].sum()
        result = {'total': round(float(sum_revenue), 2)}
    except (Exception,):
        result = {'total': int(0)}
    return JsonResponse(result)


def get_table_problems(request):
    """
    This method return a JSON with a dict of invoices problems items to listing.

    Returns:
    json:A dict with a dict of invoices problems items to listing.
    """
    all_params = get_all_params(request)
    filter = json.loads(all_params['filter'])
    table = general_errors(data, **all_params)
    table = table[['ACCOUNT_ID', 'INV_ID', 'INV_AMT', 'percentage_error']]
    table = table.rename(columns={'ACCOUNT_ID': 'Account ID', 'INV_ID': 'Invoice ID',
                                  'INV_AMT': 'Invoice Amount', 'percentage_error': 'Risk Level (%)'})

    def str_col(df):
        for col in df.columns:
            df[col] = df[col].apply(lambda x: str(x))
        return df

    table_str = str_col(table)

    def filter_table(df, filter):
        list_result = []
        if 'search' in filter:
            list_col = df.columns
            for col in list_col:
                list_result.append(df[df[col].str.contains(filter['search'], na=False)])
            result_df = pd.concat(list_result)
            return result_df.drop_duplicates()
        return df

    df_filter = filter_table(table_str, filter)
    pagination = Pagination(filter['currentPage'], filter['pageSize'], len(df_filter))
    slice_table = df_filter[(int(pagination.currentPage) - 1) * int(pagination.pageSize): (
        (int(pagination.currentPage) * int(pagination.pageSize)))]
    columns = np.array(slice_table.columns)
    row = np.array(slice_table.values)
    size_cols = np.arange(len(columns)) + 1
    if len(slice_table) > 0:
        new_table = generate_new_table(row, columns, size_cols)
        return JsonResponse(data=new_table, totalPages=pagination.pages(), currentPage=pagination.currentPage,
                            totalItems=len(df_filter),
                            hasNext=pagination.has_next(), hasPrev=pagination.has_prev())
    return JsonResponse(data=[], totalPages='0', currentPage='0', totalItems='0',
                        hasNext=False, hasPrev=False)


def get_dashboard_table(request):
    """
    This method return a JSON with a dict test of invoices problems.

    Returns:
    json:A dict with a dict test of invoices problems.
    """
    all_params = get_all_params(request)
    try:
        return JsonResponse(
            rows=[
                {
                    "Name Error": "Invoice amount variation",
                    "Total client affected": 641,
                    "Sum of invoice affected": 702364.42
                },
                {
                    "Name Error": "Smallest group",
                    "Total client affected": 198,
                    "Sum of invoice affected": 357927.13
                },
                {
                    "Name Error": "Set service Outliers",
                    "Total client affected": 168,
                    "Sum of invoice affected": 238440.31
                },
                {
                    "Name Error": "Rare service packages",
                    "Total client affected": 130,
                    "Sum of invoice affected": 194766.87
                },
                {
                    "Name Error": "Rare service combination",
                    "Total client affected": 106,
                    "Sum of invoice affected": 122667.90
                },
                {
                    "Name Error": "Outliers",
                    "Total client affected": 50,
                    "Sum of invoice affected": 159255.26
                },
                {
                    "Name Error": "Negative amounts",
                    "Total client affected": 46,
                    "Sum of invoice affected": 78147.81
                },
                {
                    "Name Error": "Smallest group",
                    "Total client affected": 1,
                    "Sum of invoice affected": 50593.07
                }
            ],
            columns=[

                {
                    "name": "Name Error",
                    "label": "Name error",
                    "sort": "asc"
                },
                {
                    "name": "Sum of invoice affected",
                    "label": "Sum of invoice affected",
                    "sort": "asc"
                },
                {
                    "name": "Total client affected",
                    "label": "Total client affected",
                    "sort": "asc"
                }
            ])
    except (Exception,):
        return JsonResponse(rows=[],
                            columns=[])


def get_account_invoices(request):
    """
    This method return a JSON with a mean count account all time.

    Returns:
    json:A dict with a mean count account all time.
    """
    all_params = get_all_params(request)
    try:
        total_invoices = mean_count_account_all_time(data, all_params['acc'])
        result = {'total': int(total_invoices[0])}
    except (Exception,):
        result = {'total': int(0)}
    return JsonResponse(result)


def get_amount_average_invoices(request):
    """
    This method return a JSON with a amount average count invoices in all time.

    Returns:
    json:A dict with a amount average count invoices in all time.
    """
    all_params = get_all_params(request)
    try:
        total_invoices = mean_count_account_all_time(data, all_params['acc'])
        result = {'amount': total_invoices[1]}
    except (Exception,):
        result = {'amount': int(0)}
    return JsonResponse(result)


def get_list_problems(request):
    """
    This method return a JSON with a amount average count invoices in all time.

    Returns:
    json:A dict with a amount average count invoices in all time.
    """
    all_params = get_all_params(request)
    # try:
    table = general_errors(data, **all_params)
    list_problems = error_account(table, all_params['acc'])
    result = {'list': list_problems}
    # except (Exception,):
    #     result = {'list': []}
    return JsonResponse(result)


def submit_invoice(request):
    """
    This method return a JSON with a amount average count invoices in all time.

    Returns:
    json:A dict with a amount average count invoices in all time.
    """
    all_params = get_all_params(request)
    to = 'Backoffice'
    if int(all_params['status']) == 3:
        to = 'Customer'
    elif int(all_params['status']) == 2:
        to = 'Review'
    elif int(all_params['status']) == 4:
        to = 'Finish'
    message = 'Invoice ' + all_params['invoice'] + ' sent to ' + to
    try:
        table = general_errors(data, **all_params)
        prev_status_acc = str(int(table[table['INV_ID'] == int(all_params['invoice'])]['status']))
        change_status_acc(table, all_params['invoice'], all_params['status'], all_params)
        if 'message' in all_params:
            change_coment_acc(table, all_params['invoice'], all_params, all_params['message'])
        if 'listproblems' in all_params:
            listproblems = json.loads(all_params['listproblems'])
            set_status_error_acc(table, all_params['acc'], listproblems, all_params)
        result = {'message': message, 'status_code': 200, 'prev_status_acc': prev_status_acc}
    except (Exception,):
        result = {'message': '', 'status_code': 404}
    return JsonResponse(result)


def submit_others(request):
    """
    This method return a JSON with a amount average count invoices in all time.

    Returns:
    json:A dict with a amount average count invoices in all time.
    """
    all_params = get_all_params(request)
    table = general_errors(data, **all_params)

    table_status = str(int(table[table['INV_ID'] == int(all_params['invoice'])]['status']))
    if all_params['prev_status_acc'] == '2':
        table_review = table[table['status'] == 2]
        row_invoice = table[table['INV_ID'] == int(all_params['invoice'])]
        table_concat = pd.concat([table_review, row_invoice])

        list_invoice_same = list(same_invoice_pattern_review(data, table_concat, all_params))
        qtd_invoice = len(list_invoice_same)
    else:
        list_invoice_same = list(same_invoice_pattern(data, table, all_params))
        qtd_invoice = len(list_invoice_same)
    message = ''
    if table_status == '1':
        message = '%d Invoices sent to Backoffice' % qtd_invoice
    elif table_status == '3':
        message = '%d Invoices sent to Customer' % qtd_invoice
    try:
        change_status_acc(table, list_invoice_same, table_status, all_params)
        result = {'message': message}
    except (Exception,):
        result = {'message': ''}
    return JsonResponse(result)


def get_qtd_similar(request):
    all_params = get_all_params(request)
    table = general_errors(data, **all_params)
    # table_status = str(int(table[table['INV_ID'] == int(all_params['invoice'])]['status']))
    try:
        if all_params['prev_status_acc'] == '2':
            qtd = len(list(same_invoice_pattern_review(data, table, all_params)))
        else:
            qtd = len(list(same_invoice_pattern(data, table, all_params)))
        result = {'qtd': str(qtd)}
    except (Exception,):
        result = {'qtd': '0'}
    return JsonResponse(result)


def has_recommendation_invoices(request):
    """
    This method return a JSON with a amount average count invoices in all time.

    Returns:
    json:A dict with a amount average count invoices in all time.
    """
    all_params = get_all_params(request)
    table = general_errors(data, **all_params)
    try:
        all_params_last = make_all_params_last(all_params)
        df_past = read_past_df(all_params_last)
        if ((len(df_past) >= 0)
                and (len(df_past[df_past['status'] == 1]) >= 0)
                and (len(table[table['status'] == 0]) == table.shape[0])):
            result = {'status': 1}
        else:
            result = {'status': 0}
    except (Exception,):
        result = {'status': 0}
    return JsonResponse(result)


def submit_others_complete(request):
    """
    This method return a JSON with a amount average count invoices in all time.

    Returns:
    json:A dict with a amount average count invoices in all time.
    """
    all_params = get_all_params(request)
    table = general_errors(data, **all_params)
    try:
        all_params_last = make_all_params_last(all_params)
        df_past = read_past_df(all_params_last)
        list_invoices_submit_back = df_same_pattern_last_month(data, table, df_past, 1, all_params, all_params_last)
        list_invoices_submit_customer = df_same_pattern_last_month(data, table, df_past, 2, all_params, all_params_last)
        qtd_submit_back = len(list_invoices_submit_back)
        qts_submit_customer = len(list_invoices_submit_customer)
        qtd_submit = qtd_submit_back + qts_submit_customer
        change_status_acc(table, list_invoices_submit_back, 1, all_params)
        change_status_acc(table, list_invoices_submit_customer, 2, all_params)
        result = {'message': '{} Invoices have been resolved'.format(qtd_submit)}
    except (Exception,):
        result = {'message': ''}
    return JsonResponse(result)


def get_qtd_similar_complete(request):
    all_params = get_all_params(request)
    table = general_errors(data, **all_params)

    try:
        all_params_last = make_all_params_last(all_params)
        df_past = read_past_df(all_params_last)
        qtd_back = len(df_same_pattern_last_month(data, table, df_past, 1, all_params, all_params_last))
        qtd_custumer = len(df_same_pattern_last_month(data, table, df_past, 2, all_params, all_params_last))
        qtd = qtd_back + qtd_custumer
        result = {'qtd': qtd}
    except (Exception,):
        result = {'qtd': '0'}
    return JsonResponse(result)


def get_services_details_invoice(request):
    all_params = get_all_params(request)
    items = list_service_value_inv(int(all_params['invoice']), data)
    try:
        result = {'items': items}
    except (Exception,):
        result = {'items': []}
    return JsonResponse(result)


def get_invoices_chart(request):
    all_params = get_all_params(request)
    try:
        invoices = plot_values_invoice_time(data, all_params['acc'])
        result = transform_to_highchart_ts_line(invoices)
    except (Exception,):
        result = {'series': []}
    return JsonResponse(result)


def get_services_chart(request):
    all_params = get_all_params(request)
    try:
        services = service_by_time_invoice_line_plot(data, all_params['acc'])
        result = transform_to_highchart_ts_line(services)
    except (Exception,):
        result = {'series': []}
    return JsonResponse(result)


def get_services_stacked_chart(request):
    all_params = get_all_params(request)
    try:
        services = service_by_time_invoice(data, all_params['acc'])
        result = transform_to_highchart_ts_stacked(services)
    except (Exception,):
        result = {'series': []}
    return JsonResponse(result)


def get_total_invoices_in_month(request):
    all_params = get_all_params(request)
    try:
        total_invoices = total_invoices_in_month(data, **all_params)
        result = {'total': total_invoices}
    except (Exception,):
        result = {'total': int(0)}
    return JsonResponse(result)


def get_percent_invoices_in_risk(request):
    all_params = get_all_params(request)
    # try:
    total_invoices = total_invoices_in_month(data, **all_params)
    table = general_errors(data, **all_params)
    invoices_problems = table.shape[0]
    percent_at_risk = round(
        ((invoices_problems * 100) / total_invoices), 2)
    result = {'total': percent_at_risk}
    # except (Exception,):
    #     result = {'total': int(0)}
    return JsonResponse(result)


def get_total_revenue_at_risk(request):
    all_params = get_all_params(request)
    try:
        table = general_errors(data, **all_params)
        revenue_at_risk = table['INV_AMT'].sum()
        sum_revenue_in_month = sum_amount_invoices_in_month(data, **all_params)
        percent_at_risk = round(
            ((revenue_at_risk * 100) / sum_revenue_in_month), 2)
        result = {'total': percent_at_risk}
    except (Exception,):
        result = {'total': int(0)}
    return JsonResponse(result)


def get_customer_data_chart(request):
    all_params = get_all_params(request)
    try:
        table = general_errors(data, **all_params)
        # dic_bar_total_clients = error_describe_customers(table)
        dic_bar_total_clients = ''
        result = {'data': dic_bar_total_clients}
    except (Exception,):
        result = {'data': []}
    return JsonResponse(result)


def get_value_problems_chart(request):
    all_params = get_all_params(request)
    try:
        table = general_errors(data, **all_params)
        # dic_bar_total_values = error_describe_amount(table)
        dic_bar_total_values = ''
        result = {'data': dic_bar_total_values}
    except (Exception,):
        result = {'data': []}
    return JsonResponse(result)


def get_info_card(request):
    all_params = get_all_params(request)
    table = general_errors(data, **all_params)

    renevue_at_risk, invoices_at_risk, percent_at_risk = get_renevue_invoices_customers(table, data, **all_params)
    percent_at_risk = str(percent_at_risk) + '%'

    pill = get_pill(data, renevue_at_risk, **all_params)
    percent_down = get_percent_down(table, renevue_at_risk)
    renevue_at_risk = int(renevue_at_risk / 1000000)
    icon_new = get_icon_new(percent_down)

    result = {
        'pill': pill,
        'revenueAtRisk': renevue_at_risk,
        'invoicesAtRisk': invoices_at_risk,
        'percentRevenueAtRisk': percent_at_risk,
        'percentDown': percent_down,
        'iconNew': icon_new
    }
    return JsonResponse(result)


def get_summary(request):
    all_params = get_all_params(request)
    table = general_errors(data, **all_params)

    total_month = data[(data['month'] == int(all_params['month'])) & (data['year'] == int(all_params['year']))][
        'INV_ID'].unique().shape[0]
    invoices_at_risk = table.shape[0]
    invoices_to_analyze, invoices_sent_customers, invoices_sent_backoffice = status_invoices(table)
    renevue_at_risk, invoices_at_risk, percent_at_risk = get_renevue_invoices_customers(table, data, **all_params)

    result = {
        'totalMonth': pretty_number(total_month),
        'totalInvoices': pretty_number(invoices_at_risk),
        'toBeAnalyze': pretty_number(invoices_to_analyze),
        'percentRevenueAtRisk': percent_at_risk,
        'sentCustomers': invoices_sent_customers,
        'sentBackOffice': invoices_sent_backoffice
    }
    return JsonResponse(result)


def get_types_risk(request):
    all_params = get_all_params(request)
    table = general_errors(data, **all_params)
    try:
        result = {'types': plot_methods(table, data, all_params)}
    except (Exception,):
        result = {'types': []}
    return JsonResponse(result)


def reset_database(request):
    try:
        reset()
        result = {'status': '1'}
    except (Exception,):
        result = {'status': '0'}
    return JsonResponse(result)


def get_not_analyzed_list(request):
    all_params = get_all_params(request)
    filter = json.loads(all_params['filter'])
    table = general_errors(data, **all_params)
    table_analyse = filter_status(table, 0)
    table_analyse = query_by_methods(table_analyse, all_params['label'].replace('_', ' '))
    table = table_analyse[['ACCOUNT_ID', 'INV_ID', 'INV_AMT', 'percentage_error']]
    table = table.rename(columns={'ACCOUNT_ID': 'Account ID', 'INV_ID': 'Invoice ID',
                                  'INV_AMT': 'Invoice Amount', 'percentage_error': 'Risk Level (%)'})

    def str_col(df):
        for col in df.columns:
            df[col] = df[col].apply(lambda x: str(x))
        return df

    table_str = str_col(table)

    def filter_table(df, filter):
        list_result = []
        if 'search' in filter:
            list_col = df.columns
            for col in list_col:
                list_result.append(df[df[col].str.contains(filter['search'], na=False)])
            result_df = pd.concat(list_result)
            return result_df.drop_duplicates()
        return df

    df_filter = filter_table(table_str, filter)
    pagination = Pagination(filter['currentPage'], filter['pageSize'], len(df_filter))
    slice_table = df_filter[(int(pagination.currentPage) - 1) * int(pagination.pageSize): (
        (int(pagination.currentPage) * int(pagination.pageSize)))]
    columns = np.array(slice_table.columns)
    row = np.array(slice_table.values)
    size_cols = np.arange(len(columns)) + 1
    if len(slice_table) > 0:
        new_table = generate_new_table(row, columns, size_cols)
        resp = {'data': new_table, 'totalPages': pagination.pages(), 'currentPage': pagination.currentPage,
                'totalItems': len(df_filter), 'hasNext': pagination.has_next(), 'hasPrev': pagination.has_prev()}
        return JsonResponse(resp)
    return JsonResponse({'data': [], 'totalPages': '0', 'currentPage': '0', 'totalItems': '0',
                         'hasNext': False, 'hasPrev': False})


def get_backoffice_list(request):
    all_params = get_all_params(request)
    filter = json.loads(all_params['filter'])

    table = general_errors(data, **all_params)
    table_backoffice = filter_status(table, 1)

    table_backoffice = query_by_methods(table_backoffice, all_params['label'].replace('_', ' '))
    table = table_backoffice[['ACCOUNT_ID', 'INV_ID', 'INV_AMT', 'percentage_error']]
    table = table.rename(columns={'ACCOUNT_ID': 'Account ID', 'INV_ID': 'Invoice ID',
                                  'INV_AMT': 'Invoice Amount', 'percentage_error': 'Risk Level (%)'})

    table_str = str_col(table)

    df_filter = filter_table(table_str, filter)
    pagination = Pagination(filter['currentPage'], filter['pageSize'], len(df_filter))
    slice_table = df_filter[(int(pagination.currentPage) - 1) * int(pagination.pageSize): (
        (int(pagination.currentPage) * int(pagination.pageSize)))]
    columns = np.array(slice_table.columns)
    row = np.array(slice_table.values)
    size_cols = np.arange(len(columns)) + 1
    if len(slice_table) > 0:
        new_table = generate_new_table(row, columns, size_cols)
        resp = {'data': new_table, 'totalPages': pagination.pages(), 'currentPage': pagination.currentPage,
                'totalItems': len(df_filter), 'hasNext': pagination.has_next(), 'hasPrev': pagination.has_prev()}
        return JsonResponse(resp)
    return JsonResponse({'data': [], 'totalPages': '0', 'currentPage': '0', 'totalItems': '0',
                         'hasNext': False, 'hasPrev': False})


def get_customer_list(request):
    all_params = get_all_params(request)
    filter = json.loads(all_params['filter'])
    table = general_errors(data, **all_params)
    table_customer = filter_status(table, 3)
    table_customer = query_by_methods(table_customer, all_params['label'].replace('_', ' '))
    table = table_customer[['ACCOUNT_ID', 'INV_ID', 'INV_AMT', 'percentage_error']]
    table = table.rename(columns={'ACCOUNT_ID': 'Account ID', 'INV_ID': 'Invoice ID',
                                  'INV_AMT': 'Invoice Amount', 'percentage_error': 'Risk Level (%)'})

    table_str = str_col(table)

    df_filter = filter_table(table_str, filter)
    pagination = Pagination(filter['currentPage'], filter['pageSize'], len(df_filter))
    slice_table = df_filter[(int(pagination.currentPage) - 1) * int(pagination.pageSize): (
        (int(pagination.currentPage) * int(pagination.pageSize)))]
    columns = np.array(slice_table.columns)
    row = np.array(slice_table.values)
    size_cols = np.arange(len(columns)) + 1
    if len(slice_table) > 0:
        new_table = generate_new_table(row, columns, size_cols)
        resp = {'data': new_table, 'totalPages': pagination.pages(), 'currentPage': pagination.currentPage,
                'totalItems': len(df_filter), 'hasNext': pagination.has_next(), 'hasPrev': pagination.has_prev()}
        return JsonResponse(resp)
    return JsonResponse({'data': [], 'totalPages': '0', 'currentPage': '0', 'totalItems': '0',
                         'hasNext': False, 'hasPrev': False})


def get_review_list(request):
    all_params = get_all_params(request)
    filter = json.loads(all_params['filter'])
    table = general_errors(data, **all_params)
    table_analyse = filter_status(table, 2)
    table_analyse = query_by_methods(table_analyse, all_params['label'].replace('_', ' '))
    table = table_analyse[['ACCOUNT_ID', 'INV_ID', 'INV_AMT', 'percentage_error']]
    table = table.rename(columns={'ACCOUNT_ID': 'Account ID', 'INV_ID': 'Invoice ID',
                                  'INV_AMT': 'Invoice Amount', 'percentage_error': 'Risk Level (%)'})

    def str_col(df):
        for col in df.columns:
            df[col] = df[col].apply(lambda x: str(x))
        return df

    table_str = str_col(table)

    def filter_table(df, filter):
        list_result = []
        if 'search' in filter:
            list_col = df.columns
            for col in list_col:
                list_result.append(df[df[col].str.contains(filter['search'], na=False)])
            result_df = pd.concat(list_result)
            return result_df.drop_duplicates()
        return df

    df_filter = filter_table(table_str, filter)
    pagination = Pagination(filter['currentPage'], filter['pageSize'], len(df_filter))
    slice_table = df_filter[(int(pagination.currentPage) - 1) * int(pagination.pageSize): (
        (int(pagination.currentPage) * int(pagination.pageSize)))]
    columns = np.array(slice_table.columns)
    row = np.array(slice_table.values)
    size_cols = np.arange(len(columns)) + 1
    if len(slice_table) > 0:
        new_table = generate_new_table(row, columns, size_cols)
        resp = {'data': new_table, 'totalPages': pagination.pages(), 'currentPage': pagination.currentPage,
                'totalItems': len(df_filter), 'hasNext': pagination.has_next(), 'hasPrev': pagination.has_prev()}
        return JsonResponse(resp)
    return JsonResponse({'data': [], 'totalPages': '0', 'currentPage': '0', 'totalItems': '0',
                         'hasNext': False, 'hasPrev': False})


def login_auth(request):
    user = authenticate(username=request.GET['username'], password=request.GET['password'])
    if user is not None:
        resp = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.customuser.role.name,
            'group': user.customuser.group.name,
        }
        login(request, user)
        return JsonResponse(resp)
    return HttpResponseNotFound('<h1>Page not found</h1>')


def logout_auth(request):
    logout(request)
    return JsonResponse({'message': 'Logout Successfully', 'status_code': '200'})


# MOCKUP CARDS for LIST RISKS for QA CONFIGURATOR
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return super(CustomJSONEncoder, self).encode(bool(obj))
        return super(CustomJSONEncoder, self).default(obj)


def transform_dict_to_list(dic_t):
    if len(dic_t['items']) > 0:
        result = [(dic_t['name_type'], dic_t['favorite'], dic_t['category'], item['name'], item['status'])
                  for item in dic_t['items']]
    else:
        result = [(dic_t['name_type'], dic_t['favorite'], dic_t['category'], None, None)]
    return result


def make_unit(list_input, list_out):
    return [list_out.append(i) for i in list_input]


def transform_list_to_df(dic_t):
    list_c = list(map(transform_dict_to_list, dic_t))
    list_result = []
    [make_unit(list_c[index], list_result) for index in range(len(list_c))]
    return pd.DataFrame(list_result, columns=['name_type', 'favorite', 'category', 'name', 'status'])


def transform_df_to_list(df):
    list_type = list(df['name_type'].drop_duplicates().values)
    df.fillna(value=0, inplace=True)
    return [{'name_type': type_n, 'favorite': df[df['name_type'] == type_n]['favorite'].drop_duplicates().values[0],
             'category': df[df['name_type'] == type_n]['category'].drop_duplicates().values[0],
             'items': df[df['name_type'] == type_n]
             [['name', 'status']].to_dict('records')} if list(df[df['name_type'] == type_n]['name'].values)[0] != 0 else
            {'name_type': type_n, 'favorite': df[df['name_type'] == type_n]['favorite'].drop_duplicates().values[0],
             'category': df[df['name_type'] == type_n]['category'].drop_duplicates().values[0],
             'items': []} for type_n in list_type]


def save_df_to_csv(path, df):
    df.to_csv(path_or_buf=path, index=False)


def load_csv_to_df(path):
    return pd.read_csv(filepath_or_buffer=path, header=0)


def change_service_status(df, name_service, new_status):
    df.loc[df['name'] == name_service, 'status'] = new_status


def change_favorite(df, name_type):
    df.loc[df['name_type'] == name_type, 'favorite'] = not \
        df.loc[df['name_type'] == name_type]['favorite'].drop_duplicates().values[0]


def qa_get_all_risks_names(request):
    df = load_csv_to_df(PATH_METHODS_STATUS)
    result = list(df['name_type'].drop_duplicates().values)
    return JsonResponse({'result': result})


# Get risk card by name risk
def qa_get_card_by_risk(request):
    df = load_csv_to_df(PATH_METHODS_STATUS)
    risks_list = transform_df_to_list(df)
    if 'risk' in request.GET:
        risk = request.GET['risk']
        result = [dic for dic in risks_list if dic['name_type'] == risk][0]
    else:
        result = {}
    return JsonResponse(result, encoder=CustomJSONEncoder)


def deep_search_dic(string_input, list_input):
    list_a = [list_input for key in list_input.keys() if
              ((type(list_input[key]) == str) and (list_input[key].lower().find(string_input.lower())) >= 0)]
    list_b = [list_input for item in list_input['items'] if item['name'].lower().find(string_input.lower()) >= 0]
    return list_a + list_b


def search_list_qa(string_input, risks_list=transform_df_to_list(load_csv_to_df(PATH_METHODS_STATUS))):
    if string_input.lower() == 'favorite':
        list_result = [item for item in risks_list if item['favorite']]
        return list_result
    else:
        list_result = [deep_search_dic(string_input, dic_list) for dic_list in risks_list]
        list_result = list(filter(None, list_result))
    list_result = [item[0] for item in list_result]
    return list_result


# Function aux to filter
def search_after_sort_array_qa(string_input, risks_list=transform_df_to_list(load_csv_to_df(PATH_METHODS_STATUS))):
    list_result = [deep_search_dic(string_input, dic_list) for dic_list in risks_list]
    list_result = list(filter(None, list_result))
    list_result = [item[0]['name_type'] for item in list_result]
    return list_result


# Filter View To List array risks
def filter_risks_by_string(request):
    df = load_csv_to_df(PATH_METHODS_STATUS)
    risks_list = transform_df_to_list(df)
    string_input = request.GET['q']
    string_sort_select = request.GET['sort']
    primary_list = search_list_qa(string_sort_select, risks_list)
    return JsonResponse({'results': search_after_sort_array_qa(string_input, primary_list)}, encoder=CustomJSONEncoder)


def set_status_method_item(request):
    item = request.GET['item']
    item = json.loads(item)
    df = load_csv_to_df(PATH_METHODS_STATUS)
    change_service_status(df, item['name'], item['status'])
    save_df_to_csv(PATH_METHODS_STATUS, df)
    return JsonResponse({'message': 'ok', 'status_code': 200}, encoder=CustomJSONEncoder)


def favorite_status_method(request):
    name_risk = request.GET['risk']
    df = load_csv_to_df(PATH_METHODS_STATUS)
    change_favorite(df, name_risk)
    save_df_to_csv(PATH_METHODS_STATUS, df)
    return JsonResponse({'message': 'ok', 'status_code': 200}, encoder=CustomJSONEncoder)


def get_reasons_by_inv(request):
    all_params = get_all_params(request)
    df = general_errors(data, **all_params)
    acc = request.GET['acc']
    inv_id = request.GET['invoice']
    comments = get_comment_acc(df, acc, inv_id)
    return JsonResponse({'comments': comments}, encoder=CustomJSONEncoder)
