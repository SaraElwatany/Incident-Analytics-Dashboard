# 🌍 Incidentlytics - Incident Analytics & Forecasting Dashboard


## Table of Contents

* [📌 Intro](#intro)
* [🔍 Project Overview](#-project-overview)

  * [🗺️ Home Page – Exploratory Data Analysis](#️-home-page--exploratory-data-analysis)
  * [📈 Insights Page – Analytical Trends](#-insights-page--analytical-trends)
  * [🤖 Forecasting Page – Predictive Modeling](#-forecasting-page--predictive-modeling)
* [📁 Project Structure](#-project-structure)
* [💡 Key Technologies](#-key-technologies)
* [🚀 How to Run the App](#-how-to-run-the-app)
* [🤝 Let's Collaborate](#-lets-collaborate)
* [👥 Collaborators](#-collaborators)




## Intro

Incidentlytics is an interactive web application built with Dash (Plotly) to visualize and analyze global accident data. The dashboard provides insights into accident trends, locations, and other critical statistics. It features maps, graphs, and filters for user-friendly exploration. Moreover, Classical Machine Learning models were incorporated for forecasting and assessment purposes.

![DashVideo-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/1095449a-7585-454a-ac47-48dd57ec7de0)



## 🔍 Project Overview

This dashboard is structured into multiple pages, each offering a different perspective:


### 🗺️ **Home Page – Exploratory Data Analysis**

* **Accident Density by Country**: An interactive choropleth map highlights global accident hotspots.
* **Top Cities with Most Accidents**: A bar chart showing cities with the highest incident counts.
* **Weather × Road Conditions**: A heatmap exploring the relationship between environmental conditions and accident rates.

💡 *Key Features*:

* Sidebar filters for date, country, and weather.
* Real-time updates to all visuals.
* Clean and responsive UI for intuitive navigation.



### 📈 **Insights Page – Analytical Trends**

* **Monthly Accident Trends**: Time series visualization highlights peak accident periods (e.g., July 2024, Sep 2023).
* **Leading Causes**: Human-related factors dominate accident causes.
* **Severity Analysis**: 66.6% of incidents are marked as severe.
* **Time of Day**: Most accidents occur in morning and night—weather/road conditions are secondary factors.

📌 *Conclusion*: Human error is the leading cause of accidents, with incident rates increasing in 2024.



### 🤖 **Forecasting Page – Predictive Modeling**

This section features three ML-driven models powered by **XGBoost Regressor**:

1. **Casualty Assessment Model**

   * Predicts deaths and injuries using user inputs and plots results against monthly averages for comparison.

2. **Global Casualty Forecasting**

   * Interactive slider forecasts global casualty trends.

3. **Global Accidents Forecasting**

   * Projects the number of accidents over time worldwide.

🛠 *Techniques Used*:

* **Time-Delayed Embedding** for forecasting features.
* **Feature Engineering** for temporal/contextual insights like time of day.

⚠️ *Observation*: Classical ML struggled with forecasting complex non-stationary data. Future improvements could include **SARIMA** or **Prophet** models for better time-series performance.




## 📁 Project Structure

```
├── app.py                # Main Dash app launcher
├── data.py               # Data loading and filtering functions
├── tools.py              # Utility functions for visualization and preprocessing
├── requirements.txt      # Python package dependencies
├── model_development/    # Notebooks and scripts for training ML models
├── models/               # Trained models and slider logic
├── dataset/              # Raw dataset files
├── pages/                # Modular Dash pages (EDA, Forecasting, etc.)
├── assets/               # CSS and static assets
├── .gitignore            # Files to ignore in version control
└── README.md             # Project overview and documentation
```




## 💡 Key Technologies

* **Dash & Plotly** – Interactive UI and visualization framework
* **Pandas, NumPy** – Data processing
* **XGBoost** – ML model for regression forecasting
* **Scikit-learn** – Preprocessing and evaluation
* **Matplotlib, Seaborn** – Additional plots
* **SARIMA, Prophet (future scope)** – Advanced time series models




## 🚀 How to Run the App

1. **Clone the repository**

   ```bash
   git clone https://github.com/SaraElwatany/Incident-Analytics-Dashboard.git
   cd Incident-Analytics-Dashboard
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**

   ```bash
   python app.py
   ```

Then visit `http://127.0.0.1:8050/` in your browser.




## 🤝 Let's Collaborate

This project was a great experience combining data science, visualization, and ML modeling. If you’re passionate about forecasting, urban safety, or real-world ML applications—feel free to connect!






## 👥 Collaborators

* **Amany Alsayed**
  🔗 [LinkedIn](https://www.linkedin.com/in/amany-alsayed82) | 💻 [GitHub](https://github.com/Amany-alsayed) | ✉️ [Email](mailto:amanyalsayed82@gmail.com)

* **Sara Elwatany**
  🔗 [LinkedIn](https://www.linkedin.com/in/sara-elwatany) | 💻 [GitHub](https://github.com/SaraElwatany) | ✉️ [Email](mailto:saraayman10000@gmail.com)

* **Zad Walid**
  🔗 [LinkedIn](https://www.linkedin.com/in/zadwalid) | 💻 [GitHub](https://github.com/Zad-Walid) | ✉️ [Email](mailto:zadwalid06@gmail.com)


