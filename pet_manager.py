# pet_manager.py
from colorama import Fore, Style
import time, os, random
from data_handler import load_data, save_data

MAX_STAT = 100

def progress_bar(value, length=20):
    """Buat progress bar text-based."""
    value = max(0, min(MAX_STAT, int(value)))
    filled = int((value / MAX_STAT) * length)
    empty = length - filled
    return "[" + "█" * filled + "░" * empty + f"] {value}%"

class PetManager:
    def __init__(self):
        self.data = load_data()
        self.current_pet = None
        # Pastikan setiap pet punya field level & exp
        for pet, attrs in list(self.data.items()):
            attrs.setdefault("level", 1)
            attrs.setdefault("exp", 0)

    def create_pet(self, name):
        name = name.strip()
        if not name:
            print(Fore.RED + "Name cannot be empty.")
            return
        if name in self.data:
            print(Fore.RED + "Pet already exists!")
            return
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
        if name not in self.data:
            print(Fore.RED + "Pet not found!")
            return
        self.current_pet = name
        print(Fore.YELLOW + f"You selected {name} 🐾")

    def show_status(self):
        if not self._ensure_selected(): return
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
        if not self.data:
            print(Fore.RED + "No pets found.")
            return
        print(Fore.YELLOW + "🐾 Your pets:")
        for pet, attrs in self.data.items():
            lvl = attrs.get("level",1)
            hp = attrs.get("health",0)
            print(f" - {pet} (Lv {lvl}) | Health: {hp}%")

    def stats_all(self):
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

    def feed(self):
        if not self._ensure_selected(): return
        print(Fore.YELLOW + f"\nFeeding {self.current_pet} 🍖")
        for frame in ["(˶ᵔᴗᵔ)っ🍗", "( ˘▽˘)っ🍗", "(๑>◡<๑)っ🍖"]:
            print(Fore.GREEN + frame, end="\r", flush=True)
            time.sleep(0.5)
        print(Fore.GREEN + "\nYummy! That was delicious 😋")
        pet = self.data[self.current_pet]
        pet["hunger"] = min(MAX_STAT, pet["hunger"] + 20)
        self._gain_exp(10)
        self._random_event("feed")
        self.save_data()

    def play(self):
        if not self._ensure_selected(): return
        print(Fore.MAGENTA + f"\nPlaying with {self.current_pet} ⚽")
        for frame in ["(•ᴗ•)ノ⚽", "(⚽>ᴗ<)ノ", "ヽ(>ᴗ<⚽)ノ"]:
            print(Fore.MAGENTA + frame, end="\r", flush=True)
            time.sleep(0.45)
        print(Fore.MAGENTA + "\nThat was fun! 😄")
        pet = self.data[self.current_pet]
        pet["happy"] = min(MAX_STAT, pet["happy"] + 20)
        pet["energy"] = max(0, pet["energy"] - 10)
        self._gain_exp(15)
        self._random_event("play")
        self.save_data()

    def sleep(self):
        if not self._ensure_selected(): return
        print(Fore.BLUE + f"\n{self.current_pet} is sleeping... 😴")
        for frame in ["(˘ω˘) z", "(˘ω˘) zz", "(˘ω˘) zzz"]:
            print(Fore.BLUE + frame, end="\r", flush=True)
            time.sleep(0.8)
        print(Fore.CYAN + "\nAll rested up! 🌞")
        pet = self.data[self.current_pet]
        pet["energy"] = min(MAX_STAT, pet["energy"] + 30)
        pet["hunger"] = max(0, pet["hunger"] - 10)
        self._gain_exp(8)
        self._random_event("sleep")
        self.save_data()

    def heal(self):
        if not self._ensure_selected(): return
        print(Fore.LIGHTGREEN_EX + f"\nHealing {self.current_pet} ✨")
        for frame in ["💖", "💫", "✨", "💫", "💖"]:
            print(Fore.LIGHTGREEN_EX + frame, end="\r", flush=True)
            time.sleep(0.35)
        print(Fore.LIGHTGREEN_EX + "\nFeeling much better now! ❤️‍🩹")
        pet = self.data[self.current_pet]
        pet["health"] = min(MAX_STAT, pet["health"] + 25)
        self._gain_exp(12)
        self._random_event("heal")
        self.save_data()

    def rename(self, old_name, new_name):
        old_name = old_name.strip()
        new_name = new_name.strip()
        if not old_name or not new_name:
            print(Fore.RED + "Both old and new name required.")
            return
        if old_name not in self.data:
            print(Fore.RED + "Pet not found.")
            return
        if new_name in self.data:
            print(Fore.RED + "New name already used by another pet.")
            return
        self.data[new_name] = self.data.pop(old_name)
        if self.current_pet == old_name:
            self.current_pet = new_name
        print(Fore.GREEN + f"Renamed '{old_name}' to '{new_name}' ✅")
        self.save_data()

    def delete(self, name):
        name = name.strip()
        if not name:
            print(Fore.RED + "Name required.")
            return
        if name not in self.data:
            print(Fore.RED + "Pet not found.")
            return
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
        save_data(self.data)

    # === internal helpers ===
    def _ensure_selected(self):
        if not self.current_pet:
            print(Fore.RED + "Select a pet first using 'select [name]'.")
            return False
        return True

    def _gain_exp(self, amount):
        pet = self.data[self.current_pet]
        pet["exp"] = pet.get("exp", 0) + amount
        leveled = False
        while pet["exp"] >= 100:
            pet["exp"] -= 100
            pet["level"] = pet.get("level", 1) + 1
            # small bonus on level-up
            pet["hunger"] = max(0, pet["hunger"] - 5)
            pet["happy"] = min(MAX_STAT, pet["happy"] + 5)
            leveled = True
        if leveled:
            print(Fore.CYAN + f"✨ {self.current_pet} leveled up! Now Lv {pet['level']} ✨")
        else:
            print(Fore.CYAN + f"{self.current_pet} gained {amount} EXP.")

    def _random_event(self, action):
        """Kadang muncul event lucu — bikin game terasa hidup."""
        chance = random.randint(1, 100)
        # contoh event kecil
        if action == "play" and chance <= 15:
            print(Fore.YELLOW + f"🎁 Lucky! {self.current_pet} found a toy and got +10 happy!")
            self.data[self.current_pet]["happy"] = min(MAX_STAT, self.data[self.current_pet]["happy"] + 10)
        elif action == "feed" and chance <= 10:
            print(Fore.MAGENTA + f"😮 Surprise! {self.current_pet} found a treat and +5 health!")
            self.data[self.current_pet]["health"] = min(MAX_STAT, self.data[self.current_pet]["health"] + 5)
        elif action == "sleep" and chance <= 12:
            print(Fore.BLUE + f"🌙 Dream event: {self.current_pet} had a happy dream (+8 happy)!")
            self.data[self.current_pet]["happy"] = min(MAX_STAT, self.data[self.current_pet]["happy"] + 8)
        # negatif event ketika energy/hunger buruk
        pet = self.data[self.current_pet]
        if pet["hunger"] <= 10 and random.randint(1,100) <= 8:
            print(Fore.RED + f"⚠️ {self.current_pet} is starving! Health -10.")
            pet["health"] = max(0, pet["health"] - 10)
