import streamlit as st
import requests
import pandas as pd
import time
import difflib
st.set_page_config(page_title="MedSync", page_icon="💊", layout="wide")
st.markdown("""
    <style>
    /* Full background gradient */
    body, .stApp {
        background: linear-gradient(135deg, #d1f2eb, #d6eaf8);
        background-attachment: fixed;
    }
    </style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* 📘 Gradient Background */
body, .stApp {
    background: linear-gradient(to bottom right, #d1f2eb, #d6eaf8);
    background-attachment: fixed;
}

/* 🧠 Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #eaf6f6;
    border-right: 1px solid #d4e6f1;
}
.css-1n76uvr {
    color: #1b4f72;
}

/* 🎛️ Sliders */
.css-1c7y2kd {
    color: #1b4f72 !important;
}
.stSlider > div > div {
    background: #3498db !important;
}

/* 📦 Metric Cards */
.stMetric {
    background-color: #fefefe;
    border: 1px solid #d6eaf8;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* 📋 Table Header */
thead tr th {
    background-color: #d6eaf8 !important;
    color: #154360 !important;
    font-weight: 600;
}

/* 🔘 Buttons */
button[kind="primary"] {
    background-color: #3498db !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease;
}
button[kind="primary"]:hover {
    background-color: #2c80b4 !important;
    box-shadow: 0 0 10px rgba(52,152,219,0.4);
}

/* 🗨️ Chat input & message cards */
.stChatInputContainer {
    background: #eaf2f8;
    border-top: 1px solid #d4e6f1;
}
.stChatMessage {
    background-color: #fefefe;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* Reset slider track to match sidebar background */
.stSlider > div[data-baseweb="slider"] {
    background: transparent !important;
}

.stSlider > div > div {
    background-color: #eaf6f6 !important;  /* Soft pastel blue track */
    border-radius: 8px !important;
    height: 6px !important;
}

/* Slider thumb */
.stSlider .css-1ldz3zw {
    background-color: #e74c3c !important;  /* Keeps it visible */
    border: 2px solid white;
    box-shadow: 0px 0px 4px rgba(0,0,0,0.15);
}

/* Label and value colors */
.stSlider span {
    color: #154360 !important;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)
# --------- PRELOADER (5 sec with pill animation) ---------
loader = st.empty()
loader.markdown("""
    <style>
    .pill-loader {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #e74c3c 50%, #3498db 50%);
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        animation: pulse 1.4s infinite ease-in-out;
        position: relative;
    }

    .pill-text {
        font-family: 'Segoe UI';
        font-size: 22px;
        color: #2c3e50;
        margin-top: 20px;
        animation: fadeIn 2s infinite alternate;
        text-align: center;
    }

    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.9; }
        50% { transform: scale(1.2); opacity: 0.4; }
        100% { transform: scale(1); opacity: 0.9; }
    }

    @keyframes fadeIn {
        0% { opacity: 0.2; }
        100% { opacity: 1; }
    }
    </style>

    <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh;'>
        <div class="pill-loader"></div>
        <div class="pill-text">Loading MedSync...</div>
    </div>
""", unsafe_allow_html=True)

time.sleep(3)
loader.empty()


#style
st.markdown("""
<style>
/* Fade-in sections */
.fade-in {
  animation: fadeIn 0.9s ease-in-out;
}

/* Hover Glow Button */
.nav-button:hover {
  box-shadow: 0 0 12px #3498db;
  transform: scale(1.03);
}

/* Metrics Hover Zoom */
.metric-card {
  transition: transform 0.3s ease;
}
.metric-card:hover {
  transform: scale(1.07);
}

/* Alert Animation */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
.critical-alert {
  animation: bounce 0.6s infinite;
  color: #e74c3c;
  font-weight: bold;
}

/* Section fadeIn */
@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}

/* Rounded cards */
.rounded-box {
  background: rgba(255,255,255,0.1);
  padding: 15px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

#dashboard
st.markdown("""
    <h1 id="dashboard" style='text-align:center; font-size:48px; margin-bottom:10px;'>
        💊 <span style='color:#e74c3c;'>Med</span><span style='color:#2980b9;'>Sync</span>
    </h1>
    <p style='text-align:center; font-size:18px; margin-top:0px;'>Your AI-powered Medicine Demand Dashboard</p>
""", unsafe_allow_html=True)

#fetch preddata
try:
    response = requests.get("http://127.0.0.1:5000/predict")
    data = response.json()
    predictions = data['predictions']
except:
    st.error("⚠️ Backend not reachable. Start your Flask API first.")
    st.stop()

df = pd.read_csv("../backend/data/data.csv")
df['Predicted_Daily_Usage'] = predictions

#sidebar
st.sidebar.markdown("## 🛠️ Filters")
low_stock_threshold = st.sidebar.slider("📉 Low Stock Threshold", 5, 50, 30)
expiry_threshold = st.sidebar.slider("⌛ Expiry Warning Threshold", 15, 180, 60)

df['Status'] = '✅ Normal'
df.loc[df['Current_Stock'] < low_stock_threshold, 'Status'] = '⚠️ Low Stock'
df.loc[df['Days_Until_Expiry'] < expiry_threshold, 'Status'] = '⌛ Expiring Soon'
df.loc[(df['Current_Stock'] < low_stock_threshold) & (df['Days_Until_Expiry'] < expiry_threshold), 'Status'] = '🔥 Critical'

view_option = st.sidebar.radio("🔍 View Options", ["All", "Low Stock", "Expiring Soon", "Critical Only"])
if view_option == "Low Stock":
    filtered_df = df[df['Status'].str.contains("Low Stock|Critical")]
elif view_option == "Expiring Soon":
    filtered_df = df[df['Status'].str.contains("Expiring Soon|Critical")]
elif view_option == "Critical Only":
    filtered_df = df[df['Status'] == "🔥 Critical"]
else:
    filtered_df = df

#search
st.markdown("### 🔍 Search Medicine")

medicine_options = sorted(df["Medicine_Name"].unique())
selected_search = st.selectbox(
    "Start typing or pick from dropdown 👇",
    options=["All"] + medicine_options,
    index=0
)

if selected_search != "All":
    filtered_df = filtered_df[filtered_df["Medicine_Name"].str.contains(selected_search, case=False)]

# stats
st.markdown("### 📊 Inventory Summary")
col1, col2, col3 = st.columns(3)
col1.metric("🔥 Critical", df[df['Status'] == '🔥 Critical'].shape[0])
col2.metric("⚠️ Low Stock", df[df['Status'] == '⚠️ Low Stock'].shape[0])
col3.metric("⌛ Expiring Soon", df[df['Status'] == '⌛ Expiring Soon'].shape[0])

st.markdown("### 📋 Current Stats of Common Medicines")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

st.markdown("<h3 id='stats'>📈 Predicted Daily Usage</h3>", unsafe_allow_html=True)
st.bar_chart(filtered_df.set_index('Medicine_Name')['Predicted_Daily_Usage'])

#fileupload
st.markdown("---")
st.markdown("<h3 id='upload'>📤 Upload Your Own Inventory</h3>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    user_data = pd.read_csv(uploaded_file)
    try:
        payload = {
            "current_stock": user_data["Current_Stock"].tolist(),
            "expiry": user_data["Days_Until_Expiry"].tolist()
        }
        response = requests.post("http://127.0.0.1:5000/predict_batch", json=payload)
        preds = response.json()["predictions"]
        user_data["Predicted_Daily_Usage"] = preds
        st.success("✅ Prediction Successful!")
        st.dataframe(user_data)
        st.bar_chart(user_data.set_index("Medicine_Name")["Predicted_Daily_Usage"])
    except:
        st.error("❌ Uploaded CSV must have columns: 'Medicine_Name', 'Current_Stock', 'Days_Until_Expiry'")

st.markdown("---")
st.markdown("<h3 id='manual'>🧪 Try Manual Entry</h3>", unsafe_allow_html=True)

medicine_name = st.text_input("💊 Medicine Name", placeholder="e.g., Paracetamol")
col1, col2 = st.columns(2)
stock_input = col1.number_input("📦 Current Stock", 1, 1000, 50)
expiry_input = col2.number_input("⏳ Days Until Expiry", 1, 365, 90)

if st.button("🔮 Predict Usage"):
    if not medicine_name:
        st.warning("⚠️ Please enter a medicine name.")
    else:
        payload = {"stock": stock_input, "expiry": expiry_input}
        res = requests.post("http://127.0.0.1:5000/predict_single", json=payload)
        pred = res.json()["prediction"]
        st.success(f"📈 **{medicine_name}** — Predicted Daily Usage: **{round(pred, 2)} units/day**")

#chatbot

st.markdown("---")
st.subheader("💬 MedSync Assistant (in beta)")

faq_df = pd.read_csv("faq.csv")

st.chat_message("assistant").write("Hi! I'm your MedSync Assistant 🤖. Ask me anything about this dashboard.")

query = st.chat_input("Ask a question...")

if query:
    st.chat_message("user").write(query)

    # match faq.csv
    match = difflib.get_close_matches(query.lower(), faq_df['question'].str.lower(), n=1, cutoff=0.4)

    if match:
        answer = faq_df.loc[faq_df['question'].str.lower() == match[0], 'answer'].values[0]
    else:
        answer = "🤖 Sorry, I couldn’t find a good answer. Try rephrasing your question."

    st.chat_message("assistant").write(answer)
