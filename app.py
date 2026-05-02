import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")

# LOAD CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="topbar">
    <div class="logo">❄️ FROZEN MART</div>
    <div class="info">
        🌡️ -18.6°C | ⏰ 10:30:45 | 👤 Admin
    </div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
st.markdown("""
<div class="sidebar">
    <h2>❄️ Frozen Mart</h2>
    <ul>
        <li>🏠 Dashboard</li>
        <li>📦 Produk</li>
        <li>🌡️ Monitoring</li>
        <li>⚙️ Pengaturan</li>
        <li>🚪 Logout</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# PRODUK
st.markdown("<h3>DAFTAR PRODUK</h3>", unsafe_allow_html=True)

cols = st.columns(4)
products = [
    ("Wall's Vanilla", "Rp 15.000", "25"),
    ("Frozen Chicken", "Rp 35.000", "18"),
    ("Sosis Premium", "Rp 28.000", "30"),
    ("Ikan Dori", "Rp 32.000", "20"),
]

for i, (name, price, stock) in enumerate(products):
    with cols[i]:
        st.markdown(f"""
        <div class="card">
            <h4>{name}</h4>
            <h2>{price}</h2>
            <p>Stok: {stock}</p>
        </div>
        """, unsafe_allow_html=True)

# DASHBOARD
st.markdown("<h3>DASHBOARD ADMIN</h3>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

c1.markdown('<div class="metric">🌡️<br>-18.6°C</div>', unsafe_allow_html=True)
c2.markdown('<div class="metric">📦<br>4 Produk</div>', unsafe_allow_html=True)
c3.markdown('<div class="metric">🔥<br>2 Promo</div>', unsafe_allow_html=True)
c4.markdown('<div class="metric">📊<br>93 Unit</div>', unsafe_allow_html=True)

# GRAFIK
x = list(range(10))
y = [-18, -20, -19, -21, -18, -22, -20, -19, -18, -17]

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers'))

fig.update_layout(
    template="plotly_white",
    margin=dict(l=0, r=0, t=30, b=0),
    height=300
)

st.plotly_chart(fig, use_container_width=True)
