import os
import pickle
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# First API Endpoint (Demographic and Economic Data)
api_url_1 = 'https://api.census.gov/data/2021/acs/acs5'
params_1 = {
    'get': 'NAME,B01001_001E,B19013_001E,B23025_003E,B25077_001E,B15003_001E',  # Population, Income, Employment, Housing, Education
    'for': 'state:*',
    'key': '7f96458e1c960a8411c15c2e298b1b456a4d15ad'
}
cache_filename_1 = 'acs_data_1.pkl'

# Second API Endpoint (Finance Data)
api_url_2 = 'https://api.census.gov/data/2021/gov/finance'
params_2 = {
    'get': 'NAME,REVENUE,EXPENDITURE',  # Revenue and Expenditure data for each state
    'for': 'state:*',
    'key': '7f96458e1c960a8411c15c2e298b1b456a4d15ad'
}
cache_filename_2 = 'gov_finance_data.pkl'

# Function to fetch and cache data from the Census API
def fetch_and_cache(api_url, params, cache_filename):
    if os.path.exists(cache_filename):
        print(f"Loading cached data from {cache_filename}")
        with open(cache_filename, 'rb') as f:
            data = pickle.load(f)
    else:
        print(f"Fetching data from API: {api_url}")
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an error for a bad response
        data = response.json()
        with open(cache_filename, 'wb') as f:
            pickle.dump(data, f)
    return data

# Function to fetch data from both APIs
def fetch_and_analyze_data():
    # Fetch data from both API endpoints
    data_1 = fetch_and_cache(api_url_1, params_1, cache_filename_1)
    data_2 = fetch_and_cache(api_url_2, params_2, cache_filename_2)

    # Print the column names for both datasets
    columns_1 = data_1[0]
    columns_2 = data_2[0]
    print("Column Names for Dataset 1 (Demographic & Economic Data):")
    print(", ".join(columns_1))
    print("Column Names for Dataset 2 (Finance Data):")
    print(", ".join(columns_2))

    # Convert the remaining data into DataFrames
    df_1 = pd.DataFrame(data_1[1:], columns=columns_1)
    df_2 = pd.DataFrame(data_2[1:], columns=columns_2)

    # Clean and process the data from both datasets
    # Dataset 1 (Demographic, Income, Employment, Housing, Education)
    df_1['Population'] = pd.to_numeric(df_1['B01001_001E'], errors='coerce')
    df_1['Median_Income'] = pd.to_numeric(df_1['B19013_001E'], errors='coerce')
    df_1['Employed_Population'] = pd.to_numeric(df_1['B23025_003E'], errors='coerce')
    df_1['Housing_Units'] = pd.to_numeric(df_1['B25077_001E'], errors='coerce')
    df_1['Education'] = pd.to_numeric(df_1['B15003_001E'], errors='coerce')

    # Dataset 2 (Revenue and Expenditure)
    df_2['Revenue'] = pd.to_numeric(df_2['REVENUE'], errors='coerce')
    df_2['Expenditure'] = pd.to_numeric(df_2['EXPENDITURE'], errors='coerce')

    # Merge both datasets on the 'NAME' (state) column
    df = pd.merge(df_1, df_2, on='NAME')

    # Side Gig Opportunity Factors
    print("\nSide Gig Opportunity Factors:")

    # Example: Top 5 States by Population
    top_states_population = df[['NAME', 'Population']].sort_values(by='Population', ascending=False).head(5)
    print("Top 5 States by Population (Bigger market size):")
    print(top_states_population)

    # Example: States with Highest Median Income
    top_states_income = df[['NAME', 'Median_Income']].sort_values(by='Median_Income', ascending=False).head(5)
    print("\nTop 5 States by Median Income (Potential higher spend on side gigs):")
    print(top_states_income)

    # Example: States with Highest Employment Rate
    top_states_employment = df[['NAME', 'Employed_Population']].sort_values(by='Employed_Population', ascending=False).head(5)
    print("\nTop 5 States by Employed Population (Potential for flexible side gigs):")
    print(top_states_employment)

    # Example: States with Highest Housing Units
    top_states_housing = df[['NAME', 'Housing_Units']].sort_values(by='Housing_Units', ascending=False).head(5)
    print("\nTop 5 States by Housing Units (In-person side gig demand):")
    print(top_states_housing)

    # Finance Data Analysis
    print("\nState Revenue and Expenditure Analysis:")
    print(df[['NAME', 'Revenue', 'Expenditure']].head())

    # Visualizations for side gig potential
    plt.scatter(df['Education'], df['Median_Income'], alpha=0.5)
    plt.title('Education Level vs Median Income by State (Skilled Side Gig Potential)')
    plt.xlabel('Education Level')
    plt.ylabel('Median Income')
    plt.show()

    # Correlation Analysis
    correlation_matrix = df[['Population', 'Median_Income', 'Employed_Population', 'Housing_Units', 'Education', 'Revenue', 'Expenditure']].corr()
    print("\nCorrelation Matrix:")
    print(correlation_matrix)

    # Heatmap for correlation matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap')
    plt.show()

    # Employment vs Housing Units
    plt.scatter(df['Employed_Population'], df['Housing_Units'], alpha=0.5)
    plt.title('Employed Population vs Housing Units (Housing-based Side Gigs)')
    plt.xlabel('Employed Population')
    plt.ylabel('Housing Units')
    plt.show()

    # Market Potential Score Calculation (Combines factors from both datasets)
    df['Market_Potential_Score'] = (df['Population'] * 0.3) + (df['Median_Income'] * 0.25) + (df['Employed_Population'] * 0.2) + (df['Housing_Units'] * 0.15) + (df['Revenue'] * 0.1)
    top_states_market_potential = df[['NAME', 'Market_Potential_Score']].sort_values(by='Market_Potential_Score', ascending=False).head(5)
    print("\nTop 5 States by Market Potential for Side Gigs (Composite Score):")
    print(top_states_market_potential)

    # Regional Demand for Side Gigs
    region_map = {
        "Northeast": ['Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'Connecticut', 'New York', 'New Jersey', 'Pennsylvania'],
        "Midwest": ['Ohio', 'Indiana', 'Illinois', 'Michigan', 'Wisconsin', 'Minnesota', 'Iowa', 'Missouri', 'North Dakota', 'South Dakota', 'Nebraska', 'Kansas'],
        "South": ['Delaware', 'Maryland', 'Virginia', 'West Virginia', 'North Carolina', 'South Carolina', 'Georgia', 'Florida', 'Alabama', 'Kentucky', 'Tennessee', 'Mississippi', 'Arkansas', 'Louisiana', 'Oklahoma', 'Texas'],
        "West": ['Montana', 'Idaho', 'Wyoming', 'Colorado', 'New Mexico', 'Arizona', 'Utah', 'Nevada', 'California', 'Oregon', 'Washington', 'Alaska', 'Hawaii']
    }

    df['Region'] = df['NAME'].apply(lambda x: next((region for region, states in region_map.items() if x in states), 'Unknown'))

    region_comparison = df.groupby('Region')[['Population', 'Median_Income', 'Employed_Population', 'Revenue', 'Expenditure']].mean().reset_index()
    print("\nRegional Market Demand for Side Gigs:")
    print(region_comparison)

    # Visualizing Regional Comparison
    region_comparison.plot(kind='bar', x='Region', y=['Population', 'Median_Income', 'Employed_Population', 'Revenue', 'Expenditure'], figsize=(10, 6))
    plt.title('Regional Demand for Side Gigs')
    plt.ylabel('Value')
    plt.xlabel('Region')
    plt.show()

    # Top States for Education Level
    top_states_education = df[['NAME', 'Education']].sort_values(by='Education', ascending=False).head(5)
    print("\nTop 5 States by Education Level (Skilled Side Gigs Demand):")
    print(top_states_education)

# Run the function to fetch and analyze the data
fetch_and_analyze_data()
