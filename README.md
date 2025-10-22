# 🐾 Virtual Pet CLI v2

### 👥 Kelompok:
- Rajib Zidan  
- Thorik  
- Fauzan  

---

## 📝 Deskripsi
Virtual Pet CLI v2 adalah program berbasis terminal yang memungkinkan pengguna untuk memelihara hewan virtual secara interaktif.  
Pengguna dapat membuat, memberi makan, mengajak bermain, menyembuhkan, dan menidurkan peliharaan mereka lewat perintah sederhana di Command Line Interface (CLI).

Proyek ini dikembangkan untuk memenuhi tugas **Project Akhir Mata Kuliah Pemrograman Dasar**.

---

## ⚙️ Fitur Utama
create [nama] → Membuat hewan baru  
list → Menampilkan semua hewan yang sudah dibuat  
select [nama] → Memilih hewan untuk dimainkan  
status → Melihat status hewan (hunger, energy, happy, health)  
feed → Memberi makan hewan 🍗  
play → Bermain dengan hewan ⚽  
sleep → Menidurkan hewan 😴  
heal → Menyembuhkan hewan ❤️‍🩹  
save → Menyimpan data ke file JSON 💾  
exit → Keluar dari program 🐾  

---

## 🧩 Struktur Project
📁 virtual-pet-cli/  
├── 📄 main.py → File utama (CLI dan command handler)  
├── 📄 pet_manager.py → Class utama untuk mengatur logika hewan  
├── 📄 data_handler.py → Menangani load & save data JSON  
├── 📄 pet_data.json → Tempat penyimpanan data peliharaan  
└── 📄 README.md → Dokumentasi project  

---

## 💡 Library yang Digunakan
colorama → Memberikan warna pada teks di terminal  
time → Menambahkan efek delay dan animasi  
json → Menyimpan data peliharaan tanpa database  
os → Mengecek dan memproses file JSON  

---

## 🚀 Cara Menjalankan Program
1. Pastikan Python sudah terinstal  
   Versi yang disarankan: **Python 3.10+**

2. Instal library yang dibutuhkan  
   ```bash
   pip install colorama
