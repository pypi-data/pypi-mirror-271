## Introduction

**Overview**

The AutoML Web App revolutionizes the credit underwriting process by automating critical steps, including data preprocessing, model fitting, and hyperparameter tuning, to ensure accurate risk assessments. Designed to streamline the workflow, it significantly enhances efficiency and precision in lending risk management for both individuals and businesses.

**Features**

- **Streamlined Credit Underwriting**: Traditionally, credit underwriting is a meticulous process essential for evaluating lending risks. This app simplifies these complexities, transforming how risk assessments are conducted.
- **Overcoming Manual Constraints**: The manual fitting of models for credit underwriting is both time-consuming and prone to human error, potentially leading to suboptimal algorithm selection and overlooked risks. Our app addresses these challenges by automating model selection.
- **Efficient Model Selection**: The AutoML Web App stands out by enabling the efficient selection of machine learning models tailored to specific tasks. It sifts through a targeted set of algorithms to find the best fit, balancing automation with user control to achieve optimal outcomes.
- **No-Code Solution**: With the goal of democratizing technology, the app eliminates the need for intricate coding. It offers a user-friendly interface where complex underwriting tasks can be executed with just a few clicks, making sophisticated data analysis accessible to all.
- **Precision and Efficiency**: By offering a carefully curated selection of options at each stage of the underwriting process, the app ensures that both efficiency and precision are not just promised but delivered. This meticulous approach guarantees that every dataset is handled with the optimal blend of speed and accuracy.

## Getting Started

Welcome to the AutoML Web App for credit underwriting. This section will guide you through the initial steps needed to get the app up and running on your system.

### Prerequisites:

Before proceeding with the installation of the AutoML Web App, ensure your system meets the following requirements:

- **Python 3.10**: The application is developed in Python, requiring Python 3.10 to function correctly. Python 3.10 can be downloaded from [the official Python website](https://www.python.org/downloads/).
- **PIP**: PIP, the Python package installer, must be available on your system to install the Python packages the app depends on.
- **Internet Connection**: An active internet connection is necessary during the installation process for downloading required Python packages.

A basic understanding of Python and the use of virtual environments for managing package dependencies is also recommended.

### Installation:

To install the AutoML Web App, follow these steps:

1. **Clone the Repository**: Begin by cloning the AutoML Web App repository to your local machine with Git:
   ```bash
   git clone https://github.com/Adityaa2805/AutoMLApp.git
   cd AutoMLApp
   ```

2. **Create a Virtual Environment** (Optional but Recommended): To prevent potential conflicts with existing Python packages on your system, it is advisable to create a virtual environment within the cloned directory:
   ```bash
   python3 -m venv venv
   # Activate the virtual environment
   # On Windows
   venv\Scripts\activate
   # On macOS and Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**: Install all necessary Python packages using the provided `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the App**: After installing the dependencies, you can launch the AutoML Web App by executing:
   ```bash
   streamlit run app.py
   ```

   This command initiates the app and should automatically open it in your default web browser. If the app does not open automatically, a URL will be displayed in your terminal, which you can use to access the app manually.


