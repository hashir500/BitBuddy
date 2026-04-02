import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
from pet import Pet


BASE_SIZE = 400 
ANIMATION_SPEED = 4000

class TamagotchiApp:
    def __init__(self, root, pet):
        self.root = root
        self.pet = pet
        
       
        self.root.title("Desktop Dino")
        self.root.attributes('-topmost', True)
       
        self.root.geometry(f"{BASE_SIZE}x{BASE_SIZE + 100}+100+100") 
        self.root.resizable(False, False)
        self.root.config(bg="#2c3e50")

        
        self.img_obj = Image.open("idle.gif")
        self.frames = []
        
        for frame in ImageSequence.Iterator(self.img_obj):
           
            resized_frame = frame.copy().convert('RGBA').resize((BASE_SIZE, BASE_SIZE), Image.Resampling.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(resized_frame))
        
        self.frame_idx = 0

        
        self.anim_label = tk.Label(root, image=self.frames[0], bd=0, bg="#2c3e50")
        self.anim_label.pack()

        self.status_label = tk.Label(
            root, text=self.pet.get_status(),
            font=("Arial", 12, "bold"),
            fg="white", bg="#2c3e50",
            pady=5
        )
        self.status_label.pack(fill="x")

       
        btn_frame = tk.Frame(root, bg="#2c3e50")
        btn_frame.pack(fill="x", pady=5)

        tk.Button(btn_frame, text="FEED", command=self.feed_action, width=8).pack(side="left", padx=20)
        tk.Button(btn_frame, text="SLEEP", command=self.sleep_action, width=8).pack(side="right", padx=20)

        self.animate_gif()
        self.update_logic()

    def animate_gif(self):
        
        self.anim_label.config(image=self.frames[self.frame_idx])
        
       
        self.frame_idx = (self.frame_idx + 1) % len(self.frames)
        
        
        self.root.after(ANIMATION_SPEED, self.animate_gif)

    def update_logic(self):
        self.pet.time_passes()
        self.status_label.config(text=self.pet.get_status())
        self.root.after(5000, self.update_logic)

    def feed_action(self):
        self.pet.feed()
        self.status_label.config(text=self.pet.get_status())

    def sleep_action(self):
        self.pet.sleep()
        self.status_label.config(text=self.pet.get_status())

if __name__ == "__main__":
    root = tk.Tk()
    my_pet = Pet(name="Rex")
    app = TamagotchiApp(root, my_pet)
    root.mainloop()