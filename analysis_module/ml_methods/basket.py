from ..utils import *
import pandas as pd
from apyori import apriori

def basket_to_results(association_rules):
    """
    Transform the association rules in basket in dictionary and dataframe

    :param
    (Dictionary) association_rules:

    :return
    (Dataframe Pandas) df:
    (Dictionary) items_base_dict:
    (Dictionary) items_add_dict:
    """
    items_base_dict = {}
    items_add_dict = {}

    suports = []
    confidences = []
    lifts = []
    items_id = []

    i = 0

    for item in association_rules:
        suports.append(item[1])
        lifts.append(item[2][0][3])
        confidences.append(item[2][0][2])

        items_id.append(i)

        item_base = list(item[2][0].items_base)
        item_add = list(item[2][0].items_add)

        items_base_dict[i] = item_base
        items_add_dict[i] = item_add

        i += 1

    data = {
        'support': suports,
        'confidence': confidences,
        'lift': lifts,
        'items_id': items_id
    }

    df = pd.DataFrame(data)

    return df, items_base_dict, items_add_dict

def transform_df_to_basket(df, month, year):
    """
    Apply apriori in dataframe

    :param
    (Dataframe Pandas) df:
    (Int) month:
    (Int) year:

    :return

    (Int List) all_invoices: Invoice have  rare association rules in services
    """
    records = []
    df = slice_df(df, month, year)

    df = df.sort_values('DESCRIPTION')
    series = df.groupby(['INV_ID'])['DESCRIPTION'].unique()

    for line in series:
        records.append(list(line))

    association_rules = apriori(
        records, min_support=0.01, min_confidence=0.01, min_lift=2, min_length=2)
    rules_df, items_base_dict, items_add_dict = basket_to_results(
        association_rules)

    rules_df = rules_df.sort_values('support')
    rules_df = rules_df[rules_df['support'] < 0.05]

    all_invoices = invoices_with_rule_services(
        df, rules_df, items_base_dict, items_add_dict)
    return all_invoices


def invoices_with_rule_services(df, rules_df, items_base_dict, items_add_dict):
    """
    Search invoice with rare association rules in services

    :param
    (Dataframe Pandas) df:
    (Dataframe Pandas) rules_df:
    (Dictionary) items_base_dict:
    (Dictionary) items_add_dict:

    :return
    (Int List) all_invoices: Invoice have  rare association rules in services
    """
    all_invoices = []

    for i in range(len(rules_df)):
        id = int(rules_df['items_id'].iloc[i])
        all_services = items_base_dict[id] + items_add_dict[id]
        invoices_whith_services = df.loc[(
            df['DESCRIPTION'].str.contains('|'.join(all_services)))]
        invoices_num_services = invoices_whith_services.groupby(
            'INV_ID')['DESCRIPTION'].nunique().to_frame()
        invoices_id = invoices_num_services.index[invoices_num_services['DESCRIPTION'] == len(
            all_services)].tolist()
        all_invoices.extend(invoices_id)

    return all_invoices