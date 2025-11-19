# ============================================================================
# PET MANAGER - Virtual Pet System
# Sistem manajemen hewan peliharaan virtual dengan fitur leveling & stats
# ============================================================================

from colorama import Fore, Style
import time, os, random
from data_handler import load_data, save_data

# Konstanta untuk batas maksimal stat (0-100%)
MAX_STAT = 100


# ============================================================================
# PROGRESS BAR FUNCTION
# ============================================================================
# Membuat progress bar visual untuk menampilkan nilai stat (0-100)
# Alasan def: Fungsi ini digunakan berkali-kali di berbagai method,
# jadi lebih efisien dibuat sekali lalu dipanggil daripada duplikasi kode
def progress_bar(value, length=20):
    """
    Buat progress bar text-based.
    
    Args:
        value: Nilai stat (0-100)
        length: Panjang bar dalam karakter (default 20)
    
    Returns:
        String visual progress bar dengan persentase
    """
    # Pastikan nilai berada di range 0-100
    value = max(0, min(MAX_STAT, int(value)))
    
    # Hitung jumlah karakter terisi dan kosong
    filled = int((value / MAX_STAT) * length)
    empty = length - filled
    
    # Gabungkan karakter █ (terisi) dan ░ (kosong)
    return "[" + "█" * filled + "░" * empty + f"] {value}%"


# ============================================================================
# PET MANAGER CLASS
# ============================================================================
# Alasan menggunakan Class: Merangkum semua fungsi pet menjadi satu object
# sehingga lebih terorganisir, reusable, dan mudah manage state data
class PetManager:
    """
    Manager untuk mengelola hewan peliharaan virtual.
    Mencakup create, select, feed, play, sleep, heal, dll.
    """
    
    def __init__(self):
        """
        Inisialisasi PetManager dengan load data dari file.
        Memastikan setiap pet punya field level & exp.
        """
        self.data = load_data()
        self.current_pet = None
        
        # Pastikan setiap pet punya field level & exp (untuk backward compatibility)
        for pet, attrs in list(self.data.items()):
            attrs.setdefault("level", 1)
            attrs.setdefault("exp", 0)

    # ========================================================================
    # CREATE & SELECT PET METHODS
    # ========================================================================
    
    def create_pet(self, name):
        """
        Buat pet baru dengan stats awal.
        Alasan def: Logika pembuatan pet cukup kompleks (validasi, init data)
        """
        name = name.strip()
        
        # Validasi input
        if not name:
            print(Fore.RED + "Name cannot be empty.")
            return
        
        if name in self.data:
            print(Fore.RED + "Pet already exists!")
            return
        
        # Inisialisasi stat baru pet dengan nilai awal
        self.data[name] = {
            "hunger": 50,
            "energy": 50,
            "happy": 50,
            "health": 100,
            "level": 1,
            "exp": 0
        }
        
        print(Fore.GREEN + f"Pet '{name}' created successfully! 🐣")
        self.save_data()

    def select_pet(self, name):
        """
        Pilih pet yang akan diinteraksi.
        Alasan def: Fungsi ini perlu divalidasi dan mengubah state current_pet
        """
        if name not in self.data:
            print(Fore.RED + "Pet not found!")
            return
        
        self.current_pet = name
        print(Fore.YELLOW + f"You selected {name} 🐾")

    # ========================================================================
    # STATUS & INFO DISPLAY METHODS
    # ========================================================================
    
    def show_status(self):
        """
        Tampilkan status detail pet yang sedang dipilih.
        Alasan def: Display method terpisah agar clean & reusable
        """
        if not self._ensure_selected():
            return
        
        pet = self.data[self.current_pet]
        
        print(Fore.CYAN + f"""
--- {self.current_pet}'s Status ---
Level: {pet.get('level',1)}   EXP: {pet.get('exp',0)}/100
🍖 Hunger : {progress_bar(pet['hunger'])}
⚡ Energy : {progress_bar(pet['energy'])}
😊 Happy  : {progress_bar(pet['happy'])}
❤️ Health : {progress_bar(pet['health'])}
""")

    def list_pets(self):
        """
        Tampilkan daftar semua pet dengan info ringkas.
        Alasan def: Display logic terpisah untuk modularitas
        """
        if not self.data:
            print(Fore.RED + "No pets found.")
            return
        
        print(Fore.YELLOW + "🐾 Your pets:")
        for pet, attrs in self.data.items():
            lvl = attrs.get("level", 1)
            hp = attrs.get("health", 0)
            print(f" - {pet} (Lv {lvl}) | Health: {hp}%")

    def stats_all(self):
        """
        Tampilkan ringkasan lengkap semua pet dengan bar stats.
        Alasan def: Method terpisah untuk reporting yang komprehensif
        """
        if not self.data:
            print(Fore.RED + "No pets found.")
            return
        
        print(Fore.MAGENTA + "📊 All Pets Summary")
        
        for pet, attrs in self.data.items():
            print(Fore.MAGENTA + f"\n{pet} — Lv {attrs.get('level',1)} | EXP {attrs.get('exp',0)}/100")
            print("  " + "Hunger :", progress_bar(attrs['hunger']))
            print("  " + "Energy :", progress_bar(attrs['energy']))
            print("  " + "Happy  :", progress_bar(attrs['happy']))
            print("  " + "Health :", progress_bar(attrs['health']))

    # ========================================================================
    # PET INTERACTION METHODS
    # ========================================================================
    
    def feed(self):
        """
        Beri makan pet. Kurangi hunger, gain EXP, cek random event.
        Alasan def: Setiap interaksi punya logika serupa (animasi, stat change, exp)
        jadi lebih clean jika terpisah method
        """
        if not self._ensure_selected():
            return
        
        print(Fore.YELLOW + f"\nFeeding {self.current_pet} 🍖")
        
        # Animasi feeding dengan frame berbeda
        for frame in ["(˶ᵔᴗᵔ)っ🍗", "( ˘▽˘)っ🍗", "(๑>◡<๑)っ🍖"]:
            print(Fore.GREEN + frame, end="\r", flush=True)
            time.sleep(0.5)
        
        print(Fore.GREEN + "\nYummy! That was delicious 😋")
        
        # Update stat
        pet = self.data[self.current_pet]
        pet["hunger"] = min(MAX_STAT, pet["hunger"] + 20)
        
        # Gain EXP dan cek event
        self._gain_exp(10)
        self._random_event("feed")
        
        self.save_data()

    def play(self):
        """
        Main dengan pet. Naikkan happy, turunkan energy, gain EXP.
        Alasan def: Interaction logic yang perlu terpisah & reusable
        """
        if not self._ensure_selected():
            return
        
        print(Fore.MAGENTA + f"\nPlaying with {self.current_pet} ⚽")
        
        # Animasi play dengan 3 frame
        for frame in ["(•ᴗ•)ノ⚽", "(⚽>ᴗ<)ノ", "ヽ(>ᴗ<⚽)ノ"]:
            print(Fore.MAGENTA + frame, end="\r", flush=True)
            time.sleep(0.45)
        
        print(Fore.MAGENTA + "\nThat was fun! 😄")
        
        # Update stat
        pet = self.data[self.current_pet]
        pet["happy"] = min(MAX_STAT, pet["happy"] + 20)
        pet["energy"] = max(0, pet["energy"] - 10)
        
        # Gain EXP dan cek event
        self._gain_exp(15)
        self._random_event("play")
        
        self.save_data()

    def sleep(self):
        """
        Tidurkan pet. Naikkan energy, turunkan hunger, gain EXP.
        Alasan def: Interaksi berbeda perlu method terpisah untuk clarity
        """
        if not self._ensure_selected():
            return
        
        print(Fore.BLUE + f"\n{self.current_pet} is sleeping... 😴")
        
        # Animasi sleep dengan karakter "z" bertambah
        for frame in ["(˘ω˘) z", "(˘ω˘) zz", "(˘ω˘) zzz"]:
            print(Fore.BLUE + frame, end="\r", flush=True)
            time.sleep(0.8)
        
        print(Fore.CYAN + "\nAll rested up! 🌞")
        
        # Update stat
        pet = self.data[self.current_pet]
        pet["energy"] = min(MAX_STAT, pet["energy"] + 30)
        pet["hunger"] = max(0, pet["hunger"] - 10)
        
        # Gain EXP dan cek event
        self._gain_exp(8)
        self._random_event("sleep")
        
        self.save_data()

    def heal(self):
        """
        Sembuhkan pet. Naikkan health, gain EXP.
        Alasan def: Interaksi spesifik yang perlu isolated logic
        """
        if not self._ensure_selected():
            return
        
        print(Fore.LIGHTGREEN_EX + f"\nHealing {self.current_pet} ✨")
        
        # Animasi heal dengan emoji healing
        for frame in ["💖", "💫", "✨", "💫", "💖"]:
            print(Fore.LIGHTGREEN_EX + frame, end="\r", flush=True)
            time.sleep(0.35)
        
        print(Fore.LIGHTGREEN_EX + "\nFeeling much better now! ❤️‍🩹")
        
        # Update stat
        pet = self.data[self.current_pet]
        pet["health"] = min(MAX_STAT, pet["health"] + 25)
        
        # Gain EXP dan cek event
        self._gain_exp(12)
        self._random_event("heal")
        
        self.save_data()

    # ========================================================================
    # PET MANAGEMENT METHODS
    # ========================================================================
    
    def rename(self, old_name, new_name):
        """
        Ubah nama pet.
        Alasan def: Perlu validasi & update reference (current_pet),
        jadi perlu method tersendiri
        """
        old_name = old_name.strip()
        new_name = new_name.strip()
        
        # Validasi input
        if not old_name or not new_name:
            print(Fore.RED + "Both old and new name required.")
            return
        
        if old_name not in self.data:
            print(Fore.RED + "Pet not found.")
            return
        
        if new_name in self.data:
            print(Fore.RED + "New name already used by another pet.")
            return
        
        # Update data & reference
        self.data[new_name] = self.data.pop(old_name)
        if self.current_pet == old_name:
            self.current_pet = new_name
        
        print(Fore.GREEN + f"Renamed '{old_name}' to '{new_name}' ✅")
        self.save_data()

    def delete(self, name):
        """
        Hapus pet dengan konfirmasi.
        Alasan def: Operasi destruktif perlu confirmation logic terpisah
        """
        name = name.strip()
        
        # Validasi input
        if not name:
            print(Fore.RED + "Name required.")
            return
        
        if name not in self.data:
            print(Fore.RED + "Pet not found.")
            return
        
        # Minta konfirmasi dari user
        confirm = input(Fore.RED + f"Are you sure to delete '{name}'? (y/n): ").strip().lower()
        
        if confirm == "y":
            del self.data[name]
            if self.current_pet == name:
                self.current_pet = None
            print(Fore.YELLOW + f"Pet '{name}' deleted.")
            self.save_data()
        else:
            print(Fore.CYAN + "Delete cancelled.")

    def save_data(self):
        """
        Simpan data ke file.
        Alasan def: Wrapper untuk save_data dari data_handler,
        memudahkan future updates atau logging
        """
        save_data(self.data)

    # ========================================================================
    # INTERNAL HELPER METHODS (Private dengan prefix _)
    # ========================================================================
    # Alasan prefix "_": Menandakan method ini internal & tidak perlu dipanggil
    # dari luar class
    
    def _ensure_selected(self):
        """
        Validasi apakah ada pet yang dipilih.
        Alasan def: Check ini digunakan di hampir setiap method,
        jadi better extract ke helper function
        """
        if not self.current_pet:
            print(Fore.RED + "Select a pet first using 'select [name]'.")
            return False
        return True

    def _gain_exp(self, amount):
        """
        Tambah EXP & cek apakah pet bisa level up.
        Alasan def: Logika leveling cukup kompleks, perlu terpisah & reusable
        """
        pet = self.data[self.current_pet]
        
        # Tambah EXP
        pet["exp"] = pet.get("exp", 0) + amount
        
        leveled = False
        
        # Cek apakah EXP >= 100 (level up)
        while pet["exp"] >= 100:
            pet["exp"] -= 100
            pet["level"] = pet.get("level", 1) + 1
            
            # Bonus stat saat level up
            pet["hunger"] = max(0, pet["hunger"] - 5)
            pet["happy"] = min(MAX_STAT, pet["happy"] + 5)
            
            leveled = True
        
        # Output message
        if leveled:
            print(Fore.CYAN + f"✨ {self.current_pet} leveled up! Now Lv {pet['level']} ✨")
        else:
            print(Fore.CYAN + f"{self.current_pet} gained {amount} EXP.")

    def _random_event(self, action):
        """
        Trigger random event yang membuat game terasa lebih hidup & dinamis.
        
        Alasan def: Event logic terpisah agar mudah di-maintain & di-extend.
        Setiap action bisa punya multiple random event outcomes.
        
        Args:
            action: Tipe action ('feed', 'play', 'sleep', 'heal')
        """
        chance = random.randint(1, 100)
        pet = self.data[self.current_pet]
        
        # ====== POSITIVE EVENTS ======
        
        # 15% chance ketika play: pet menemukan mainan bonus
        if action == "play" and chance <= 15:
            print(Fore.YELLOW + f"🎁 Lucky! {self.current_pet} found a toy and got +10 happy!")
            pet["happy"] = min(MAX_STAT, pet["happy"] + 10)
        
        # 10% chance ketika feed: pet menemukan treat bonus
        elif action == "feed" and chance <= 10:
            print(Fore.MAGENTA + f"😮 Surprise! {self.current_pet} found a treat and +5 health!")
            pet["health"] = min(MAX_STAT, pet["health"] + 5)
        
        # 12% chance ketika sleep: pet mimpi indah
        elif action == "sleep" and chance <= 12:
            print(Fore.BLUE + f"🌙 Dream event: {self.current_pet} had a happy dream (+8 happy)!")
            pet["happy"] = min(MAX_STAT, pet["happy"] + 8)
        
        # ====== NEGATIVE EVENTS ======
        
        # Jika hunger sangat rendah (<= 10): 8% chance pet kelaparan & health -10
        if pet["hunger"] <= 10 and random.randint(1, 100) <= 8:
            print(Fore.RED + f"⚠️ {self.current_pet} is starving! Health -10.")
            pet["health"] = max(0, pet["health"] - 10)
