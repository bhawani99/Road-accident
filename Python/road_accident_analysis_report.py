#!/usr/bin/env python
# coding: utf-8

# ## **Road Accident Analysis**  

# ###  **Project Overview**: 
# The"Road Accident Analysis" project is a data validation and cross-checking project in Python, previously implemented using tools like Tableau, Power BI, Excel, and SQL. The primary objective of this project is to analyze and compare the number of road accidents and casualties that occurred between the years 2021 and 2022 in England. The analysis will focus on key aspects such as the number of casualties by year, accident severity, road type, area, light condition, and vehicle type involved in the accidents. 

# ### Goals : 
# Analyze road accidents and casualties between 2021 and 2022.
#  
# Investigate accident severity, road type, area, light condition, and vehicle type's impact on casualties.

# In[1]:


#importing libraries
import pandas as pd
import plotly.graph_objects as go
import warnings 
warnings.filterwarnings('ignore')


# In[2]:


# Load the data into a DataFrame named 'road_accident'
road_accident = pd.read_csv("road_accident.csv")
road_accident.head(5)


# ### **Data Preprocessing**

# In[3]:


#number of rows and columns
road_accident.shape


# In[4]:


#checking for null values
road_accident.isnull().sum()


# In[5]:


#checking for duplicate values
road_accident.duplicated().sum()


# In[6]:


#checking data types
road_accident.dtypes


# In[7]:


# changing data type of column [accident_date] to datetime for further analysis
road_accident['accident_date'] = pd.to_datetime(road_accident['accident_date'], dayfirst=True)


# In[8]:


#checking data types
road_accident.dtypes


# In[9]:


#checking the descriptive statistics
road_accident.describe()


# In[10]:


road_accident.info()


# ### **Data Analysis and Visualization**

# In[11]:


# Number of accident by years
def total_accident_by_year(year):
    filtered_data = road_accident[(road_accident['accident_date'].dt.year == year)]
    total_casualties = filtered_data['accident_index'].nunique()
    return f"{year} Accidents : {total_casualties}"


# In[12]:


print(total_accident_by_year(year=2022))


# In[13]:


# Total number of Accident
total_accident_count = road_accident['accident_index'].nunique()
print("Total number of Accidents :",total_accident_count)


# In[14]:


# Number of Casualties by years
def total_casualties_by_year(year):
    filtered_data = road_accident[(road_accident['accident_date'].dt.year == year)]
    total_casualties = filtered_data['number_of_casualties'].sum()
    return f"{year} Casualties : {total_casualties}"


# In[15]:


print(total_casualties_by_year(year=2022))


# In[16]:


# Total number of Casualties
total_casualties = road_accident['number_of_casualties'].sum()
print("Total number of Casualties :",total_casualties)


# In[17]:


# Casualties by year and accident severity
def total_casualties_by_year_and_severity(year, severity):
    filtered_data = road_accident[(road_accident['accident_date'].dt.year == year) & (road_accident['accident_severity'] == severity)]
    total_casualties = filtered_data['number_of_casualties'].sum()
    return f"{year} {severity} Casualties : {total_casualties}"


# In[18]:


print(total_casualties_by_year_and_severity(year=2022, severity="Fatal"))


# In[19]:


# Function to calculate the total casualties for a specific severity
def total_casualties_by_severity(severity):
    filtered_data = road_accident[road_accident['accident_severity'] == severity]
    return f"{severity} Casualties : {filtered_data['number_of_casualties'].sum()}"


# In[20]:


print(total_casualties_by_severity(severity = "Fatal"))


# In[21]:


# Function to calculate the total casualties for a specific year
def total_casualties_by_year(year):
    filtered_data = road_accident[road_accident['accident_date'].dt.year == year]
    return f"{year} Casualties: {filtered_data['number_of_casualties'].sum()} "


# In[22]:


print(total_casualties_by_year(year=2022))


# In[23]:


# Casualties by month
# Extract month and month name from the 'accident_date' column
road_accident['month'] = road_accident['accident_date'].dt.month
road_accident['month_name'] = road_accident['accident_date'].dt.strftime('%B')

# Filter data for each year and calculate the casualties by each month
year_2021_data = road_accident[road_accident['accident_date'].dt.year == 2021].groupby(['month', 'month_name'])['number_of_casualties'].sum()
year_2022_data = road_accident[road_accident['accident_date'].dt.year == 2022].groupby(['month', 'month_name'])['number_of_casualties'].sum()


# In[24]:


print("Casualties in 2022:", "\n",year_2022_data)


# In[25]:


print("Casualties in 2021:", "\n",year_2021_data)


# In[26]:


#monthly casualties area chart
road_accident['accident_date'] = pd.to_datetime(road_accident['accident_date'], dayfirst=True)
road_accident['month_name'] = road_accident['accident_date'].dt.strftime('%B')
road_accident['year'] = road_accident['accident_date'].dt.year
casualties_by_month_year = road_accident.groupby(['year', 'month_name'])['number_of_casualties'].sum().reset_index()
fig = go.Figure()
years = casualties_by_month_year['year'].unique()
for year in years:
    data_by_year = casualties_by_month_year[casualties_by_month_year['year'] == year]
    fig.add_trace(go.Scatter(x=data_by_year['month_name'], y=data_by_year['number_of_casualties'],
                             mode='lines+markers', stackgroup='one', name=str(year)))


fig.update_layout(title='Monthly Casualties by Year',
                  xaxis_title='Month',
                  yaxis_title='Number of Casualties',
                  xaxis=dict(type='category', categoryorder='array', categoryarray=[
                      'January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']),
                  yaxis=dict(title_standoff=0))


fig.show()


# In[27]:


# casualties by road type for a specific year
def casualties_by_road_type(year):
    road_accident_year = road_accident[road_accident['accident_date'].dt.year == year]
    result = road_accident_year.groupby('road_type')['number_of_casualties'].sum().reset_index()
    result.rename(columns={'number_of_casualties': 'Casualties'}, inplace=True)
    result.sort_values(by='Casualties', ascending=True, inplace=True)
    return result


# In[28]:


casualties_by_road_type(year=2022)


# In[29]:


# clustered bar chart for casualties by road type for a specific year
def clustered_bar_chart_by_road_type(year):
    road_accident_year = road_accident[road_accident['accident_date'].dt.year == year]
    result = road_accident_year.groupby('road_type')['number_of_casualties'].sum().reset_index()
    result.rename(columns={'number_of_casualties': 'Casualties'}, inplace=True)
    result.sort_values(by='Casualties', ascending=True, inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=result['road_type'],
        x=result['Casualties'],
        orientation='h',
        text=result['Casualties'],
        textposition='inside',
        name=str(year),
    ))

    fig.update_layout(
        title=f'Total Casualties per Road Type for {year}',
        xaxis_title='Casualties',
        yaxis_title='Road Type',
    )

    fig.show()


# In[30]:


clustered_bar_chart_by_road_type(year=2022)


# In[31]:


#calculate the total casualties by urban/rural area and plot a donut chart
def donut_chart_by_urban_rural_area():
    total_casualties = road_accident['number_of_casualties'].sum()
    result = road_accident.groupby('urban_or_rural_area')['number_of_casualties'].sum().reset_index()
    result['% Total'] = (result['number_of_casualties'] / total_casualties) * 100
    result['% Total'] = result['% Total'].round(2)
    result.drop(columns=['number_of_casualties'], inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=result['urban_or_rural_area'],
        values=result['% Total'],
        hole=0.6,
        hoverinfo='label+percent',
        textinfo='label+percent',
        textfont_size=15,
        marker=dict(line=dict(color='#000000', width=1))
    ))

    fig.update_layout(
        title='Percentage of Total Casualties by Urban/Rural Area',
        showlegend=False,
    )

    fig.show()


# In[32]:


donut_chart_by_urban_rural_area()


# In[33]:


#calculate the total casualties by vehicle type
def casualties_by_vehicle_type():
    vehicle_type_mapping = {
        'Agricultural vehicle': 'Agriculture',
        'Car': 'Cars',
        'Taxi/Private hire car': 'Cars',
        'Motorcycle 125cc and under': 'Bike',
        'Motorcycle 50cc and under': 'Bike',
        'Motorcycle over 125cc and up to 500cc': 'Bike',
        'Motorcycle over 500cc': 'Bike',
        'Pedal cycle': 'Bike',
        'Bus or coach (17 or more pass seats)': 'Bus',
        'Minibus (8 - 16 passenger seats)': 'Bus',
        'Goods 7.5 tonnes mgw and over': 'Goods',
        'Goods over 3.5t. and under 7.5t': 'Goods',
        'Van / Goods 3.5 tonnes mgw or under': 'Goods',
    }

    road_accident['vehicle_group'] = road_accident['vehicle_type'].map(vehicle_type_mapping)
    result = road_accident.groupby('vehicle_group')['number_of_casualties'].sum().sort_values(ascending=False).reset_index()
    result.rename(columns={'number_of_casualties': 'Casualties'}, inplace=True)
    return result


# In[34]:


casualties_by_vehicle_type()


# In[35]:


#calculate the total casualties by light conditions and plot a donut chart
def donut_chart_by_light_conditions():
    total_casualties = road_accident['number_of_casualties'].sum()
    light_conditions_mapping = {
        'Daylight': 'Day',
        'Darkness - lighting unknown': 'Night',
        'Darkness - lights lit': 'Night',
        'Darkness - lights unlit': 'Night',
        'Darkness - no lighting': 'Night',
    }
    road_accident['Light_Conditions'] = road_accident['light_conditions'].map(light_conditions_mapping)
    result = road_accident.groupby('Light_Conditions')['number_of_casualties'].sum().reset_index()
    result['Total % Casualties'] = (result['number_of_casualties'] / total_casualties) * 100
    result['Total % Casualties'] = result['Total % Casualties'].round(2)
    result.drop(columns=['number_of_casualties'], inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=result['Light_Conditions'],
        values=result['Total % Casualties'],
        hole=0.6,
        hoverinfo='label+percent',
        textinfo='label+percent',
        textfont_size=15,
        marker=dict(line=dict(color='#000000', width=1))
    ))

    fig.update_layout(
        title='Percentage of Total Casualties by Light Conditions',
        showlegend=False,
    )

    fig.show()


donut_chart_by_light_conditions()


# ### Insights from Analysis:

# The dataset consists of 19 columns and 307,973 rows, with no duplicate values and very few null values. 
# 
# Key findings are as follows:
# 
# 1. Total accidents and casualties decreased in the year 2022 compared to 2021.
# 2. In terms of casualties by road type, the "Single Carriage Road" type reported the highest number of casualties.
# 3. Urban areas had the highest number of casualties compared to other areas.
# 4. The vehicle type "car" was involved in the most accidents, with a total of 333,485 occurrences.
# 5. Daytime had the highest number of casualties compared to other light conditions, accounting for 73% of the total casualties.
# 
