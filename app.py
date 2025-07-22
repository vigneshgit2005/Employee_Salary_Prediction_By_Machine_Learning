import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# Page Configuration
st.set_page_config(
    page_title="Employee Salary Data Viewer",
    page_icon="📊",
    layout="wide"
)

# Header Styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    file_path = "Salary Data.csv"
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            required_cols = {'Age', 'Gender', 'Education Level', 'Job Title', 'Years of Experience', 'Salary'}
            if required_cols.issubset(df.columns):
                return df.dropna()
        except Exception:
            pass
    return generate_sample_data()

# Fallback Sample Data
@st.cache_data
def generate_sample_data(n_samples=300):
    np.random.seed(42)
    job_titles = [
        'Software Engineer', 'Data Analyst', 'Senior Manager', 'Sales Associate',
        'Director', 'Marketing Analyst', 'Product Manager', 'Sales Manager',
        'Marketing Coordinator', 'Senior Scientist', 'Business Analyst',
        'Project Manager', 'Operations Coordinator', 'Financial Analyst',
        'HR Manager', 'Senior Developer', 'Marketing Manager', 'Quality Assurance'
    ]
    data = []
    for _ in range(n_samples):
        age = np.random.randint(22, 61)
        gender = np.random.choice(['Male', 'Female'])
        education = np.random.choice(['Bachelor\'s', 'Master\'s', 'PhD'], p=[0.6, 0.3, 0.1])
        job_title = np.random.choice(job_titles)
        experience = min(np.random.randint(0, age - 20), 40)
        base = 40000 + experience * 3000
        if education == "Master's": base += 20000
        elif education == "PhD": base += 40000
        if 'Manager' in job_title or 'Senior' in job_title: base *= 1.2
        if 'Director' in job_title: base *= 1.4
        salary = round(base * (0.9 + np.random.rand() * 0.3) / 1000) * 1000
        data.append({
            'Age': age,
            'Gender': gender,
            'Education Level': education,
            'Job Title': job_title,
            'Years of Experience': experience,
            'Salary': salary
        })
    return pd.DataFrame(data)

# Experience Grouping Function
def group_experience(exp):
    if exp <= 5: return "0-5 yrs"
    elif exp <= 10: return "6-10 yrs"
    elif exp <= 15: return "11-15 yrs"
    elif exp <= 20: return "16-20 yrs"
    else: return "20+ yrs"

# App Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white;">📊 Employee Salary Dashboard</h1>
    <p style="color: white;">Visual insights from salary dataset</p>
</div>
""", unsafe_allow_html=True)

# Load the Data
df = load_data()

# Show DataFrame
st.subheader("📋 Data Preview")
st.dataframe(df, use_container_width=True)

# Add Experience Group
df['Experience Group'] = df['Years of Experience'].apply(group_experience)

# Plot 1: Age Distribution
st.subheader("📅 Age Distribution")
age_fig = px.histogram(df, x='Age', nbins=20, color_discrete_sequence=['#636EFA'])
age_fig.update_layout(bargap=0.1)
st.plotly_chart(age_fig, use_container_width=True)
# Section: Mean vs Median Age
st.subheader("📊 Mean vs Median Age")

mean_age = df['Age'].mean()
median_age = df['Age'].median()

stat_df = pd.DataFrame({
    'Statistic': ['Mean Age', 'Median Age'],
    'Value': [mean_age, median_age]
})

stat_fig = px.bar(stat_df, x='Statistic', y='Value', color='Statistic', text_auto='.2f', color_discrete_sequence=['#AB63FA', '#FFA15A'])
stat_fig.update_layout(yaxis_title="Age")
st.plotly_chart(stat_fig, use_container_width=True)


# Plot 2: Salary Distribution
st.subheader("💰 Salary Distribution")
salary_fig = px.histogram(df, x='Salary', nbins=20, color_discrete_sequence=['#00CC96'])
salary_fig.update_layout(bargap=0.1)
st.plotly_chart(salary_fig, use_container_width=True)

# Plot 3: Average Salary by Gender
st.subheader("👨‍👩‍👧‍👦 Average Salary by Gender")
gender_salary = df.groupby("Gender")['Salary'].mean().reset_index()
gender_fig = px.bar(gender_salary, x='Gender', y='Salary', color='Gender', text_auto='.2s')
st.plotly_chart(gender_fig, use_container_width=True)

# Plot 4: Average Salary by Education Level
st.subheader("🎓 Average Salary by Education Level")
edu_salary = df.groupby("Education Level")['Salary'].mean().reset_index()
edu_fig = px.bar(edu_salary, x='Education Level', y='Salary', color='Education Level', text_auto='.2s')
st.plotly_chart(edu_fig, use_container_width=True)

# Plot 5: Average Salary by Experience Group
st.subheader("💼 Average Salary by Experience Group")
exp_salary = df.groupby("Experience Group")['Salary'].mean().reset_index().sort_values("Experience Group")
exp_fig = px.bar(exp_salary, x='Experience Group', y='Salary', color='Experience Group', text_auto='.2s')
st.plotly_chart(exp_fig, use_container_width=True)

# Plot 6: Correlation Heatmap
st.subheader("🔗 Correlation Heatmap")
numeric_df = df[['Age', 'Years of Experience', 'Salary']].copy()
corr = numeric_df.corr()
corr_fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu', title="Correlation Matrix")
st.plotly_chart(corr_fig, use_container_width=True)

# Plot 7: Salary vs Experience Scatter Plot
st.subheader("📈 Salary vs Years of Experience")
scatter_fig = px.scatter(
    df, x='Years of Experience', y='Salary', 
    color='Education Level', size='Age',
    hover_data=['Gender', 'Job Title']
)
st.plotly_chart(scatter_fig, use_container_width=True)

