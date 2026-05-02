import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIG
st.set_page_config(page_title="Frozen Mart", layout="wide")

# LOAD CSS
st.markdown("""
<style>
.topbar {
    background: white;
    padding: 15px;
    border-radius: 10px;
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)
# HEADER
st.markdown(f"""
<div class="topbar">
    <div><b>❄️ FROZEN MART</b><br><small>Smart Freezer • Digital Price Tag</small></div>
    <div>🌡️ -18.6°C | ⏰ {datetime.now().strftime("%H:%M:%S")} | 👤 Admin</div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("❄️ Frozen Mart")
    menu = st.radio("Menu", ["Dashboard", "Produk", "Monitoring"])

# DATA
data = [
    {"nama": "Wall's Vanilla", "harga": 15000, "stok": 25},
    {"nama": "Frozen Chicken", "harga": 35000, "stok": 18},
    {"nama": "Sosis Premium", "harga": 28000, "stok": 30},
    {"nama": "Ikan Dori", "harga": 32000, "stok": 20},
]
df = pd.DataFrame(data)

# DASHBOARD
if menu == "Dashboard":

    st.subheader("📊 Dashboard Admin")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Suhu Freezer", "-18.6 °C")
    col2.metric("Total Produk", len(df))
    col3.metric("Produk Promo", 2)
    col4.metric("Total Stok", df["stok"].sum())

    st.subheader("Grafik Suhu")

    suhu_data = pd.DataFrame({
        "Suhu": [-18, -20, -19, -21, -18, -22, -20]
    })

    st.line_chart(suhu_data)

# PRODUK
elif menu == "Produk":

    st.subheader("🛒 Daftar Produk")

    cols = st.columns(4)
    for i, row in df.iterrows():
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <h4>{row['nama']}</h4>
                <h2>Rp {row['harga']:,}</h2>
                <p>Stok: {row['stok']}</p>
            </div>
            """, unsafe_allow_html=True)

# MONITORING
elif menu == "Monitoring":

    st.subheader("🌡️ Monitoring Suhu")

    suhu = -18.6
    st.metric("Suhu Saat Ini", f"{suhu} °C")

    st.success("Sistem Normal ✅")

# FOOTER
st.markdown("""
<hr>
<center>© 2025 Frozen Mart</center>
""", unsafe_allow_html=True)
