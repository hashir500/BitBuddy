from dataclasses import dataclass
import time

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
        return (f"""Hiya! {self.name} here, here are my stats:\n
    Health: {self.health} / {self.healthMax} 
    Hunger: {self.hunger} / {self.hungerMax} 
    Energy: {self.energy} / {self.energyMax} 
    Happiness: {self.happiness} / {self.happinessMax} 
            
            """)

    def time_passes(self):
        current_time = time.time()
        time_passed = current_time - self.initial_time

        if time_passed >= self.interval:
            chunk = int(time_passed // self.interval)
            
           
            self.energy = max(0, self.energy - (5 * chunk))
            self.hunger = max(0, self.hunger - (5 * chunk))
            self.happiness = max(0, self.happiness - (3 * chunk))

            
            if self.hunger <= 0 or self.energy <= 0:
                self.health = max(0, self.health - (10 * chunk))
            
            
            self.initial_time += (chunk * self.interval)

    def feed(self):
        if self.hunger < self.hungerMax:
            self.hunger = min(self.hungerMax, self.hunger + 20)
            self.health = min(self.healthMax, self.health + 2)
            return True, "Thank you for the meal!"
        return False, "I'm too full to eat right now."

    def sleep(self):
        if self.energy < self.energyMax:
            self.energy = min(self.energyMax, self.energy + 40)
            self.hunger = max(0, self.hunger - 10)
            return True, "Zzz... Rex is feeling refreshed!"
        return False, "Not sleepy! I want to play!"
    
    def play(self):
        if self.energy >= 20:
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
        
        
