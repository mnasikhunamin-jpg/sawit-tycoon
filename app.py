import streamlit as st
import random

st.set_page_config(page_title="Sawit Tycoon 3D Pro", page_icon="🌴", layout="centered")

# CSS Kustom Styling Box Neon agar Dashboard rapi dan teks tidak terpotong
st.markdown("""
<style>
    .metric-box {
        background-color: #111827;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #1f2937;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .status-val {
        font-size: 18px;
        font-weight: bold;
        color: #34d399;
    }
    h1, h2, h3 {
        color: #10b981 !important;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
""", unsafe_allow_html=True)

# --- SISTEM LOGIN SIMULASI ---
if "user_logged_in" not in st.session_state:
    st.title("🚜 SAWIT TYCOON 3D SIMULATOR")
    st.write("Selamat Datang! Masukkan nama Anda untuk mengklaim aset perkebunan.")
    nama_pemain = st.text_input("Nama Pemilik / Direktur:", placeholder="Contoh: Nasikhun")
    
    if st.button("Masuk Lahan 🚀", type="primary"):
        if nama_pemain.strip() != "":
            st.session_state["user_logged_in"] = nama_pemain
            st.rerun()
        else:
            st.error("Nama wajib diisi!")
    st.stop()

nama_user = st.session_state["user_logged_in"]

# --- DATABASE STATE GAME ---
if "db" not in st.session_state:
    st.session_state.db = {
        "dana": 60000000,
        "lahan_hektar": 1,
        "kecambah_ppks": 0,
        "polibag_isi": 0,
        "populasi_pohon": 0,
        "umur_bulan": 0,
        "kesehatan_tanaman": 100,
        "kebersihan_gulma": 100,
        "harga_tbs_hari_ini": 2500,
        "hama_aktif": False,
        "id_pemain": random.randint(1000, 9999),
        "logs": [f"Sesi dimulai. Sukses untuk perkebunan {nama_user}!"]
    }

db = st.session_state.db

# --- FLUKTUASI HARGA & HAMA ---
def update_kondisi_pasar():
    perubahan_harga = random.randint(-300, 300)
    db["harga_tbs_hari_ini"] = max(1800, min(3500, db["harga_tbs_hari_ini"] + perubahan_harga))
    
    if db["populasi_pohon"] > 0 and not db["hama_aktif"] and random.random() < 0.15:
        db["kesehatan_tanaman"] = max(20, db["kesehatan_tanaman"] - 40)
        db["hama_aktif"] = True
        db["logs"].append("⚠️ KRITIS: Kebun diserang Hama Ulat Api! Kesehatan tanaman drop.")

update_kondisi_pasar()

# --- HEADER GAME ---
st.title("🌴 SAWIT TYCOON 3D")
st.caption(f"Direktur Utama: **{nama_user}** | ID: SAWIT-{db['id_pemain']}")

# ==============================================================================
# 🧊 ENGINES VISUALISASI MODEL 3D DINAMIS (LOW-POLY RENDER)
# ==============================================================================
st.header("🧱 Live 3D View Lapangan")

# Mengganti visualisasi gambar biasa dengan 3D Model Render berlatar studio game
if db["umur_bulan"] == 0:
    # Aset 3D Kecambah di Rak Laboratorium Gudang PPKS
    img_3d = "https://turbosquid.com" 
    caption_3d = "📦 MODEL 3D: Status Gudang - Kecambah Unggul PPKS Siap Produksi"
elif db["umur_bulan"] < 12:
    # Aset 3D Bibit Kecil Polibag Low Poly (Fase TBM Awal)
    img_3d = "https://cgtrader.com"
    caption_3d = "🌱 MODEL 3D: Fase Pembibitan Polibag Pre-Nursery (1-12 Bulan)"
elif db["umur_bulan"] < 48:
    # Aset 3D Pohon Kelapa Sawit Muda (Low Poly Game Asset)
    img_3d = "https://shapespark.com" # Fallback rendering studio
    # Menggunakan aset cadangan terverifikasi jika tautan rendering eksternal bermasalah
    img_3d = "https://cgtrader.com"
    caption_3d = "🌴 MODEL 3D: Vegetatif Lapangan - Fase Belum Menghasilkan (12-47 Bulan)"
else:
    # Aset 3D Pohon Kelapa Sawit Dewasa Lebat Siap Panen (High Production Render)
    img_3d = "https://cgtrader.com"
    caption_3d = "👑 MODEL 3D: Fase Menghasilkan (TM) - Perkebunan Siap Panen Raya!"

st.image(img_3d, caption=caption_img if 'caption_img' in locals() else caption_3d, use_container_width=True)
# ==============================================================================

# --- SIDEBAR ADS ---
st.sidebar.markdown("### 📢 SPONSOR RESMI")
st.sidebar.info("**🌱 TOKO TANI UTAMA**\nSponsori game ini sekarang!")

# --- DASHBOARD INDIKATOR UTAMA ---
st.header("📈 Dashboard Perkebunan")
st.metric(label="💰 Harga TBS Hari Ini", value=f"Rp {db['harga_tbs_hari_ini']}/Kg")

col_1, col_2, col_3 = st.columns(3)
with col_1:
    st.markdown(f"<div class='metric-box'>💵 <b>Dana Tunai</b><br><span class='status-val'>Rp {db['dana']:,}</span></div>", unsafe_allow_html=True)
with col_2:
    st.markdown(f"<div class='metric-box'>🗺️ <b>Aset Lahan</b><br><span class='status-val'>{db['lahan_hektar']} Hektar</span></div>", unsafe_allow_html=True)
with col_3:
    st.markdown(f"<div class='metric-box'>⏳ <b>Umur Tanaman</b><br><span class='status-val'>{db['umur_bulan']} Bulan</span></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_4, col_5 = st.columns(2)
with col_4:
    st.markdown(f"<div class='metric-box'>❤️ <b>Kesehatan</b><br><span class='status-val' style='color:#10b981;'>{db['kesehatan_tanaman']}%</span></div>", unsafe_allow_html=True)
with col_5:
    st.markdown(f"<div class='metric-box'>🌿 <b>Kebersihan</b><br><span class='status-val' style='color:#3b82f6;'>{db['kebersihan_gulma']}%</span></div>", unsafe_allow_html=True)

# Keluar Game
if st.sidebar.button("Keluar Game 🚪"):
    del st.session_state["user_logged_in"]
    if "db" in st.session_state:
        del st.session_state["db"]
    st.rerun()

# Kebangkrutan
if db["dana"] < 0:
    st.error("🚨 GAME OVER: Modal Anda Habis!")
    if st.button("Mulai Baru 🔄"):
        del st.session_state["db"]
        st.rerun()
    st.stop()

# QRIS
if db["hama_aktif"]:
    st.error("🐛 Kebun terserang wabah Hama Ulat Api!")
    if st.button("🛡️ Pulihkan Instan (Rp 2.000 via QRIS)", type="primary"):
        st.session_state["tampilkan_qris"] = True

    if st.session_state.get("tampilkan_qris", False):
        st.markdown("### 💳 Pembayaran Instan")
        st.info(f"📌 Taruh Pesan: 'SAWIT-{db['id_pemain']}' saat transfer.")
        st.image("https://wikimedia.org", width=230)
        
        if st.button("Klaim Pulih ✅"):
            db["kesehatan_tanaman"] = 100
            db["hama_aktif"] = False
            st.session_state["tampilkan_qris"] = False
            db["logs"].append(f"💸 PREMIUM: Verifikasi ID SAWIT-{db['id_pemain']} Berhasil!")
            st.rerun()

# --- OPERASIONAL ---
st.header("🕹️ Menu Eksekusi Agribisnis")

pembelian_aktif = db["kecambah_ppks"] == 0 and db["polibag_isi"] == 0 and db["populasi_pohon"] == 0
polibag_aktif = db["kecambah_ppks"] > 0
pindah_aktif = db["polibag_isi"] > 0
perawatan_aktif = db["populasi_pohon"] > 0
panen_aktif = db["umur_bulan"] >= 48 and db["populasi_pohon"] > 0

if st.button("1. Beli Kecambah Unggul PPKS", disabled=not pembelian_aktif):
    biaya = 15000 * 150
    if db["dana"] >= biaya:
        db["dana"] -= biaya
        db["kecambah_ppks"] = 150
        db["logs"].append("Membeli kecambah PPKS.")
        st.rerun()

if st.button("2. Isi Polibag & Tanam", disabled=not polibag_aktif):
    biaya = db["kecambah_ppks"] * 6000
    if db["dana"] >= biaya:
        db["dana"] -= biaya
        db["polibag_isi"] = db["kecambah_ppks"]
        db["kecambah_ppks"] = 0
        db["logs"].append("Tanam di Pre-Nursery.")
        st.rerun()

if st.button("3. Pindah ke Lahan Utama (Main Nursery)", disabled=not pindah_aktif):
    db["populasi_pohon"] = 143
    db["polibag_isi"] = 0
    db["umur_bulan"] = 12
    db["logs"].append("Pindah tanam ke lapangan selesai.")
    st.rerun()

col_a1, col_a2 = st.columns(2)
with col_a1:
    if st.button("4. Pupuk Tanaman (+6 Bulan)", disabled=not perawatan_aktif):
        biaya = db["populasi_pohon"] * 0.5 * 15000
        if db["dana"] >= biaya:
            db["dana"] -= biaya
            db["kesehatan_tanaman"] = min(100, db["kesehatan_tanaman"] + 15)
            db["umur_bulan"] += 6
            db["kebersihan_gulma"] = max(10, db["kebersihan_gulma"] - 20)
            db["logs"].append("Aplikasi pupuk kelapa sawit selesai.")
            st.rerun()
with col_a2:
    if st.button("5. Semprot Herbisida Gulma", disabled=not perawatan_aktif):
        biaya = db["lahan_hektar"] * 1200000
        if db["dana"] >= biaya:
            db["dana"] -= biaya
            db["kebersihan_gulma"] = 100
            db["kesehatan_tanaman"] = min(100, db["kesehatan_tanaman"] + 10)
            db["umur_bulan"] += 6
            db["logs"].append("Piringan bersih disemprot herbisida.")
            st.rerun()

if st.button("🔥 6. PANEN PRODUKSI & JUAL TBS (USIA 4 TAHUN)", disabled=not panen_aktif, type="primary"):
    faktor_kesehatan = db["kesehatan_tanaman"] / 100
    tonase = (db["lahan_hektar"] * 2.5) * faktor_kesehatan
    pendapatan = tonase * 1000 * db["harga_tbs_hari_ini"] 
    db["dana"] += pendapatan
    db["logs"].append(f"PANEN RAYA! Profit masuk: +Rp {pendapatan:,.0f}!")
    
    if db["dana"] >= 45000000:
        db["dana"] -= 45000000
        db["lahan_hektar"] += 1
        db["kecambah_ppks"] = 150
        db["umur_bulan"] = 0
        db["populasi_pohon"] = 0
        db["logs"].append("🚀 INVESTASI BALIK: Ekspansi 1 Hektar lahan baru.")
    st.rerun()

st.header("📝 Log Aktivitas")
for log in reversed(db["logs"]):
    st.text(log)
