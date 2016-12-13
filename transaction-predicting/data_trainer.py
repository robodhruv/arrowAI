import pandas as pd
import numpy as np
import sklearn as ml
import matplotlib.pyplot as plt
import scipy.stats
from datetime import datetime

def convert_to_date(date_int):
     date_str = str(date_int)
     return datetime(year=int('19'+ date_str[0:2]),\
      month=int(date_str[2:4]), \
      day=int(date_str[4:6]))

def is_periodic(date_diff):
    intervals = [7,100,300,10000,100000]
    per_tens = []
    for inter in intervals:
        per_tens.append(date_diff/inter)
    num = 0
    for tens in per_tens:
        # print tens
        if scipy.stats.mode(tens)[0][0] == -1:
            return intervals[num],True
    num += 1
    return 0,False

def find_periodic_function(df,acc_var,var_type,min_period):
    amounts = df.loc[:,\
    ['amount','date_of_transaction','account','type_trans','operation']]
    amounts_df = amounts.loc[lambda df: df[var_type] == acc_var]
    print amounts_df
    amount_arr = amounts_df.as_matrix()
    date_int = amount_arr[:,1]
    if date_int.shape[0] < min_period:
        print "non periodic"
        return 0,amount_arr[0,0],amount_arr[0,1]
    else:
        date_shifted = np.roll(date_int,1)
        date_difference = date_shifted - date_int
        date_difference = date_difference[1:]
        # print date_difference
        # if scipy.stats.mode(date_difference)[1][0]\
        # > date_difference.shape[0]/2:
        period,is_period = is_periodic(date_difference)
        if is_period:
            print "periodic"
            # print -scipy.stats.mode(date_difference)[0][0],amount_arr[0,0],amount_arr[0,1]
            return period,\
            amount_arr[0,0],amount_arr[0,1]
        else:
            print "non periodic"
            return 0,amount_arr[0,0],amount_arr[0,1]


def convert_to_coordinates(df):
    coordinate_df = pd.DataFrame({'operation':[],'type':[],\
    'amount':[],'balance':[],'account':[],\
    'norm_amount':[],'norm_balance':[]})
    type_ref = {'PRIJEM':1,'VYDAJ':2,'nan':3,'VYBER':4}
    operation_ref = {'VYBER KARTOU':1,'VKLAD':2,\
    'PREVOD Z UCTU':3,'VYBER':4,'PREVOD NA UCET':5,'nan':6}
    cols_to_norm = ['amount','balance']
    df[['norm_amount','norm_balance']] = df[cols_to_norm].apply(\
    lambda x: abs((x - x.mean()) / (x.max() - x.min())))
    # df[cols_to_norm] = df[cols_to_norm].apply(\
    # lambda x: abs((x - x.mean()) / (x.max() - x.min())))
    num = 0
    # print df
    # print df.amount.shape,df.norm_amount.shape
    # print coordinate_df.loc[num].operation
    for i in df.iterrows():
        # print str(i[1].operation)
        coordinate_df.loc[num] = [i[1].account,\
        i[1].amount,i[1].norm_amount,i[1].norm_balance,\
        i[1].balance,\
        operation_ref[str(i[1].operation)],\
        type_ref[str(i[1].type_trans)]]
        num += 1
    return coordinate_df

# def find_type_periodic_function(df,acc_type):
#     amounts = df.loc[:,\
#     ['amount','type_trans','date_of_transaction','account']]
#     amounts_account_df = amounts.loc[lambda df: df.type_trans == acc_type]
#

def train(file,cusId):
    """
    The function expects a csv file as a file path string.
    assumptions:
        1. the first version excludes the 1st point and we focus only
        on one person's transactions.
        2. the first version assumes trades are in a sorted order.
    1. first it segregates the customers based on their features
    by using knn and stores the trainer in a file.
    2. then it separates periodic payments to similar sources for
    each and every customer at different periods save the function
    with all such added periods.
    3. This function is then subtracted from the transaction data and
    the rest of the transaction data is written to a new data file.
    4. patterns are then recognised based on the customers past data
    these patterns are stores in the file with the periodic functions.
    5. on predict we look at the periodic function and the various
    patterns to give the next prediction.
    """
    data = pd.read_csv(file)
    spec_cust_data = data.loc[lambda df: df.client_id == cusId]
    # spec_cust_data.to_csv('./specific_data.csv')
    periodic_df = pd.DataFrame({'account':[],'amount':[],\
    'start_date':[],'period':[]})
    # print data.columns
    #run a for loop through all account numbers
    num = 0
    per_check_list = ['account','type_trans','operation']
    for var in per_check_list:
        for acc_i in \
        pd.Series.unique(spec_cust_data[var]):
            if str(acc_i) != 'nan':
                # print acc_iter,acc_no
                # print find_periodic_function(spec_cust_data,acc_no)
                period,amount,date = find_periodic_function\
                (spec_cust_data,acc_i,var,3)
                if period != 0:
                    if var == 'account':
                        acc_number = acc_i
                    else:
                        acc_number = 'nan'
                    periodic_df.loc[num] = [acc_number,amount,period,date]
                    num += 1
    # print periodic_df
    periodic_df.drop_duplicates(\
    subset = 'start_date',keep = 'first',inplace = True)
    periodic_df.to_csv('./periodic_data.csv')
    # now we deal with non periodic transactions
    """
    for non periodic data we consider each transaction to be a point in space
    and for the last transaction we find the closest previous transaction
    and assume that the next to that transaction is bound to repeat.
    """
    coordinate_df = convert_to_coordinates(spec_cust_data)
    # print coordinate_df
    coordinate_df.to_csv('./coordinate_data.csv')
    # print "done"
train('./final_data.csv',3)
