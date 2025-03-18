import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# API endpoint for ACS 2021 5-Year Data
api_url = "https://api.census.gov/data/2021/acs/acs5"

# API parameters to fetch relevant data for side gigs
params = {
    "get": "NAME,B01001_001E,B19013_001E,B23025_003E,B25077_001E,B15003_001E",  # Population, Income, Employment, Housing, Education
    "for": "state:*",  # Get data for all states
    "key": "7f96458e1c960a8411c15c2e298b1b456a4d15ad"  # Your API key here
}

# Function to fetch data from the Census API
def fetch_census_data():
    try:
        response = requests.get(api_url, params=params)
        print("Response Status Code:", response.status_code)  # Print status code
        print("Response Text:", response.text)  # Print response content

        response.raise_for_status()  # Raise error for non-200 responses
        data = response.json()

        if data:
            print("Data fetched successfully.")
            return data
        else:
            print("No data available.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Fetch data
data = fetch_census_data()

# Process and print the data
if data:
    # Convert data to a DataFrame
    headers = data[0]
    df = pd.DataFrame(data[1:], columns=headers)

    # Clean and process the data
    df['Population'] = pd.to_numeric(df['B01001_001E'], errors='coerce')
    df['Median_Income'] = pd.to_numeric(df['B19013_001E'], errors='coerce')
    df['Employed_Population'] = pd.to_numeric(df['B23025_003E'], errors='coerce')
    df['Housing_Units'] = pd.to_numeric(df['B25077_001E'], errors='coerce')
    df['Education'] = pd.to_numeric(df['B15003_001E'], errors='coerce')

    # Side Gig Opportunity Factors
    print("\nSide Gig Opportunity Factors:")

    # Example: Top 5 States by Population (Large population = bigger market size for gigs)
    top_states_population = df[['NAME', 'Population']].sort_values(by='Population', ascending=False).head(5)
    print("Top 5 States by Population (Bigger market size):")
    print(top_states_population)

    # Example: States with Highest Median Income (Higher income = more disposable income for side gigs)
    top_states_income = df[['NAME', 'Median_Income']].sort_values(by='Median_Income', ascending=False).head(5)
    print("\nTop 5 States by Median Income (Potential higher spend on side gigs):")
    print(top_states_income)

    # Example: States with Highest Employment Rate (High employment rate may correlate to time scarcity for side gigs)
    top_states_employment = df[['NAME', 'Employed_Population']].sort_values(by='Employed_Population', ascending=False).head(5)
    print("\nTop 5 States by Employed Population (Potential for flexible side gigs):")
    print(top_states_employment)

    # Example: States with Highest Housing Units (More housing units = higher demand for in-person side gigs)
    top_states_housing = df[['NAME', 'Housing_Units']].sort_values(by='Housing_Units', ascending=False).head(5)
    print("\nTop 5 States by Housing Units (In-person side gig demand):")
    print(top_states_housing)

    # Education Levels (Higher education = higher skilled side gigs)
    plt.scatter(df['Education'], df['Median_Income'], alpha=0.5)
    plt.title('Education Level vs Median Income by State (Skilled Side Gig Potential)')
    plt.xlabel('Education Level')
    plt.ylabel('Median Income')
    plt.show()

    # Correlation Analysis (To understand relationships between variables like income, employment, and housing)
    correlation_matrix = df[['Population', 'Median_Income', 'Employed_Population', 'Housing_Units', 'Education']].corr()
    print("\nCorrelation Matrix:")
    print(correlation_matrix)

    # Heatmap for correlation matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap')
    plt.show()

    # Employment vs Housing Units (Demand for housing-based gigs)
    plt.scatter(df['Employed_Population'], df['Housing_Units'], alpha=0.5)
    plt.title('Employed Population vs Housing Units (Housing-based Side Gigs)')
    plt.xlabel('Employed Population')
    plt.ylabel('Housing Units')
    plt.show()

    # Market Potential Score Calculation (Combines factors like Population, Median Income, Employed Population, Housing Units)
    df['Market_Potential_Score'] = (df['Population'] * 0.4) + (df['Median_Income'] * 0.3) + (df['Employed_Population'] * 0.2) + (df['Housing_Units'] * 0.1)
    top_states_market_potential = df[['NAME', 'Market_Potential_Score']].sort_values(by='Market_Potential_Score', ascending=False).head(5)
    print("\nTop 5 States by Market Potential for Side Gigs (Composite Score):")
    print(top_states_market_potential)

    # Regional Demand for Side Gigs (Regional market demand based on population and income)
    region_map = {
        "Northeast": ['Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'Connecticut', 'New York', 'New Jersey', 'Pennsylvania'],
        "Midwest": ['Ohio', 'Indiana', 'Illinois', 'Michigan', 'Wisconsin', 'Minnesota', 'Iowa', 'Missouri', 'North Dakota', 'South Dakota', 'Nebraska', 'Kansas'],
        "South": ['Delaware', 'Maryland', 'Virginia', 'West Virginia', 'North Carolina', 'South Carolina', 'Georgia', 'Florida', 'Alabama', 'Kentucky', 'Tennessee', 'Mississippi', 'Arkansas', 'Louisiana', 'Oklahoma', 'Texas'],
        "West": ['Montana', 'Idaho', 'Wyoming', 'Colorado', 'New Mexico', 'Arizona', 'Utah', 'Nevada', 'California', 'Oregon', 'Washington', 'Alaska', 'Hawaii']
    }

    df['Region'] = df['NAME'].apply(lambda x: next((region for region, states in region_map.items() if x in states), 'Unknown'))

    region_comparison = df.groupby('Region')[['Population', 'Median_Income', 'Employed_Population']].mean().reset_index()
    print("\nRegional Market Demand for Side Gigs:")
    print(region_comparison)

    # Visualizing Regional Comparison
    region_comparison.plot(kind='bar', x='Region', y=['Population', 'Median_Income', 'Employed_Population'], figsize=(10, 6))
    plt.title('Regional Demand for Side Gigs')
    plt.ylabel('Value')
    plt.xlabel('Region')
    plt.show()

    # Top States for Education Level (potential for high-skilled side gigs)
    top_states_education = df[['NAME', 'Education']].sort_values(by='Education', ascending=False).head(5)
    print("\nTop 5 States by Education Level (Skilled Side Gigs Demand):")
    print(top_states_education)

else:
    print("Data fetch failed or no data available.")

