import numpy as np
from geopy import *
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.cluster import *
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.stats import pearsonr
import re

cases = pd.read_csv('data/time_series_covid19_confirmed_US.csv') # https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv
vaccinations = pd.read_csv('data/people_vaccinated_us_timeline.csv') # https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/people_vaccinated_us_timeline.csv
counties = pd.read_csv('data/co-est2020.csv', encoding='latin-1') # https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/counties/totals/co-est2020.csv
mask_use = pd.read_csv('data/mask-use-by-county.csv') # https://github.com/nytimes/covid-19-data/blob/master/mask-use/mask-use-by-county.csv


cases['FIPS'] = cases['FIPS'].fillna(0)
cases['Admin2'] = cases['Admin2'].fillna('')
vaccinations = vaccinations.fillna(0)

counties['FIPS'] = counties['STATE'].astype(str).str.zfill(2) + counties['COUNTY'].astype(str).str.zfill(3)
counties['FIPS'] = counties['FIPS'].astype(int)

county_data = pd.merge(
    left = counties,
    right = cases,
    left_on = 'FIPS',
    right_on = 'FIPS'
)

county_data = pd.merge(
    left = county_data,
    right = mask_use,
    left_on = 'FIPS',
    right_on = 'COUNTYFP'
)

county_data.shape

mask_use.columns
tmp_q5a = pd.DataFrame(index = county_data['STNAME'].unique())
tmp_q5a[['NEVER', 'RARELY', 'SOMETIMES', 'FREQUENTLY', 'ALWAYS']] = (county_data.groupby('STNAME')
                                                                     .mean()[['NEVER', 'RARELY', 'SOMETIMES', 'FREQUENTLY', 'ALWAYS']])
tmp_q5a['Cases'] = county_data.groupby('STNAME').sum()['9/12/21']
tmp_q5a.head()
sns.heatmap(tmp_q5a.corr(), annot = True)

import matplotlib
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(18.5, 10.5, forward=True)
fig.set_dpi(100);

X_q5b = county_data.iloc[:, -5:]
y_q5b = county_data.loc[:, '9/12/21']

# Make sure to set random_state = 42 and test_size = 0.33!
X_q5b_train, X_q5b_test, y_q5b_train, y_q5b_test = train_test_split(X_q5b, y_q5b,
                                                                    test_size = 0.33,
                                                                    random_state = 42)

model = LinearRegression()

model.fit(X_q5b_train, y_q5b_train)

y_pred_train = model.predict(X_q5b_train)
y_pred_test = model.predict(X_q5b_test)


from sklearn.metrics import mean_squared_error
# squared = False means RMSE instead of MSE
train_rmse_cases = mean_squared_error(y_q5b_train, y_pred_train, squared = False)
test_rmse_cases = mean_squared_error(y_q5b_test, y_pred_test, squared = False)


train_rmse_cases, test_rmse_cases

X_q5d = county_data.iloc[:, -5:]
y_q5d = county_data.loc[:, '9/12/21'] / county_data['POPESTIMATE2020']

# Make sure to set random_state = 42 and test_size = 0.33!
X_q5d_train, X_q5d_test, y_q5d_train, y_q5d_test = train_test_split(X_q5d, y_q5d,
                                                                    test_size = 0.33,
                                                                    random_state = 42)

model = LinearRegression()

model.fit(X_q5d_train, y_q5d_train)

y_pred_train = model.predict(X_q5d_train)
y_pred_test = model.predict(X_q5d_test)


from sklearn.metrics import mean_squared_error
# squared = False means RMSE instead of MSE
train_rmse_cpc = mean_squared_error(y_q5d_train, y_pred_train, squared = False)
test_rmse_cpc = mean_squared_error(y_q5d_test, y_pred_test, squared = False)

train_rmse_cpc, test_rmse_cpc

sns.scatterplot(x = y_pred_train, y = y_q5d_train);

models = []

for _ in range(1000):
    X_q5f_train, X_q5f_test, y_q5f_train, y_q5f_test = train_test_split(X_q5d, y_q5d,
                                                                    test_size = 0.33,
                                                                    random_state = 42)
    model = LinearRegression()
    model.fit(X_q5f_train, y_q5f_train)
    models.append(model)


specil_x, special_y = X_q5d_test.iloc[100], y_q5d_test.iloc[100]

y_pred = np.array([model.predict([specil_x]) for model in models])
y_true = np.repeat(special_y, 1000)

prop_var = np.var(y_pred) / np.mean((y_true - y_pred) ** 2)
prop_var

y_pred = np.array([model.predict(X_q5d_test) for model in models])

avg_var = np.mean(np.var(y_pred, axis = 0))

y_5i_test = np.expand_dims(y_q5d_test, axis = 0)
avg_mse = np.mean(np.mean((y_5i_test - y_pred) ** 2))

avg_var, avg_mse

