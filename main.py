import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from pet import Pet

# Standard GIF speed is usually between 50ms and 150ms
BASE_SIZE = 400 
ANIMATION_SPEED = 100 

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
        self.current_anim_file = None  # Track what is currently playing
        self.is_busy = False           # Prevents overlapping animations
        
        # Load the default animation immediately
        self.set_animation("assets/idle.gif")

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

        # Start loops
        self.animate_loop()
        self.update_logic()

    def set_animation(self, filename):
        """Helper to load and switch GIFs. Only reloads if the file is different."""
        if self.current_anim_file == filename:
            return # Already playing this animation, don't reset it!

        try:
            img = Image.open(filename)
            self.current_frames = [
                ImageTk.PhotoImage(frame.copy().convert('RGBA').resize((BASE_SIZE, BASE_SIZE), Image.Resampling.LANCZOS)) 
                for frame in ImageSequence.Iterator(img)
            ]
            self.frame_idx = 0
            self.current_anim_file = filename
        except Exception as e:
            print(f"Could not load {filename}: {e}")

    def play_temp_animation(self, gif_file, duration_ms=3000):
        """Swaps to an action GIF then returns to state-based animation."""
        self.is_busy = True
        self.set_animation(gif_file)
        self.root.after(duration_ms, self.reset_to_default)

    def reset_to_default(self):
        """Resumes background animation based on current health/life."""
        self.is_busy = False
        condition = self.pet.get_condition()
        if condition == "DEAD":
            self.set_animation("assets/dead.gif")
        elif condition == "SICK":
            self.set_animation("assets/sick.gif")
        else:
            self.set_animation("assets/idle.gif")

    def animate_loop(self):
        """Cycles through the frames of the current animation."""
        if self.current_frames:
            self.anim_label.config(image=self.current_frames[self.frame_idx])
            self.frame_idx = (self.frame_idx + 1) % len(self.current_frames)
            
            # Special case: If dead and not performing a temp action, 
            # stop at the last frame of the death animation (e.g., the grave).
            if self.pet.get_condition() == "DEAD" and not self.is_busy:
                if self.frame_idx == 0: # We just finished the loop
                    self.anim_label.config(image=self.current_frames[-1])
                    return # Stop the loop here

        self.root.after(ANIMATION_SPEED, self.animate_loop)

    def update_logic(self):
        """Handles pet decay and background state switching."""
        self.pet.time_passes()
        self.status_label.config(text=self.pet.get_status())
        
        # Auto-switch background animation if not busy playing a specific action
        if not self.is_busy:
            condition = self.pet.get_condition()
            if condition == "DEAD": 
                self.set_animation("assets/dead.gif")
            elif condition == "SICK": 
                self.set_animation("assets/sick.gif")
            else:
                self.set_animation("assets/idle.gif")
            
        # Check logic every 5 seconds
        self.root.after(5000, self.update_logic)

    def feed_action(self):
        if self.pet.get_condition() == "DEAD": return
        success, msg = self.pet.feed()
        self.status_label.config(text=f"{msg}\n{self.pet.get_status()}")
        if success:
            self.play_temp_animation("assets/eat.gif")

    def play_action(self):
        if self.pet.get_condition() == "DEAD": return
        success, msg = self.pet.play()
        self.status_label.config(text=f"{msg}\n{self.pet.get_status()}")
        if success:
            self.play_temp_animation("assets/play.gif")

    def sleep_action(self):
        if self.pet.get_condition() == "DEAD": return
        success, msg = self.pet.sleep()
        self.status_label.config(text=f"{msg}\n{self.pet.get_status()}")
        if success:
            # Sleep usually takes longer
            self.play_temp_animation("assets/sleep.gif", duration_ms=5000)

if __name__ == "__main__":
    root = tk.Tk()
    my_pet = Pet(name="Rex")
    app = TamagotchiApp(root, my_pet)
    root.mainloop()