# =============================================================================
# Section 1: Import Libraries and Set Plot Styles
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# =============================================================================
# Section 2: Load and Inspect the Data
# =============================================================================

df = pd.read_csv("C:\\Users\\Anshul Jain\\OneDrive\\pyt data.csv")

print(df.info())
print(df.describe())

# =============================================================================
# Section 3: Data Cleaning and Preparation
# =============================================================================

# Clean column names
df.columns = df.columns.str.strip().str.replace(r"[()]", "", regex=True).str.replace(' ', '_')

# Convert numeric columns
cols_to_convert = [
    'Monthly_Listeners_Millions',
    'Total_Streams_Millions',
    'Total_Hours_Streamed_Millions',
    'Avg_Stream_Duration_Min',
    'Streams_Last_30_Days_Millions',
    'Skip_Rate_%'
]
df[cols_to_convert] = df[cols_to_convert].apply(pd.to_numeric, errors='coerce')

# Drop missing or duplicate entries
df = df.dropna()
df = df.drop_duplicates()

# Create a new feature
df['Streams_per_Hour'] = df['Total_Streams_Millions'] / df['Total_Hours_Streamed_Millions']

# =============================================================================
# Section 4: Visualizations
# =============================================================================

# 4.1 Top 10 Streamed Artists
top_artists = df.groupby('Artist')['Total_Streams_Millions'].sum().sort_values(ascending=False).head(10).reset_index()
plt.figure(figsize=(12, 7))
sns.barplot(data=top_artists, y='Artist', x='Total_Streams_Millions', hue='Artist', palette='viridis', dodge=False, legend=False)
plt.title("Top 10 Streamed Artists (Total Streams)", fontsize=16)
plt.xlabel("Total Streams (Millions)")
plt.ylabel("Artist")
for index, value in enumerate(top_artists['Total_Streams_Millions']):
    plt.text(value + 1, index, f'{value:.1f}', va='center')
plt.tight_layout()
plt.show()

# 4.2 Total Streams by Country
top_countries = df.groupby('Country')['Total_Streams_Millions'].sum().sort_values(ascending=False).reset_index()
plt.figure(figsize=(14, 7))
sns.barplot(data=top_countries, y='Country', x='Total_Streams_Millions', hue='Country', palette='coolwarm', dodge=False, legend=False)
plt.title("Total Streams by Country", fontsize=16)
plt.xlabel("Total Streams (Millions)")
plt.ylabel("Country")
for index, value in enumerate(top_countries['Total_Streams_Millions']):
    plt.text(value + 1, index, f'{value:.1f}', va='center')
plt.tight_layout()
plt.show()

# =============================================================================
# Section 5: More Visualizations
# =============================================================================

# 5.1 Box Plot: Total Streams by Platform Type
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Platform_Type', y='Total_Streams_Millions', hue='Platform_Type', palette='Set2', dodge=False, legend=False)
plt.title("Total Streams by Platform Type", fontsize=16)
plt.xlabel("Platform Type")
plt.ylabel("Total Streams (Millions)")
plt.tight_layout()
plt.show()

# 5.2 Pie Chart: Top 5 Genres
top_genres = df.groupby('Genre')['Total_Streams_Millions'].sum().sort_values(ascending=False).head(5)
plt.figure(figsize=(8, 8))
plt.pie(top_genres.values, labels=top_genres.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title("Top 5 Genres by Total Streams", fontsize=16)
plt.tight_layout()
plt.show()

# 5.3 Pie Chart: Artist Distribution by Country
country_counts = df['Country'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(country_counts.values, labels=country_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3'))
plt.title('Artist Distribution by Country', fontsize=16)
plt.tight_layout()
plt.show()

# =============================================================================
# Section 6: Scatter, Histogram, Heatmap
# =============================================================================

# 6.1 Scatter Plot: Skip Rate vs Avg Stream Duration
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Avg_Stream_Duration_Min', y='Skip_Rate_%', hue='Genre', palette='Set2', s=100)
plt.title('Skip Rate vs Avg Stream Duration', fontsize=16)
plt.xlabel('Avg Stream Duration (Min)')
plt.ylabel('Skip Rate (%)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 6.2 Histogram: Distribution of Monthly Listeners
plt.figure(figsize=(8, 5))
sns.histplot(df['Monthly_Listeners_Millions'], bins=20, kde=True, color='skyblue')
plt.title('Distribution of Monthly Listeners', fontsize=16)
plt.xlabel('Monthly Listeners (Millions)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# 6.3 Heatmap: Correlation
plt.figure(figsize=(10, 6))
sns.heatmap(df[[
    'Monthly_Listeners_Millions',
    'Total_Streams_Millions',
    'Total_Hours_Streamed_Millions',
    'Avg_Stream_Duration_Min',
    'Streams_Last_30_Days_Millions',
    'Skip_Rate_%'
]].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap', fontsize=16)
plt.tight_layout()
plt.show()

# =============================================================================
# Section 7: Extra Analysis
# =============================================================================

# 7.1 Top 10 Countries by Streams
top10_countries = top_countries.head(10)
plt.figure(figsize=(10, 5))
sns.barplot(data=top10_countries, x='Country', y='Total_Streams_Millions', hue='Country', palette='mako', dodge=False, legend=False)
plt.title('Top 10 Countries by Total Streams', fontsize=16)
plt.xticks(rotation=45)
plt.xlabel('Country')
plt.ylabel('Total Streams (Millions)')
plt.tight_layout()
plt.show()

# 7.2 Top 10 Artists by Streams Per Hour
top10_efficiency = df.sort_values('Streams_per_Hour', ascending=False).head(10)
plt.figure(figsize=(10, 5))
sns.barplot(data=top10_efficiency, x='Artist', y='Streams_per_Hour', hue='Artist', palette='cubehelix', dodge=False, legend=False)
plt.title('Top 10 Artists: Streams per Hour Efficiency', fontsize=16)
plt.xticks(rotation=45)
plt.ylabel('Streams per Hour')
plt.xlabel('Artist')
plt.tight_layout()
plt.show()
