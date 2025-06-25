# EDA Script for 'DATA SET.csv' File (VS Code Compatible)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Visual settings
sns.set(style="darkgrid")
plt.rcParams["figure.figsize"] = (12, 6)

# Load the dataset
df = pd.read_csv("DATA SET.csv")

# Drop high-missing columns
df.drop(columns=["Results First Posted", "Study Documents"], inplace=True)

# Fill missing categorical columns with indicator values
cat_cols = df.select_dtypes(include='object').columns
df[cat_cols] = df[cat_cols].fillna(df[cat_cols].apply(lambda x: "Missing_" + x.name))

# Fill numerical missing values with median if any
if df['Enrollment'].isnull().sum() > 0:
    df['Enrollment'] = df['Enrollment'].fillna(df['Enrollment'].median())

# Extract 'Country' from 'Locations'
df['Country'] = df['Locations'].apply(lambda x: str(x).split(',')[-1].strip())

# Convert 'Start Date' to datetime
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['Start Month'] = df['Start Date'].dt.to_period('M')

# Visualization helper
def plot_bar(column, title):
    df[column].value_counts().plot(kind='bar', title=title)
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Visualizations
plot_bar("Status", "Status of Clinical Trials")
plot_bar("Phases", "Distribution of Trial Phases")
plot_bar("Age", "Age Group Distribution")
plot_bar("Country", "Top Contributing Countries")

# Time trend of trial starts
df['Start Month'].value_counts().sort_index().plot(kind='line', title='Trials Started Over Time')
plt.ylabel("Number of Trials")
plt.xlabel("Start Month")
plt.tight_layout()
plt.show()

# Save cleaned data
df.to_csv("cleaned_DATA_SET.csv", index=False)
print("EDA completed. Cleaned file saved as 'cleaned_DATA_SET.csv'")
