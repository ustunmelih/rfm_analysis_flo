# Customer Segmentation by RFM Analysis in a FLO Dataset

![rfm](https://analyticahouse.com/Website/assets/img/Blogs/1662302115478/rfm-analizi-nedir_xp2vgk.png)

## What is RFM?

RFM analysis is a data-driven marketing technique that categorizes customers based on their purchasing behavior. By evaluating customers' recency (how recently they made a purchase), frequency (how often they buy), and monetary value (how much they spend), businesses can identify high-value customers and tailor marketing efforts accordingly.Essentially, RFM analysis transforms raw customer data into actionable insights that drive sales and loyalty.

**Recency:** How recently a customer made a purchase. Recent customers are more likely to engage with the brand again.

**Frequency:** How often a customer makes purchases. Regular customers are valuable assets for any business.

**Monetary:** The total amount a customer spends. High-spending customers contribute significantly to revenue.

## Business Case

FLO aims to enhance its marketing strategy by dividing customers into distinct segments based on their purchasing behavior. To achieve this, the company will employ RFM analysis to categorize customers according to their recency, frequency, and monetary value.

## The story of the dataset

- **master_id:** Unique customer number
- **order_channel:** Which channel of the shopping platform used (Android, iOS, desktop, mobile)
- **last_order_channel:** Channel where the last shopping was made
- **first_order_date:** Customer's first shopping date
- **last_order_date:** Customer's latest shopping date
- **last_order_date_online:** Customer's latest shopping date on the online platform
- **last_order_date_offline:** Customer's latest shopping date on offline platform
- **order_num_total_ever_online:** Customer's total number of shopping on the online platform
- **order_num_total_ever_offline:** Customer's total number of shopping on the offline platform
- **customer_value_total_ever_offline:** Total fee paid by the customer in offline shopping
- **customer_value_total_ever_online:** Total fee paid by the customer in online shopping
- **interested_in_categories_12:** List of categories where the customer shopping in the last 12 months

![segments](https://guillaume-martin.github.io/images/rfm-segments.png)
