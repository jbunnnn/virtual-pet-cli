import json  # Modul 'json' dipakai untuk mengubah data Python (seperti dict, list, dsb)
              # menjadi format JSON, dan sebaliknya. JSON ini dipakai buat nyimpen data
              # biar bisa dibuka lagi nanti.

import os    # Modul 'os' dipakai buat operasi sistem, di sini gunanya buat ngecek
              # apakah file JSON kita udah ada atau belum di penyimpanan lokal.

# Nama file tempat data disimpan.
DATA_FILE = "pet_data.json"


def load_data():
    """
    Fungsi ini dipakai buat *membaca* data dari file JSON.
    Kalau file-nya belum ada atau rusak, fungsi ini bakal ngembaliin dictionary kosong.
    """
    # Mengecek apakah file JSON belum ada
    if not os.path.exists(DATA_FILE):
        return {}  # Kalau belum ada, balikin data kosong supaya program nggak error

    # Kalau file-nya ada, buka file itu dalam mode "read" (r)
    # 'encoding="utf-8"' biar karakter non-ASCII (misal nama hewan aneh) bisa kebaca
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            # json.load() = baca isi file dan ubah dari format JSON ke Python dictionary
            return json.load(f)
        except Exception:
            # Kalau isi file-nya rusak (misal format JSON-nya salah),
            # biar program tetap jalan, kita balikin data kosong
            return {}


def save_data(data):
    """
    Fungsi ini dipakai buat *menyimpan* data ke file JSON.
    Data yang disimpan biasanya berupa dictionary (dict) dari program utama.
    """
    # Buka file dalam mode "write" (w), jadi isinya bakal ditimpa setiap kali nyimpen
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        # json.dump() = ubah data Python jadi format JSON dan tulis ke file
        # indent=4 -> biar hasil JSON rapi (ada jarak 4 spasi)
        # ensure_ascii=False -> biar karakter non-ASCII (misal huruf é, ü) tetap tampil
        json.dump(data, f, indent=4, ensure_ascii=False)
