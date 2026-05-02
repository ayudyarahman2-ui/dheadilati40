import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout="wide")

conn = sqlite3.connect("data.db", check_same_thread=False)

# BUAT TABLE KALAU BELUM ADA
conn.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    harga INTEGER,
    stok INTEGER
)
""")

# CEK URL (ADMIN MODE)
params = st.query_params
mode_admin = params.get("admin") == "1"

# HALAMAN KONSUMEN
st.title("❄️ Frozen Mart")
st.subheader("Daftar Produk")

df = pd.read_sql("SELECT * FROM produk", conn)

if df.empty:
    st.warning("Belum ada produk")
else:
    cols = st.columns(4)
    for i, row in df.iterrows():
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:white;padding:20px;border-radius:15px;text-align:center;">
                <h4>{row['nama']}</h4>
                <h2 style="color:#007bff;">Rp {row['harga']:,}</h2>
                <p>Stok: {row['stok']}</p>
            </div>
            """, unsafe_allow_html=True)

# tombol rahasia admin
if st.button("⚙️"):
    st.query_params["admin"] = "1"
    st.rerun()
