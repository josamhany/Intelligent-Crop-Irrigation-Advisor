import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os
import sys
import requests
from dotenv import load_dotenv
from supabase import create_client
import plotly.express as px
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import json
import tensorflow as tf
from PIL import Image


# Set page configuration
st.set_page_config(
    page_title="AgriTech",
    page_icon="🌱",
    layout="wide"
)


# Load environment variables from .env (local) and support Streamlit Cloud secrets
# First try default .env in current working directory
load_dotenv()
# Establish repository root (robustly) and ensure it's on sys.path so
# pickled models that reference top-level package imports (e.g. `models`)
# can be imported during unpickling.
try:
    current_file = os.path.abspath(__file__)
    # repo root is three levels up from frontend/streamlit_dashboard/app.py
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
except Exception:
    repo_root = os.path.abspath(os.curdir)

if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Also try loading .env from the project root (one level above models/frontend folders)
try:
    env_path = os.path.join(repo_root, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path, override=False)
except Exception:
    pass

st.title("🌾 AgriTech")
st.markdown("### Get intelligent crop recommendations and irrigation decisions based on soil and environmental conditions")

# --- IoT Live Data Section ---
with st.expander("Live Sensor Data (IoT)", expanded=False):
    st.markdown("Click 'Refresh Data' to fetch latest readings from Supabase or use demo data")
    
    # Supabase credentials (from .env or Streamlit secrets)
    SUPABASE_URL = os.getenv("SUPABASE_URL") or (st.secrets.get("SUPABASE_URL") if hasattr(st, "secrets") else None)
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or (st.secrets.get("SUPABASE_SERVICE_KEY") if hasattr(st, "secrets") else None)
    
    # Button row
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        refresh_btn = st.button("🔄 Refresh Data", disabled=(not SUPABASE_URL or not SUPABASE_KEY))
    with btn_col2:
        demo_btn = st.button("🎲 Load Demo Data")
    
    # Demo data function
    def generate_demo_data():
        """Generate demo sensor data for testing"""
        import numpy as np
        from datetime import datetime, timedelta
        
        # Generate 50 time points over last 24 hours
        now = datetime.now()
        times = [now - timedelta(hours=24-i*0.5) for i in range(50)]
        
        # Generate realistic sensor data with some variation
        np.random.seed(42)
        data = {
            'created_at': times,
            'temperature': 26.97 + np.random.normal(0, 2, 50),
            'humidity': 62.02 + np.random.normal(0, 5, 50),
            'soil_moisture': 35 + np.random.normal(0, 8, 50),
            'water_level': 50 + np.random.normal(0, 10, 50),
            'wind_speed': 8 + np.random.normal(0, 3, 50),
            'rainfall': np.random.exponential(2, 50)
        }
        return pd.DataFrame(data)
    
    if SUPABASE_URL and SUPABASE_KEY:
        if refresh_btn:
            with st.spinner("Fetching sensor data..."):
                try:
                    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                    response = supabase.table("Sensor readings").select("*").order("created_at", desc=True).limit(100).execute()
                    data = response.data
                    if data:
                        df = pd.DataFrame(data)
                        df_sorted = df.sort_values("created_at")
                        
                        # Quick Stats Section
                        st.subheader("📊 Latest Sensor Readings")
                        cols = st.columns(4)
                        
                        if "temperature" in df.columns:
                            with cols[0]:
                                latest_temp = df.iloc[0].get("temperature", "N/A")
                                avg_temp = df["temperature"].mean()
                                st.metric("🌡️ Temperature", f"{latest_temp:.1f}°C" if isinstance(latest_temp, (int, float)) else latest_temp, 
                                         delta=f"Avg: {avg_temp:.1f}°C")
                        
                        if "humidity" in df.columns:
                            with cols[1]:
                                latest_hum = df.iloc[0].get("humidity", "N/A")
                                avg_hum = df["humidity"].mean()
                                st.metric("💧 Humidity", f"{latest_hum:.1f}%" if isinstance(latest_hum, (int, float)) else latest_hum,
                                         delta=f"Avg: {avg_hum:.1f}%")
                        
                        if "soil_moisture" in df.columns:
                            with cols[2]:
                                latest_sm = df.iloc[0].get("soil_moisture", "N/A")
                                avg_sm = df["soil_moisture"].mean()
                                st.metric("🌱 Soil Moisture", f"{latest_sm:.1f}%" if isinstance(latest_sm, (int, float)) else latest_sm,
                                         delta=f"Avg: {avg_sm:.1f}%")
                        
                        if "water_level" in df.columns:
                            with cols[3]:
                                latest_wl = df.iloc[0].get("water_level", "N/A")
                                avg_wl = df["water_level"].mean()
                                st.metric("💦 Water Level", f"{latest_wl:.1f}" if isinstance(latest_wl, (int, float)) else latest_wl,
                                         delta=f"Avg: {avg_wl:.1f}")
                        
                        st.divider()
                        
                        # Visualizations
                        st.subheader("📈 Sensor Data Visualization")
                        
                        # Temperature and Humidity Chart (2 separate lines with different colors)
                        if "temperature" in df.columns and "humidity" in df.columns:
                            fig1 = px.line(df_sorted, x="created_at", y="temperature", 
                                          title="🌡️ Temperature Over Time",
                                          labels={"created_at": "Time", "temperature": "Temperature (°C)"},
                                          markers=True)
                            fig1.update_traces(line_color='#FF6B6B', marker=dict(size=6))
                            fig1.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig1, use_container_width=True)
                            
                            fig2 = px.line(df_sorted, x="created_at", y="humidity",
                                          title="💧 Humidity Over Time",
                                          labels={"created_at": "Time", "humidity": "Humidity (%)"},
                                          markers=True)
                            fig2.update_traces(line_color='#4ECDC4', marker=dict(size=6))
                            fig2.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig2, use_container_width=True)
                        
                        # Soil Moisture and Water Level Chart
                        if "soil_moisture" in df.columns:
                            fig3 = px.line(df_sorted, x="created_at", y="soil_moisture",
                                          title="🌱 Soil Moisture Over Time",
                                          labels={"created_at": "Time", "soil_moisture": "Soil Moisture (%)"},
                                          markers=True)
                            fig3.update_traces(line_color='#95E1D3', marker=dict(size=6))
                            fig3.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig3, use_container_width=True)
                        
                        if "water_level" in df.columns:
                            fig4 = px.line(df_sorted, x="created_at", y="water_level",
                                          title="💦 Water Level Over Time",
                                          labels={"created_at": "Time", "water_level": "Water Level"},
                                          markers=True)
                            fig4.update_traces(line_color='#3742FA', marker=dict(size=6))
                            fig4.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig4, use_container_width=True)
                        
                        # Additional sensors if available
                        if "wind_speed" in df.columns:
                            fig5 = px.line(df_sorted, x="created_at", y="wind_speed",
                                          title="🌬️ Wind Speed Over Time",
                                          labels={"created_at": "Time", "wind_speed": "Wind Speed (km/h)"},
                                          markers=True)
                            fig5.update_traces(line_color='#FFA502', marker=dict(size=6))
                            fig5.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig5, use_container_width=True)
                        
                        if "rainfall" in df.columns:
                            fig6 = px.bar(df_sorted, x="created_at", y="rainfall",
                                         title="🌧️ Rainfall Over Time",
                                         labels={"created_at": "Time", "rainfall": "Rainfall (mm)"})
                            fig6.update_traces(marker_color='#5F27CD')
                            fig6.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig6, use_container_width=True)
                        
                        # Data Table (collapsible)
                        with st.expander("📋 View Raw Data Table"):
                            st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No sensor data found in Supabase.")
                except Exception as e:
                    st.error(f"Error fetching data from Supabase: {e}")
                    st.info("💡 Try using Demo Data instead")
        elif not refresh_btn and not demo_btn:
            st.info("👆 Click 'Refresh Data' to load IoT sensor readings from Supabase")
    else:
        st.warning("⚠️ Supabase credentials not found. Use Demo Data button instead.")
    
    # Handle demo data button (works regardless of Supabase credentials)
    if demo_btn:
        with st.spinner("Generating demo data..."):
            try:
                df = generate_demo_data()
                df_sorted = df.sort_values("created_at")
                
                st.success("✅ Demo data loaded successfully!")
                
                # Quick Stats Section
                st.subheader("📊 Latest Sensor Readings (Demo)")
                cols = st.columns(4)
                
                with cols[0]:
                    latest_temp = df.iloc[-1]["temperature"]
                    avg_temp = df["temperature"].mean()
                    st.metric("🌡️ Temperature", f"{latest_temp:.1f}°C", delta=f"Avg: {avg_temp:.1f}°C")
                
                with cols[1]:
                    latest_hum = df.iloc[-1]["humidity"]
                    avg_hum = df["humidity"].mean()
                    st.metric("💧 Humidity", f"{latest_hum:.1f}%", delta=f"Avg: {avg_hum:.1f}%")
                
                with cols[2]:
                    latest_sm = df.iloc[-1]["soil_moisture"]
                    avg_sm = df["soil_moisture"].mean()
                    st.metric("🌱 Soil Moisture", f"{latest_sm:.1f}%", delta=f"Avg: {avg_sm:.1f}%")
                
                with cols[3]:
                    latest_wl = df.iloc[-1]["water_level"]
                    avg_wl = df["water_level"].mean()
                    st.metric("💦 Water Level", f"{latest_wl:.1f}", delta=f"Avg: {avg_wl:.1f}")
                
                st.divider()
                
                # Visualizations
                st.subheader("📈 Sensor Data Visualization")
                
                # Temperature Chart
                fig1 = px.line(df_sorted, x="created_at", y="temperature", 
                              title="🌡️ Temperature Over Time",
                              labels={"created_at": "Time", "temperature": "Temperature (°C)"},
                              markers=True)
                fig1.update_traces(line_color='#FF6B6B', marker=dict(size=6))
                fig1.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig1, use_container_width=True)
                
                # Humidity Chart
                fig2 = px.line(df_sorted, x="created_at", y="humidity",
                              title="💧 Humidity Over Time",
                              labels={"created_at": "Time", "humidity": "Humidity (%)"},
                              markers=True)
                fig2.update_traces(line_color='#4ECDC4', marker=dict(size=6))
                fig2.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig2, use_container_width=True)
                
                # Soil Moisture Chart
                fig3 = px.line(df_sorted, x="created_at", y="soil_moisture",
                              title="🌱 Soil Moisture Over Time",
                              labels={"created_at": "Time", "soil_moisture": "Soil Moisture (%)"},
                              markers=True)
                fig3.update_traces(line_color='#95E1D3', marker=dict(size=6))
                fig3.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig3, use_container_width=True)
                
                # Water Level Chart
                fig4 = px.line(df_sorted, x="created_at", y="water_level",
                              title="💦 Water Level Over Time",
                              labels={"created_at": "Time", "water_level": "Water Level"},
                              markers=True)
                fig4.update_traces(line_color='#3742FA', marker=dict(size=6))
                fig4.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig4, use_container_width=True)
                
                # Wind Speed Chart
                fig5 = px.line(df_sorted, x="created_at", y="wind_speed",
                              title="🌬️ Wind Speed Over Time",
                              labels={"created_at": "Time", "wind_speed": "Wind Speed (km/h)"},
                              markers=True)
                fig5.update_traces(line_color='#FFA502', marker=dict(size=6))
                fig5.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig5, use_container_width=True)
                
                # Rainfall Bar Chart
                fig6 = px.bar(df_sorted, x="created_at", y="rainfall",
                             title="🌧️ Rainfall Over Time",
                             labels={"created_at": "Time", "rainfall": "Rainfall (mm)"})
                fig6.update_traces(marker_color='#5F27CD')
                fig6.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig6, use_container_width=True)
                
                # Data Table (collapsible)
                with st.expander("📋 View Raw Data Table"):
                    st.dataframe(df, use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ Error generating demo data: {e}")

# Global status tracker for all models
MODEL_STATUS = {
    'crop_model': False,
    'irrigation_model': False,
    'optimization_model': False,
    'soil_model': False
}

def load_crop_model():
    import os
    import joblib
    
    # Get the absolute path to the repository root  
    current_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    
    # Direct path to the crop model
    model_path = os.path.join(repo_root, "models", "crop recommendation", "crop_model.pkl")

    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            MODEL_STATUS['crop_model'] = True
            return model
        except Exception as e:
            st.error(f"Error loading crop model from {model_path}: {type(e).__name__}: {e}")
            MODEL_STATUS['crop_model'] = False
            return None
    else:
        st.error(f"❌ Crop model file not found at: {model_path}")
        MODEL_STATUS['crop_model'] = False
        return None

def load_irrigation_model():
    import os
    import joblib
    
    # Get the absolute path to the repository root
    current_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    
    # Direct path to the irrigation model
    model_path = os.path.join(repo_root, "models", "Smart_Irrigation_Classifier", "catboost_model.pkl")

    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            MODEL_STATUS['irrigation_model'] = True
            return model
        except Exception as e:
            st.error(f"Error loading irrigation model from {model_path}: {type(e).__name__}: {e}")
            MODEL_STATUS['irrigation_model'] = False
            return None
    else:
        st.error(f"❌ Irrigation model file not found at: {model_path}")
        MODEL_STATUS['irrigation_model'] = False
        return None

def load_optimization_model():
    import os
    import joblib
    
    # Get the absolute path to the repository root
    current_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    
    # Direct path to the optimization model
    model_path = os.path.join(repo_root, "models", "irrigation_optimization_model", "catboost_irrigation_model.pkl")

    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            MODEL_STATUS['optimization_model'] = True
            return model
        except Exception as e:
            st.error(f"Error loading optimization model from {model_path}: {type(e).__name__}: {e}")
            MODEL_STATUS['optimization_model'] = False
            return None
    else:
        st.error(f"❌ Optimization model file not found at: {model_path}")
        MODEL_STATUS['optimization_model'] = False
        return None

MODEL_STATUS = {'soil_model': False} 

def load_soil_model():
    """Load TensorFlow soil type classification model (supports .h5 and SavedModel)"""
    # يجب تعريف _file_ بشكل صحيح في بيئة Streamlit
    # سنستخدم اسم ملف وهمي لكي يعمل الكود هنا
    _file_ = __file__ # يجب أن يكون هذا السطر موجودًا في الملف الأصلي

    # Get the absolute path to the repository root
    current_file = os.path.abspath(_file_)
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    
    # Try loading .h5 file first (your model)
    h5_path = os.path.join(repo_root, "soil_model_savedmodel", "my_soil_model.h5")
    savedmodel_path = os.path.join(repo_root, "soil_model_savedmodel")
    
    # قائمة التسميات الصحيحة التي تدرب عليها النموذج (مستخلصة من إخراجك السابق)
    # هذا الترتيب يجب أن يطابق ترتيب الفئات في مجلدات التدريب: (0: Peat, 1: Sandy, 2: Silt)
    CORRECT_SOIL_LABELS = ["Peat Soil", "Sandy Soil", "Silt Soil"]
    
    # Try .h5 model first
    if os.path.exists(h5_path):
        try:
            # Use compile=False to avoid Keras 3 compatibility issues with custom layers
            model = tf.keras.models.load_model(h5_path, compile=False)
            MODEL_STATUS['soil_model'] = True
            
            # --- الإصلاح هنا: استخدام التسميات الصحيحة ---
            soil_labels = CORRECT_SOIL_LABELS
            
            return model, soil_labels
        except Exception as e:
            st.error(f"Error loading H5 model from {h5_path}: {type(e).__name__}: {e}")
    
    # Fallback to SavedModel
    elif os.path.exists(savedmodel_path):
        try:
            from tensorflow.keras.layers import TFSMLayer
            model = TFSMLayer(savedmodel_path, call_endpoint='serving_default')
            MODEL_STATUS['soil_model'] = True
            
            # --- الإصلاح هنا: استخدام التسميات الصحيحة ---
            soil_labels = CORRECT_SOIL_LABELS
            
            st.info(f"ℹ Using SavedModel from: {savedmodel_path}")
            return model, soil_labels
        except Exception as e:
            st.error(f"Error loading SavedModel from {savedmodel_path}: {type(e).__name__}: {e}")
    
    # No model found
    st.warning(f"⚠ Soil model not found. Tried:\n- {h5_path}\n- {savedmodel_path}")
    MODEL_STATUS['soil_model'] = False
    return None, None

# Load all models
crop_model = load_crop_model()
irrigation_model = load_irrigation_model()
optimization_model = load_optimization_model()
soil_model, soil_labels = load_soil_model()


def fetch_latest_iot_reading():
    """Fetch the latest sensor reading from Supabase (table: 'Sensor readings').
    Returns a dict with float values or None on failure.
    Converts soil_moisture from 0-1 to 0-100 automatically if needed.
    """
    SUPABASE_URL = os.getenv("SUPABASE_URL") or (st.secrets.get("SUPABASE_URL") if hasattr(st, "secrets") else None)
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or (st.secrets.get("SUPABASE_SERVICE_KEY") if hasattr(st, "secrets") else None)
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = supabase.table("Sensor readings").select("*").order("created_at", desc=True).limit(1).execute()
        data = response.data
        if not data:
            return None
        rec = data[0]

        def _f(key, default=None):
            v = rec.get(key)
            try:
                return float(v) if v is not None else default
            except Exception:
                return default

        result = {
            'temperature': _f('temperature', None),
            'humidity': _f('humidity', None),
            'soil_moisture': _f('soil_moisture', None),
            'wind_speed': _f('wind_speed', None),
            'pressure': _f('pressure', None),
            'rainfall': _f('rainfall', None),
        }

        # If soil_moisture looks normalized (0-1) convert to percent
        sm = result.get('soil_moisture')
        if sm is not None and sm <= 1.0:
            result['soil_moisture'] = sm * 100.0

        return result
    except Exception:
        return None

# Soil classification function
def predict_soil_type(image, soil_model, soil_labels):
    """Predict soil type from uploaded image using TensorFlow model"""
    if soil_model is None or soil_labels is None:
        return None, None, "Model not loaded", None
    
    try:
        # Enhanced preprocessing for better accuracy
        # 1. Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 2. Resize to model input size (224x224)
        img = image.resize((224, 224), Image.Resampling.LANCZOS)
        
        # 3. Convert to array
        img_array = np.array(img, dtype=np.float32)
        
        # 4. Normalize to [0, 1] range (standard for most models)
        img_array = img_array / 255.0
        
        # 5. Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # 6. Predict using the model
        if hasattr(soil_model, 'predict'):
            # H5 model - use standard predict
            predictions = soil_model.predict(img_array, verbose=0)
            all_probs = predictions[0]
        else:
            # TFSMLayer - returns dictionary
            img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)
            output = soil_model(img_tensor)
            
            # Extract predictions from output dictionary
            predictions = None
            for key in output.keys():
                predictions = output[key].numpy()
                break
            
            if predictions is None:
                return None, None, "Could not extract predictions from model output", None
            
            all_probs = predictions[0]
        
        # Apply softmax to normalize probabilities if they're not already normalized
        if not np.isclose(np.sum(all_probs), 1.0, rtol=0.1):
            exp_probs = np.exp(all_probs - np.max(all_probs))  # Numerical stability
            all_probs = exp_probs / np.sum(exp_probs)
        
        # Get predicted class and confidence
        predicted_class = np.argmax(all_probs)
        confidence = float(all_probs[predicted_class])
        
        # --- هذا السطر يستخدم القائمة المصححة ---
        soil_type = soil_labels[predicted_class]
        
        return soil_type, confidence, None, all_probs
    except Exception as e:
        return None, None, f"Prediction error: {e}", None

# Feature engineering functions
def create_irrigation_features(soil_moisture, temperature, humidity, ph, n, p, k, rainfall=0):
    """Create all required features for irrigation model"""
    import numpy as np
    
    # Basic features
    soil_humidity = humidity * 0.8  # Approximate soil humidity
    air_temperature = temperature
    
    # Derived features
    relative_soil_saturation = min(soil_moisture / 100.0, 1.0)
    temp_diff = abs(temperature - 25)  # Difference from optimal temp
    evapotranspiration = max(0, (temperature - 10) * 0.1 + (100 - humidity) * 0.05)
    rain_vs_soil = rainfall / max(soil_moisture, 1)
    ph_encoded = 1 if ph > 7 else 0  # Alkaline vs acidic
    
    # NPK ratios
    np_ratio = n / max(p, 1)
    nk_ratio = n / max(k, 1)
    npk_balance = (n + p + k) / 3
    
    # Additional derived features
    crop_encoded = 1  # Default crop type
    rain_3days = rainfall * 3  # Assume same rainfall for 3 days
    moisture_temp_ratio = soil_moisture / max(temperature, 1)
    evapo_ratio = evapotranspiration / max(rainfall, 0.1)
    rain_effect = min(rainfall / 10, 1.0)
    moisture_change_rate = 0.1  # Default change rate
    temp_scaled = temperature / 40  # Scale temperature
    wind_ratio = 0.5  # Default wind effect
    
    return np.array([[
        soil_moisture, temperature, soil_humidity, relative_soil_saturation,
        temp_diff, evapotranspiration, rain_vs_soil, rainfall, ph_encoded,
        n, p, k, np_ratio, nk_ratio, crop_encoded, rain_3days,
        moisture_temp_ratio, evapo_ratio, rain_effect, moisture_change_rate,
        temp_scaled, npk_balance, wind_ratio
    ]])

def create_optimization_features(soil_moisture, temperature, humidity, ph, n, p, k, rainfall=0):
    """Create all required features for optimization model"""
    import numpy as np
    
    # Basic environmental features
    soil_humidity = humidity * 0.8
    air_temperature = temperature
    wind_speed = 10  # Default wind speed
    wind_gust = wind_speed * 1.5
    pressure = 101.325  # Standard atmospheric pressure
    
    # Derived features
    soil_moisture_diff = 0.1  # Default change
    relative_soil_saturation = min(soil_moisture / 100.0, 1.0)
    temp_diff = abs(temperature - 25)
    wind_effect = wind_speed * 0.1
    evapotranspiration = max(0, (temperature - 10) * 0.1 + (100 - humidity) * 0.05)
    rain_3days = rainfall * 3
    rain_vs_soil = rainfall / max(soil_moisture, 1)
    
    # NPK features
    np_ratio = n / max(p, 1)
    nk_ratio = n / max(k, 1)
    npk_balance = (n + p + k) / 3
    
    # Encoded features
    ph_encoded = 1 if ph > 7 else 0
    crop_encoded = 1
    
    # Additional ratios
    moisture_temp_ratio = soil_moisture / max(temperature, 1)
    evapo_ratio = evapotranspiration / max(rainfall, 0.1)
    rain_effect = min(rainfall / 10, 1.0)
    moisture_change_rate = 0.1
    temp_scaled = temperature / 40
    wind_ratio = wind_speed / 50
    
    return np.array([[
        soil_moisture, temperature, soil_humidity, air_temperature,
        wind_speed, humidity, wind_gust, pressure, ph, rainfall,
        n, p, k, soil_moisture_diff, relative_soil_saturation,
        temp_diff, wind_effect, evapotranspiration, rain_3days,
        rain_vs_soil, np_ratio, nk_ratio, ph_encoded, crop_encoded,
        moisture_temp_ratio, evapo_ratio, rain_effect, moisture_change_rate,
        temp_scaled, npk_balance, wind_ratio
    ]])


def recommend_from_dataset(N, P, K, temperature, humidity, ph, rainfall, k=5):
    """Lightweight nearest-neighbour recommender that uses data/crop_data.csv.

    Returns (label, confidence) where confidence is fraction of the k nearest neighbors
    that agree with the predicted label.
    """
    import pandas as _pd
    import numpy as _np
    import os as _os

    cache_name = '_crop_dataset_cache'
    if cache_name not in globals():
        data_path = _os.path.join(repo_root, 'data', 'crop_data.csv')
        if not _os.path.exists(data_path):
            raise FileNotFoundError(f"Dataset not found: {data_path}")
        df = _pd.read_csv(data_path)
        feats = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']].values.astype(float)
        labels = df['label'].astype(str).values
        mean = feats.mean(axis=0)
        std = feats.std(axis=0)
        std[std == 0] = 1.0
        globals()[cache_name] = {'feats': feats, 'labels': labels, 'mean': mean, 'std': std}

    cache = globals()[cache_name]
    feat = _np.array([N, P, K, temperature, humidity, ph, rainfall], dtype=float)
    norm = (feat - cache['mean']) / cache['std']
    feats_norm = (cache['feats'] - cache['mean']) / cache['std']
    dists = _np.linalg.norm(feats_norm - norm, axis=1)
    idx = _np.argsort(dists)[:k]
    top_labels = cache['labels'][idx]
    uniques, counts = _np.unique(top_labels, return_counts=True)
    mode = uniques[counts.argmax()]
    conf = float(counts.max()) / float(k)
    return str(mode), conf


def call_gemini_chat(prompt, context=None, system_instruction=None):
    """Call the Gemini REST API and return a dict with text + metadata."""
    
    # Check for Service Account authentication first
    service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.path.join(
        os.path.dirname(__file__), "service-account.json"
    )
    
    access_token = None
    api_key = None
    
    # Try Service Account authentication first
    if os.path.exists(service_account_path):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=['https://www.googleapis.com/auth/generative-language.retriever']
            )
            credentials.refresh(Request())
            access_token = credentials.token
        except Exception as e:
            st.warning(f"Service Account auth failed, trying API key: {e}")
    
    # Fall back to API key if Service Account not available
    if not access_token:
        api_key = os.getenv("GEMINI_API_KEY") or (st.secrets.get("GEMINI_API_KEY") if hasattr(st, "secrets") else None)
        if not api_key:
            raise ValueError("Neither GOOGLE_APPLICATION_CREDENTIALS nor GEMINI_API_KEY found. Please set one in .env or Streamlit secrets.")

    model_name = (os.getenv("GEMINI_MODEL", "gemini-1.5-flash") or "").strip() or "gemini-1.5-flash"
    endpoint_override = os.getenv("GEMINI_REST_URL")

    def _build_endpoint(model):
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    headers = {"Content-Type": "application/json"}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    user_parts = [
        {"text": prompt}
    ]
    if context:
        user_parts.append({"text": f"\nContext:\n{context}"})

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": user_parts
            }
        ]
    }

    if system_instruction:
        payload["system_instruction"] = {
            "parts": [{"text": system_instruction}]
        }

    attempt_log = []
    available_model_cache = {"names": None, "error": None}

    def _make_request(url):
        try:
            # Use Bearer token if available, otherwise use API key
            if access_token:
                return requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
            else:
                return requests.post(
                    url,
                    params={"key": api_key},
                    headers=headers,
                    json=payload,
                    timeout=30
                )
        except requests.RequestException as req_err:
            raise RuntimeError(f"Gemini request failed: {req_err}") from req_err

    def _call_model(target_model, reason=None):
        target_url = endpoint_override or _build_endpoint(target_model)
        response = _make_request(target_url)
        attempt_log.append({
            "model": target_model,
            "status": getattr(response, "status_code", None),
            "ok": getattr(response, "ok", False),
            "reason": reason or ("endpoint override" if endpoint_override else "default")
        })
        return response

    def _fetch_available_models():
        if available_model_cache["names"] is not None or available_model_cache["error"] is not None:
            return available_model_cache["names"]
        try:
            # Use Bearer token if available, otherwise use API key
            if access_token:
                resp = requests.get(
                    "https://generativelanguage.googleapis.com/v1beta/models",
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=15
                )
            else:
                resp = requests.get(
                    "https://generativelanguage.googleapis.com/v1beta/models",
                    params={"key": api_key},
                    timeout=15
                )
            if resp.ok:
                data = resp.json()
                names = set()
                for model in data.get("models", []):
                    name = model.get("name")
                    if not name:
                        continue
                    short_name = name.split("/")[-1]
                    methods = model.get("supportedGenerationMethods", []) or []
                    if "generateContent" in methods:
                        names.add(short_name)
                available_model_cache["names"] = names
                return names
            else:
                available_model_cache["error"] = resp.text
        except requests.RequestException as fetch_err:
            available_model_cache["error"] = str(fetch_err)
        return None

    response = _call_model(model_name)
    used_model = model_name
    fallback_notice = None
    fallback_used = False

    if not response.ok and response.status_code == 404 and not endpoint_override:
        fallback_notice_parts = []
        fallback_chain = []

        if model_name.endswith("-latest"):
            trimmed = model_name.removesuffix("-latest")
            if trimmed and trimmed != model_name:
                fallback_chain.append((trimmed, "'-latest' alias unavailable"))

        preferred_order = [
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-2.5-flash-lite-preview-06-17"
        ]
        for candidate in preferred_order:
            if candidate and candidate != model_name:
                fallback_chain.append((candidate, "Primary model unavailable"))

        available_names = _fetch_available_models()

        def _allowed(candidate):
            if not available_names:
                return True
            return candidate in available_names

        filtered_chain = [(model, reason) for model, reason in fallback_chain if _allowed(model)]

        if available_names:
            missing_models = [model for model, _ in fallback_chain if model not in available_names]
            if missing_models:
                fallback_notice_parts.append(
                    "Models not in your account were skipped: " + ", ".join(missing_models)
                )

        for fallback_model, reason in filtered_chain:
            fallback_notice_parts.append(
                f"{reason}. Retrying with '{fallback_model}'. Update GEMINI_MODEL to pin a working model."
            )
            response = _call_model(fallback_model, reason=reason)
            if response.ok:
                used_model = fallback_model
                fallback_notice = " ".join(fallback_notice_parts)
                fallback_used = True
                break

    if not response.ok:
        try:
            err_payload = response.json()
            err_detail = err_payload.get("error", {}).get("message") or err_payload.get("error", {}).get("status")
        except ValueError:
            err_detail = response.text

        attempt_summary = ", ".join(
            f"{entry['model']}→{entry.get('status')}" if entry.get('status') else entry['model']
            for entry in attempt_log
        )
        if attempt_summary:
            err_detail = f"{err_detail} (attempts: {attempt_summary})"

        if available_model_cache["names"]:
            sorted_names = ", ".join(sorted(available_model_cache["names"]))
            err_detail = f"{err_detail} | Available models for key: {sorted_names}"
        elif available_model_cache["error"]:
            err_detail = f"{err_detail} | Unable to list models: {available_model_cache['error']}"

        extra_hint = ""
        if response.status_code == 404 and not endpoint_override:
            if model_name.endswith("-latest") and not fallback_used:
                extra_hint = " Tip: remove the '-latest' suffix or set GEMINI_REST_URL explicitly."
            else:
                extra_hint = " Ensure your GEMINI_MODEL matches an available model for your API key."
        elif endpoint_override:
            extra_hint = " Verify GEMINI_REST_URL is correct or unset it to allow automatic fallbacks."

        raise RuntimeError(f"Gemini API error ({response.status_code}): {err_detail}{extra_hint}")

    data = response.json()

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        text = ""

    if not text:
        text = "No response returned from Gemini."

    return {
        "text": text,
        "model_used": used_model,
        "notice": fallback_notice,
        "attempts": attempt_log
    }

# Check overall system status
def check_system_status():
    """Returns True only if ALL required models are loaded successfully"""
    all_loaded = all(MODEL_STATUS.values())
    if not all_loaded:
        failed_models = [model for model, status in MODEL_STATUS.items() if not status]
        st.error(f"🚨 **System Status: FAILED** - Models not loaded: {', '.join(failed_models)}")
        st.warning("⚠️ **Fail-Safe Mode**: All predictions will return 0/False due to missing models")
        return False
    else:
        st.success("✅ **System Status: OPERATIONAL** - All models loaded successfully")
        return True

# Check system status
system_operational = check_system_status()

# Try to auto-fill inputs from the latest IoT reading (if available)
sensor_defaults = fetch_latest_iot_reading() or {}

# Helper that treats explicit None as missing and falls back to default
def _safe_default(key, default):
    v = sensor_defaults.get(key, None)
    return default if v is None else v

# prepare defaults (fall back to previous hard-coded defaults)
temp_default = _safe_default('temperature', 23.0)
hum_default = _safe_default('humidity', 82.0)
soil_moisture_default = _safe_default('soil_moisture', 35.0)
wind_speed_default = _safe_default('wind_speed', 8.0)
pressure_default = _safe_default('pressure', 101.3)
rain_default = _safe_default('rainfall', 240.0)

# Create two columns layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 Soil & Environment Data")
    # Option to auto-fill selected inputs from IoT and lock those widgets
    auto_fill = st.checkbox("🔁 Auto-fill Temperature / Humidity / Soil Moisture from IoT", value=True, help="When enabled, temperature, humidity and soil moisture are populated from IoT and locked for editing")

    # Manual refresh button to fetch latest IoT values into session state
    if st.button("🔄 Fetch IoT Now"):
        new = fetch_latest_iot_reading()
        if new:
            st.session_state['sensor_defaults'] = new
        else:
            st.warning("No IoT data available or failed to fetch.")
        # `st.experimental_rerun()` is not present in all Streamlit builds/environments.
        # Try to call it if available; otherwise inform the user to refresh.
        try:
            if hasattr(st, 'experimental_rerun'):
                st.experimental_rerun()
            elif hasattr(st, 'rerun'):
                # some versions expose a different API
                st.rerun()
            else:
                st.success("IoT values fetched — please refresh the page to apply the new defaults.")
        except Exception:
            st.success("IoT values fetched — please refresh the page to apply the new defaults.")

    # Prefer session-cached sensor values if present (after manual refresh)
    current_sensor = st.session_state.get('sensor_defaults', sensor_defaults)
    
    # Input fields for crop recommendation
    N = st.number_input("🟤 Nitrogen (N)", min_value=0, max_value=200, value=101, help="Nitrogen content in soil")
    P = st.number_input("🟠 Phosphorus (P)", min_value=0, max_value=200, value=33, help="Phosphorus content in soil")
    K = st.number_input("🟡 Potassium (K)", min_value=0, max_value=200, value=33, help="Potassium content in soil")
    
    st.divider()
    
    temp_val = current_sensor.get('temperature', temp_default)
    hum_val = current_sensor.get('humidity', hum_default)
    temp = st.number_input("🌡️ Temperature (°C)", min_value=0.0, max_value=50.0, value=float(temp_val), help="Average temperature", disabled=auto_fill)
    hum = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=float(hum_val), help="Relative humidity", disabled=auto_fill)
    ph = st.number_input("⚗️ Soil pH", min_value=0.0, max_value=14.0, value=6.91, help="Soil pH level")
    rain = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, max_value=300.0, value=142.86, help="Annual rainfall")
    
    st.divider()
    
    # Additional inputs for irrigation models
    # Use percentage (0-100) for soil moisture so downstream feature calculations
    # that divide by 100 (to compute relative saturation) work as intended.
    soil_val = current_sensor.get('soil_moisture', soil_moisture_default)
    soil_moisture = st.number_input(
        "💧 Soil Moisture (%)",
        min_value=0.0,
        max_value=100.0,
        value=float(soil_val),
        step=0.1,
        help="Soil moisture as percentage (0-100). Example: 35 means 35% volumetric water content",
        disabled=auto_fill,
    )
    # wind_speed and pressure remain manual inputs (always editable)
    wind_speed = st.number_input("🌬️ Wind Speed (km/h)", min_value=0.0, max_value=50.0, value=float(wind_speed_default), help="Wind speed")
    pressure = st.number_input("🌡️ Pressure (kPa)", min_value=80.0, max_value=110.0, value=float(pressure_default), help="Atmospheric pressure")
    
    # === SOIL TYPE CLASSIFICATION SECTION ===
    st.divider()
    st.header("🏞️ Soil Type Classification")
    st.markdown("Upload a soil image to identify the soil type using AI")
    
    uploaded_file = st.file_uploader("Choose a soil image...", type=["jpg", "jpeg", "png"], help="Upload a clear image of the soil surface")
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.image(image, caption="Uploaded Soil Image", use_container_width=True)
        
        # Classify button
        if st.button("🔍 Classify Soil Type", type="primary", use_container_width=True, key="classify_soil"):
            if not MODEL_STATUS.get('soil_model') or soil_model is None:
                st.error("❌ **SOIL CLASSIFIER NOT LOADED**: Cannot classify soil type")
                st.info("🔄 Please ensure soil_model_savedmodel is available in the project root")
            else:
                with st.spinner("🔄 Analyzing soil image..."):
                    # Get prediction with all probabilities
                    result = predict_soil_type(image, soil_model, soil_labels)
                    
                    if len(result) == 3:
                        soil_type, confidence, error = result
                        all_probs = None
                    else:
                        soil_type, confidence, error, all_probs = result
                    
                    if error:
                        st.error(f"❌ Classification failed: {error}")
                    else:
                        st.success("✅ Classification Complete!")
                        
                        # Display result in a nice card (without confidence)
                        st.markdown(f"""
                        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                            <h2 style="color: #2e7d32; margin: 0;">🌍 Predicted Soil Type</h2>
                            <h1 style="color: #1976d2; margin: 10px 0; font-size: 3em;">{soil_type}</h1>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Soil type information
                        soil_info = {
                            'Alluvial': '🌊 **Alluvial Soil**: Rich in minerals and nutrients, formed by river deposits. Excellent for agriculture with good water retention.',
                            'Black': '🖤 **Black Soil**: High in clay content, rich in calcium, iron, and magnesium. Ideal for cotton cultivation and retains moisture well.',
                            'Clay': '🧱 **Clay Soil**: Heavy texture with very fine particles. Good water retention but poor drainage. Needs proper management for cultivation.',
                            'Red': '🔴 **Red Soil**: Contains iron oxide giving it red color. Good for crops like groundnuts, potatoes, and pulses. Moderate fertility.'
                        }
                        
                        if soil_type in soil_info:
                            st.info(soil_info[soil_type])
                        
                        # Add interpretation help
                        if confidence < 0.6:
                            st.warning("⚠️ **Low Confidence**: The model is not very confident about this prediction. Consider taking a clearer photo with better lighting.")
                        elif confidence < 0.8:
                            st.info("ℹ️ **Medium Confidence**: The prediction is reasonably confident but could be improved with a better quality image.")
                        else:
                            st.success("💡 **High Confidence**: The model is very confident about this prediction!")
                        
                        st.success("💡 **Tip**: For best results, use clear, well-lit images showing the soil texture and color clearly.")

with col2:
    st.header("🎯 Recommendations & Decisions")
    # Developer debug toggle: show raw inputs/outputs on the page
    show_debug = st.checkbox("🔧 Show raw inputs & model outputs", value=False, key="show_debug")
    
    # === CROP RECOMMENDATION SECTION ===
    st.subheader("🌱 Crop Recommendation")
    
    if st.button("🚀 Get Crop Recommendation", type="primary", width="stretch", key="crop_recommendation"):
        # Check if crop model is loaded
        if not MODEL_STATUS.get('crop_model') or crop_model is None:
            st.error("❌ **CROP MODEL NOT LOADED**: Cannot provide recommendations")
            st.info("🔄 Please ensure crop_model.pkl is available in models/crop recommendation/")
        else:
            try:
                # Create DataFrame with proper column names to avoid warnings
                feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                input_data = pd.DataFrame([[N, P, K, temp, hum, ph, rain]], columns=feature_names)
                # Debug: log inputs to help trace behavior and optionally show on the page
                crop_inputs_dict = input_data.to_dict(orient='records')[0]
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"CROP_INPUTS: {crop_inputs_dict}\n")
                except Exception:
                    pass

                # Make prediction using crop_model
                prediction = None
                confidence = None

                try:
                    prediction = crop_model.predict(input_data)[0]
                    try:
                        confidence = crop_model.predict_proba(input_data).max()
                    except Exception:
                        confidence = None
                except Exception as pred_error:
                    st.error(f"❌ **PREDICTION FAILED**: {str(pred_error)}")
                    prediction = 'unknown'
                    confidence = None
                
                # Debug: log model outputs as well and (optionally) print them to the page
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"CROP_OUTPUT: pred={prediction}, conf={confidence}\n")
                except Exception:
                    pass

                if show_debug:
                    st.markdown("**Debug — crop model inputs**")
                    st.write(input_data)
                    st.markdown("**Debug — crop model outputs**")
                    st.write({"prediction": str(prediction), "confidence": float(confidence) if confidence is not None else None})

                # Display results only if prediction was successful
                if prediction != 'unknown':
                    st.success(f"🌱 **Recommended Crop: {prediction.title()}**")
                    if confidence is not None:
                        st.info(f"🎯 **Confidence: {confidence:.2%}**")
                    
                    # Add crop information
                    crop_info = {
                        'rice': '🍚 Rice - High water requirement, suitable for humid conditions',
                        'maize': '🌽 Maize - Moderate water requirement, good for moderate climate',
                        'chickpea': '🫘 Chickpea - Low water requirement, drought tolerant',
                        'kidneybeans': '🫘 Kidney Beans - Nitrogen-fixing legume',
                        'pigeonpeas': '🫛 Pigeon Peas - Drought resistant pulse crop',
                        'mothbeans': '🫘 Moth Beans - Heat and drought tolerant',
                        'mungbean': '🫛 Mung Bean - Quick growing pulse crop',
                        'blackgram': '🫘 Black Gram - Protein-rich pulse crop',
                        'lentil': '🟤 Lentil - Cool season pulse crop',
                        'pomegranate': '🍎 Pomegranate - Antioxidant-rich fruit',
                        'banana': '🍌 Banana - Tropical fruit, high potassium needs',
                        'mango': '🥭 Mango - King of fruits, tropical climate',
                        'grapes': '🍇 Grapes - Mediterranean climate preferred',
                        'watermelon': '🍉 Watermelon - High water requirement in summer',
                        'muskmelon': '🍈 Muskmelon - Warm season crop',
                        'apple': '🍎 Apple - Temperate climate fruit',
                        'orange': '🍊 Orange - Citrus fruit, warm climate',
                        'papaya': '🥭 Papaya - Tropical fruit, year-round growing',
                        'coconut': '🥥 Coconut - Coastal tropical crop',
                        'cotton': '🌿 Cotton - Cash crop, moderate water needs',
                        'jute': '🌿 Jute - Fiber crop, high humidity required',
                        'coffee': '☕ Coffee - Shade-grown, specific climate needs'
                    }
                    
                    if prediction.lower() in crop_info:
                        st.info(crop_info[prediction.lower()])
                        
            except Exception as e:
                st.error(f"❌ **PREDICTION FAILED**: {str(e)}")
                st.info("🔄 **Returned Value**: 0 (Exception fail-safe)")
    
    # === IRRIGATION DECISIONS SECTION ===
    st.divider()
    st.subheader("💧 Smart Irrigation Analysis")
    
    # Unified Irrigation Check & Optimization
    if st.button("🔍 Analyze Irrigation Needs", type="primary", width="stretch", key="irrigation_analysis"):
        if not system_operational or not MODEL_STATUS['irrigation_model']:
            st.error("❌ **FAIL-SAFE ACTIVATED**: Irrigation model unavailable")
            st.info("🔄 **Returned Value**: 0 (Safe failure mode)")
        else:
            try:
                # STEP 1: Smart Irrigation Check
                st.markdown("### 📊 Step 1: Irrigation Decision")
                
                # Create features for irrigation model
                irrigation_features = create_irrigation_features(
                    soil_moisture, temp, hum, ph, N, P, K, rain
                )
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"IRR_INPUTS: soil_moisture={soil_moisture}, temp={temp}, hum={hum}, ph={ph}, N={N}, P={P}, K={K}, rain={rain}\n")
                except Exception:
                    pass
                
                pred = irrigation_model.predict(irrigation_features)[0]
                
                # Get prediction probability if available
                try:
                    prob = irrigation_model.predict_proba(irrigation_features).max()
                except Exception:
                    prob = None
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"IRR_OUTPUT: pred={pred}, conf={prob}\n")
                except Exception:
                    pass

                if show_debug:
                    st.markdown("**Debug — irrigation model inputs**")
                    st.write(irrigation_features.tolist())
                    st.markdown("**Debug — irrigation model outputs**")
                    st.write({"prediction": str(pred), "confidence": float(prob) if prob is not None else None})

                # Display irrigation decision
                irrigation_needed = (pred == 1 or pred == 'irrigate')
                
                if irrigation_needed:
                    st.success(f"✅ **Irrigation Needed**")
                    if prob is not None:
                        st.info(f"🎯 **Confidence: {prob:.2%}**")
                    
                    # STEP 2: Calculate Optimal Irrigation Amount (only if irrigation is needed)
                    st.markdown("### ⚡ Step 2: Optimal Irrigation Amount")
                    
                    if not MODEL_STATUS['optimization_model']:
                        st.warning("⚠️ **Optimization model unavailable** - Cannot calculate optimal amount")
                    else:
                        try:
                            # Create features for optimization model
                            optimization_features = create_optimization_features(
                                soil_moisture, temp, hum, ph, N, P, K, rain
                            )
                            
                            try:
                                with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                                    _dbg.write(f"OPT_INPUTS: soil_moisture={soil_moisture}, temp={temp}, hum={hum}, ph={ph}, N={N}, P={P}, K={K}, rain={rain}\n")
                            except Exception:
                                pass
                            
                            optimization_pred = optimization_model.predict(optimization_features)[0]
                            
                            try:
                                with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                                    _dbg.write(f"OPT_OUTPUT: pred={optimization_pred}\n")
                            except Exception:
                                pass

                            if show_debug:
                                st.markdown("**Debug — optimization model inputs**")
                                st.write(optimization_features.tolist())
                                st.markdown("**Debug — optimization model outputs**")
                                st.write({"prediction": float(optimization_pred)})
                            
                            # Validation check
                            if optimization_pred < 0 or optimization_pred > 100:
                                st.error("❌ **INVALID OPTIMIZATION RESULT**")
                                st.info("🔄 **Returned Value**: 0 (Validation fail-safe)")
                            else:
                                st.success(f"💧 **Recommended Irrigation: {optimization_pred:.2f} units**")
                                
                                # Summary box
                                st.success(f"""
                                ### 🎯 Irrigation Summary
                                - **Decision**: Irrigation Required ✅
                                - **Optimal Amount**: {optimization_pred:.2f} units
                                - **Confidence**: {prob:.2%} (Classification)
                                """)
                                
                        except Exception as e:
                            st.error(f"❌ **OPTIMIZATION FAILED**: {str(e)}")
                            st.info("🔄 **Returned Value**: 0 (Exception fail-safe)")
                else:
                    st.info(f"🚫 **No Irrigation Needed**")
                    if prob is not None:
                        st.info(f"🎯 **Confidence: {prob:.2%}**")
                    
                    # Display recommended units as 0
                    st.success("💧 **Recommended Irrigation: 0.00 units**")
                    st.info("✅ Soil conditions are adequate - no irrigation required at this time")
                    
                    # Summary box
                    st.success(f"""
                    ### 🎯 Irrigation Summary
                    - **Decision**: No Irrigation Required ✅
                    - **Recommended Amount**: 0.00 units
                    - **Confidence**: {prob:.2%} (Classification)
                    - **Reason**: Soil moisture and environmental conditions are adequate
                    """)
                        
            except Exception as e:
                st.error(f"❌ **IRRIGATION ANALYSIS FAILED**: {str(e)}")
                st.info("🔄 **Returned Value**: 0 (Exception fail-safe)")

    st.divider()
    st.subheader("🤖 Gemini Chatbot")
    st.markdown("Get quick crop & irrigation tips powered by Gemini.")

    gemini_prompt = st.text_area(
        "💬 Enter your question or request",
        placeholder="Example: What's the best way to irrigate rice during a heat wave?",
        key="gemini_prompt",
        height=120
    )

    context_snippet = (
        f"Current soil inputs -> N:{N}, P:{P}, K:{K}, Temp:{temp}°C, Humidity:{hum}%, pH:{ph}, Rainfall:{rain}mm, "
        f"Soil moisture:{soil_moisture}, Wind:{wind_speed}km/h, Pressure:{pressure}kPa"
    )

    if st.button("✨ Ask Gemini", type="primary", key="gemini_button"):
        clean_prompt = gemini_prompt.strip()
        if not clean_prompt:
            st.warning("⚠️ Please type a question first.")
        else:
            with st.spinner("Contacting Gemini..."):
                try:
                    try:
                        with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                            _dbg.write(f"GEMINI_PROMPT: {clean_prompt}\n")
                    except Exception:
                        pass

                    system_instruction = (
                        "You are AgriTech Assistant (Gemini) that explains crop and irrigation guidance in concise, practical English. "
                        "Use the provided soil context when relevant and keep responses under 200 words."
                    )
                    gemini_result = call_gemini_chat(
                        clean_prompt,
                        context=context_snippet,
                        system_instruction=system_instruction
                    )

                    if isinstance(gemini_result, dict):
                        gemini_response = gemini_result.get("text", "")
                        gemini_notice = gemini_result.get("notice")
                        gemini_model_used = gemini_result.get("model_used")
                        gemini_attempts = gemini_result.get("attempts")
                    else:
                        gemini_response = gemini_result
                        gemini_notice = None
                        gemini_model_used = None
                        gemini_attempts = None

                    st.success("✅ Response from Gemini")
                    st.markdown(gemini_response)

                    if gemini_notice:
                        st.info(gemini_notice)
                    if gemini_model_used:
                        st.caption(f"Gemini model: {gemini_model_used}")
                    if show_debug and gemini_attempts:
                        st.markdown("**Debug — Gemini attempts**")
                        st.write(gemini_attempts)

                    try:
                        with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                            _dbg.write(
                                f"GEMINI_RESPONSE: model={gemini_model_used}, notice={gemini_notice}, attempts={gemini_attempts}, text={gemini_response}\n"
                            )
                    except Exception:
                        pass

                except Exception as e:
                    st.error(f"❌ Gemini API error: {str(e)}")
                    st.info("Please verify your API key and internet connection, then try again.")
                    st.caption("Troubleshooting: set GEMINI_API_KEY in .env, pin GEMINI_MODEL=gemini-1.5-flash, and restart Streamlit after edits.")
                    try:
                        with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                            _dbg.write(f"GEMINI_ERROR: {str(e)}\n")
                    except Exception:
                        pass

# Display input summary at the bottom
st.subheader("📋 Input Summary")
summary_data = {
    'Parameter': ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall', 'Soil Moisture', 'Wind Speed', 'Pressure'],
    'Value': [f"{N}", f"{P}", f"{K}", f"{temp}°C", f"{hum}%", f"{ph}", f"{rain}mm", f"{soil_moisture}%", f"{wind_speed}km/h", f"{pressure}kPa"],
    'Status': ['✅' if val > 0 else '⚠️' for val in [N, P, K, temp, hum, ph, rain, soil_moisture, wind_speed, pressure]]
}

summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df, hide_index=True, width="stretch")

# Footer
st.markdown("---")
st.markdown("**AgriTech - Smart Agriculture Advisor** - Empowering farmers with AI-driven crop and irrigation insights")
st.markdown("💡 *Tip: Adjust the input parameters to see how they affect the recommendations*")
