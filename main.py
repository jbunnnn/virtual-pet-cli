# main.py
from pet_manager import PetManager # import class utama untuk mengatur logika hewan
from colorama import Fore, Style, init # libary untuk membari warna pada teks terminal
import time, sys # time untuk delay animasi, sys untuk output teks manual

#Inisiasi colorama agar warna otomatis reset setelah digunakan
init(autoreset=True)

# Menampilkan teks karakter demi karakter 
# Output saat di run (tampilan awal)
def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char) #tulis satu karakter ke terminal tanpa newline
        sys.stdout.flush() #untuk memastikan karakter langsung muncul
        time.sleep(delay) #delay antar karakter
    print()

#nampilin daftar perintah (command list) yang bisa digunakan oleh user
def show_help():
    print(Fore.CYAN + """
Available commands:
  list                     - Show all your pets
  create [name]            - Create a new pet (e.g. create maww)
  delete [name]            - Delete a pet
  rename [old] [new]       - Rename a pet
  select [name]            - Select a pet to play with
  status                   - Show current pet's status
  stats                    - Show all pets' stats
  feed                     - Feed your pet 🍗
  play                     - Play with your pet ⚽
  sleep                    - Let your pet rest 😴
  heal                     - Heal your pet ❤️‍🩹
  save                     - Save pet data 💾
  exit                     - Quit the game 🐾
  help                     - Show this help
""")

#fungsi utama tempat program berjalan secara interaktif
def main():
    manager = PetManager() #membuat instance petmanager untuk mengatur semua hewan

    #menampilkan teks pembuka dengan efek animasi
    slow_print(Fore.CYAN + "🐾 Booting up Virtual Pet CLI v2... Loading cuddles ❤️", 0.03)
    time.sleep(0.3) #jeda singkat biar efeknya halus
    print(Fore.CYAN + "Welcome to Virtual Pet CLI v2 🐾 (Cute Mode)")
    print(Fore.YELLOW + "Type 'help' to see available commands.\n")

    #loop utama (program berjalan terus)
    while True:
        try:
            #minta input dari user
            user_input = input(Fore.GREEN + ">> ").strip()
        except (KeyboardInterrupt, EOFError):
            #jika user menekan ctl+c atau ctrl+z program berhenti dengan aman
            print(Fore.YELLOW + "\nDetected exit signal. Saving and quitting...")
            manager.save_data() #buat nyimpen data sebelum keluar
            break

        #jika input kosong, lanjut ke loop berikutnya
        if not user_input:
            continue

        # proses input
        parts = user_input.replace("'", "").replace('"', "").split() #pisahkan input jadi dua bagian: command & argumen
        cmd = parts[0].lower() #command utama (misal: create, list, feed)
        args = parts[1:] #sisanya (nama hewan, dll)


        #eksekusi berdasarkan perintah user
        if cmd == "help":
            show_help()

        elif cmd == "list":
            manager.list_pets() #menampilkan daftar semua hewan

        elif cmd == "create":
            #jika user tidak menulis nama di command, minta input tambahan
            name = " ".join(args) if args else input("Enter new pet name: ")
            manager.create_pet(name) #buat hewan baru

        elif cmd == "delete":
            name = " ".join(args) if args else input("Enter pet name to delete: ")
            manager.delete(name) #hapus hewan dari data

        elif cmd == "rename":
            #jika user langsung nulis dua nama, pakai langsung
            if len(args) >= 2:
                old = args[0]
                new = " ".join(args[1:])
            else:
                #kalau belum ada, minta input manual
                old = input("Old name: ")
                new = input("New name: ")
            manager.rename(old, new) #jalankan rename

        elif cmd == "select":
            name = " ".join(args) if args else input("Enter pet name to select: ")
            manager.select_pet(name) #pilih hewan yang mau dimainkan

        elif cmd == "status":
            manager.show_status() #lihat status hewan aktif

        elif cmd == "stats":
            manager.stats_all() #tampilin statistik semua hewan

        elif cmd == "feed":
            manager.feed() #kasih makan

        elif cmd == "play":
            manager.play() #bermain dengan hewan

        elif cmd == "sleep":
            manager.sleep() #istirahatkan hewan

        elif cmd == "heal":     
            manager.heal() #sembuhkan hewan

        elif cmd == "save":
            # simpan semua data ke file json
            manager.save_data()
            print(Fore.CYAN + "Data saved ✅")

        elif cmd == "exit" or cmd == "quit":
            #animasi keluar program
            print(Fore.YELLOW + "\nSaving data and saying goodbye...")
            for frame in ["🐾", "🐾🐾", "🐾🐾🐾"]:
                print(Fore.YELLOW + frame, end="\r", flush=True)
                time.sleep(0.4)
            print(Fore.CYAN + "\nGoodbye! See you next time 👋")
            manager.save_data() #simpan data sebelum keluar
            break
        else:
            #jika command tidak dikenal
            print(Fore.RED + "Unknown command! Type 'help' for list of commands.")


#memastikan program hanya dijalankan jika file ini langsung dieksekusi (bukan di import dari file lain)
if __name__ == "__main__":
    main()
