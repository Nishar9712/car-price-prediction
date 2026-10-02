
# 🚗 Car Price Prediction, EDA & Streamlit Web App

A complete end-to-end Machine Learning and Exploratory Data Analysis (EDA) project for used car price valuation, featuring comprehensive data cleaning, comparative benchmarking of 5 regression algorithms, and an intuitive Streamlit dashboard.

---

## 📁 Project Structure

All project files are located directly in this folder:

```text
Miniproject/
│
├── car_price.csv              # Original raw dataset
├── car_price_cleaned.csv      # Cleaned and processed dataset
│
├── eda_and_cleaning.py        # Data cleaning & EDA generation script
├── eda_and_cleaning.ipynb     # Jupyter Notebook: Data Cleaning & EDA
├── train_models.py            # Model training & benchmarking script
├── train_models.ipynb         # Jupyter Notebook: ML Model Benchmarking
├── app.py                     # Streamlit web application
│
├── best_model.pkl             # Trained pipeline of the best model (Gradient Boosting)
├── model_metadata.json        # Model details and feature options
├── model_comparison.csv       # Comparison metrics table of all 5 algorithms
├── model_comparison.png       # Comparison bar chart (R² & MAE)
│
├── eda_plots/                 # Generated EDA charts
│   ├── price_distribution.png
│   ├── top_manufacturers.png
│   ├── category_median_price.png
│   ├── price_vs_age.png
│   ├── correlation_heatmap.png
│   └── fuel_type_analysis.png
│
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation & guide
```

---

## 🧹 1. Data Cleaning Workflow

The raw dataset (`car_price.csv`) had numerous real-world anomalies, formatting issues, and missing values. The cleaning pipeline (`eda_and_cleaning.py`) resolved:

1. **Non-predictive Identifier:** Dropped the arbitrary `ID` column.
2. **Duplicate Records:** Detected and removed 55 redundant entries.
3. **Target Variable (`Price`) Cleaning:**
   - Dropped 563 rows missing the target variable `Price`.
   - Filtered out extreme price anomalies: values below **$500** (dummy/scrap/symbolic $1 listings) and above **$150,000** (extreme luxury/unrealistic entries such as $26M).
4. **Mileage Standardization:**
   - Stripped the `' km'` string suffix and converted to numeric float.
   - Filtered out corrupt/dummy records exceeding **600,000 km** (e.g., maximum 32-bit integer $2.14 \times 10^9$ km entries).
5. **Engine Volume & Turbo Extraction:**
   - Extracted numeric engine displacement in Liters (`Engine_Volume`).
   - Created a binary feature `Turbo` (1 if "Turbo" appeared in the string, 0 otherwise).
6. **Doors Format Standardization:**
   - Fixed Excel auto-date conversion issues: `'04-May'` $\rightarrow$ `'4-5'`, `'02-Mar'` $\rightarrow$ `'2-3'`, `'>5'` $\rightarrow$ `'>5'`.
7. **Missing Value Imputation:**
   - **Numerical Features** (`Levy`, `Prod. year`, `Mileage_km`, `Engine_Volume`, `Cylinders`, `Airbags`): Imputed with column median to prevent distortion from skewness.
   - **Categorical Features** (`Manufacturer`, `Model`, `Category`, `Fuel type`, `Gear box type`, `Drive wheels`, `Doors`, `Wheel`, `Color`): Imputed with the column mode.
8. **Feature Engineering:**
   - `Car_Age`: Computed as $\text{Reference Year} - \text{Prod\_Year}$ to reflect vehicle depreciation directly.
   - Standardized column names into snake/camel case for consistent downstream processing.
9. **Export:** Cleaned dataset saved to `car_price_cleaned.csv` (16,872 valid records).

---

## 📊 2. Exploratory Data Analysis (EDA) Highlights

Generated high-resolution visualization charts are saved in `eda_plots/`:

- **Price Distribution (`price_distribution.png`):** Shows right-skewed car pricing with median price at \$13,172.
- **Top Manufacturers (`top_manufacturers.png`):** Hyundai, Toyota, Mercedes-Benz, Ford, and Chevrolet lead the market share.
- **Median Price by Category (`category_median_price.png`):** Jeeps, Coupes, and Sedans command high market valuations, while Goods Wagons and Hatchbacks remain budget-oriented.
- **Depreciation Curve (`price_vs_age.png`):** Captures the steep initial depreciation over the first 5–8 years before flattening out for mature vehicles.
- **Correlation Heatmap (`correlation_heatmap.png`):** Demonstrates strong negative correlation between car price and vehicle age/mileage, and positive correlation with engine volume and airbags.
- **Fuel Type Analysis (`fuel_type_analysis.png`):** Petrol and Diesel dominate market share, while Plug-in Hybrids and Hybrids exhibit higher average resale prices.

---

## 🤖 3. Machine Learning Models & Evaluation

We trained and benchmarked **5 regression algorithms** on an 80% train / 20% test split:

| Model | $R^2$ Score (Higher is Better) | MAE (\$) (Lower is Better) | RMSE (\$) (Lower is Better) | MAPE (%) |
| :--- | :---: | :---: | :---: | :---: |
| 🥇 **Gradient Boosting Regressor** | **0.5880** | **\$6,685.44** | **\$10,783.98** | **147.49%** |
| 🥈 **Random Forest Regressor** | 0.5674 | \$6,654.61 | \$11,050.05 | 148.67% |
| 🥉 **Decision Tree Regressor** | 0.3907 | \$7,903.82 | \$13,113.43 | 154.92% |
| 4️⃣ **Linear Regression** | 0.2958 | \$9,615.34 | \$14,097.88 | 228.61% |
| 5️⃣ **Ridge Regression** | 0.2956 | \$9,608.78 | \$14,100.07 | 228.97% |

### Key Observations:
- **Gradient Boosting** achieved the highest overall predictive power ($R^2 = 0.5880$) and lowest RMSE.
- **Random Forest** had the closest competing accuracy with the lowest Mean Absolute Error (\$6,654).
- The best performing model was serialized and saved to `best_model.pkl`.

---

## 🌐 4. Streamlit Web Application

The Streamlit web application (`app.py`) is streamlined specifically for **Car Price Prediction**:
- **Vehicle Input Form:** Select car manufacturer, body category, production year, mileage, engine displacement, turbo option, fuel type, transmission, drive wheels, doors, airbags, and leather interior.
- **Instant Valuation:** Computes the fair market price in real-time with an estimated valuation confidence range.
- **Vehicle Summary Cards:** Displays key specs (calculated vehicle age, mileage, and vehicle class).

---

## 🚀 5. How to Run

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Data Cleaning & EDA
```bash
python eda_and_cleaning.py
```

### Run Model Training & Evaluation
```bash
python train_models.py
```

### Launch the Streamlit Web Application
```bash
streamlit run app.py
```
After running this command, open your browser at `http://localhost:8501`.
