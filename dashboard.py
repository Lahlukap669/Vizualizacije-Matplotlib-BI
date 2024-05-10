import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
podatki = pd.read_csv("podatkovni_set/heart_2020.csv")

# Data preprocessing
podatki["HeartDisease"] = podatki["HeartDisease"].replace({"Yes": "Ja", "No": "Ne"})
podatki["PhysicalActivity"] = podatki["PhysicalActivity"].replace({"Yes": "Ja", "No": "Ne"})
podatki["AlcoholDrinking"] = podatki["AlcoholDrinking"].replace({"Yes": "Ja", "No": "Ne"})
podatki["Race"] = podatki["Race"].replace({
    "White": "Belopolti",
    "Asian": "Azijci",
    "American Indian/Alaskan Native": "Ameriški Indijanci/Aljaški Domorodci",
    "Hispanic": "Latinski Američani",
    "Black": "Temnopolti",
    "Other": "Drugo"
})

# Set up the Streamlit page configuration
st.set_page_config(layout="wide")
st.title('Nadzorna plošča - Srčne bolezni')

# Unified plot sizes
plot_width, plot_height = 6, 4

# First row: Line plot, BMI box plot, and Physical Activity pie chart
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    starost_bolezen = podatki.groupby(['AgeCategory', 'HeartDisease']).size().unstack()
    fig1, ax1 = plt.subplots(figsize=(plot_width, plot_height))
    starost_bolezen.plot(kind='line', ax=ax1, marker='o')
    ax1.set_xlabel('Starostna kategorija')
    ax1.set_ylabel('Frekvenca ljudi')
    ax1.set_title('Prisotnost srčne bolezni glede na starost', pad=10)
    st.pyplot(fig1, clear_figure=True)

with col2:
    fig2, ax2 = plt.subplots(figsize=(plot_width, plot_height))
    podatki.boxplot(column='BMI', by='HeartDisease', ax=ax2)
    ax2.set_xlabel('Srčna bolezen')
    ax2.set_ylabel('BMI')
    ax2.set_title('Distribucija BMI vrednosti', pad=10)
    fig2.suptitle('')  # Clear the default title from pandas
    st.pyplot(fig2, clear_figure=True)

with col3:
    physical_activity_counts = podatki[podatki['HeartDisease'] == 'Ja']['PhysicalActivity'].value_counts()
    fig3, ax3 = plt.subplots(figsize=(plot_width, plot_height))
    physical_activity_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax3)
    ax3.set_ylabel('')
    ax3.set_title('Delež srčnih bolnikov, ki se ukvarjajo s telesno dejavnostjo', pad=10)
    st.pyplot(fig3, clear_figure=True)

# Second row: Alcohol bar chart and Race bar chart
col4, col5 = st.columns([1, 1])

with col4:
    alcohol_counts = podatki[podatki['HeartDisease'] == 'Ja']['AlcoholDrinking'].value_counts()
    fig4, ax4 = plt.subplots(figsize=(plot_width, plot_height))
    alcohol_counts.plot(kind='bar', ax=ax4)
    ax4.set_xlabel('Uživanje alkohola')
    ax4.set_ylabel('Število posameznikov s srčno boleznijo')
    ax4.set_title('Povezava med uživanjem alkohola in srčno boleznijo', pad=10)
    st.pyplot(fig4, clear_figure=True)

with col5:
    racial_counts = podatki[podatki['HeartDisease'] == 'Ja']['Race'].value_counts(normalize=True) * 100
    fig5, ax5 = plt.subplots(figsize=(plot_width, plot_height))
    racial_counts.plot(kind='bar', ax=ax5)
    ax5.set_xlabel('Rasa')
    ax5.set_ylabel('Odstotki')
    ax5.set_title('Število ljudi s srčno boleznijo glede na raso', pad=10)
    st.pyplot(fig5, clear_figure=True)
