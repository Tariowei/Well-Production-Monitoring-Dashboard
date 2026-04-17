import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.title("Well Production Analytics Dashboard")

# Upload file (better than hardcoding path)
file = st.file_uploader('2-production_history.txt', type=["txt", "csv"])

if file is not None:

    # Read data
    data = pd.read_csv(file, sep="\t")

    # Select well
    wells = data['UID'].unique()
    selected_well = st.sidebar.radio("Select Well", wells)

    # Filter data
    df_well = data[data['UID'] == selected_well].copy()

    # -------------------------
    # METRICS
    # -------------------------
    total_oil = df_well['OIL'].sum()
    total_water = df_well['WATER'].sum()
    total_hours = df_well['HOURS'].sum()

    # Avoid division issues
    avg_gor = (df_well['GAS'] / df_well['OIL'].replace(0, 1)).mean()

    c1, c2 = st.columns(2)

    c1.metric("Total Oil (STB)", int(total_oil))
    c2.metric("Total Water (STB)", int(total_water))

    c1.metric("Average GOR (SCF/STB)", int(avg_gor * 1000))
    c2.metric("Total Hours", int(total_hours))

    # -------------------------
    # PRODUCTION PLOTS
    # -------------------------
    st.subheader("Production Trends")

    fig_oil = px.area(df_well, x='Date', y='OIL', title='Oil Production')
    c1.plotly_chart(fig_oil)

    fig_water = px.area(df_well, x='Date', y='WATER', title='Water Production')
    c2.plotly_chart(fig_water)

    fig_gas = px.area(df_well, x='Date', y='GAS', title='Gas Production')
    c1.plotly_chart(fig_gas)

    fig_hours = px.area(df_well, x='Date', y='HOURS', title='Operating Hours')
    c2.plotly_chart(fig_hours)

    # -------------------------
    # YEARLY SUMMARY
    # -------------------------
    st.subheader("Yearly Production Summary")

    df_well['Date'] = pd.to_datetime(df_well['Date'])
    df_well.set_index('Date', inplace=True)

    yearly = df_well[['OIL', 'WATER', 'GAS', 'HOURS']].resample('Y').sum()

    st.dataframe(yearly)

else:
    st.write("Please upload a dataset to begin.")