# SMART-RETAIL-ASSISTANT


## Business Understanding

Safaricom's procurement function spans multiple departments, suppliers, and categories — often with varying levels of spend control and oversight. In today’s competitive and cost-sensitive environment, the CFO and leadership team require actionable insights into where money is going, who is spending it, and whether that spend is aligned with strategic priorities such as efficiency, digital transformation, and sustainability.

The goal is to establish a data-driven procurement intelligence system that:

Tracks purchase order (PO) trends over time,

Identifies cost-saving levers,

Highlights supplier performance and risk,

Supports proactive, not reactive, financial decisions.


## Problem Statement

Despite extensive procurement activity, the current visibility into spend data is fragmented and lacks granularity. Key challenges include:

1. Inconsistent classification of spend categories

2. Lack of consolidated supplier insights and trend tracking,

3. Difficulty comparing actual spend versus budget due to missing baseline alignment,

4. No forward-looking spend forecast or variance explanation.

## Objectives

The primary objective of this project are to:

1. Determine the total spend during the review period

2. Perform monthly trend analysis to highlight spikes or anomalies

3. Estimate future spending using current trends

3. Recommend cost-saving opportunities

3. Evaluate strategic alignment of spend with business goals


## Data Preprocessing

This section we prepared the working data for analysis. We intend to do the following:

### Dataset Overview

Load and explore the dataset to understand its structure including available tables, columns, data types and missing values.

Identity relevant data for analysis and determine which columns to focus on.

### Handling Missing values

Use domain knowledge and imputation techniques to manage missing values.

### Data Cleaning
- Standardize categorical values.

- Derive useful data-related data.

- Remove duplicates and inconsistencies.

### Python Libraries Initialization

First, we initialize common libraries we project to utilize in this exercise:

- Pandas, numpy to create and manipulate dataframes

- Seaborn, matplotlib and wordcloud to facilitate any requisite visualizations within the notebook

- Scikit-learn, xgboost  to provide tools for machine learning models, feature scaling,  train-test-split and evaluation metrics.

- nltk, string, textwrap, re to handle cleaning, tokenization and lemmatization.

- tensorflow.keras, keras_tuner used to build and tune neural networks for more complex tasks.

- prophet is used for time series forecasting.

- pickle, json, datetime, os, itertools, warnings for savings models, suppressing warningd and working with loops.

- pulp for linear programming and optimization tasks.

## Data Understanding 

Exploratory Data analysis

Used notebook to explore the data and established the following insights:

### Univariate Analysis

The bulk of purchase orders fall below ksh 5,000, suggesting many small-value transactions. There is also fewer, high value transactions beyond ksh 20,000.

![image](https://github.com/user-attachments/assets/d36c5d2f-544b-4ed3-9390-de1950897033)


### Bivariate Analysis 
1. Top Spending Departments 

The unknown category contributes the largest share of spending, over ksh 12M. This may indicate missing or unclassified data. Major spenders includes: Physical Security CEO, Segments Tribe, Regional Networks Implementation and Operations.

![image](https://github.com/user-attachments/assets/3de34750-4de3-437d-b648-4e9fea4ab6c0)


2. Supplier Frequency

CVXXXX is the most engaged supplier with over 2,000 interactions, significantly ahead of others. This level of activity suggests a strong relationship but also raises a flag on dependency.

![image](https://github.com/user-attachments/assets/c0582e47-747f-43f7-8032-49ee7515f9c1)


3. Monthly trend of PO Amounts 

There is a major spike in PO spending in APRIL 2024, likely tied to year end procurement. Then a dip in May followed by a gradual recovery in June and July.

![image](https://github.com/user-attachments/assets/2a5e93ee-b425-48be-aa50-629a0c7f5d2f)


4. PO Amount by Supplier Type (Local vs Foreign)

Foreign suppliers generally recieve larger, more consistent PO amounts. Local suppliers handle many small orders and a few very large ones.

![image](https://github.com/user-attachments/assets/aba5828f-b7f1-405f-95dc-528ed43d6e96)


5. Spend per Main Category

Corporate Services has the highest spend by far dominating all other categories. Technology Networks, IT and Terminals have very low spend in comparison. There is a large spending imbalance.

![image](https://github.com/user-attachments/assets/3d28a55e-732e-4d78-9a21-694c959de679)


6. Spend per sub-category (top 10)

HR & Staff Welfare, Facilities and Property and Sales and Marketing, Security dominate spending.

![image](https://github.com/user-attachments/assets/607d1cbe-ac42-4200-869c-cfb18271069c)


7. Spend on Women/Youth owned businesses

The majority of POs are going to non-SIG(Others) suppliers. Women-owned suppliers recieve a notable share while youth-owned suppliers are significantly underrepresented.

![image](https://github.com/user-attachments/assets/995dbeab-745d-45b9-b7ac-c8d6c88519ec)


8. Distribution of PO to special Interest Groups

The majority of purchases orders go to suppliers outside of Special Interest Groups. Women-owned businesses account for 17% and youth-owned suppliers are significantly underrepresented at just 3%.

![image](https://github.com/user-attachments/assets/0917a3ed-de08-44c3-a24e-84fb90fb7467)


9. Product Type breakdown

Most procurement activities centers around Travel & Accommodation, Advertising and Facilities Management.

![image](https://github.com/user-attachments/assets/5e47a293-ea83-41b6-999a-2013c2581201)


### Multi-Variate analysis

This chart highlights a clear value disparity between local SIG suppliers and foreign or non-SIG vendors. While youth-owned suppliers have a higher median spend than women-owned ones, both are still on the lower end compared to others. Foreign suppliers consistently receive higher value POs, possibly due to specialization or contract size.

![image](https://github.com/user-attachments/assets/fd5de1f0-f58f-4a00-bf9f-9f29590a7e0e)



## Model Performance & Evaluation 

We evaluated multiple models for Spend Optimization. Key findings include:

- Logistic Regression provided a solid baseline.

- Random Forest and XGBoost offered improved performance by handling more complex patterns.

- Deep Neural Network stood out achieving a validation of accuracy of 89% after hyperparameter tuning.

- This model was selected for deployment in the chatbot.

### Model Performance Comparison Graph

![image](https://github.com/user-attachments/assets/096ede09-0291-4127-ab0d-4c86a4841185)


## Recommendation

- High Model Accuracy

Achieved 89% validation accuracy using Deep neural network, outperforming baseline and tree-based models.

- Real-Time Predictions

Successfully deployed the model in a chatbot that predicts products categoried from natural language input.

- User-Friendly Interface 

Developed a sleek, intuitive chatbot UI streamlit and Tailwild CSS, enhancing adoption across teams.

- Improved Accessibility

Users can access procurement  data through simple chat queries.

- Operational Efficiency

Reduced time spent on repetitive data lookups by empowering teams with instant self-serve insights.


## Conclusions 

- Model Improvement 

Continue iterating on the Deep Learning model with more labeled data to boost accuracy and generalization.

- Pipeline & automation

Set up a model retraining pipeline to automate updates when new data is available.

- Intergrate with real tools

Connecting the Chatbot to the actual systems used by procurement teams, so it becomes part of their everyday work.

- Get real feedback

We plan to test the chatbot with real users, gather feedback and keep improving it based on what is working and what is confusing. 

- Document and Share

We will polish our documentation and create a case study or Github write-up, both to showcase our skills and to  help others who want to build similar tools.

