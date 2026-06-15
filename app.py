import streamlit as st
import random

st.set_page_config(page_title="Sawit Tycoon Pro Edisi Instan", page_icon="🌴", layout="centered")

# --- SISTEM LOGIN SIMULASI (BYPASS GOOGLE CLOUD) ---
if "user_logged_in" not in st.session_state:
    st.title("🌴 Sawit Tycoon Pro - Edisi Pengusaha")
    st.write("Masukan Nama Anda untuk Memulai Petualangan Agribisnis Kelapa Sawit.")
    
    # Input nama pemain sebagai pengganti login Google
    nama_pemain = st.text_input("Nama Pemain / Nama Perusahaan:", placeholder="Contoh: Sawit Makmur Jaya")
    
    if st.button("Masuk & Mulai Berbisnis 🚀", type="primary"):
        if nama_pemain.strip() != "":
            st.session_state["user_logged_in"] = nama_pemain
            st.rerun()
        else:
            st.error("Silakan isi nama Anda terlebih dahulu!")
    st.stop()

# --- AMBIL NAMA PEMAIN YANG AKTIF ---
nama_user = st.session_state["user_logged_in"]

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
        "hama_aktif": False,
        "id_pemain": random.randint(1000, 9999),
        "logs": [f"Selamat Datang {nama_user}! Perkebunan Anda resmi dibuka hari ini."]
    }

db = st.session_state.db

# --- SIMULASI FLUKTUASI HARGA & RISIKO HAMA ---
def update_kondisi_pasar():
    perubahan_harga = random.randint(-300, 300)
    db["harga_tbs_hari_ini"] = max(1800, min(3500, db["harga_tbs_hari_ini"] + perubahan_harga))
    
    if db["populasi_pohon"] > 0 and not db["hama_aktif"] and random.random() < 0.15:
        db["kesehatan_tanaman"] = max(20, db["kesehatan_tanaman"] - 40)
        db["hama_aktif"] = True
        db["logs"].append("⚠️ KRITIS: Perkebunan terserang Hama Ulat Api! Kesehatan tanaman anjlok 40%.")

update_kondisi_pasar()

# --- TAMPILAN UTAMA WEB ---
st.title("🌴 SAWIT TYCOON PRO: SIMULATOR PASAR")
st.caption(f"Direktur Utama: **{nama_user}** | ID Pemain: SAWIT-{db['id_pemain']}")

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

# Tombol Keluar Akun
if st.sidebar.button("Keluar Game 🚪"):
    del st.session_state["user_logged_in"]
    if "db" in st.session_state:
        del st.session_state["db"]
    st.rerun()

# Proteksi Kebangkrutan
if db["dana"] < 0:
    st.error("🚨 GAME OVER: Anda Bangkrut! Silakan coba lagi.")
    if st.button("Mulai Dari Awal 🔄"):
        del st.session_state["db"]
        st.rerun()
    st.stop()

# QRIS MIKROTRANSAKSI
if db["hama_aktif"]:
    st.error("🐛 Kebun Anda sedang mengalami wabah Hama Ulat Api! Pertumbuhan terhambat.")
    if st.button("🛡️ Pulihkan Kesehatan Tanaman Instan (Rp 2.000 via QRIS)", type="primary"):
        st.session_state["tampilkan_qris"] = True

    if st.session_state.get("tampilkan_qris", False):
        st.markdown("### 💳 Pembayaran Pemulihan Instan")
        st.write(f"Silakan pindai QRIS di bawah ini sebesar **Rp 2.000**.")
        st.info(f"📌 **PENTING:** Masukkan Kode Unik atau Pesan **'SAWIT-{db['id_pemain']}'** pada e-wallet saat membayar.")
        st.image("https://wikimedia.org", width=250, caption="Scan QRIS Anda Disini")
        
        if st.button("Klaim Pulih (Setelah Transfer) ✅"):
            db["kesehatan_tanaman"] = 100
            db["hama_aktif"] = False
            st.session_state["tampilkan_qris"] = False
            db["logs"].append(f"💸 PREMIUM: Pemain SAWIT-{db['id_pemain']} berhasil memulihkan tanaman via QRIS!")
            st.success("Sukses! Tanaman Anda telah pulih 100% menjadi prima.")
            st.rerun()

# --- MENU OPERASIONAL GAME ---
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
