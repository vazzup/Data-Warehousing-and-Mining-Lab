import pandas as pd
import pymysql
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://parth:parth@localhost:3306/dwm')

train_bigmart = pd.read_csv('train_bigmart.csv')

train_loan = pd.read_csv('train_loan.csv')

train_loan.info()

temp = train_loan[['Loan_ID',
                  'Gender',
                  'Married',
                  'Dependents',
                  'Education',
                  'ApplicantIncome',
                  'Credit_History']]
temp = temp.dropna(axis = 0, how='any')
temp.to_csv('customers.json')
train_bigmart.info()
train_bigmart.head()
string = 'Item_Identifier Item_Weight Item_Fat_Content Item_Visibility Item_Type Item_MRP'
items = train_bigmart[string.split()]
items.info()
items = items.dropna(axis = 0, how='any')
items.to_csv('item.csv')
string = 'Outlet_Identifier Outlet_Establishment_Year Outlet_Size Outlet_Location_Type Outlet_Type'
outlets = train_bigmart[string.split()]
outlets.info()
outlets = outlets.dropna(axis = 0, how='any')
outlets.to_excel('out.xlsx')

items = pd.read_csv('items.csv')
outlets = pd.read_excel('OUTLETS.xlsx')
customers = pd.read_json('customer.json')

customers.rename(columns={'Loan_ID': 'c_id'}, inplace=True)
items = items.drop_duplicates(subset='Item_Identifier', keep="last")
items.info()

outlets.info()

customers.info()

item_list = items['Item_Identifier']
item_list = list(item_list)
item_list = list(map(lambda x: str(x),item_list))


from random import randrange
import time

start_timestamp = time.mktime(time.strptime('Jun 1 2010  01:33:00', '%b %d %Y %I:%M:%S'))
end_timestamp = time.mktime(time.strptime('Jun 1 2017  12:33:00', '%b %d %Y %I:%M:%S'))

def randomize_time(start_timestamp,end_timestamp):
    return time.strftime('%b %d %Y %I:%M:%S', time.localtime(randrange(start_timestamp,end_timestamp)))

from random import choice
times = []
for i in range(100):
    d = dict()
    temp = randomize_time(start_timestamp,end_timestamp)
    d['id'] = i
    d['time'] = temp[12:]
    d['season'] = choice(['winter','fall','spring','summer'])
    d['date'] = temp[:11]
    d['month'] = temp[:3]
    times.append(d)

timestamps = pd.DataFrame(times)
timestamps.to_csv('timestamps',header = False)

f = open('timestamps','r')
timestamps = pd.DataFrame()
timestamps['id'] = ''
timestamps['time'] = ''
timestamps['months'] = ''
timestamps['season'] = ''
timestamps['date']  = ''
indexs_t = [line.split(sep=',')[0] for line in open('timestamps','r')]
dates_t  = [line.split(sep=',')[1] for line in open('timestamps','r')]
months_t  = [line.split(sep=',')[3] for line in open('timestamps','r')]
season_t  = [line.split(sep=',')[4] for line in open('timestamps','r')]
time_t  = [line.split(sep=',')[5].strip() for line in open('timestamps','r')]
timestamps['id'] = indexs_t
timestamps['time'] = dates_t
timestamps['months'] = months_t
timestamps['season'] = season_t
timestamps['date'] = dates_t

timestamps.info()

timestamps.head()

timestamps['year'] = timestamps['date'].apply(lambda x: x[7:])

timestamps = timestamps[:50].append(timestamps[50:])

## Generating fact table

from random import randint
import random
fact = []
for i in range(100):
    d = dict()
    d['f_id'] = i
    d['o_id'] = outlets['Outlet_Identifier'].iloc[randint(0,99)]
    d['c_id'] = customers['c_id'].iloc[randint(0,99)]
    d['t_id'] = timestamps['id'].iloc[randint(0,99)]
    d['i_id'] = random.choices(item_list,k = 4)
    d['total quantity'] = 4
    total = 0
    
    for i in d['i_id']:
        total += int(items[items['Item_Identifier'] == i]['Item_MRP'])
    
    d['total amount'] = total
    d['i_id'] = str(d['i_id'])
    fact.append(d)

fact_table = pd.DataFrame(fact)
fact_table.head(10)

##OLAP
fact_table.transpose()

fact_table[fact_table['o_id'] == 'OUT046']

t = fact_table[fact_table['o_id'] == 'OUT046']
t[t['total amount'] > 500]

v = fact_table.copy()

def r(id):
    return timestamps.iloc[id]['year']


v['year'] = v['t_id'].apply(r)
v.head(10)

def r(id):
    return timestamps.iloc[id]['date']

v['date'] = v['t_id'].apply(r)
v.drop('year',axis=1).head(10)

v.groupby('year')['total amount'].sum()

a = v.set_index(['year']).sort_index()

a

a[['total amount']].plot(title='Sales amount per year',figsize=(20,6),colormap='flag')

item_list = items['Item_Identifier']
count = dict()


for item in fact_table['i_id']:
    l = item[1:-1].replace('\'','').replace(',',' ').split()
    for each_item in l:
        if each_item not in count.keys():
            count[each_item] = 1
        else:
            count[each_item] += 1

df = pd.DataFrame({'item':list(count.keys()),'count':list(count.values())})
df.head()

%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

f, ax = plt.subplots(figsize=(10, 30))
sns.despine()
sns.set_color_codes("pastel")
sns.barplot(x="count", y="item", data=df,
            label="Total", color="b")


fact_table.to_sql(name='fact_dim_table', con=engine, if_exists = 'append', index=False)

timestamps.to_sql(name='timestamps_dim_table', con=engine, if_exists = 'append', index=False)

items.to_sql(name='items_dim_table', con=engine, if_exists = 'append', index=False)

outlets.to_sql(name='outlets_dim_table', con=engine, if_exists = 'append', index=False)

customers.to_sql(name='customers_dim_table', con=engine, if_exists = 'append', index=False)