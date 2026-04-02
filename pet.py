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
         self.interval =7200

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

    def feed(self):
            
            if self.hunger == self.hungerMax:
                print(f"I am full")
                return
    
            print(f"Feeding {self.name}")
            self.hunger += 10
            self.happiness +=2
            

            if self.hunger >= self.hungerMax:
                self.hunger = self.hungerMax

            if self.happiness >= self.happinessMax:
                self.happiness = self.happinessMax 

            print(f"Thank you for the meal!")
            


    def sleep(self):
            print("Going to sleep, Bye!")
            self.energy = min(self.energyMax,self.energy + 10)
            self.hunger = max(0,self.hunger - 5)
            self.happiness = min(self.happinessMax,self.happiness + 5)
            print("I am back now, missed me?")
         
        
        
def main():
   p1 = Pet(name='Buddy')
   p1.time_passes() 
   print(p1.get_status())

main()