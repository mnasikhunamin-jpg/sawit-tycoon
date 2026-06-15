import streamlit as st
from streamlit_oauth import OAuth2Component
import random

# --- GOOGLE OAUTH CONFIGURATION ---
CLIENT_ID = "MASUKKAN_CLIENT_ID_ANDA_://googleusercontent.com"
CLIENT_SECRET = "GOCSPX-abcdefg123456"
AUTHORIZE_URL = "https://google.com"
TOKEN_URL = "https://googleapis.com"
REVOKE_URL = "https://googleapis.com"

st.set_page_config(page_title="Sawit Tycoon Pro Monetized", page_icon="🌴", layout="centered")

# Inisialisasi OAuth
oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, TOKEN_URL, REVOKE_URL)

# --- ALUR LOGIN ---
if "auth" not in st.session_state:
    st.title("🌴 Sawit Tycoon Pro - Edisi Komersial")
    st.write("Silakan login dengan Google untuk mulai bermain dan mengelola perkebunan sawit.")
    result = oauth2.authorize_button(
        name="Masuk dengan Google",
        redirect_uri="http://localhost:8501/", 
        scope="openid email profile",
        key="google_auth"
    )
    if result:
        st.session_state["auth"] = result
        st.rerun()
    st.stop()

# --- DATABASE / STATE GAME ---
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
        "hama_aktif": False,  # Indikator jika sedang terserang hama
        "id_pemain": random.randint(1000, 9999), # ID unik untuk verifikasi bayar
        "logs": ["Akun terverifikasi. Kelola risiko dengan bijak untuk keuntungan maksimal."]
    }

db = st.session_state.db

# --- SIMULASI FLUKTUASI HARGA & RISIKO HAMA ---
def update_kondisi_pasar():
    perubahan_harga = random.randint(-300, 300)
    db["harga_tbs_hari_ini"] = max(1800, min(3500, db["harga_tbs_hari_ini"] + perubahan_harga))
    
    # Peluang serangan hama ulat api (15%) jika pohon sudah di lapangan dan belum diserang
    if db["populasi_pohon"] > 0 and not db["hama_aktif"] and random.random() < 0.15:
        db["kesehatan_tanaman"] = max(20, db["kesehatan_tanaman"] - 40)
        db["hama_aktif"] = True
        db["logs"].append("⚠️ KRITIS: Perkebunan terserang Hama Ulat Api! Kesehatan tanaman anjlok 40%.")

update_kondisi_pasar()

# --- TAMPILAN UTAMA WEB ---
st.title("🌴 SAWIT TYCOON PRO: SIMULATOR PASAR")

# --- BANNER SPONSOR DI SIDEBAR (PENGHASILAN 1) ---
st.sidebar.markdown("### 📢 SPONSOR PERKEBUNAN")
st.sidebar.info("""
**🌱 TOKO TANI MAJU UTAMA**
Menyediakan herbisida dan pupuk sawit original.
*Hubungi email pemilik game untuk pasang iklan di sini!*
""")

# --- DASHBOARD ASET & KONDISI PASAR ---
st.header("📈 Dashboard Pasar & Kondisi Perkebunan")
st.metric(label="💰 Harga TBS Pabrik Hari Ini", value=f"Rp {db['harga_tbs_hari_ini']}/Kg")

col1, col2, col3 = st.columns(3)
col1.metric("Dana Tunai", f"Rp {db['dana']:,}")
col2.metric("Aset Lahan", f"{db['lahan_hektar']} Hektar")
col3.metric("Umur Tanaman", f"{db['umur_bulan']} Bulan")

col4, col5 = st.columns(2)
col4.metric("Kesehatan Tanaman", f"{db['kesehatan_tanaman']}%")
col5.metric("Kebersihan Lahan (Gulma)", f"{db['kebersihan_gulma']}%")

# Proteksi Kebangkrutan
if db["dana"] < 0:
    st.error("🚨 GAME OVER: Anda Bangkrut! Silakan coba lagi.")
    if st.button("Mulai Dari Awal 🔄"):
        del st.session_state["db"]
        st.rerun()
    st.stop()

# ==============================================================================
# 🔥 FITUR PENGHASIL CUAL 2: MIKROTRANSAKSI INSTANT RECOVERY VIA QRIS
# ==============================================================================
if db["hama_aktif"]:
    st.error("🐛 Kebun Anda sedang mengalami wabah Hama Ulat Api! Pertumbuhan terhambat.")
    
    # Tombol pemicu pembayaran muncul
    if st.button("🛡️ Pulihkan Kesehatan Tanaman Instan (Rp 2.000 via QRIS)", type="primary"):
        st.session_state["tampilkan_qris"] = True

    # Jika tombol ditekan, tampilkan QRIS dan kode unik pembayarannya
    if st.session_state.get("tampilkan_qris", False):
        st.markdown("### 💳 Pembayaran Pemulihan Instan")
        st.write(f"Silakan pindai QRIS di bawah ini sebesar **Rp 2.000**.")
        st.info(f"📌 **PENTING:** Masukkan Kode Unik atau Pesan **'SAWIT-{db['id_pemain']}'** pada aplikasi e-wallet (DANA/OVO) Anda saat membayar agar admin bisa memverifikasi.")
        
        # GANTI LINK DI BAWAH INI DENGAN URL GAMBAR QRIS DANA/OVO/LINKAJA ASLI ANDA
        st.image("https://wikimedia.org", width=250, caption="Scan QRIS Anda Disini")
        
        st.warning("Konfirmasi Pembayaran: Setelah Anda mentransfer, hubungi Admin melalui WhatsApp atau tekan tombol klaim di bawah setelah transfer selesai.")
        
        if st.button("Klaim Pulih (Setelah Transfer) ✅"):
            # Simulasi persetujuan (Pada sistem nyata, Anda mengecek mutasi masuk e-wallet sesuai kode unik pemain)
            db["kesehatan_tanaman"] = 100
            db["hama_aktif"] = False
            st.session_state["tampilkan_qris"] = False
            db["logs"].append(f"💸 PREMIUM: Pemain dengan ID SAWIT-{db['id_pemain']} berhasil memulihkan tanaman via QRIS!")
            st.success("Sukses! Tanaman Anda telah pulih 100% menjadi prima.")
            st.rerun()
# ==============================================================================

# --- MENU OPERASIONAL GAME STANDARD ---
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
        db["logs"].append("Sukses membeli 150 kecambah PPKS asli.")
        st.rerun()

if st.button("2. Isi Polibag & Tanam", disabled=not polibag_aktif):
    biaya = db["kecambah_ppks"] * 6000
    if db["dana"] >= biaya:
        db["dana"] -= biaya
        db["polibag_isi"] = db["kecambah_ppks"]
        db["kecambah_ppks"] = 0
        db["logs"].append("Kecambah ditanam di Pre-Nursery.")
        st.rerun()

if st.button("3. Pindah ke Lahan Utama (Main Nursery)", disabled=not pindah_aktif):
    db["populasi_pohon"] = 143
    db["polibag_isi"] = 0
    db["umur_bulan"] = 12
    db["logs"].append("Bibit dipindahkan ke lapangan utama.")
    st.rerun()

col_aksi1, col_aksi2 = st.columns(2)
with col_aksi1:
    if st.button("4. Pupuk Tanaman Manual (+6 Bulan)", disabled=not perawatan_aktif):
        biaya = db["populasi_pohon"] * 0.5 * 15000
        if db["dana"] >= biaya:
            db["dana"] -= biaya
            db["kesehatan_tanaman"] = min(100, db["kesehatan_tanaman"] + 15)
            db["umur_bulan"] += 6
            db["kebersihan_gulma"] = max(10, db["kebersihan_gulma"] - 20)
            db["logs"].append("Nutrisi ditambahkan secara manual.")
            st.rerun()

with col_aksi2:
    if st.button("5. Semprot Herbisida Pengendali Gulma", disabled=not perawatan_aktif):
        biaya = db["lahan_hektar"] * 1200000
        if db["dana"] >= biaya:
            db["dana"] -= biaya
            db["kebersihan_gulma"] = 100
            db["kesehatan_tanaman"] = min(100, db["kesehatan_tanaman"] + 10)
            db["umur_bulan"] += 6
            db["logs"].append("Lahan dibersihkan menggunakan herbisida.")
            st.rerun()

if st.button("🔥 6. PANEN PRODUKSI & JUAL KE PABRIK (USIA 4 TAHUN)", disabled=not panen_aktif, type="primary"):
    faktor_kesehatan = db["kesehatan_tanaman"] / 100
    tonase = (db["lahan_hektar"] * 2.5) * faktor_kesehatan
    pendapatan = tonase * 1000 * db["harga_tbs_hari_ini"] 
    db["dana"] += pendapatan
    db["logs"].append(f"PANEN SUKSES! Menjual {tonase:.2f} Ton seharga Rp {db['harga_tbs_hari_ini']}/Kg. Kas: +Rp {pendapatan:,.0f}!")
    
    if db["dana"] >= 45000000:
        db["dana"] -= 45000000
        db["lahan_hektar"] += 1
        db["kecambah_ppks"] = 150
        db["umur_bulan"] = 0
        db["populasi_pohon"] = 0
        db["logs"].append("🚀 INVESTASI BALIK: Membeli 1 Ha Lahan Baru untuk kembangkan aset bagus!")
    st.rerun()

st.header("📝 Catatan Aktivitas Perkebunan")
for log in reversed(db["logs"]):
    st.text(log)
