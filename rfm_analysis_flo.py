# import libraries
import pandas as pd
import numpy as np
import datetime as dt


# Setting the display options for the pandas library.
pd.set_option('display.max_columns', None)


# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


# Reading the dataset.
df_ = pd.read_csv("Case\\rfm_analysis_flo\\flo_data_20k.csv")
df = df_.copy()


# Data Provisioning and Data Understanding
df.head(10)
df.columns
df.info()
df.shape
df.describe()
df.isnull().sum()

df["total_purchase"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["total_spend"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

df.head()


# Converting the date columns to datetime format.
date_columns = ["first_order_date", "last_order_date", "last_order_date_online", "last_order_date_offline"]
df[date_columns] = df[date_columns].apply(lambda x: [pd.to_datetime(date) for date in x])
df.dtypes


# Analyzing the data and making the necessary interpretations.
df.groupby('order_channel').agg({'total_purchase': 'sum',
                                 'total_spend': 'sum',
                                 'master_id': 'count'}).sort_values(by='master_id', ascending=False)

df[["master_id", "total_spend"]].sort_values(by="total_spend", ascending=False).head(10)


df[["master_id", "total_purchase"]].sort_values(by="total_purchase", ascending=False).head(10)


# Data Processing with function
def data_processing(df):
    df["total_purchase"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["total_spend"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]
    date_columns = ["first_order_date", "last_order_date", "last_order_date_online", "last_order_date_offline"]
    df[date_columns] = df[date_columns].apply(lambda x: [pd.to_datetime(date) for date in x])
    return df

data_processing(df)


# Data Preparation for RFM Analysis
last_order = df["last_order_date"].max()
recency_date = dt.datetime(2021, 6, 2)

rfm = df.groupby('master_id').agg({'last_order_date': lambda last_order_date: (recency_date - last_order_date.max()).days,
                                   'total_purchase': lambda total_purchase: total_purchase.sum(),
                                   'total_spend': lambda total_spend: total_spend.sum()})

rfm.columns = ['Recency', 'Frequency', 'Monetary']

rfm.describe().T


# RFM Analysis
rfm["recency_score"] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['Frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm.head()


# Combining the RFM scores to create a single RFM score.
rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm.head()


# Defining the segments based on the RFM scores.
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}


rfm['segment'] = rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str)
rfm['segment'] = rfm['segment'].replace(seg_map, regex=True)

rfm.head()


# Exporting the RFM Analysis Results
rfm[["segment", "Recency", "Frequency", "Monetary"]].groupby("segment").agg(["mean", "count"])
segments = rfm['segment'].value_counts().sort_values(ascending=False)

new_df = df.merge(rfm, on="master_id")
new_df = new_df[new_df["segment"].isin(["loyal_customers", "champions"])]
new_df = new_df[new_df["interested_in_categories_12"].str.contains("KADIN")]
new_df.reset_index(drop=True, inplace=True)
new_df['segment'].unique()
new_df['interested_in_categories_12'].unique()
new_df["master_id"].to_csv("target_customers.csv")



new_df2 = df.merge(rfm, on="master_id")
new_df2 = new_df2[new_df2["segment"].isin(["about_to_sleep", "new_customers"])]
new_df2.reset_index(drop=True, inplace=True)
new_df2["master_id"].to_csv("discount.csv")