import streamlit as st
import pandas as pd
import random

# ---------- CONFIG ----------
st.set_page_config(layout="wide")

# ---------- THEME TOGGLE ----------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

mode = st.sidebar.toggle("🌙 Dark Mode", value=True)
st.session_state.theme = "dark" if mode else "light"

# ---------- THEME SET ----------
theme = st.session_state.theme

if theme == "dark":
    bg = "#0f172a"
    card = "#1e293b"
    text = "white"
else:
    bg = "#f8fafc"
    card = "white"
    text = "black"

# ---------- STYLE ----------
st.markdown(f"""
<style>

/* BACKGROUND */
.stApp {{
    background: {bg};
    color: {text};
}}

/* CARD */
.card {{
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 20px;
    transition: 0.3s;
}}

.card:hover {{
    transform: translateY(-5px);
}}

/* PRICE */
.price {{
    font-size: 18px;
    font-weight: bold;
    color: #38bdf8;
}}

.promo {{
    color: #22c55e;
    font-size: 20px;
    font-weight: bold;
}}

.old-price {{
    text-decoration: line-through;
    color: gray;
}}

/* TEXT */
h1,h2,h3,p,label {{
    color: {text};
}}

/* BUTTON */
.stButton>button {{
    background-color: #22c55e;
    color: white;
    border-radius: 10px;
    border: none;
}}

</style>
""", unsafe_allow_html=True)
# ---------- DATA ----------
if "produk_data" not in st.session_state or "Gambar" not in st.session_state.produk_data.columns:
    st.session_state.produk_data = pd.DataFrame({
        "Nama": [
            "Nugget Fiesta", "Sosis So Nice", "Dimsum Ayam",
            "Kentang Goreng", "Bakso Frozen"
        ],
        "Harga": [25000, 18000, 22000, 15000, 20000],
        "Promo": [20000, None, None, 12000, None],
        "Gambar": [
            "https://via.placeholder.com/150",
            "https://via.placeholder.com/150",
            "https://via.placeholder.com/150",
            "https://via.placeholder.com/150",
            "https://via.placeholder.com/150"
        ]
    })

# ---------- AUTH ----------
USER_CREDENTIALS = {"admin": "12345"}

if "login" not in st.session_state:
    st.session_state.login = False

if "page" not in st.session_state:
    st.session_state.page = "konsumen"

# ---------- SIMULASI SUHU ----------
def read_temperature():
    return round(random.uniform(-25, -5), 2)

# ---------- LOGIN ----------
def login_page():
    st.markdown("<h2 style='text-align:center;'>🔐 Login Admin</h2>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.login = True
            st.session_state.page = "admin"
        else:
            st.error("Salah login")

    if st.button("Kembali"):
        st.session_state.page = "konsumen"

# ---------- ADMIN ----------
def admin_dashboard():
    df = st.session_state.produk_data

    st.sidebar.title("Menu Admin")
    menu = st.sidebar.radio("Menu", ["Dashboard", "Monitoring Suhu", "Manajemen Harga"])

    st.title("Admin Dashboard")

    # DASHBOARD
    if menu == "Dashboard":
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Produk", len(df))
        col2.metric("Promo Aktif", df['Promo'].count())
        col3.metric("Rata-rata Harga", int(df["Harga"].mean()))

        st.subheader("📈 Grafik Harga Produk")
        st.bar_chart(df.set_index("Nama")["Harga"])

    # MONITORING
    elif menu == "Monitoring Suhu":
        temps = [read_temperature() for _ in range(10)]

        st.metric("Suhu Terakhir", f"{temps[-1]} °C")
        st.line_chart(temps)

        if temps[-1] > -10:
            st.error("⚠️ Suhu terlalu tinggi!")
        else:
            st.success("✅ Suhu normal")

    # MANAJEMEN
    elif menu == "Manajemen Harga":
        produk = st.selectbox("Pilih Produk", df["Nama"])
        idx = df[df["Nama"] == produk].index[0]

        harga = st.number_input("Harga", value=int(df.loc[idx, "Harga"]))
        promo = st.number_input("Promo (0 jika tidak ada)", value=int(df.loc[idx, "Promo"] or 0))

        if st.button("Simpan"):
            df.loc[idx, "Harga"] = harga
            df.loc[idx, "Promo"] = promo if promo != 0 else None
            st.success("Update berhasil")

        st.subheader("Preview Data")
        st.dataframe(df)

    if st.sidebar.button("Logout"):
        st.session_state.login = False
        st.session_state.page = "konsumen"

# ---------- KONSUMEN ----------
def customer_display():
    temp = read_temperature()
    df = st.session_state.produk_data

    # HEADER
    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/869/869869.png", width=60)

    with col2:
        st.markdown("<h2 style='text-align:center;'>❄️ REDBOX FROZEN SOGIRI</h2>", unsafe_allow_html=True)

    with col3:
        if st.button("Admin"):
            st.session_state.page = "login"

    st.markdown(f"<div style='text-align:right;'>🌡️ {temp} °C</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("<h2 style='text-align:center;'>🛒 Produk Kami</h2>", unsafe_allow_html=True)

    cols = st.columns(4)

    for i, row in df.iterrows():
        with cols[i % 4]:
            if pd.notna(row["Promo"]):
                st.markdown(f"""
                <div class="card">
                    <img src="{row['Gambar']}" width="100%">
                    <h4>{row['Nama']}</h4>
                    <p class="old-price">Rp {row['Harga']:,}</p>
                    <p class="promo">Rp {int(row['Promo']):,}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="card">
                    <img src="{row['Gambar']}" width="100%">
                    <h4>{row['Nama']}</h4>
                    <p class="price">Rp {row['Harga']:,}</p>
                </div>
                """, unsafe_allow_html=True)

# ---------- MAIN ----------
if st.session_state.page == "konsumen":
    customer_display()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "admin":
    if st.session_state.login:
        admin_dashboard()
    else:
        st.session_state.page = "login"
        login_page()
