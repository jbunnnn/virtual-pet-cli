# pet_manager.py
from colorama import Fore, Style
import time, os
from data_handler import load_data, save_data

class PetManager:
    def __init__(self):
        self.data = load_data()
        self.current_pet = None

    def create_pet(self, name):
        if name in self.data:
            print(Fore.RED + "Pet already exists!")
            return
        self.data[name] = {"hunger": 50, "energy": 50, "happy": 50, "health": 100}
        print(Fore.GREEN + f"Pet '{name}' created successfully!")
        self.save_data()

    def select_pet(self, name):
        if name not in self.data:
            print(Fore.RED + "Pet not found!")
            return
        self.current_pet = name
        print(Fore.YELLOW + f"You selected {name} 🐾")

    def show_status(self):
        if not self.current_pet:
            print(Fore.RED + "No pet selected.")
            return
        pet = self.data[self.current_pet]
        print(Fore.CYAN + f"""
--- {self.current_pet}'s Status ---
🍖 Hunger : {pet['hunger']}
⚡ Energy : {pet['energy']}
😊 Happy  : {pet['happy']}
❤️ Health : {pet['health']}
""")

    # === ANIMATED ACTIONS ===
    def feed(self):
        self._ensure_selected()
        print(Fore.YELLOW + f"\nFeeding {self.current_pet} 🍖")
        for frame in ["(˶ᵔᴗᵔ)っ🍗", "( ˘▽˘)っ🍗", "(๑>◡<๑)っ🍖"]:
            print(Fore.GREEN + frame, end="\r", flush=True)
            time.sleep(0.6)
        print(Fore.GREEN + "\nYummy! That was delicious 😋")
        self.data[self.current_pet]["hunger"] = min(100, self.data[self.current_pet]["hunger"] + 20)
        self.save_data()

    def play(self):
        self._ensure_selected()
        print(Fore.MAGENTA + f"\nPlaying with {self.current_pet} ⚽")
        for frame in ["(•ᴗ•)ノ⚽", "(⚽>ᴗ<)ノ", "ヽ(>ᴗ<⚽)ノ"]:
            print(Fore.MAGENTA + frame, end="\r", flush=True)
            time.sleep(0.5)
        print(Fore.MAGENTA + "\nThat was fun! 😄")
        self.data[self.current_pet]["happy"] = min(100, self.data[self.current_pet]["happy"] + 20)
        self.save_data()

    def sleep(self):
        self._ensure_selected()
        print(Fore.BLUE + f"\n{self.current_pet} is sleeping... 😴")
        for frame in ["(˘ω˘) z", "(˘ω˘) zz", "(˘ω˘) zzz"]:
            print(Fore.BLUE + frame, end="\r", flush=True)
            time.sleep(1)
        print(Fore.CYAN + "\nAll rested up! 🌞")
        self.data[self.current_pet]["energy"] = min(100, self.data[self.current_pet]["energy"] + 30)
        self.save_data()

    def heal(self):
        self._ensure_selected()
        print(Fore.LIGHTGREEN_EX + f"\nHealing {self.current_pet} ✨")
        for frame in ["💖", "💫", "✨", "💫", "💖"]:
            print(Fore.LIGHTGREEN_EX + frame, end="\r", flush=True)
            time.sleep(0.4)
        print(Fore.LIGHTGREEN_EX + "\nFeeling much better now! ❤️‍🩹")
        self.data[self.current_pet]["health"] = min(100, self.data[self.current_pet]["health"] + 25)
        self.save_data()

    def list_pets(self):
        if not self.data:
            print(Fore.RED + "No pets found.")
            return
        print(Fore.YELLOW + "🐾 Your pets:")
        for pet in self.data:
            print(" -", pet)

    def save_data(self):
        save_data(self.data)

    def _ensure_selected(self):
        if not self.current_pet:
            print(Fore.RED + "Select a pet first using 'select'")
            raise Exception("No pet selected")
