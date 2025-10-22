# main.py
from pet_manager import PetManager
from colorama import Fore, Style, init
import time, sys

init(autoreset=True)

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

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

def main():
    manager = PetManager()

    slow_print(Fore.CYAN + "🐾 Booting up Virtual Pet CLI v2... Loading cuddles ❤️", 0.03)
    time.sleep(0.3)
    print(Fore.CYAN + "Welcome to Virtual Pet CLI v2 🐾 (Cute Mode)")
    print(Fore.YELLOW + "Type 'help' to see available commands.\n")

    while True:
        try:
            user_input = input(Fore.GREEN + ">> ").strip()
        except (KeyboardInterrupt, EOFError):
            print(Fore.YELLOW + "\nDetected exit signal. Saving and quitting...")
            manager.save_data()
            break

        if not user_input:
            continue

        # sanitize and split
        parts = user_input.replace("'", "").replace('"', "").split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "help":
            show_help()
        elif cmd == "list":
            manager.list_pets()
        elif cmd == "create":
            name = " ".join(args) if args else input("Enter new pet name: ")
            manager.create_pet(name)
        elif cmd == "delete":
            name = " ".join(args) if args else input("Enter pet name to delete: ")
            manager.delete(name)
        elif cmd == "rename":
            if len(args) >= 2:
                old = args[0]
                new = " ".join(args[1:])
            else:
                old = input("Old name: ")
                new = input("New name: ")
            manager.rename(old, new)
        elif cmd == "select":
            name = " ".join(args) if args else input("Enter pet name to select: ")
            manager.select_pet(name)
        elif cmd == "status":
            manager.show_status()
        elif cmd == "stats":
            manager.stats_all()
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
            print(Fore.CYAN + "Data saved ✅")
        elif cmd == "exit" or cmd == "quit":
            print(Fore.YELLOW + "\nSaving data and saying goodbye...")
            for frame in ["🐾", "🐾🐾", "🐾🐾🐾"]:
                print(Fore.YELLOW + frame, end="\r", flush=True)
                time.sleep(0.4)
            print(Fore.CYAN + "\nGoodbye! See you next time 👋")
            manager.save_data()
            break
        else:
            print(Fore.RED + "Unknown command! Type 'help' for list of commands.")

if __name__ == "__main__":
    main()
