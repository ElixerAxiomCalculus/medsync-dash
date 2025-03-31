import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import time
st.set_page_config(page_title="📊 Insights", layout="wide")

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



st.title("📊 Advanced Data Insights")

@st.cache_data
def load_data():
    return pd.read_csv("../backend/data/data.csv")

df = load_data()

#heatmap
st.subheader("🔗 Correlation Heatmap")

numeric_cols = ["Current_Stock", "Days_Until_Expiry", "Average_Daily_Usage"]
corr = df[numeric_cols].corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)


st.subheader("📉 Trendline: Usage vs Days Until Expiry")

chart = alt.Chart(df).mark_circle(size=60).encode(
    x='Days_Until_Expiry',
    y='Average_Daily_Usage',
    tooltip=["Medicine_Name", "Current_Stock"]
).interactive()

regression = alt.Chart(df).transform_regression(
    "Days_Until_Expiry", "Average_Daily_Usage"
).mark_line(color='red')

st.altair_chart(chart + regression, use_container_width=True)

#smart alert
st.subheader("📌 Smart Alerts")


low_stock_threshold = 30
expiry_threshold = 60

df['Status'] = '✅ Normal'
df.loc[df['Current_Stock'] < low_stock_threshold, 'Status'] = '⚠️ Low Stock'
df.loc[df['Days_Until_Expiry'] < expiry_threshold, 'Status'] = '⌛ Expiring Soon'
df.loc[(df['Current_Stock'] < low_stock_threshold) & 
       (df['Days_Until_Expiry'] < expiry_threshold), 'Status'] = '🔥 Critical'


critical_count = len(df[df['Status'] == "🔥 Critical"])
low_stock_count = len(df[df['Status'].str.contains("Low Stock")])
expiring_count = len(df[df['Status'].str.contains("Expiring Soon")])


st.markdown(f"""
- 🔥 **Critical entries**: `{critical_count}` ⚠️  
- 📦 **Low stock medicines**: `{low_stock_count}`  
- ⌛ **Expiring soon**: `{expiring_count}`
""")

if critical_count > 0.15 * len(df):
    st.error("🚨 More than 15% of inventory is in CRITICAL condition!")
elif low_stock_count > 0.3 * len(df):
    st.warning("⚠️ Over 30% of medicines are low on stock.")
else:
    st.success("✅ Inventory health looks good overall.")
