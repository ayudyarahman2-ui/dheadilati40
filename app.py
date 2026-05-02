import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(layout="wide")

# ================= DATABASE =================
conn = sqlite3.connect("data.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    harga INTEGER,
    harga_promo INTEGER,
    promo INTEGER,
    stok INTEGER
)
""")
conn.commit()

# ================= MODE =================
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

# ================= KONSUMEN =================
if not st.session_state.admin_mode:

    st.title("❄️ Frozen Mart")
    st.subheader("Daftar Produk")

    df = pd.read_sql("SELECT * FROM produk", conn)

    if df.empty:
        st.warning("Belum ada produk")
    else:
        cols = st.columns(4)

        for i, row in df.iterrows():
            with cols[i % 4]:

                # ===== PROMO LOGIC =====
                if row["promo"] == 1:
                    harga_html = f"""
                    <p style="text-decoration: line-through; color: gray;">
                        Rp {row['harga']:,}
                    </p>
                    <h2 style="color:red;">
                        Rp {row['harga_promo']:,}
                    </h2>
                    <span style="background:red;color:white;padding:4px 8px;border-radius:6px;">
                        PROMO
                    </span>
                    """
                else:
                    harga_html = f"""
                    <h2 style="color:#007bff;">
                        Rp {row['harga']:,}
                    </h2>
                    """

                st.markdown(f"""
                <div style="
                    background:white;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    box-shadow:0 5px 15px rgba(0,0,0,0.1);
                ">
                    <h4>{row['nama']}</h4>
                    {harga_html}
                    <p>Stok: {row['stok']}</p>
                </div>
                """, unsafe_allow_html=True)

    # 🔐 MASUK ADMIN
    st.markdown("### 🔐 Admin Access")
    code = st.text_input("Masukkan kode admin", type="password")

    if code == "admin123":
        st.session_state.admin_mode = True
        st.rerun()

# ================= ADMIN =================
else:

    st.title("⚙️ Admin Panel")

    if st.button("Logout"):
        st.session_state.admin_mode = False
        st.rerun()

    menu = st.sidebar.radio("Menu", ["Produk", "Tambah Produk"])

    # ===== LIHAT + HAPUS =====
    if menu == "Produk":

        df = pd.read_sql("SELECT * FROM produk", conn)

        if df.empty:
            st.warning("Belum ada produk")
        else:
            for i, row in df.iterrows():
                col1, col2 = st.columns([4,1])

                with col1:
                    st.write(f"{row['nama']} - Rp {row['harga']:,} | Stok: {row['stok']}")

                with col2:
                    if st.button("🗑️", key=row['id']):
                        c.execute("DELETE FROM produk WHERE id=?", (row['id'],))
                        conn.commit()
                        st.rerun()

    # ===== TAMBAH PRODUK =====
    elif menu == "Tambah Produk":

        st.subheader("Tambah Produk")

        nama = st.text_input("Nama Produk")
        harga = st.number_input("Harga Asli", min_value=0)

        promo = st.checkbox("Produk Promo?")

        if promo:
            harga_promo = st.number_input("Harga Promo", min_value=0)
        else:
            harga_promo = 0

        stok = st.number_input("Stok", min_value=0)

        if st.button("Simpan"):
            try:
                c.execute(
                    "INSERT INTO produk (nama, harga, harga_promo, promo, stok) VALUES (?, ?, ?, ?, ?)",
                    (nama, harga, harga_promo, int(promo), stok)
                )
                conn.commit()
                st.success("Produk berhasil ditambahkan ✅")
            except Exception as e:
                st.error(f"Error: {e}")
