import streamlit as st
import pandas as pd

st.set_page_config(page_title="Palo Alto Networks HR Analytics", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("Palo Alto Networks.csv")

df = load_data()

st.title("Career Progression & Promotion Gap Analysis")
st.subheader("Palo Alto Networks HR Analytics")

# Promotion gap
df["Promotion Gap"] = df["YearsSinceLastPromotion"]

def promotion_status(x):
    if x <= 2:
        return "Recently Promoted"
    elif x <= 5:
        return "Promotion Due"
    return "Promotion Stagnation"

df["Promotion Status"] = df["Promotion Gap"].apply(promotion_status)

# Filters
st.sidebar.header("Filters")
if "Department" in df.columns:
    departments = st.sidebar.multiselect("Department", sorted(df["Department"].dropna().unique()))
    if departments:
        df = df[df["Department"].isin(departments)]

if "JobRole" in df.columns:
    roles = st.sidebar.multiselect("Job Role", sorted(df["JobRole"].dropna().unique()))
    if roles:
        df = df[df["JobRole"].isin(roles)]

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Employees", len(df))
if "Attrition" in df.columns:
    attrition_rate = (df["Attrition"].eq("Yes").mean() * 100)
    c2.metric("Attrition Rate", f"{attrition_rate:.1f}%")
c3.metric("Avg Promotion Gap", f"{df['Promotion Gap'].mean():.1f} years")
c4.metric("Avg Years at Company", f"{df['YearsAtCompany'].mean():.1f} years")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Promotion Status")
    st.bar_chart(df["Promotion Status"].value_counts())

with col2:
    st.subheader("Average Promotion Gap by Department")
    if "Department" in df.columns:
        dept = df.groupby("Department")["Promotion Gap"].mean().sort_values(ascending=False)
        st.bar_chart(dept)

st.subheader("Job Role vs Average Promotion Gap")
if "JobRole" in df.columns:
    role = df.groupby("JobRole")["Promotion Gap"].mean().sort_values(ascending=False)
    st.bar_chart(role)

st.subheader("Employee Promotion Details")
cols = [c for c in ["JobRole","Department","YearsAtCompany",
                    "YearsSinceLastPromotion","Promotion Gap","Promotion Status",
                    "Attrition"] if c in df.columns]
st.dataframe(df[cols], use_container_width=True)

st.caption("Project: Career Progression and Promotion Gap Analysis for Retention Optimization")
