import os
import tkinter as tk
from tkinter import ttk

import mpv


class MusicPlayerApp:
    def __init__(self, master):
        self.master = master
        master.title("Music Player")
        master.configure(bg="#494D64")  # Set background color

        self.player = mpv.MPV(
            ytdl=True,
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=False,
            vo=False,
        )

        self.label = tk.Label(
            master,
            text="KISS Music Player",
            bg="#494D64",
            fg="#A5ADCB",
            font=("Helvetica", 16),
            anchor="center",
        )
        self.label.pack(side=tk.TOP)

        self.label = tk.Label(
            master,
            text="Search for a song:",
            bg="#494D64",
            fg="#A5ADCB",
            anchor="w",
        )
        self.label.pack(side=tk.TOP)

        self.search_entry = tk.Entry(
            master, bg="#494D64", fg="#A6ADCB", insertbackground="#A5ADCB"
        )
        self.search_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.filter_music_list)

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.tab_latest = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.tab_alphabetical = ttk.Frame(self.notebook, style="Dark.TFrame")

        self.notebook.add(self.tab_latest, text="Latest Songs")
        self.notebook.add(self.tab_alphabetical, text="Alphabetical Order")

        self.music_listbox_latest = tk.Listbox(
            self.tab_latest,
            width=40,
            height=20,
            bg="#494D64",
            fg="#B8C0E0",
            selectbackground="#8AADF4",
            selectforeground="#494D64",
        )
        self.music_listbox_latest.pack(side=tk.LEFT, padx=10, pady=10)
        self.filtered_music_list_latest = []  # Corrected variable name
        self.populate_music_list_latest()
        self.music_listbox_latest.bind("<Double-1>", self.play_selected_music)
        self.music_listbox_latest.bind(
            "<Control-h>",
            lambda event: self.focus_list(event, self.music_listbox_latest),
        )

        self.music_listbox_alphabetical = tk.Listbox(
            self.tab_alphabetical,
            width=40,
            height=20,
            bg="#494D64",
            fg="#B8C0E0",
            selectbackground="#8AADF4",
            selectforeground="#494D64",
        )
        self.music_listbox_alphabetical.pack(side=tk.LEFT, padx=10, pady=10)
        self.filtered_music_list_alphabetical = []  # Corrected variable name
        self.populate_music_list_alphabetical()
        self.music_listbox_alphabetical.bind("<Double-1>", self.play_selected_music)
        self.music_listbox_alphabetical.bind(
            "<Control-h>",
            lambda event: self.focus_list(event, self.music_listbox_alphabetical),
        )

        self.play_pause_button = tk.Button(
            master,
            font=("Symbols Nerd Font", 12),
            text="",
            command=self.toggle_play_pause,
            bg="#494D64",
            fg="#A5ADCB",
        )
        self.play_pause_button.pack(side=tk.LEFT, padx=10, pady=10)
        master.bind("<space>", self.toggle_play_pause)

        self.stop_button = tk.Button(
            master, text="Stop", command=self.stop_music, bg="#494D64", fg="#A5ADCB"
        )
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.volume_scale = tk.Scale(
            master,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.set_volume,
            bg="#494D64",
            fg="#A5ADCB",
        )
        self.volume_scale.set(100)  # Default volume
        self.volume_scale.pack(side=tk.RIGHT, padx=10, pady=10)

        self.selected_file = None

    def populate_music_list_latest(self):
        music_directory = (
            os.path.expanduser("~/Music") if os.name == "posix" else "Music"
        )
        supported_formats = (".mp3", ".wav", ".flac", ".ogg")
        files_with_mtime = []
        for file in os.listdir(music_directory):
            if any(file.endswith(format) for format in supported_formats):
                file_path = os.path.join(music_directory, file)
                mtime = os.path.getmtime(file_path)
                files_with_mtime.append((file, mtime))
        files_with_mtime.sort(
            key=lambda x: x[1], reverse=True
        )  # Sort by modification time (latest first)
        for file, _ in files_with_mtime:
            self.music_listbox_latest.insert(tk.END, file)
            self.filtered_music_list_latest.append(file)  # Corrected variable name

    def populate_music_list_alphabetical(self):
        music_directory = (
            os.path.expanduser("~/Music") if os.name == "posix" else "Music"
        )
        supported_formats = (".mp3", ".wav", ".flac", ".ogg")
        files = [
            file
            for file in os.listdir(music_directory)
            if any(file.endswith(format) for format in supported_formats)
        ]
        files.sort()  # Sort alphabetically
        for file in files:
            self.music_listbox_alphabetical.insert(tk.END, file)
            self.filtered_music_list_alphabetical.append(
                file
            )  # Corrected variable name

    def toggle_play_pause(self, event=None):
        if self.selected_file:
            if self.player.pause:
                self.player.pause = False
                self.play_pause_button.config(text="󰏤")
            else:
                self.player.pause = True
                self.play_pause_button.config(text="")
        else:
            self.play_selected_music(
                None
            )  # Play the selected music file if not already playing

    def play_selected_music(self, event):
        selected_index = self.notebook.index("current")
        if selected_index == 0:  # Check if the 'Latest Songs' tab is selected
            listbox = self.music_listbox_latest
        else:
            listbox = self.music_listbox_alphabetical
        selected_index = listbox.curselection()
        if selected_index:
            self.selected_file = listbox.get(selected_index)
            music_directory = (
                os.path.expanduser("~/Music") if os.name == "posix" else "Music"
            )
            file_path = os.path.join(music_directory, self.selected_file)
            self.player.play(file_path)
            self.play_pause_button.config(text="󰏤")

    def stop_music(self):
        self.player.stop()
        self.selected_file = None
        self.play_pause_button.config(text="")

    def set_volume(self, volume):
        self.player.volume = int(volume)

    def filter_music_list(self, event):
        search_term = self.search_entry.get().lower()
        latest_listbox = self.music_listbox_latest
        alphabetical_listbox = self.music_listbox_alphabetical

        # Clear previous filtered lists
        latest_listbox.delete(0, tk.END)
        alphabetical_listbox.delete(0, tk.END)

        # Tokenize the search string
        search_tokens = search_term.split()

        # Filter latest music list
        for song in self.filtered_music_list_latest:
            match = True
            for token in search_tokens:
                if token not in song.lower():
                    match = False
                    break
            if match:
                latest_listbox.insert(tk.END, song)

        # Filter alphabetical music list
        for song in self.filtered_music_list_alphabetical:
            match = True
            for token in search_tokens:
                if token not in song.lower():
                    match = False
                    break
            if match:
                alphabetical_listbox.insert(tk.END, song)

    def focus_list(self, event, listbox):
        listbox.focus_set()

    def move_up(self, event):
        if self.search_entry != self.master.focus_get():
            self.music_listbox_latest.event_generate("<Up>")
            self.music_listbox_alphabetical.event_generate("<Up>")
        else:
            self.music_listbox_latest.focus_set()
            self.music_listbox_latest.event_generate("<Up>")
            self.music_listbox_alphabetical.focus_set()
            self.music_listbox_alphabetical.event_generate("<Up>")

    def move_down(self, event):
        if self.search_entry != self.master.focus_get():
            self.music_listbox_latest.event_generate("<Down>")
            self.music_listbox_alphabetical.event_generate("<Down>")
        else:
            self.music_listbox_latest.focus_set()
            self.music_listbox_latest.event_generate("<Down>")
            self.music_listbox_alphabetical.focus_set()
            self.music_listbox_alphabetical.event_generate("<Down>")

    def play_selected_music_on_enter(self, event):
        if self.master.focus_get() in [
            self.music_listbox_latest,
            self.music_listbox_alphabetical,
        ]:
            self.play_selected_music(event)


def main():
    root = tk.Tk()
    root.configure(bg="#494D64")  # Set background color
    style = ttk.Style(root)
    style.theme_use("clam")

    # Define dark mode colors
    dark_mode_colors = {
        "background": "#494D64",
        "foreground": "#A5ADCB",
        "selectBackground": "#8AADF4",
        "selectForeground": "#494D64",
    }

    # Configure style for dark mode
    style.configure("Dark.TFrame", background=dark_mode_colors["background"])

    app = MusicPlayerApp(root)
    root.bind("<Control-j>", app.move_down)
    root.bind("<Control-k>", app.move_up)
    root.bind("/", lambda event: app.search_entry.focus_set())
    root.bind("<Return>", app.play_selected_music_on_enter)
    root.mainloop()


if __name__ == "__main__":
    main()
