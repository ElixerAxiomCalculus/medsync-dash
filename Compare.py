import streamlit as st
import pandas as pd
import altair as alt
import time
st.set_page_config(page_title="🆚 Compare Medicines", layout="wide")
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



st.title("🆚 Compare Two Medicines Side-by-Side")

@st.cache_data
def load_data():
    return pd.read_csv("../backend/data/data.csv")

df = load_data()
medicine_list = sorted(df["Medicine_Name"].unique())

# --- Dropdowns to Select Medicines ---
col1, col2 = st.columns(2)
with col1:
    med1 = st.selectbox("Select Medicine 1", medicine_list, key="med1")
with col2:
    med2 = st.selectbox("Select Medicine 2", medicine_list, key="med2")

df1 = df[df["Medicine_Name"] == med1]
df2 = df[df["Medicine_Name"] == med2]

if df1.empty or df2.empty:
    st.warning("⚠️ One of the selected medicines has no data.")
    st.stop()

st.markdown("### 📊 Key Stats Comparison")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"#### 📌 {med1}")
    st.metric("📦 Avg. Stock", f"{df1['Current_Stock'].mean():.2f}")
    st.metric("📈 Avg. Predicted Usage", f"{df1['Average_Daily_Usage'].mean():.2f}")
    st.metric("⏳ Avg. Expiry Days", f"{df1['Days_Until_Expiry'].mean():.2f}")

with col2:
    st.markdown(f"#### 📌 {med2}")
    st.metric("📦 Avg. Stock", f"{df2['Current_Stock'].mean():.2f}")
    st.metric("📈 Avg. Predicted Usage", f"{df2['Average_Daily_Usage'].mean():.2f}")
    st.metric("⏳ Avg. Expiry Days", f"{df2['Days_Until_Expiry'].mean():.2f}")

st.markdown("### 📊 Distribution Charts")

b1, b2 = st.columns(2)
with b1:
    st.altair_chart(
        alt.Chart(df1).mark_bar().encode(
            x=alt.X("Average_Daily_Usage", bin=True),
            y='count()'
        ).properties(title=f"{med1} - Daily Usage Distribution"),
        use_container_width=True
    )
with b2:
    st.altair_chart(
        alt.Chart(df2).mark_bar().encode(
            x=alt.X("Average_Daily_Usage", bin=True),
            y='count()'
        ).properties(title=f"{med2} - Daily Usage Distribution"),
        use_container_width=True
    )

st.markdown("### 📈 Daily Usage Line Chart Comparison")

df1 = df1.reset_index(drop=True)
df2 = df2.reset_index(drop=True)
df1["Index"] = df1.index
df2["Index"] = df2.index

df1["Medicine"] = med1
df2["Medicine"] = med2
combined_df = pd.concat([df1, df2])

line = alt.Chart(combined_df).mark_line(point=True).encode(
    x='Index',
    y='Average_Daily_Usage',
    color='Medicine',
    tooltip=['Medicine', 'Average_Daily_Usage', 'Current_Stock', 'Days_Until_Expiry']
).properties(title="Predicted Daily Usage Trend")

st.altair_chart(line, use_container_width=True)

