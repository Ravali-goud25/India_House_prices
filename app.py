import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(layout="wide")

# -------------------------------
# Title
# -------------------------------
st.title("🏠 Real Estate Investment Advisor: Predicting Property Profitability & Future Value")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("processed_real_estate_data.csv")

df = load_data()

# -------------------------------
# Sidebar (Global Filters)
# -------------------------------
st.sidebar.header("Global Filters")

selected_city = st.sidebar.multiselect("Select City", df['City'].unique(), default=df['City'].unique()[:3])
selected_bhk = st.sidebar.multiselect("Select BHK", df['BHK'].unique(), default=df['BHK'].unique())

df_filtered = df[
    (df['City'].isin(selected_city)) &
    (df['BHK'].isin(selected_bhk))
]

# -------------------------------
# Tabs
# -------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "📍 Market Explorer",
    "📈 Investment Analysis",
    "🔍 Property Finder"
])

# ===============================
# TAB 1: OVERVIEW
# ===============================
with tab1:
    st.subheader("Market Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Properties", len(df_filtered))
    col2.metric("Avg Price", round(df_filtered['Price_in_Lakhs'].mean(), 2))
    col3.metric("Avg Size", round(df_filtered['Size_in_SqFt'].mean(), 2))

    st.markdown("---")

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Price Distribution")
        fig, ax = plt.subplots()
        sns.histplot(df_filtered['Price_in_Lakhs'], bins=30, kde=True, ax=ax)
        st.pyplot(fig)

    with col5:
        st.subheader("Property Type Distribution")
        fig2, ax2 = plt.subplots()
        sns.countplot(x='Property_Type', data=df_filtered, ax=ax2)
        st.pyplot(fig2)

# ===============================
# TAB 2: MARKET EXPLORER
# ===============================
with tab2:
    st.subheader("Explore Market Trends")

    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox("Select City", df['City'].unique())
    
    with col2:
        price_range = st.slider("Price Range", 0, 500, (50, 300))

    df_city = df[
        (df['City'] == city) &
        (df['Price_in_Lakhs'] >= price_range[0]) &
        (df['Price_in_Lakhs'] <= price_range[1])
    ]

    st.markdown("### Price vs Size")
    fig, ax = plt.subplots()
    sns.scatterplot(x='Size_in_SqFt', y='Price_in_Lakhs', data=df_city, alpha=0.3, ax=ax)
    st.pyplot(fig)

    st.markdown("### Avg Price by BHK")
    bhk_avg = df_city.groupby('BHK')['Price_in_Lakhs'].mean()

    fig2, ax2 = plt.subplots()
    bhk_avg.plot(kind='bar', ax=ax2)
    st.pyplot(fig2)

# ===============================
# TAB 3: INVESTMENT ANALYSIS
# ===============================
with tab3:
    st.subheader("Investment Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Investment Distribution")
        fig, ax = plt.subplots()
        sns.countplot(x='Good_Investment', data=df_filtered, ax=ax)
        st.pyplot(fig)

    with col2:
        st.markdown("### Price Comparison")
        fig2, ax2 = plt.subplots()
        sns.boxplot(x='Good_Investment', y='Price_in_Lakhs', data=df_filtered, ax=ax2)
        st.pyplot(fig2)

    st.markdown("### Amenities vs Investment")

    fig3, ax3 = plt.subplots()
    sns.boxplot(x='Good_Investment', y='Amenities_Count', data=df_filtered, ax=ax3)
    st.pyplot(fig3)

# ===============================
# TAB 4: PROPERTY FINDER
# ===============================
with tab4:
    st.subheader("Find Properties")

    col1, col2, col3 = st.columns(3)

    with col1:
        city = st.selectbox("City", df['City'].unique(), key="finder_city")
    with col2:
        bhk = st.selectbox("BHK", df['BHK'].unique(), key="finder_bhk")
    with col3:
        price = st.slider("Max Price", 0, 500, 200)

    df_search = df[
        (df['City'] == city) &
        (df['BHK'] == bhk) &
        (df['Price_in_Lakhs'] <= price)
    ]

    st.dataframe(df_search.head(20))

    st.markdown("### Investment Checker")

    size = st.number_input("Size", 500, 5000)
    amenities = st.slider("Amenities", 1, 5)
    transport = st.selectbox("Transport", [1, 2, 3])

    if st.button("Check Investment"):
        if (amenities >= 3) and (transport >= 2):
            st.success("Good Investment")
        else:
            st.error("Not a Good Investment")