# 💰 Employee Salary Prediction using Machine Learning

## Overview

This project presents a Streamlit web application designed to predict employee salaries based on various attributes such as age, gender, education level, years of experience, and job title. Leveraging a Random Forest Regressor model, the application provides an intuitive interface for users to input employee details and receive an instant salary estimation. Additionally, it offers a feature to generate and download a printable PDF report of the prediction.

## Features

* **Interactive Input Fields**: Easily input employee details like Age, Gender, Education Level, Years of Experience, and Job Title using Streamlit widgets.
* **Real-time Salary Prediction**: Get an instant estimated salary based on the entered parameters.
* **PDF Report Generation**: Download a comprehensive PDF report summarizing the input parameters and the predicted salary.
* **Clear & Intuitive UI**: Built with Streamlit for a user-friendly and responsive experience.
* **Data Preprocessing**: Handles categorical features using Label Encoding (for `Gender`) and One-Hot Encoding (for `Education Level` and `Job Title`).
* **Robust Model**: Utilizes a pre-trained `RandomForestRegressor` for accurate salary estimations.
* **Reset Functionality**: A "Reset" button to clear all input fields for new predictions.

## Technologies and Libraries Used

* **Python**: The core programming language.
* **Streamlit**: For building the interactive web application.
* **Pandas**: For data manipulation and loading (`pd`).
* **NumPy**: For numerical operations (`np`).
* **Scikit-learn (sklearn)**: For machine learning functionalities:
    * `RandomForestRegressor` for the prediction model.
    * `LabelEncoder` for encoding categorical features like Gender.
    * `train_test_split` for splitting data (though the final app trains on full data, it's used in development).
* **Plotly Express (plotly.express)**: Used for generating interactive plots during the exploratory data analysis phase (notebook only).
* **ReportLab**: For generating proper PDF reports (`reportlab.lib.pagesizes`, `reportlab.platypus`, `reportlab.lib.styles`, `reportlab.lib.units`).
* **io**: For handling in-memory byte streams (`BytesIO`).

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

Ensure you have Python installed (version 3.8 or higher is recommended).

### Installation

1.  **Clone the repository (or download `app.py` and `Salary Data.csv`):**

    If you cloned the repo earlier, make sure you have the latest changes:
    ```bash
    git pull origin main # or master
    ```
    If you haven't cloned it yet:
    ```bash
    git clone [https://github.com/vigneshgit2005/Employee_Salary_Prediction_By_Machine_Learning.git](https://github.com/vigneshgit2005/Employee_Salary_Prediction_By_Machine_Learning.git)
    cd Employee_Salary_Prediction_By_Machine_Learning
    ```
    *(Note: Adjust the repository URL and directory name as per your actual GitHub repository.)*

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    * **On Windows (PowerShell):**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux (Bash/Zsh):**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required libraries:**

    ```bash
    pip install streamlit pandas numpy scikit-learn reportlab
    ```

### Running the Application

1.  **Ensure you are in the project directory** (where `app.py` and `Salary Data.csv` are located) with your virtual environment activated.
2.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

    This command will open the application in your default web browser.

## Project Structure

├── app.py                  # The main Streamlit application

├── Salary Data.csv         # The dataset used for training the model

└── README.md               # This README file

└── ML.ipynd                #Trainig and testing of the model

├── images/                 # Directory to store screenshots and other images (create this folder)

 ├── app_screenshot_1.png

 ├── app_screenshot_2.png

 └── # ... other screenshots

 ## How to Use

1.  **Launch the App**: Run `streamlit run app.py` from your terminal.
2.  **Enter Employee Name**: Type the name of the employee in the designated text box.
3.  **Select Parameters**: Choose the appropriate Gender, Education Level, and Job Title from the dropdowns. Adjust the sliders for Years of Experience and Age.
4.  **Predict Salary**: Click the "Predict Salary" button to see the estimated salary displayed.
    * **Screenshot Idea**: Take a screenshot of the app with input fields filled and the predicted salary displayed.
    ![Prediction in Action](./images/app_screenshot_1.png)
    *(Replace `./images/app_screenshot_1.png` with your actual image path)*
5.  **Reset Inputs**: Click the "Reset" button to clear all input fields and start a new prediction.
6.  **Download Report**: After a prediction is made, a "Download Report as PDF" button will appear, allowing you to save a summary of the prediction.
    * **Screenshot Idea**: Take a screenshot of the report summary section and the download button. You could also show a snippet of the generated PDF if possible.
    ![Report Summary and Download](./images/app_screenshot_2.png)
    *(Replace `./images/app_screenshot_2.png` with your actual image path)*

## Model Details

The core of the prediction logic is a `RandomForestRegressor`. This ensemble learning method operates by constructing a multitude of decision trees at training time and outputting the mean prediction of the individual trees.

* **Training Data**: The model is trained on `Salary Data.csv`.
* **Feature Engineering**:
    * `Age` and `Years of Experience` are used directly as numerical features.
    * `Gender` is converted into a numerical format (Male=1, Female=0) using `LabelEncoder`.
    * `Education Level` and `Job Title` are transformed using `One-Hot Encoding` to handle their categorical nature, ensuring the model can interpret them effectively.
* **Model Parameters**: The `RandomForestRegressor` is configured with `n_estimators=500` and `random_state=42` for consistent results and reproducibility.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find any issues, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT). (You can create a LICENSE file in your repository with the MIT license text if you don't have one).

---
*Created with ❤️ by Vignesh*
