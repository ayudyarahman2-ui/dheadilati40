import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout="wide")

conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

# LOGIN
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
            st.error("Salah")

    st.stop()

# ADMIN PANEL
st.title("⚙️ Admin Panel")

menu = st.sidebar.radio("Menu", ["Produk", "Tambah Produk"])

if menu == "Produk":
    df = pd.read_sql("SELECT * FROM produk", conn)

    for i, row in df.iterrows():
        col1, col2 = st.columns([4,1])

        with col1:
            st.write(f"{row['nama']} - Rp {row['harga']:,} (Stok: {row['stok']})")

        with col2:
            if st.button("🗑️", key=row['id']):
                c.execute("DELETE FROM produk WHERE id=?", (row['id'],))
                conn.commit()
                st.rerun()

elif menu == "Tambah Produk":
    nama = st.text_input("Nama")
    harga = st.number_input("Harga", min_value=0)
    stok = st.number_input("Stok", min_value=0)

    if st.button("Simpan"):
        c.execute("INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)", (nama, harga, stok))
        conn.commit()
        st.success("Berhasil")
