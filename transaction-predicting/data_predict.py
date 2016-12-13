import numpy as np
import pandas as pd
import sklearn as ml

def find_periodic_transactions(date_int,df):
    payments_df = pd.DataFrame({'account':[],'amount':[]})
    num = 0
    for i in df.iterrows():
        if int(date_int - i[1].start_date)%int(i[1].period) == 0:
            payments_df.loc[num] = [i[1].account,i[1].amount]
            num += 1
    # print payments_df
    return payments_df

def find_distance(first,second):
    account_contri = 0
    if first.account == second.account:
        account_contri = -1
    amount_contri = (first.norm_amount - second.norm_amount)**2
    balance_contri = (first.norm_balance - second.norm_balance)**2
    type_contri = (first.type - second.type)**2
    operation_contri = (first.operation - second.operation)**2
    distance = np.sqrt(amount_contri + balance_contri + type_contri + \
    operation_contri)

    return distance - account_contri

def find_connected_transactions(date_int,df,last_transaction):
    distance_arr = []
    for i in range(df.shape[0]-1):
        distance_arr.append(find_distance(df.loc[i],last_transaction))
    index_num = []
    for num in range(5):
        index_num.append(distance_arr.index(min(distance_arr)))
        distance_arr.remove(min(distance_arr))
    # print ind
    coordinate_df = pd.DataFrame({'account':[],'amount':[]})
    for num,ind in enumerate(index_num):
        coordinate_df.loc[num] = [df.loc[ind+1].account,df.loc[ind+1].amount]
    # print coordinate_df
    return coordinate_df

def predict(periodic_file,coordinate_file,date_int):
    periodic_df = pd.read_csv(periodic_file)
    coordinate_df = pd.read_csv(coordinate_file)
    payments_df = find_periodic_transactions(date_int,periodic_df)
    coordinate_df = find_connected_transactions(date_int,coordinate_df,\
    coordinate_df.loc[coordinate_df.shape[0]-1])
    num = payments_df.shape[0]
    # print payments_df
    for i in coordinate_df.iterrows():
        payments_df.loc[num] =\
         [i[1].account,i[1].amount]
        num += 1
    # print payments_df
    # spec_cust_data = data.loc[lambda df: df.client_id == cusId]
    temp_payments_df = payments_df[payments_df.isnull().any(axis = 1)]
    print temp_payments_df[1:]
    new_payments_df = payments_df.drop_duplicates(\
    subset = 'account',keep = 'first',inplace = False)
    num = new_payments_df.shape[0]
    for i in temp_payments_df.iterrows():
        new_payments_df.loc[num] = [i[1].account,i[1].amount]
    # new_payments_df = new_payments_df.append(temp_payments_df[1:])
    # print new_payments_df
    return new_payments_df.to_json('./predicted_values.json')

predict('./periodic_data.csv','./coordinate_data.csv',930312)
