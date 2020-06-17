def get_renevue_invoices_customers(df, data, **all_params):
    """
    Summary the month risk

    :param
    (Dataframe Pandas) df:
    (Dataframe Pandas) data:
    (Dictionary) all_params:

    :return
    (Int) sum_revenue: Sum os values in invoice in risk
    (Int) invoices_at_risk: Count invoice in risk
    (Float) percent_in_risk: Percentage invoice in risk
    """
    data = data[data['year'] == int(all_params['year'])]
    data = data[data['month'] == int(all_params['month'])]

    df_filtered = df[df['status'] == 0]

    sum_revenue = df_filtered['INV_AMT'].sum()
    sum_revenue = sum_revenue

    invoices_at_risk = df.shape[0]

    sum_all_invoices = data[['INV_ID', 'INV_AMT']].drop_duplicates()['INV_AMT'].sum()

    percent_in_risk = round((sum_revenue / sum_all_invoices) * 100, 2)

    return sum_revenue, invoices_at_risk, percent_in_risk


def get_pill(df, revenue_at_risk, **all_params):
    """
    Classify the status of Billing cycle in "Critial", "Major" or "Minor"

    :param
    (Dataframe Pandas) df:
    (Int) revenue_at_risk:
    (Dictionary) all_params:

    :return
    (String) result: Status Billing cycle
    """
    result = ''
    df = df[df['year'] == int(all_params['year'])]
    df = df[df['month'] == int(all_params['month'])]
    total_revenue = df[['INV_ID', 'INV_AMT']].drop_duplicates()['INV_AMT'].sum()
    percent_at_risk = (revenue_at_risk / total_revenue) * 100

    if percent_at_risk > 10:
        result = 'Critical'
    elif percent_at_risk > 5:
        result = 'Major'
    else:
        result = 'Minor'

    return result


def get_percent_down(df, current_revenue_at_risk):
    """

    Percentage of invoice in real risk Classify in Backofficer or Customer.
    :param
    Dataframe Pandas) df:
    (Int) current_revenue_at_risk:

    :return
    (Float) percent_down: Percentage classify
    """
    initial_revenue_at_risk = df['INV_AMT'].sum()
    percent_down = round((((current_revenue_at_risk / initial_revenue_at_risk) - 1) * 100), 2)
    return percent_down


def get_icon_new(percent_down):
    """
    Verify the Billing cycle have invoice with status different of not Classify(Status 0)

    :param
    (Float) percent_down:

    :return
    (Boolean) result: Have just invoice in not Classify status.
    """
    result = True
    if percent_down == 0.0:
        return False
    return result
