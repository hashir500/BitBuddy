from dataclasses import dataclass
import time
import json
import os


@dataclass
class Pet:
    name : str = "Buddy"
    health: int = 100
    happiness: int = 100
    energy: int = 100
    hunger: int = 100
    hungerMax: int = 100
    energyMax: int = 100
    happinessMax: int = 100
    healthMax: int = 100
   
    
    def __post_init__(self,):
         self.initial_time = time.time()
         self.interval =1

    def get_status(self):
        # Determine the warning message based on current stats
        condition = self.get_condition()
        warning = ""
        
        if condition == "DEAD":
            warning = "REX HAS PASSED AWAY..."
        elif condition == "STARVING":
            warning = "I'm starving! Please feed me!"
        elif condition == "TIRED":
            warning = "I'm exhausted... I need sleep."
        elif condition == "SICK":
            warning = "I don't feel so good..."
        else:
            warning = f"Hiya! {self.name} here!"

        return (f"{warning}\n"
                f"{'-'*30}\n"
                f"Health:    {self.health}/{self.healthMax}\n"
                f"Hunger:    {self.hunger}/{self.hungerMax}\n"
                f"Energy:    {self.energy}/{self.energyMax}\n"
                f"Happiness: {self.happiness}/{self.happinessMax}")

    def time_passes(self):
        current_time = time.time()
        time_passed = current_time - self.initial_time

        if time_passed >= self.interval:
            chunk = int(time_passed // self.interval)
            
            #Passive Decay
            self.energy = max(0, self.energy - (5 * chunk))
            self.hunger = max(0, self.hunger - (5 * chunk))
            self.happiness = max(0, self.happiness - (3 * chunk))

            #Health Decay
            if self.hunger <= 0 or self.energy <= 0:
                self.health = max(0, self.health - (10 * chunk))
            
            #DEATH LOGIC
            if self.health <= 0:
                self.health = 0
                self.hunger = 0
                self.energy = 0
                self.happiness = 0
            
            self.initial_time += (chunk * self.interval)

    def feed(self):
        if self.health <= 0:
            return False, "It's too late... Rex is gone."
        
        elif self.hunger < self.hungerMax:
            self.hunger = min(self.hungerMax, self.hunger + 20)
            self.health = min(self.healthMax, self.health + 2)
            return True, "Thank you for the meal!"
        return False, "I'm too full to eat right now."

    def sleep(self):
        if self.health <= 0:
            return False, "It's too late... Rex is gone."
        
        elif self.energy < self.energyMax:
            self.energy = min(self.energyMax, self.energy + 40)
            self.hunger = max(0, self.hunger - 10)
            return True, "Zzz... Rex is feeling refreshed!"
        return False, "Not sleepy! I want to play!"
    
    def play(self):
        if self.health <= 0:
            return False, "It's too late... Rex is gone."
        
        elif self.energy >= 20:
            self.happiness = min(self.happinessMax, self.happiness + 15)
            self.energy = max(0, self.energy - 20)
            return True, "That was fun! Let's do it again."
        return False, "I'm too tired to play... let me sleep."
         

    def get_condition(self):
        if self.health <= 0: return "DEAD"
        if self.health < 30: return "SICK"
        if self.hunger < 20: return "STARVING"
        if self.energy < 20: return "TIRED"
        return "HAPPY"
    
    
   
def save_stats(self):
    stats = {
        "health": self.health,      # Use 'self' directly
        "hunger": self.hunger,
        "happiness": getattr(self, 'happiness', 100),
        "energy": getattr(self, 'energy', 100)
    }
    with open("pet_stats.json", "w") as f:
        json.dump(stats, f)

        
        
def load_stats(self):
        """Reads stats from the JSON file and updates the pet object."""
        if os.path.exists("pet_stats.json"):
            try:
                with open("pet_stats.json", "r") as f:
                    stats = json.load(f)
                
                self.pet.health = stats.get("health", 100)
                self.pet.hunger = stats.get("hunger", 50)
                
                if hasattr(self.pet, 'happiness'):
                    self.pet.happiness = stats.get("happiness", 100)
                if hasattr(self.pet, 'energy'):
                    self.pet.energy = stats.get("energy", 100)
                    
                print("Stats loaded successfully!")
            except Exception as e:
                print(f"Error loading stats: {e}")