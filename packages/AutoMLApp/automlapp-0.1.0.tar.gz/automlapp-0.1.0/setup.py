from setuptools import setup, find_packages

setup(
    name="AutoMLApp",
    version="0.1.0",
    author="Shivam Nikam",
    author_email="shivam.nikam@think360.ai",
    description="An automated machine learning application designed for efficient model training, evaluation, and hyperparameter tuning.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/YourGithub/AutoMLApp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        'pandas==2.2.1',
        'numpy==1.26.4',
        'imbalanced-learn==0.12.0',
        'streamlit==1.32.0',
        'streamlit-extras==0.4.0',
        'streamlit-modal==0.1.2',
        'plotly==5.18.0',
        'scikit-learn==1.4.1.post1',
        'lightgbm==4.3.0',
        'xgboost==2.0.3',
        'openpyxl==3.0.10',
        'scorecardpy==0.1.9.7'  # Added to match your requirements.txt
    ],
    extras_require={
        "dev": [
            "pytest>=5.2",
            "check-manifest",
            "twine",
        ],
    },
    package_data={
        "sample": ["package_data.dat"],
    },
    entry_points={
        "console_scripts": [
            "automlapp=automlapp.cli:main",
        ],
    },
)
