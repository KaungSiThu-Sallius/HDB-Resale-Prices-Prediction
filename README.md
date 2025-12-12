# HDB Resale Price Prediction and Analysis

This project predicts HDB resale prices in Singapore using machine learning, providing a powerful tool for both buyers and sellers to make informed financial decisions.

➡️ **[Live Demo of the Interactive Dashboard](https://hdb-resale-prices-prediction.onrender.com/)**

---

## 1. The Business Problem

For hundreds of thousands of Singaporeans, buying or selling an HDB flat is the most significant financial decision of their lives. The market is complex, and accurately valuing a flat is challenging, leading to uncertainty and potential financial loss.

- **Buyers** risk overpaying.
- **Sellers** risk undervaluing their property.

Our project tackled this problem by building a tool to replace guess-work with data-driven valuation insights, empowering users to make confident decisions.

---

## 2. My Technical Approach

To solve this, I developed an end-to-end data science pipeline:

- **Data Collection & Merging**: Gathered over 100,000 transaction records from [data.gov.sg](https://data.gov.sg), along with MRT station locations and historical price indices.
- **Geocoding**: Used the OneMap API to convert addresses into coordinates.
- **Feature Engineering**: Calculated the precise distance from each flat to the nearest MRT station.
- **Data Cleaning & Inflation Adjustment**: Standardized prices to reflect consistent value over time.
- **Model Training**: Evaluated several machine learning models.
- **Final Model**: Selected an **XGBoost Regressor** for its superior accuracy.
- **Deployment**: Built an interactive web application using **Plotly Dash**.

---

## 3. The Solution & Key Findings

The final product is a user-friendly web dashboard with two main tools:

### 🧭 Analysis Page
- Explore historical price trends.
- View price distributions by flat type.
- Interactive heat map of average prices across all towns in Singapore.

### 📈 Prediction Page
- Input specific flat details (e.g., town, floor area, remaining lease).
- Receive **instant price prediction** powered by machine learning.

### 📊 Model Performance
- **R² Score**: > 0.97 (explains 97%+ of price variance)
- **Average Error**: ±5.8%

**Key Findings**:
- Floor area and remaining lease are major value drivers.
- Proximity to MRT stations significantly impacts price.

---

## 4. Business Impact

This project transforms complex datasets into **accessible financial insights** for everyday Singaporeans:

### ✅ Empowering Buyers
Verify if a listing is fairly priced and gain confidence in negotiations.

### ✅ Maximizing Seller Returns
Set a competitive, data-driven price to avoid undervaluation.

### ✅ Democratizing Data
Put advanced market intelligence—once exclusive to property agents—into the hands of everyone. Understand how specific features (e.g., high floor, MRT proximity) affect a property's value.

---

## 5. Future Enhancements

*   **Real-time Data Integration:** Implement mechanisms to automatically update the datasets from `data.gov.sg` or other relevant APIs to keep the model and analyses current.
*   **Advanced Feature Engineering:**
    *   Incorporate more granular location-based features (e.g., proximity to schools, shopping malls, parks).
    *   Include macroeconomic indicators (e.g., interest rates, GDP growth, unemployment rates) that might affect the housing market.
    *   Consider recent transaction volumes or specific government policy announcements as features.
*   **Model Exploration:**
    *   Experiment with other advanced regression models (e.g., LightGBM, CatBoost) or neural network-based approaches.
    *   Explore more sophisticated ensemble techniques.
*   **Dashboard Enhancements:**
    *   Add more interactive filtering options to the Analysis page.
    *   Improve the UI/UX for better readability and user experience.
    *   Include feature importance plots from the model on the dashboard.

---

## Author

Kaung Si Thu
kaungsithu.sallius@gmail.com

---
