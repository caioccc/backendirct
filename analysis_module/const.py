PATH_FILE = '../server/analysis_module/data/sample_intel.csv'
PATH_KMEANS = '../server/analysis_module/data/kmeans_result/'
PATH_METHODS_STATUS = '../server/analysis_module/data/risks.csv'

REMOVE_YEAR = 2007
DATE_COL = 'ENTDATE'
INVOICE_VALUE_COL = 'INV_AMT'
ITEM_PRICE_COL = 'ITEM_AMT'

ID_INVOICE_COL = 'INV_ID'
ID_ACCOUNT_COL = 'ACCOUNT_ID'
ID_CLIENT_COL = 'CLIENT_ID'

DESCRIPTION_COL = 'DESCRIPTION'

GROUP_VALUE_INVOICE = ['CLIENT_ID', 'ACCOUNT_ID', 'ENTDATE', 'INV_ID', 'INV_AMT']
GROUP_DESCRIPTION_INVOICE = ['CLIENT_ID', 'ACCOUNT_ID', 'ENTDATE', 'INV_ID', 'INV_AMT', 'DESCRIPTION']
GROUP_INVOICE = ['CLIENT_ID', 'ACCOUNT_ID', 'ENTDATE', 'INV_ID']
GROUP_ACCOUNT_SERVICE_SET = ['CLIENT_ID', 'ACCOUNT_ID', 'services_string']
GROUP_INVOICE_SERVICE_SET = ['ACCOUNT_ID', 'ENTDATE', 'INV_ID', 'services_string']
GROUP_ACCOUNT_INVOICE = ['ACCOUNT_ID', 'ENTDATE', 'INV_ID']
GROUP_ACCOUNT_VALUES = ['CLIENT_ID', 'ACCOUNT_ID', 'ENTDATE', 'INV_ID', 'INV_AMT']
GROUP_PIVOT = ['CLIENT_ID', 'ACCOUNT_ID', 'ENTDATE', 'INV_AMT', 'INV_ID', 'month', 'year']
GROUP_SELECT = ['CLIENT_ID', 'ACCOUNT_ID', 'ENTDATE', 'INV_AMT', 'INV_ID']

CLUSTER_NUMBER_COL = 'k_cluster'
DBSCAN_CLUSTER_OUTLIERS = -1

STATUS_COL = 'status'

dic_name = {'box_plot': 'Method box plot',
            'dbscan_serivce_error': 'Rare service combination',
            'invoice_expensive_cheap': 'Invoice amount variation',
            'low_cluster': 'Smallest group',
            'negative_service': 'Negative amounts',
            'outliers_kmeans': 'Outliers by amount',
            'rare_service': 'Service less frequency',
            'service_low_cluster': 'Set service smallest group',
            'service_outliers_kmeans': 'Set services outliers',
            'zero_service': 'Zero amounts',
            'roll_windows': 'Method moving average in invoice',
            'apriori_rare_service': 'Rare service packages'}

dic_input = {'Unusual service combination': ['apriori_rare_service', 'service_low_cluster', 'service_outliers_kmeans'],
             'Invoice amount variation': ['invoice_expensive_cheap'],
             'Unusual amount': ['low_cluster', 'outliers_kmeans'],
             'Services with Negative Amount': ['negative_service'],
             'Zero Service': ['zero_service']}

dic_ml = {'Unusual service combination': 1, 'Invoice amount variation': 0, 'Unusual amount': 1,
          'Services with Negative Amount': 0,
          'Zero Service': 0}

dic_desc = {'Unusual service combination': 'Invoice have a combination with rare service',
            'Invoice amount variation': 'Invoice have a lower or high values variant by the past month',
            'Unusual amount': 'Invoice have a rare value',
            'Services with Negative Amount': 'Invoices with negative services amount',
            'Zero Service': 'Have some invoice with zero value'}
STATUS_REVIEW = 'status_review'
COMMENT = 'comment_col'

LIST_STATUS_SWITCH = ['Unusual_service_combination',
 'Invoice_amount_variation',
 'Unusual_amount',
 'Services_with_Negative_Amount',
 'Zero_Service']