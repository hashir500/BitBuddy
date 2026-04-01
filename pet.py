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
    initial_time :int = time.time()
    interval:int = 7200
    

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

                chunk = int(time_passed//self.interval)
                self.energy-=5 * chunk
                self.health-=5 * chunk
                self.hunger-=5 * chunk
                self.happiness-=5 * chunk

                self.initial_time += (chunk * self.interval)
        

                self.energy = max(0, self.energy)
                self.health = max(0, self.health)
                self.hunger = max(0, self.hunger)
                self.happiness = max(0, self.happiness)
        

        
        
def main():
    p1 = Pet(name='Buddy')
    status = p1.time_passes()
    print(status)

main()