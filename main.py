import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from pet import Pet


WINDOW_SIZE = "400x600" 
GIF_SIZE = (380, 380)   
ICON_SIZE = (32, 32)    
BTN_DIAMETER = 48       

class BitBuddyTk:
    def __init__(self, pet):
        self.pet = pet
        self.root = tk.Tk()
        
        # 1. Window Styling
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry(WINDOW_SIZE)
        self.root.config(bg="#1a1a1a")

        # 2. Draggable Logic
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)

        # 3. Stats Display (Top Dashboard)
        self.stats_canvas = tk.Canvas(self.root, width=380, height=95, bg="#1a1a1a", highlightthickness=0)
        self.stats_canvas.pack(pady=(10, 0))

        # 4. Pet Animation Display
        self.canvas = tk.Label(self.root, bg="#1a1a1a", bd=0)
        self.canvas.pack(pady=5)
        
        self.frames = []
        self.current_frame = 0
        self.anim_loop_id = None 
        self.is_performing = False

        # 5. Button Row (Bottom)
        self.btn_frame = tk.Frame(self.root, bg="#1a1a1a")
        # pady=25 provides enough gap without being "too big"
        self.btn_frame.pack(side="bottom", pady=25)

        self.create_circular_buttons()

        # 6. Initialize
        self.load_animation("assets/idle.gif")
        self.update_loop() 
        self.root.mainloop()

    # --- UI RENDERING ---
    def make_circle_icon(self, color, icon_path):
        """Creates a circular background with a PNG overlay."""
        bg = Image.new("RGBA", (BTN_DIAMETER, BTN_DIAMETER), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bg)
        draw.ellipse((0, 0, BTN_DIAMETER-1, BTN_DIAMETER-1), fill=color)
        
        try:
            icon = Image.open(icon_path).convert("RGBA")
            icon = icon.resize(ICON_SIZE, Image.Resampling.LANCZOS)
            offset = ((BTN_DIAMETER - ICON_SIZE[0]) // 2, (BTN_DIAMETER - ICON_SIZE[1]) // 2)
            bg.paste(icon, offset, icon)
        except Exception as e:
            print(f"Error: Could not find {icon_path}")
        
        return ImageTk.PhotoImage(bg)

    def create_circular_buttons(self):
        self.icon_refs = {}
        btn_style = {
            "bg": "#1a1a1a",
            "activebackground": "#1a1a1a",
            "borderwidth": 0,
            "highlightthickness": 0,
            "cursor": "hand2"
        }

        # Button data mapping
        button_data = [
            ("feed", "assets/meat.png", "FEED", "assets/eat.gif"),
            ("play", "assets/play.png", "PLAY", "assets/play.gif"),
            ("sleep", "assets/sleep.png", "SLEEP", "assets/sleep.gif"),
            ("exit", "assets/exit.png", "EXIT", None)
        ]

        for i, (key, path, action, gif) in enumerate(button_data):
            self.icon_refs[key] = self.make_circle_icon("#262626", path)
            
            if action == "EXIT":
                btn = tk.Button(self.btn_frame, image=self.icon_refs[key], command=self.root.destroy, **btn_style)
            else:
                btn = tk.Button(self.btn_frame, image=self.icon_refs[key], 
                                command=lambda a=action, g=gif: self.handle_action(a, g), **btn_style)
            btn.grid(row=0, column=i, padx=10)

        # Revive Button
        self.icon_refs['rev_off'] = self.make_circle_icon("#262626", "assets/revive.png")
        self.btn_revive = tk.Button(self.btn_frame, image=self.icon_refs['rev_off'], 
                                    state="disabled", command=self.revive_pet, **btn_style)
        self.btn_revive.grid(row=0, column=4, padx=10)

    def draw_bars(self):
        self.stats_canvas.delete("all")
        BAR_WIDTH = 220
        START_X = 110
        BAR_HEIGHT = 4
        GAP = 16 # Slightly tighter gap

        def render_bar(index, label, value, color):
            y = 15 + (index * GAP)
            self.stats_canvas.create_text(40, y + 2, text=label, fill=color, font=("Courier", 8, "bold"), anchor="w")
            self.stats_canvas.create_rectangle(START_X, y, START_X + BAR_WIDTH, y + BAR_HEIGHT, fill="#262626", outline="")
            val = max(0, min(100, value))
            fill_w = START_X + (BAR_WIDTH * (val / 100))
            if val > 0:
                self.stats_canvas.create_rectangle(START_X, y, fill_w, y + BAR_HEIGHT, fill=color, outline="")

        render_bar(0, "HEALTH", self.pet.health, "#2ecc71")
        render_bar(1, "HUNGER", self.pet.hunger, "#e67e22")
        render_bar(2, "HAPPY", getattr(self.pet, 'happiness', 100), "#f1c40f")
        render_bar(3, "ENERGY", getattr(self.pet, 'energy', 100), "#9b59b6")

    def start_drag(self, event):
        self.x, self.y = event.x, event.y

    def do_drag(self, event):
        nx = self.root.winfo_x() + (event.x - self.x)
        ny = self.root.winfo_y() + (event.y - self.y)
        self.root.geometry(f"+{nx}+{ny}")

    def load_animation(self, path):
        if self.anim_loop_id: self.root.after_cancel(self.anim_loop_id)
        try:
            img = Image.open(path)
            self.frames = []
            while True:
                f = img.copy().resize(GIF_SIZE, Image.Resampling.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(f))
                img.seek(len(self.frames))
        except EOFError: pass
        self.current_frame = 0
        self.animate()

    def animate(self):
        if not self.frames: return
        self.canvas.config(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.anim_loop_id = self.root.after(100, self.animate)

    def handle_action(self, action, gif_path):
        if self.pet.get_condition() == "DEAD" or self.is_performing: return
        success = False
        if action == "FEED": success, _ = self.pet.feed()
        elif action == "PLAY": success, _ = self.pet.play()
        elif action == "SLEEP": success, _ = self.pet.sleep()
        if success:
            self.is_performing = True
            self.load_animation(gif_path)
            self.draw_bars()
            self.root.after(3500, self.end_action)

    def end_action(self):
        self.is_performing = False
        self.refresh_state()

    def update_loop(self):
        self.pet.time_passes()
        self.draw_bars()
        if not self.is_performing: self.refresh_state()
        self.root.after(4000, self.update_loop)

    def refresh_state(self):
        if self.pet.get_condition() == "DEAD":
            self.btn_revive.config(state="normal")
            self.load_animation("assets/dead.gif")
        else:
            self.btn_revive.config(state="disabled")
            if not self.is_performing: self.load_animation("assets/idle.gif")

    def revive_pet(self):
        self.pet.health, self.pet.hunger = 100, 50
        self.is_performing = False
        self.refresh_state()
        self.draw_bars()

if __name__ == "__main__":
    my_pet = Pet(name="BitBuddy")
    BitBuddyTk(my_pet)