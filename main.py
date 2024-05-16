import tkinter as tk
from tkinter import ttk, messagebox
import random
import os

class GuitarChordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Guitar Chord Display")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")

        self.chord_sets = {
            "Basic": ["A", "C", "D", "E", "G"],
            "Minor": ["Am", "Dm", "Em", "Bm"],
            "7th Chords": ["A7", "B7", "C7", "D7", "E7"]
        }
        self.selected_chord_sets = []
        self.chords = []
        self.current_chord_index = 0
        self.display_time = 2

        self.chord_images = self.load_chord_images()

        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        side_panel = ttk.Frame(main_frame, padding="10", relief=tk.RAISED, borderwidth=1)
        side_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.chord_set_listbox = tk.Listbox(side_panel, selectmode=tk.MULTIPLE, exportselection=False)
        for chord_set in self.chord_sets:
            self.chord_set_listbox.insert(tk.END, chord_set)
        self.chord_set_listbox.pack(pady=5)

        self.chord_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.chord_frame.pack(pady=20, expand=True, fill=tk.BOTH, side=tk.RIGHT)

        self.chord_label = tk.Label(self.chord_frame, text="", font=("Helvetica", 48), bg="#f0f0f0")
        self.chord_label.pack(pady=10)
        self.chord_image_label = tk.Label(self.chord_frame, bg="#f0f0f0")
        self.chord_image_label.pack(pady=10)

        tempo_frame = ttk.Frame(side_panel, padding="5")
        tempo_frame.pack(pady=10, fill=tk.X)

        self.tempo_label = ttk.Label(tempo_frame, text="Tempo (seconds):")
        self.tempo_label.pack(side=tk.LEFT, padx=5)
        
        self.tempo_slider = ttk.Scale(tempo_frame, from_=1, to=10, orient=tk.HORIZONTAL, command=self.update_display_time)
        self.tempo_slider.set(self.display_time)
        self.tempo_slider.config(to=180)
        self.tempo_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.bpm_label = ttk.Label(side_panel, text="BPM")
        self.bpm_label.pack(pady=5)
        self.bpm = 0

        button_frame = ttk.Frame(side_panel, padding="5")
        button_frame.pack(pady=10, fill=tk.X)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_display)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_display)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = ttk.Button(button_frame, text="Previous", command=self.show_previous_chord)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(button_frame, text="Next", command=self.show_next_chord)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.running = False

        self.chords_info_label = ttk.Label(side_panel, text="Current Set of Chords:")
        self.chords_info_label.pack(pady=5)
        self.current_chords_var = tk.StringVar()
        self.chords_label = ttk.Label(side_panel, textvariable=self.current_chords_var)
        self.chords_label.pack(pady=5)
        self.chord_set_listbox.bind("<<ListboxSelect>>", self.update_selected_chords)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=0)

    def load_chord_images(self):
        chord_images = {}
        for chord in self.chord_sets["Basic"] + self.chord_sets["Minor"] + self.chord_sets["7th Chords"]:
            image_path = os.path.join("images", f"{chord}.png")
            if os.path.exists(image_path):
                chord_images[chord] = tk.PhotoImage(file=image_path)
            else:
                chord_images[chord] = None
        return chord_images

    def update_display_time(self, value):
        # self.display_time = float(value)
        # self.bpm_label.config(text=f"BPM: {int(60 / self.display_time)}")
        self.bpm = round(float(value))  # Update BPM value
        self.display_time = 60 // self.bpm  # Calculate time interval per beat
        self.bpm_label.config(text=f"BPM: {self.bpm}")  # Update BPM label

    def start_display(self):
        try:
            # self.display_time = float(self.tempo_slider.get())
            self.bpm = int(self.tempo_slider.get())  # Get BPM from tempo slider
            self.display_time = 60 / self.bpm  # Calculate time interval per beat
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for display time.")
            return

        self.chords = []
        for index in self.chord_set_listbox.curselection():
            chord_set = self.chord_set_listbox.get(index)
            self.chords.extend(self.chord_sets[chord_set])
        random.shuffle(self.chords)
        self.current_chord_index = 0

        self.running = True
        self.display_chords()

    def stop_display(self):
        self.running = False

    def display_chords(self):
        if not self.running:
            return

        current_chord = self.chords[self.current_chord_index]
        self.chord_label.config(text=current_chord)
        self.chord_image_label.config(image=self.chord_images.get(current_chord))
        self.root.after(int(self.display_time * 1000), self.next_chord)

    def next_chord(self):
        if self.running:
            self.current_chord_index = (self.current_chord_index + 1) % len(self.chords)
            self.display_chords()

    def show_previous_chord(self):
        self.current_chord_index = (self.current_chord_index - 1) % len(self.chords)
        current_chord = self.chords[self.current_chord_index]
        self.chord_label.config(text=current_chord)
    
    def show_next_chord(self):
        """Show the next chord."""
        self.current_chord_index = (self.current_chord_index + 1) % len(self.chords)
        current_chord = self.chords[self.current_chord_index]
        self.chord_label.config(text=current_chord)
        self.chord_image_label.config(image=self.chord_images.get(current_chord))

    def on_set_select(self, event):
        """Handle selection of a different chord set from the combobox."""
        selected_set = self.chord_set_combo.get()
        if selected_set in self.chord_sets:
            self.current_chord_set = selected_set
            self.chords = self.chord_sets[selected_set]
            self.current_chord_index = 0
            current_chord = self.chords[self.current_chord_index]
            self.chord_label.config(text=current_chord)
            self.chord_image_label.config(image=self.chord_images.get(current_chord))
            if self.running:
                self.stop_display()

    def update_selected_chords(self, event):
        """Update the label to display the chords from the selected sets."""
        selected_chords = []
        for index in self.chord_set_listbox.curselection():
            chord_set = self.chord_set_listbox.get(index)
            selected_chords.extend(self.chord_sets[chord_set])
        self.current_chords_var.set(", ".join(selected_chords))

if __name__ == "__main__":
    root = tk.Tk()
    app = GuitarChordApp(root)
    root.mainloop()
