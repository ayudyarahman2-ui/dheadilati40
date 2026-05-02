import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# CONFIG
st.set_page_config(page_title="Frozen Mart", layout="wide")

# LOAD CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown(f"""
<div class="topbar">
    <div><b>❄️ FROZEN MART</b><br><small>Smart Freezer • Digital Price Tag</small></div>
    <div>🌡️ -18.6°C | ⏰ {datetime.now().strftime("%H:%M:%S")} | 👤 Admin</div>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.title("❄️ Frozen Mart")
    menu = st.radio("Menu", ["Dashboard", "Produk", "Monitoring"])

# ================= DATA =================
data = [
    {"nama": "Wall's Vanilla", "harga": 15000, "stok": 25},
    {"nama": "Frozen Chicken", "harga": 35000, "stok": 18},
    {"nama": "Sosis Premium", "harga": 28000, "stok": 30},
    {"nama": "Ikan Dori", "harga": 32000, "stok": 20},
]
df = pd.DataFrame(data)

# ================= DASHBOARD =================
if menu == "Dashboard":

    st.subheader("📊 Dashboard Admin")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Suhu Freezer", "-18.6 °C")
    col2.metric("Total Produk", len(df))
    col3.metric("Produk Promo", 2)
    col4.metric("Total Stok", df["stok"].sum())

    # Grafik suhu
    x = list(range(10))
    y = [-18, -20, -19, -21, -18, -22, -20, -19, -18, -17]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers'))

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

# ================= PRODUK =================
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

# ================= MONITORING =================
elif menu == "Monitoring":

    st.subheader("🌡️ Monitoring Suhu")

    suhu = -18.6
    st.metric("Suhu Saat Ini", f"{suhu} °C")

    st.success("Sistem Normal ✅")

# ================= FOOTER =================
st.markdown("""
<hr>
<center>© 2025 Frozen Mart</center>
""", unsafe_allow_html=True)
