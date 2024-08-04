# import libraries
import pandas as pd
import numpy as np
import datetime as dt

# Setting the display options for the pandas library.
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 50)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.width', 500)

# Reading the dataset.
file_path = 'flo_data_20k.csv'
main_df = pd.read_csv(file_path)

df = main_df.copy()


# Data Provisioning and Data Understanding

def check_dataframe(df, row_num=10):
    print("********** Dataset Shape **********")
    print("No. of Rows:", df.shape[0], "\nNo. of Columns:", df.shape[1])
    print("********** Dataset Information **********")
    print(df.info())
    print("********** Types of Columns **********")
    print(df.dtypes)
    print(f"********** First {row_num} Rows **********")
    print(df.head(row_num))
    print(f"********** Last {row_num} Rows **********")
    print(df.tail(row_num))
    print("********** Summary Statistics of The Dataset **********")
    print(df.describe())
    print("********** No. of Null Values In The Dataset **********")
    print(df.isnull().sum())


check_dataframe(df)



df["total_purchase"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]

df["total_spend"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

df.head()


df.info()
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

# Data Processing

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

rfm["rfm_score"] = (rfm['recency_score'].astype(str) +
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

seg_map

rfm['segment'] = rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str)

rfm['segment'] = rfm['segment'].replace(seg_map, regex=True)

rfm.head()

# RFM Analysis Results

rfm[["segment", "Recency", "Frequency", "Monetary"]].groupby("segment").agg(["mean", "count"])
segments = rfm['segment'].value_counts().sort_values(ascending=False)
segments

# Data Export
import matplotlib.pyplot as plt
import seaborn as sns

# define data and keys
data = segments.values
keys = segments.keys().values

# define color palette
palette_color = sns.color_palette('bright')

# create pie chart
plt.pie(data, labels=keys, colors=palette_color, autopct='%.0f%%')


plt.show()


# Exporting the RFM Analysis Results
new_df = df.merge(rfm, on="master_id")

new_df = new_df[new_df["segment"].isin(["loyal_customers", "champions"])]

new_df.head()

new_df = new_df[new_df["interested_in_categories_12"].str.contains("KADIN")]

new_df.reset_index(drop=True, inplace=True)

new_df['segment'].unique()
new_df['interested_in_categories_12'].unique()

new_df["master_id"].to_csv("yeni_marka_hedef_musteri_id.csv")



new_df2 = df.merge(rfm, on="master_id")

new_df2 = new_df2[new_df2["segment"].isin(["about_to_sleep", "new_customers"])]

new_df2.reset_index(drop=True, inplace=True)

new_df2["master_id"].to_csv("indirim_hedef_musteri_ids.csv")