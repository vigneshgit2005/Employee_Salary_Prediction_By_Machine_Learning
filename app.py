import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Page Configuration
st.set_page_config(
    page_title="Employee Salary Prediction App",
    page_icon="💰",
    layout="centered"
)

# Header Styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #FF6692 0%, #ab63fa 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
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

# Preprocessing and Model Training
@st.cache_resource
def train_model(df):
    clean_df = df.copy()

    # Label Encode Gender
    le = LabelEncoder()
    clean_df['Gender'] = le.fit_transform(clean_df['Gender'])  # Male=1, Female=0

    # One-hot encode Education Level and Job Title
    clean_df = pd.get_dummies(clean_df, columns=['Education Level', 'Job Title'], drop_first=True)

    # Define features (X) and target (y)
    X = clean_df.drop('Salary', axis=1)
    y = clean_df['Salary']

    # Train a RandomForestRegressor model
    model = RandomForestRegressor(n_estimators=500, random_state=42)
    model.fit(X, y)
    return model, X.columns, le

# Function to create a PDF using ReportLab
def create_pdf_report(employee_name, details, predicted_salary):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Employee Salary Prediction Report", styles['h1']))
    story.append(Spacer(1, 0.2 * inch))

    # Employee Name
    story.append(Paragraph(f"<b>Employee Name:</b> {employee_name}", styles['Normal']))
    story.append(Spacer(1, 0.1 * inch))

    # Predicted Salary
    story.append(Paragraph(f"<b>Predicted Salary:</b> ${predicted_salary:,.2f}", styles['Normal']))
    story.append(Spacer(1, 0.2 * inch))

    # Input Parameters
    story.append(Paragraph("<b>Input Parameters:</b>", styles['h3']))
    for key, value in details.items():
        story.append(Paragraph(f"- <b>{key}:</b> {value}", styles['Normal']))
        story.append(Spacer(1, 0.05 * inch))
    
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("<i>Report generated by Employee Salary Prediction App.</i>", styles['Italic']))

    doc.build(story)
    buffer.seek(0)
    return buffer

# Initialize session state for input fields
if 'employee_name' not in st.session_state:
    st.session_state.employee_name = "Enter your Name" # Changed default placeholder text
if 'gender' not in st.session_state:
    st.session_state.gender = None # Will be set by selectbox options later
if 'education_level' not in st.session_state:
    st.session_state.education_level = None # Will be set by selectbox options later
if 'job_title' not in st.session_state:
    st.session_state.job_title = None # Will be set by selectbox options later
if 'years_experience' not in st.session_state:
    st.session_state.years_experience = 5
if 'age' not in st.session_state:
    st.session_state.age = 30
if 'predicted_salary_display' not in st.session_state:
    st.session_state.predicted_salary_display = "---"
if 'show_report' not in st.session_state:
    st.session_state.show_report = False

# Function to reset inputs
def reset_inputs():
    st.session_state.employee_name = "Enter your Name" # Reset to new placeholder
    # Reset selectboxes to their first option or a default if possible
    # This assumes the first option in the unique list is a good default
    st.session_state.gender = df['Gender'].unique()[0] if df is not None else None
    st.session_state.education_level = df['Education Level'].unique()[0] if df is not None else None
    st.session_state.job_title = df['Job Title'].unique()[0] if df is not None else None
    st.session_state.years_experience = 5
    st.session_state.age = 30
    st.session_state.predicted_salary_display = "---"
    st.session_state.show_report = False


# App Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white;">💰 Employee Salary Prediction</h1>
    <p style="color: white;">Predict employee salary based on key parameters</p>
</div>
""", unsafe_allow_html=True)

# Load data and train model
df = load_data()
model, feature_columns, gender_encoder = train_model(df)

# Ensure session state defaults are set based on loaded data
if st.session_state.gender is None and df is not None:
    st.session_state.gender = df['Gender'].unique()[0]
if st.session_state.education_level is None and df is not None:
    st.session_state.education_level = df['Education Level'].unique()[0]
if st.session_state.job_title is None and df is not None:
    st.session_state.job_title = df['Job Title'].unique()[0]


# User Input Section
st.subheader("📝 Enter Employee Details")

st.text_input("Employee Name", key="employee_name")

col1, col2 = st.columns(2)

with col1:
    st.selectbox("Gender", df['Gender'].unique(), key="gender")
    st.selectbox("Education Level", df['Education Level'].unique(), key="education_level")

with col2:
    st.slider("Years of Experience", 0, 40, key="years_experience")
    st.slider("Age", 20, 65, key="age")

st.selectbox("Job Title", df['Job Title'].unique(), key="job_title")

# Prediction and Reset Buttons
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    predict_button = st.button("Predict Salary")
with col_btn2:
    reset_button = st.button("Reset", on_click=reset_inputs)

# Prediction Logic
st.subheader("🔮 Predicted Salary")

# Display predicted salary based on session state
st.markdown(f"## Estimated Salary: **{st.session_state.predicted_salary_display}**")

if predict_button:
    # Update session state with current inputs
    # These are already handled by `key` arguments in input widgets, so direct access is fine
    # e.g., st.session_state.employee_name will hold the value from the text_input

    # Create a dictionary for the new input to store for print session
    input_details = {
        'Age': st.session_state.age,
        'Gender': st.session_state.gender,
        'Education Level': st.session_state.education_level,
        'Job Title': st.session_state.job_title,
        'Years of Experience': st.session_state.years_experience,
    }

    # Create a DataFrame for model prediction
    input_df_for_prediction = pd.DataFrame([list(input_details.values()) + [0]], # Add a dummy salary column
                                           columns=list(input_details.keys()) + ['Salary'])

    # Encode the input data similar to training data
    input_df_for_prediction['Gender'] = gender_encoder.transform(input_df_for_prediction['Gender'])
    input_df_for_prediction = pd.get_dummies(input_df_for_prediction, columns=['Education Level', 'Job Title'], drop_first=True)

    # Align columns - crucial for prediction
    missing_cols = set(feature_columns) - set(input_df_for_prediction.columns)
    for c in missing_cols:
        input_df_for_prediction[c] = 0
    input_df_for_prediction = input_df_for_prediction[feature_columns]

    predicted_salary = model.predict(input_df_for_prediction)[0]
    st.session_state.predicted_salary_display = f"${predicted_salary:,.2f}"
    st.session_state.show_report = True
    st.rerun() # Rerun to update the displayed salary and show report

if st.session_state.show_report:
    predicted_salary_value = float(st.session_state.predicted_salary_display.replace('$', '').replace(',', ''))
    input_details = {
        'Age': st.session_state.age,
        'Gender': st.session_state.gender,
        'Education Level': st.session_state.education_level,
        'Job Title': st.session_state.job_title,
        'Years of Experience': st.session_state.years_experience,
    }

    # Print Session / Summary for PDF
    st.markdown("---")
    st.subheader(f"📄 Salary Prediction Report for {st.session_state.employee_name}")
    st.write(f"**Employee Name:** {st.session_state.employee_name}")
    st.write(f"**Predicted Salary:** {st.session_state.predicted_salary_display}")
    st.markdown("### Input Parameters:")
    for key, value in input_details.items():
        st.write(f"- **{key}:** {value}")

    # Generate PDF button
    pdf_buffer = create_pdf_report(st.session_state.employee_name, input_details, predicted_salary_value)
    st.download_button(
        label="Download Report as PDF",
        data=pdf_buffer,
        file_name=f"Salary_Report_{st.session_state.employee_name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

st.caption("This app uses a RandomForestRegressor model for salary prediction.")