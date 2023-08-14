#import requests
#import telebot
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

url = 'dota/train.csv'
x = pd.read_csv(url, on_bad_lines='skip', delimiter=',')
url = 'dota/target.csv'
y = pd.read_csv(url, index_col = 0, on_bad_lines='skip', delimiter=',')['radiant_won']


columns_with_single_value = [col for col in x.columns if x[col].unique().shape[0] == 1]
x = x.drop(columns_with_single_value, axis = 1)
x = x.drop(['dire_courier_time'], axis = 1)
x = x.drop(['dire_bottle_time'], axis = 1)
x = x.drop(['radiant_bottle_time'], axis = 1)
x = x.drop(['radiant_courier_time'], axis = 1)  #drop


med = x['dire_flying_courier_time'].median()
x['dire_flying_courier_time'] = x['dire_flying_courier_time'].fillna(med)

med = x['radiant_first_ward_time'].median()
x['radiant_first_ward_time'] = x['radiant_first_ward_time'].fillna(med)

med = x['dire_first_ward_time'].median()
x['dire_first_ward_time'] = x['dire_first_ward_time'].fillna(med)

med = x['radiant_flying_courier_time'].median()
x['radiant_flying_courier_time'] = x['radiant_flying_courier_time'].fillna(med) #fillna

# for col in x.columns:
#     pct_missing = np.mean(x[col].isnull())
#     print('{} - {}%'.format(col, round(pct_missing*100))) #процент пропущенных данных

x['radiant_gold'] = x['r1_gold'] + x['r2_gold'] + x['r3_gold'] + x['r4_gold'] + x['r5_gold']
x['dire_gold'] = x['d1_gold'] + x['d2_gold'] + x['d3_gold'] + x['d4_gold'] + x['d5_gold']
x['gold_diff'] = x['radiant_gold'] - x['dire_gold']
x.drop(['radiant_gold', 'dire_gold'], axis=1, inplace=True)


x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=.33, random_state=1)

x_train = x_train.fillna(0)
x_validation = x_validation.fillna(0)

scaler = MinMaxScaler()
x_train = scaler.fit_transform(x_train)
x_validation = scaler.fit_transform(x_validation)

clf = RandomForestClassifier(n_estimators=200, max_depth=7, random_state=228)
clf.fit(x_train, y_train)

print('Train Accuracy:', accuracy_score(y_train, clf.predict(x_train)))
print('Validation Accuracy:', accuracy_score(y_validation, clf.predict(x_validation)))



