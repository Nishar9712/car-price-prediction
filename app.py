import os
import json
import joblib
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Styling
st.markdown("""
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E293B;
            text-align: center;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #64748B;
            text-align: center;
            margin-bottom: 1.8rem;
        }
        .prediction-card {
            background: linear-gradient(135deg, #1E3A8A, #2563EB);
            color: white;
            padding: 24px;
            border-radius: 14px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.25);
            margin: 20px 0;
        }
        .prediction-label {
            font-size: 1.1rem;
            font-weight: 500;
            opacity: 0.9;
        }
        .prediction-value {
            font-size: 2.8rem;
            font-weight: 800;
            color: #F8FAFC;
            margin: 5px 0;
        }
        .prediction-range {
            font-size: 1.05rem;
            color: #DBEAFE;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Load Resources (Model & Metadata)
# ---------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "best_model.pkl")
METADATA_PATH = os.path.join(CURRENT_DIR, "model_metadata.json")

@st.cache_data
def load_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r") as f:
            return json.load(f)
    return None

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

metadata = load_metadata()
model = load_model()

# Fallback values if metadata file is not found
default_manufacturers = ["TOYOTA", "HYUNDAI", "MERCEDES-BENZ", "FORD", "CHEVROLET", "BMW", "HONDA", "LEXUS", "NISSAN", "VOLKSWAGEN", "Other"]
default_categories = ["Sedan", "Jeep", "Hatchback", "Minivan", "Coupe", "Universal", "Microbus", "Goods wagon", "Pickup", "Cabriolet", "Limousine"]
default_fuel_types = ["Petrol", "Diesel", "Hybrid", "LPG", "CNG", "Plug-in Hybrid"]
default_gear_boxes = ["Automatic", "Tiptronic", "Manual", "Variator"]
default_drive_wheels = ["Front", "4x4", "Rear"]
default_doors = ["4-5", "2-3", ">5"]
default_colors = ["Black", "White", "Silver", "Grey", "Blue", "Red", "Green", "Other"]

manufacturers = metadata.get("manufacturers", default_manufacturers) if metadata else default_manufacturers
categories = metadata.get("categories", default_categories) if metadata else default_categories
fuel_types = metadata.get("fuel_types", default_fuel_types) if metadata else default_fuel_types
gear_box_types = metadata.get("gear_box_types", default_gear_boxes) if metadata else default_gear_boxes
drive_wheels = metadata.get("drive_wheels", default_drive_wheels) if metadata else default_drive_wheels
doors_list = metadata.get("doors", default_doors) if metadata else default_doors
colors = metadata.get("colors", default_colors) if metadata else default_colors

# ---------------------------------------------------------
# Main Page: Car Price Predictor
# ---------------------------------------------------------
st.markdown('<div class="main-header">🚗 Used Car Price Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Select vehicle details below to estimate its fair market valuation.</div>', unsafe_allow_html=True)

if model is None:
    st.error("Model file `best_model.pkl` not found. Please run `train_models.py` first to generate the model.")
else:
    with st.form("price_prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🚘 Vehicle Info")
            manufacturer = st.selectbox(
                "Manufacturer / Brand",
                manufacturers,
                index=manufacturers.index("TOYOTA") if "TOYOTA" in manufacturers else 0
            )
            category = st.selectbox(
                "Body Category",
                categories,
                index=categories.index("Sedan") if "Sedan" in categories else 0
            )
            prod_year = st.slider("Production Year", min_value=1990, max_value=2020, value=2015, step=1)
            mileage_km = st.number_input("Mileage (in Kilometers)", min_value=0, max_value=600000, value=85000, step=5000)
            engine_volume = st.slider("Engine Volume (Liters)", min_value=0.8, max_value=6.5, value=2.0, step=0.1)
            is_turbo = st.checkbox("Turbocharged Engine (Turbo)", value=False)
            levy = st.number_input("Levy / Tax ($)", min_value=0, max_value=5000, value=781, step=50, help="Georgia auto market import levy (median: $781).")

        with col2:
            st.markdown("### ⚙️ Mechanics & Features")
            fuel_type = st.selectbox(
                "Fuel Type",
                fuel_types,
                index=fuel_types.index("Petrol") if "Petrol" in fuel_types else 0
            )
            gear_box = st.selectbox(
                "Gear Box Type",
                gear_box_types,
                index=gear_box_types.index("Automatic") if "Automatic" in gear_box_types else 0
            )
            drive_wheel = st.selectbox(
                "Drive Wheels",
                drive_wheels,
                index=drive_wheels.index("Front") if "Front" in drive_wheels else 0
            )
            doors = st.selectbox(
                "Doors",
                doors_list,
                index=doors_list.index("4-5") if "4-5" in doors_list else 0
            )
            wheel = st.selectbox("Steering Wheel", ["Left wheel", "Right-hand drive"], index=0)
            color = st.selectbox(
                "Color",
                colors,
                index=colors.index("Black") if "Black" in colors else 0
            )
            airbags = st.slider("Airbags", min_value=0, max_value=16, value=4, step=1)
            leather = st.radio("Leather Interior", ["Yes", "No"], index=0, horizontal=True)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("💰 Calculate Fair Price", use_container_width=True)

    # ---------------------------------------------------------
    # Inference & Output Display
    # ---------------------------------------------------------
    if submitted:
        car_age = max(0, 2020 - prod_year)
        mfg_val = manufacturer if manufacturer in manufacturers[:-1] else "Other"

        input_data = pd.DataFrame([{
            "Levy": float(levy),
            "Prod_Year": float(prod_year),
            "Car_Age": int(car_age),
            "Engine_Volume": float(engine_volume),
            "Mileage_km": float(mileage_km),
            "Cylinders": 4.0 if engine_volume <= 2.5 else (6.0 if engine_volume <= 4.0 else 8.0),
            "Airbags": float(airbags),
            "Turbo": 1 if is_turbo else 0,
            "Manufacturer_Grouped": mfg_val,
            "Category": category,
            "Leather_Interior": leather,
            "Fuel_Type": fuel_type,
            "Gear_Box_Type": gear_box,
            "Drive_Wheels": drive_wheel,
            "Doors": doors,
            "Wheel": wheel,
            "Color": color
        }])

        try:
            raw_pred = model.predict(input_data)[0]
            pred_price = max(500, raw_pred)

            # Expected error margin from Gradient Boosting MAE
            mae_margin = 6600
            if metadata and "best_model" in metadata:
                mae_margin = metadata["best_model"].get("mae", 6600)

            low_price = max(500, pred_price - (mae_margin * 0.75))
            high_price = pred_price + (mae_margin * 0.75)

            st.markdown(
                f"""
                <div class="prediction-card">
                    <div class="prediction-label">Estimated Fair Market Value</div>
                    <div class="prediction-value">${pred_price:,.0f} USD</div>
                    <div class="prediction-range">Expected Valuation Range: ${low_price:,.0f} &ndash; ${high_price:,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            res_c1, res_c2, res_c3 = st.columns(3)
            res_c1.metric("Vehicle Age", f"{car_age} years")
            res_c2.metric("Mileage", f"{mileage_km:,.0f} km")
            res_c3.metric("Class", f"{manufacturer} {category}")

        except Exception as e:
            st.error(f"Error calculating price: {e}")
