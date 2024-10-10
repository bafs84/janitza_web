import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Streamlit app
st.title("Janitza Time Series Data Explorer")

# Intro text
st.markdown("This application allows you to explore time series data from your Janitza devices and check your gridvis server is configured correctly. You can filter by various attributes to analyze the available data. To generate the EXCEL file, the scripts by Yannick Schüpbach need to be used.")

# Link to homepage
st.markdown("For more information, visit the [website](https://nccr-automation.ch) of the Swiss National Centre of Competence in Research 'Automation', NCCR Automation.")

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
if uploaded_file is not None:
    # Load the Excel file
    df = pd.read_excel(uploaded_file)

    # Display filters
    st.sidebar.header("Filter Options")

    # Filter by timebase
    timebase_options = df['timebase'].dropna().unique()
    selected_timebase = st.sidebar.selectbox("Select Timebase", timebase_options)

    # Filter by typename
    typename_options = df['typeName'].dropna().unique()
    selected_typenames = st.sidebar.multiselect("Select Typenames", typename_options)

    # Filter by values
    values_options = df['value'].dropna().unique()
    selected_values = st.sidebar.multiselect("Select Values", values_options)

    # Apply filters to the dataframe
    filtered_df = df[df['timebase'] == selected_timebase]
    if selected_typenames:
        filtered_df = filtered_df[filtered_df['typeName'].isin(selected_typenames)]
    if selected_values:
        filtered_df = filtered_df[filtered_df['value'].isin(selected_values)]

    # Display filtered data for unique devices with traffic light indicators
    unique_devices = df['name'].unique()
    st.write(f"### Available Devices ({len(unique_devices)})")

    for device in unique_devices:
        if device in filtered_df['name'].values:
            status = "🟢 Timeseries Exists"
        else:
            status = "🔴 Timeseries Not Found"
        st.write(f"{device}: {status}")

    # Display filtered dataframe
    st.write("### Filtered Data")
    st.dataframe(filtered_df)

    # Copyright notice
st.markdown("© by Yannick and Ben with support from WEW, 2024")