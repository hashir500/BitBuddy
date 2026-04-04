import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from pet import Pet

BASE_SIZE = 400 
ANIMATION_SPEED = 150 

class TamagotchiApp:
    def __init__(self, root, pet):
        self.root = root
        self.pet = pet
        self.root.title("Desktop Dino")
        self.root.attributes('-topmost', True)
        self.root.geometry(f"{BASE_SIZE}x700+100+100") 
        self.root.config(bg="#2c3e50")

        # --- Sprite Manager ---
        self.current_frames = []
        self.frame_idx = 0
        self.is_busy = False # Prevents overlapping animations
        
        # Load the default animation immediately
        self.set_animation("assests/idle.gif")

        # --- UI Setup ---
        self.anim_label = tk.Label(root, image=self.current_frames[0], bd=0, bg="#2c3e50")
        self.anim_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.status_label = tk.Label(
            root, text=self.pet.get_status(),
            font=("Courier", 10, "bold"), fg="#ecf0f1", bg="#34495e",
            padx=10, pady=10, justify="left", width=45, height=8 
        )
        self.status_label.grid(row=1, column=0, columnspan=3, padx=20, sticky="ew")

        btn_style = {"width": 10, "pady": 5, "font": ("Arial", 9, "bold")}
        tk.Button(root, text="FEED", command=self.feed_action, bg="#27ae60", **btn_style).grid(row=2, column=0, pady=20)
        tk.Button(root, text="PLAY", command=self.play_action, bg="#2980b9", **btn_style).grid(row=2, column=1, pady=20)
        tk.Button(root, text="SLEEP", command=self.sleep_action, bg="#8e44ad", **btn_style).grid(row=2, column=2, pady=20)

        self.animate_loop()
        self.update_logic()

    def set_animation(self, filename):
        """Helper to load and switch GIFs on the fly."""
        try:
            img = Image.open(filename)
            self.current_frames = [
                ImageTk.PhotoImage(frame.copy().convert('RGBA').resize((BASE_SIZE, BASE_SIZE), Image.Resampling.LANCZOS)) 
                for frame in ImageSequence.Iterator(img)
            ]
            self.frame_idx = 0
        except:
            print(f"Could not load {filename}")

    def play_temp_animation(self, gif_file, duration_ms=3000):
        """Swaps to a GIF for a few seconds then goes back to idle/sick/dead."""
        self.is_busy = True
        self.set_animation(gif_file)
        self.root.after(duration_ms, self.reset_to_default)

    def reset_to_default(self):
        """Checks pet status and sets the correct background animation."""
        self.is_busy = False
        condition = self.pet.get_condition()
        if condition == "DEAD":
            self.set_animation("dead.gif")
        elif condition == "SICK":
            self.set_animation("sick.gif")
        else:
            self.set_animation("assests/idle.gif")

    def animate_loop(self):
        """The main loop that cycles frames."""
        if self.current_frames:
            self.anim_label.config(image=self.current_frames[self.frame_idx])
            self.frame_idx = (self.frame_idx + 1) % len(self.current_frames)
        
        # Don't loop if the pet is dead (unless dead.gif is an animation)
        if self.pet.get_condition() == "DEAD" and not self.is_busy:
            self.anim_label.config(image=self.current_frames[0])
            return 

        self.root.after(ANIMATION_SPEED, self.animate_loop)

    def update_logic(self):
        self.pet.time_passes()
        self.status_label.config(text=self.pet.get_status())
        
        # Auto-switch to sick/dead GIF if not currently performing an action
        if not self.is_busy:
            condition = self.pet.get_condition()
            if condition == "DEAD": self.set_animation("dead.gif")
            elif condition == "SICK": self.set_animation("sick.gif")
            
        self.root.after(5000, self.update_logic)

    def feed_action(self):
        success, msg = self.pet.feed()
        self.status_label.config(text=f"{msg}\n{self.pet.get_status()}")
        if success:
            self.play_temp_animation("assests/eat.gif")

    def sleep_action(self):
        success, msg = self.pet.sleep()
        self.status_label.config(text=f"{msg}\n{self.pet.get_status()}")
        if success:
            self.play_temp_animation("assests/sleep.gif", duration_ms=5000)

    def play_action(self):
        success, msg = self.pet.play()
        self.status_label.config(text=f"{msg}\n{self.pet.get_status()}")
        if success:
            self.play_temp_animation("assests/play.gif")

if __name__ == "__main__":
    root = tk.Tk()
    my_pet = Pet(name="Rex")
    app = TamagotchiApp(root, my_pet)
    root.mainloop()