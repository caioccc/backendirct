import pandas as pd
import numpy as np

df_1 = pd.read_csv('6d96f87fbe6318f9c2193cb8a1828b20978f22043361d11c190af69b4728f010.csv')
# list_col= list(df_1.columns)
# list_col.remove('comment')
#
# df_1 = df_1[list_col]


dic_input = {'Unusual service combination': ['apriori_rare_service', 'service_low_cluster', 'service_outliers_kmeans'],
             'Invoice amount variation': ['invoice_expensive_cheap'],
             'Unusual amount': ['low_cluster', 'outliers_kmeans'],
             'Services with Negative Amount': ['negative_service'],
             'Zero Service': ['zero_service']}


def make_seq_switch(df, cols_select):
    list_data_col = list(df.columns)
    columns_select = [col for col in list_data_col if col in cols_select]
    result_array = np.sum(df[columns_select].values, 1)
    return np.where(result_array >= 1, 1, result_array)


for key in dic_input.keys():
    df_1[key.replace(' ', "_")] = make_seq_switch(df_1, dic_input[key])

df_1.to_csv('6d96f87fbe6318f9c2193cb8a1828b20978f22043361d11c190af69b4728f010.csv', index=False)
