import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from pet import Pet

# --- CONFIGURATION ---
BASE_SIZE = 400 
ANIMATION_SPEED = 150 

class TamagotchiApp:
    def __init__(self, root, pet):
        self.root = root
        self.pet = pet
        
        # --- Window Setup ---
        self.root.title("Desktop Dino")
        self.root.attributes('-topmost', True)
        
        # Increased height to 700 to ensure the long 'Hiya' message fits!
        self.root.geometry(f"{BASE_SIZE}x700+100+100") 
        self.root.resizable(False, False)
        self.root.config(bg="#2c3e50")

        # --- Load GIF ---
        self.img_obj = Image.open("idle.gif")
        self.frames = [ImageTk.PhotoImage(frame.copy().convert('RGBA').resize((BASE_SIZE, BASE_SIZE), Image.Resampling.LANCZOS)) 
                       for frame in ImageSequence.Iterator(self.img_obj)]
        self.frame_idx = 0

        # --- UI Display (Using Grid for better control) ---
        
        # Row 0: THE IMAGE
        self.anim_label = tk.Label(root, image=self.frames[0], bd=0, bg="#2c3e50")
        self.anim_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Row 1: THE STATUS TEXT
        # Note: 'height=8' ensures the 5-6 lines of your get_status() are always visible
        self.status_label = tk.Label(
            root, text=self.pet.get_status(),
            font=("Courier", 10, "bold"),
            fg="#ecf0f1", bg="#34495e",
            padx=10, pady=10,
            justify="left",
            width=45,
            height=8 
        )
        self.status_label.grid(row=1, column=0, columnspan=3, padx=20, sticky="ew")

        # Row 2: THE BUTTONS
        btn_style = {"width": 10, "pady": 5, "font": ("Arial", 9, "bold")}
        
        tk.Button(root, text="FEED", command=self.feed_action, bg="#27ae60", **btn_style).grid(row=2, column=0, pady=20)
        tk.Button(root, text="PLAY", command=self.play_action, bg="#2980b9", **btn_style).grid(row=2, column=1, pady=20)
        tk.Button(root, text="SLEEP", command=self.sleep_action, bg="#8e44ad", **btn_style).grid(row=2, column=2, pady=20)

        self.animate_gif()
        self.update_logic()

    def animate_gif(self):
        self.anim_label.config(image=self.frames[self.frame_idx])
        self.frame_idx = (self.frame_idx + 1) % len(self.frames)
        self.root.after(ANIMATION_SPEED, self.animate_gif)

    def update_logic(self):
        self.pet.time_passes()
        # This keeps the main status updated every 5 seconds
        self.status_label.config(text=self.pet.get_status())
        self.root.after(5000, self.update_logic)

    # These actions now correctly show the custom message AND the stats
    def feed_action(self):
        success, msg = self.pet.feed()
        self.status_label.config(text=f"{msg}\n{'-'*30}\n{self.pet.get_status()}")

    def sleep_action(self):
        success, msg = self.pet.sleep()
        self.status_label.config(text=f"{msg}\n{'-'*30}\n{self.pet.get_status()}")

    def play_action(self):
        success, msg = self.pet.play()
        self.status_label.config(text=f"{msg}\n{'-'*30}\n{self.pet.get_status()}")

if __name__ == "__main__":
    root = tk.Tk()
    my_pet = Pet(name="Rex")
    app = TamagotchiApp(root, my_pet)
    root.mainloop()