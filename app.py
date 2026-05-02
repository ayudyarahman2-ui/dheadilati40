import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

st.set_page_config(layout="wide")

# ================= DATABASE =================
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    harga INTEGER,
    stok INTEGER
)
""")
conn.commit()

# ================= CSS =================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #f4f7fb;
}
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
    box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
}
.metric-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(#0b1c3f, #123c8c);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login Admin")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pw == "123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Login salah ❌")

    st.stop()

# ================= HEADER =================
st.markdown(f"""
<div class="topbar">
<b>❄️ FROZEN MART</b>
<div>🌡️ -18.6°C | ⏰ {datetime.now().strftime("%H:%M:%S")} | 👤 Admin</div>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    menu = st.radio("Menu", ["Dashboard", "Produk", "Tambah Produk", "Monitoring"])
    if st.button("Logout"):
        st.session_state.login = False
        st.rerun()

# ================= DASHBOARD =================
if menu == "Dashboard":

    df = pd.read_sql("SELECT * FROM produk", conn)

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown('<div class="metric-box">🌡️<br>-18.6°C</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-box">📦<br>{len(df)} Produk</div>', unsafe_allow_html=True)
    c3.markdown('<div class="metric-box">🔥<br>2 Promo</div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-box">📊<br>{df["stok"].sum() if not df.empty else 0} Unit</div>', unsafe_allow_html=True)

    st.line_chart([-18, -20, -19, -21, -18, -22, -20])

# ================= PRODUK =================
elif menu == "Produk":

    df = pd.read_sql("SELECT * FROM produk", conn)

    st.subheader("Daftar Produk")

    if df.empty:
        st.warning("Belum ada produk")
    else:
        for i, row in df.iterrows():
            col1, col2 = st.columns([4,1])

            with col1:
                st.markdown(f"""
                <div class="card">
                    <h4>{row['nama']}</h4>
                    <h2>Rp {row['harga']:,}</h2>
                    <p>Stok: {row['stok']}</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if st.button(f"Hapus {row['id']}"):
                    c.execute("DELETE FROM produk WHERE id = ?", (row['id'],))
                    conn.commit()
                    st.success("Produk dihapus ✅")
                    st.rerun()

# ================= TAMBAH PRODUK =================
elif menu == "Tambah Produk":

    st.subheader("Tambah Produk")

    nama = st.text_input("Nama Produk")
    harga = st.number_input("Harga", min_value=0)
    stok = st.number_input("Stok", min_value=0)

    if st.button("Simpan"):
        c.execute("INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)", (nama, harga, stok))
        conn.commit()
        st.success("Produk berhasil ditambahkan ✅")

# ================= MONITORING =================
elif menu == "Monitoring":

    st.subheader("Monitoring Suhu")
    st.metric("Suhu", "-18.6 °C")
    st.success("Normal ✅")
