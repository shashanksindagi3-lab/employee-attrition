import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your Excel dataset
df = pd.read_excel("HR_ATTRITION.xlsx")

st.title("HR Attrition Dashboard")

# KPIs
attrition_rate = (df['Attrition'].value_counts().get('Yes', 0) / len(df)) * 100
total_employees = len(df)
employees_left = df['Attrition'].value_counts().get('Yes', 0)
avg_tenure = df['YearsAtCompany'].mean()
avg_salary = df['MonthlyIncome'].mean()

st.metric("Attrition Rate", f"{attrition_rate:.1f}%")
st.metric("Total Employees", total_employees)
st.metric("Employees Left", employees_left)
st.metric("Avg Tenure (Years)", f"{avg_tenure:.1f}")
st.metric("Avg Salary", f"${avg_salary:,.0f}")

# Attrition by Department
st.subheader("Attrition by Department")
dept_counts = df[df['Attrition'] == 'Yes']['Department'].value_counts()
st.bar_chart(dept_counts)

# Attrition by Age Group
st.subheader("Attrition by Age Group")
age_bins = pd.cut(df['Age'], bins=[20,30,40,50,60], labels=["20-30","31-40","41-50","51+"])
age_counts = df[df['Attrition'] == 'Yes'].groupby(age_bins).size()
st.pie_chart(age_counts)

# Attrition by Gender
st.subheader("Attrition by Gender")
gender_counts = df[df['Attrition'] == 'Yes']['Gender'].value_counts()
st.bar_chart(gender_counts)

# Attrition Trend Over Time
st.subheader("Attrition Trend Over Time")
trend = df[df['Attrition'] == 'Yes'].groupby(df['DateOfExit'].dt.month).size()
st.line_chart(trend)

