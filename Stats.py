import streamlit as st
import pandas as pd
import altair as alt
import time
import difflib
st.set_page_config(page_title="📊 Medicine Stats", layout="wide")
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



st.title("🔍 Medicine-Wise Statistics")

@st.cache_data
def load_data():
    return pd.read_csv("../backend/data/data.csv")

df = load_data()
medicine_list = sorted(df["Medicine_Name"].unique())

# Search box
search_medicine = st.selectbox("Select a medicine to view detailed stats", medicine_list)

filtered_df = df[df["Medicine_Name"] == search_medicine]

if not filtered_df.empty:
    st.markdown(f"### 📌 Statistics for: **{search_medicine}** ({len(filtered_df)} entries)")

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Avg. Stock", f"{filtered_df['Current_Stock'].mean():.2f}")
    col2.metric("📈 Avg. Predicted Usage", f"{filtered_df['Average_Daily_Usage'].mean():.2f}")
    col3.metric("⏳ Avg. Days Until Expiry", f"{filtered_df['Days_Until_Expiry'].mean():.2f}")

    st.markdown("### 📊 Visualizations")

    tab1, tab2, tab3 = st.tabs(["Usage Distribution", "Stock vs Expiry", "Boxplots"])

    with tab1:
        chart = alt.Chart(filtered_df).mark_bar().encode(
            x=alt.X("Average_Daily_Usage", bin=True),
            y='count()',
            tooltip=["Average_Daily_Usage", "count()"]
        ).properties(title="Distribution of Daily Usage")
        st.altair_chart(chart, use_container_width=True)

    with tab2:
        scatter = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='Days_Until_Expiry',
            y='Current_Stock',
            color='Average_Daily_Usage',
            tooltip=['Current_Stock', 'Days_Until_Expiry', 'Average_Daily_Usage']
        ).interactive().properties(title="Stock vs Expiry Days")
        st.altair_chart(scatter, use_container_width=True)

    with tab3:
        st.write("📦 Stock vs Usage Boxplot")
        st.box_chart = st.box_chart = alt.Chart(filtered_df).mark_boxplot().encode(
            y='Average_Daily_Usage',
            tooltip=['Medicine_Name', 'Current_Stock']
        ).properties(title="Daily Usage Spread")
        st.altair_chart(st.box_chart, use_container_width=True)
else:
    st.warning("⚠️ No entries found for this medicine.")



