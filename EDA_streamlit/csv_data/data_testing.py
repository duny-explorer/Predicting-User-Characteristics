import pandas as pd

# Assuming df is your DataFrame
df = pd.read_csv('dataframe_features.csv')

# Group by 'region' and 'category', then count the occurrences
category_counts = df.groupby(['region', 'category']).size().reset_index(name='count')

# Find the category with the maximum count for each region
max_category = category_counts.loc[category_counts.groupby('region')['count'].idxmax()]

# Rename columns for the resulting DataFrame
df_result = max_category.rename(columns={'count': 'max_count'})

# Display the resulting DataFrame
print(df_result)

df_result.to_csv('C:\PythonProjects\streamlit\result_df.csv')