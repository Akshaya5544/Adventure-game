import tkinter as tk
from tkinter import messagebox, ttk, Text, Frame, Label, Button, Entry
import textwrap

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.location = 'entrance'

    def move(self, new_location): self.location = new_location

class GameGUI:
    def __init__(self, root):
        self.root, self.player = root, None
        self.root.title("Adventure Game")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        self.rooms = {
            'entrance': {'description': 'You are at the entrance of a dark cave.Stalactites hang from the ceiling, and a cool breeze whispers from within.', 'exits': ['hallway']},
            'hallway': {'description': 'A long, narrow hallway stretches ahead. Torches flicker on the damp walls, casting dancing shadows.', 'exits': ['entrance', 'chamber']},
            'chamber': {'description': 'A grand chamber with flickering torches. Ancient symbols cover the walls, and a mysterious altar stands in the center.', 'exits': ['hallway']}
        }
        self.setup_gui()

    def setup_gui(self):
        self.title_frame, self.game_frame = Frame(self.root, bg='#2c3e50'), Frame(self.root, bg='#2c3e50')
        self.title_frame.pack(pady=20)
        self.game_frame.pack(expand=True, fill='both', padx=20)
        Label(self.title_frame, text="Adventure Game", font=("Helvetica", 24, "bold"), fg='#ecf0f1', bg='#2c3e50').pack()
        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.game_frame.winfo_children(): widget.destroy()
        login_frame = Frame(self.game_frame, bg='#34495e', padx=20, pady=20)
        login_frame.place(relx=0.5, rely=0.4, anchor='center')
        Label(login_frame, text="Enter your name:", font=("Helvetica", 12), fg='#ecf0f1', bg='#34495e').pack(pady=(0, 10))
        self.name_entry = Entry(login_frame, font=("Helvetica", 12), width=20)
        self.name_entry.pack(pady=(0, 20))
        Button(login_frame, text="Start Adventure", command=self.start_game, font=("Helvetica", 12), bg='#2ecc71', fg='white', padx=20, pady=10).pack()

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name: return messagebox.showwarning("Warning", "Please enter your name!")
        self.player = Player(name)
        self.show_game_screen()

    def show_game_screen(self):
        for widget in self.game_frame.winfo_children(): widget.destroy()
        left_frame = Frame(self.game_frame, bg='#34495e')
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        right_frame = Frame(self.game_frame, bg='#34495e')
        right_frame.pack(side='right', fill='both', padx=10, pady=10)
        
        self.description_text = Text(left_frame, wrap=tk.WORD, width=40, height=10, font=("Helvetica", 12), bg='#ecf0f1', padx=10, pady=10, state='disabled')
        self.description_text.pack(pady=(0, 20))
        movement_frame = Frame(right_frame, bg='#34495e')
        movement_frame.pack(pady=20)
        Label(movement_frame, text="Movement Options:", font=("Helvetica", 12, "bold"), fg='#ecf0f1', bg='#34495e').pack(pady=(0, 10))
        
        buttons_frame = Frame(right_frame, bg='#34495e')
        buttons_frame.pack(pady=20)
        Button(buttons_frame, text="Check Inventory", command=self.show_inventory, bg='#3498db', fg='white', font=("Helvetica", 10), padx=10, pady=5).pack(pady=5)
        Button(buttons_frame, text="Check Health", command=self.show_health, bg='#e74c3c', fg='white', font=("Helvetica", 10), padx=10, pady=5).pack(pady=5)
        Button(buttons_frame, text="Quit Game", command=self.quit_game, bg='#95a5a6', fg='white', font=("Helvetica", 10), padx=10, pady=5).pack(pady=5)
        
        self.movement_buttons_frame = Frame(movement_frame, bg='#34495e')
        self.movement_buttons_frame.pack()
        self.update_room_display()

    def update_room_display(self):
        room = self.rooms[self.player.location]
        description = textwrap.fill(room['description'], width=60)
        self.description_text.config(state='normal')
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, f"Location: {self.player.location.title()}\n\n{description}")
        self.description_text.config(state='disabled')
        
        for widget in self.movement_buttons_frame.winfo_children(): widget.destroy()
        for exit in room['exits']:
            Button(self.movement_buttons_frame, text=f"Go to {exit.title()}", command=lambda x=exit: self.move_player(x), bg='#2ecc71', fg='white', font=("Helvetica", 10), padx=10, pady=5).pack(pady=2)

    def move_player(self, destination):
        self.player.move(destination)
        self.update_room_display()

    def show_inventory(self):
        inventory_text = "Your inventory is empty." if not self.player.inventory else f"Inventory: {', '.join(self.player.inventory)}"
        messagebox.showinfo("Inventory", inventory_text)

    def show_health(self):
        messagebox.showinfo("Health Status", f"Health: {self.player.health}%")

    def quit_game(self):
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    game = GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
