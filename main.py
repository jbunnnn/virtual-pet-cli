# main.py
from pet_manager import PetManager
from colorama import Fore, Style, init
import time, sys

init(autoreset=True)

def slow_print(text, delay=0.03):
    """Animasi teks berjalan (buat efek dramatis 😎)"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    manager = PetManager()

    # Animasi opening
    slow_print(Fore.CYAN + "🐾 Booting up Virtual Pet CLI...", 0.04)
    time.sleep(0.5)
    print(Fore.CYAN + "🐾 Welcome to Virtual Pet CLI 🐾")
    print(Fore.YELLOW + "Type 'help' to see available commands.\n")

    while True:
        # Ambil input dan bersihkan dari kutip
        user_input = input(Fore.GREEN + ">> ").strip().lower().replace("'", "").replace('"', "")
        parts = user_input.split()
        cmd = parts[0] if len(parts) > 0 else ""
        args = parts[1:]

        if cmd == "help":
            print(Fore.CYAN + """
Available commands:
  list           - Show all your pets
  create [name]  - Create a new pet (e.g. create maww)
  select [name]  - Select a pet to play with
  status         - Show current pet's status
  feed           - Feed your pet 🍗
  play           - Play with your pet ⚽
  sleep          - Let your pet rest 😴
  heal           - Heal your pet ❤️‍🩹
  save           - Save pet data 💾
  exit           - Quit the game 🐾
""")

        elif cmd == "list":
            manager.list_pets()

        elif cmd == "create":
            if len(args) == 0:
                name = input("Enter new pet name: ")
            else:
                name = " ".join(args)
            manager.create_pet(name)

        elif cmd == "select":
            if len(args) == 0:
                name = input("Enter pet name to select: ")
            else:
                name = " ".join(args)
            manager.select_pet(name)

        elif cmd == "status":
            manager.show_status()

        elif cmd == "feed":
            manager.feed()

        elif cmd == "play":
            manager.play()

        elif cmd == "sleep":
            manager.sleep()

        elif cmd == "heal":
            manager.heal()

        elif cmd == "save":
            manager.save_data()

        elif cmd == "exit":
            print(Fore.YELLOW + "\nSaving data and saying goodbye...")
            for frame in ["🐾", "🐾🐾", "🐾🐾🐾"]:
                print(Fore.YELLOW + frame, end="\r", flush=True)
                time.sleep(0.4)
            print(Fore.CYAN + "\nGoodbye! See you next time 👋")
            manager.save_data()
            break

        elif cmd == "":
            continue

        else:
            print(Fore.RED + "Unknown command! Type 'help' for list of commands.")

if __name__ == "__main__":
    main()
