# Thesis

## Overview
This project is designed to forecast stock prices using machine learning and time series analysis. Specifically, it focuses on predicting Apple (AAPL) stock prices, leveraging historical data and advanced modeling techniques. While the project is tailored for AAPL stock, the methodology and code can be applied to any stock with appropriate data. It integrates DVC for data versioning and dependency tracking, ensuring reproducibility and efficient collaboration.
---

## Table of Contents

1. [Setup and Installation](#setup-and-installation)
2. [Fetching Data](#fetching-data)
3. [Running the Application](#running-the-application)
4. [Project Structure](#project-structure)

---

## Setup and Installation

1. **Clone the Repository**  
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/ivanmanhique/thesis-code.git
   cd thesis-code

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install DVC**
   ```bash
   pip install dvc
   ```
## Fetching Data
To fetch the required data files tracked by DVC (e.g., model.h5 and scaler.pkl):

1. **Pull the Data**
Ensure DVC is set up correctly, then pull all tracked files:
  ```bash
  dvc pull
  ```

## Running the Application
1. Run the fastapi command
```bash
fastapi run
```
## Project Structure

├── .dvc
│   ├── .gitignore
│   ├── config
│   └── tmp
│       ├── btime
│       ├── lock
│       ├── rwlock
│       └── rwlock.lock
├── .dvcignore
├── .gitignore
├── app
│   ├── .DS_Store
│   ├── __init__.py
│   ├── main.py
│   └── predictor
│       ├── __init__.py
│       └── model.py
├── data
│   ├── .gitignore
│   ├── model.h5
│   ├── model.h5.dvc
│   ├── scaler.pkl
│   └── scaler.pkl.dvc
├── notebook
│   └── thesis.ipynb
└── requirements.txt

### Notes
- Make sure to have the appropriate permissions to access the DVC remote storage.
- For any issues, feel free to open a new [issue](https://github.com/ivanmanhique/thesis-code/issues/new)
