import streamlit as st
import pandas as pd

# Load your Excel dataset
# Make sure HR_ATTRITION.xlsx is in the same folder
df = pd.read_excel("HR_ATTRITION.xlsx")

st.title("HR Attrition Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
selected_dept = st.sidebar.multiselect("Department", df['Department'].unique())
selected_gender = st.sidebar.multiselect("Gender", df['Gender'].unique())
selected_age = st.sidebar.slider("Age Range", int(df['Age'].min()), int(df['Age'].max()), (20, 50))
selected_edu = st.sidebar.multiselect("Education Level", df['Education'].unique())
selected_salary = st.sidebar.slider("Salary Range", int(df['MonthlyIncome'].min()), int(df['MonthlyIncome'].max()), (2000, 8000))

# Apply filters
filtered_df = df.copy()
if selected_dept:
    filtered_df = filtered_df[filtered_df['Department'].isin(selected_dept)]
if selected_gender:
    filtered_df = filtered_df[filtered_df['Gender'].isin(selected_gender)]
filtered_df = filtered_df[(filtered_df['Age'] >= selected_age[0]) & (filtered_df['Age'] <= selected_age[1])]
if selected_edu:
    filtered_df = filtered_df[filtered_df['Education'].isin(selected_edu)]
filtered_df = filtered_df[(filtered_df['MonthlyIncome'] >= selected_salary[0]) & (filtered_df['MonthlyIncome'] <= selected_salary[1])]

# KPIs
attrition_rate = (filtered_df['Attrition'].value_counts().get('Yes', 0) / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
total_employees = len(filtered_df)
employees_left = filtered_df['Attrition'].value_counts().get('Yes', 0)
avg_tenure = filtered_df['YearsAtCompany'].mean() if len(filtered_df) > 0 else 0
avg_salary = filtered_df['MonthlyIncome'].mean() if len(filtered_df) > 0 else 0

st.metric("Attrition Rate", f"{attrition_rate:.1f}%")
st.metric("Total Employees", total_employees)
st.metric("Employees Left", employees_left)
st.metric("Avg Tenure (Years)", f"{avg_tenure:.1f}")
st.metric("Avg Salary", f"${avg_salary:,.0f}")

# Attrition by Department
st.subheader("Attrition by Department")
dept_counts = filtered_df[filtered_df['Attrition'] == 'Yes']['Department'].value_counts()
st.bar_chart(dept_counts)

# Attrition by Gender
st.subheader("Attrition by Gender")
gender_counts = filtered_df[filtered_df['Attrition'] == 'Yes']['Gender'].value_counts()
st.bar_chart(gender_counts)

# Attrition by Age Group
st.subheader("Attrition by Age Group")
age_bins = pd.cut(filtered_df['Age'], bins=[20,30,40,50,60], labels=["20-30","31-40","41-50","51+"])
age_counts = filtered_df[filtered_df['Attrition'] == 'Yes'].groupby(age_bins).size()
st.bar_chart(age_counts)

# Attrition by Education
st.subheader("Attrition by Education Level")
edu_counts = filtered_df[filtered_df['Attrition'] == 'Yes']['Education'].value_counts()
st.bar_chart(edu_counts)

# Attrition by Salary Range
st.subheader("Attrition by Salary Range")
salary_bins = pd.cut(filtered_df['MonthlyIncome'], bins=[0,4000,6000,8000,10000], labels=["<$40k","$40k-$60k","$60k-$80k",">$80k"])
salary_counts = filtered_df[filtered_df['Attrition'] == 'Yes'].groupby(salary_bins).size()
st.line_chart(salary_counts)

# Attrition Trend Over Time
st.subheader("Attrition Trend Over Time")
if 'DateOfExit' in filtered_df.columns:
    trend = filtered_df[filtered_df['Attrition'] == 'Yes'].groupby(filtered_df['DateOfExit'].dt.month).size()
    st.line_chart(trend)
