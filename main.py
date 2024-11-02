import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from pygame import mixer
import os
import random
import io

# Initialize the mixer for music
mixer.init()

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player with Album Art and Playlist")
        self.root.geometry("700x600")

        # Set the directory where the button images are located
        img_dir = "C:/Users/SK MUSTAKIM ALI/Desktop/Programming files/Music Player/"
        self.default_album_art_path = "C:/Users/SK MUSTAKIM ALI/Desktop/Programming files/Music Player/music.png"

        # Load button images for play, pause, previous, next, repeat, stop, and shuffle
        self.play_image = ImageTk.PhotoImage(Image.open(img_dir + "play.png").resize((50, 50)))
        self.pause_image = ImageTk.PhotoImage(Image.open(img_dir + "pause.png").resize((50, 50)))
        self.prev_image = ImageTk.PhotoImage(Image.open(img_dir + "previous.png").resize((50, 50)))
        self.next_image = ImageTk.PhotoImage(Image.open(img_dir + "next.png").resize((50, 50)))
        self.repeat_image = ImageTk.PhotoImage(Image.open(img_dir + "repeate.png").resize((50, 50)))
        self.stop_image = ImageTk.PhotoImage(Image.open(img_dir + "stop.png").resize((50, 50)))
        self.shuffle_image = ImageTk.PhotoImage(Image.open(img_dir + "shuffel.png").resize((50, 50)))

        # Variables to store playlist and player state
        self.playlist = []
        self.current_song_index = 0
        self.is_playing = False
        self.is_shuffling = False
        self.is_repeating = False
        self.song_length = 0

        # Playlist listbox
        self.playlist_box = tk.Listbox(self.root, selectmode=tk.SINGLE, width=40, height=10, font=("Arial", 12))
        self.playlist_box.pack(pady=10)
        self.playlist_box.bind('<Double-1>', self.play_selected_track)

        # Label to show track info and album art
        self.track_label = tk.Label(self.root, text="No track selected", font=("Arial", 14))
        self.track_label.pack(pady=10)
        
        self.album_art_label = tk.Label(self.root)
        self.album_art_label.pack(pady=10)

        # Control buttons
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=10)

        self.play_button = tk.Button(self.controls_frame, image=self.play_image, command=self.play_pause)
        self.play_button.grid(row=0, column=1, padx=5)

        self.stop_button = tk.Button(self.controls_frame, image=self.stop_image, command=self.stop)
        self.stop_button.grid(row=0, column=2, padx=5)

        self.next_button = tk.Button(self.controls_frame, image=self.next_image, command=self.next_track)
        self.next_button.grid(row=0, column=3, padx=5)

        self.prev_button = tk.Button(self.controls_frame, image=self.prev_image, command=self.prev_track)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.shuffle_button = tk.Button(self.controls_frame, image=self.shuffle_image, command=self.toggle_shuffle)
        self.shuffle_button.grid(row=0, column=4, padx=5)

        self.repeat_button = tk.Button(self.controls_frame, image=self.repeat_image, command=self.toggle_repeat)
        self.repeat_button.grid(row=0, column=5, padx=5)

        # Volume control next to repeat button
        self.volume_scale = tk.Scale(self.controls_frame, from_=100, to=0, orient="vertical", label="Volume", command=self.set_volume)
        self.volume_scale.set(100)
        self.volume_scale.grid(row=0, column=6, padx=5)

        # Time display with slider
        self.time_frame = tk.Frame(self.root)
        self.time_frame.pack(pady=5)

        self.current_time_label = tk.Label(self.time_frame, text="00:00", font=("Arial", 10))
        self.current_time_label.pack(side=tk.LEFT)

        self.time_slider = tk.Scale(self.time_frame, from_=0, to=100, orient="horizontal", length=300, command=self.seek)
        self.time_slider.pack(side=tk.LEFT, fill="x", expand=True)

        self.total_time_label = tk.Label(self.time_frame, text="00:00", font=("Arial", 10))
        self.total_time_label.pack(side=tk.RIGHT)

        # Load button for songs
        self.load_button = tk.Button(self.root, text="Load Songs", command=self.load_songs)
        self.load_button.pack(pady=5)

        # Continuously update the time slider
        self.update_slider()

    def load_songs(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if files:
            for file in files:
                self.playlist.append(file)
                self.playlist_box.insert(tk.END, os.path.basename(file))
            if len(self.playlist) == len(files):
                self.current_song_index = 0
                self.update_track_label()

    def update_track_label(self):
        if self.playlist:
            song_name = os.path.basename(self.playlist[self.current_song_index])
            self.track_label.config(text=song_name)
            self.show_album_art(self.playlist[self.current_song_index])
        else:
            self.track_label.config(text="No track selected")
            self.album_art_label.config(image='')

    def show_album_art(self, song_path):
        try:
            audio = MP3(song_path, ID3=ID3)
            for tag in audio.tags.values():
                if isinstance(tag, APIC):
                    image_data = tag.data
                    image = Image.open(io.BytesIO(image_data))
                    image = image.resize((200, 200))
                    album_art = ImageTk.PhotoImage(image)
                    self.album_art_label.config(image=album_art)
                    self.album_art_label.image = album_art
                    return
            raise ValueError("No album art found")
        except (UnidentifiedImageError, AttributeError, ValueError, FileNotFoundError):
            default_image = Image.open(self.default_album_art_path).resize((200, 200))
            default_album_art = ImageTk.PhotoImage(default_image)
            self.album_art_label.config(image=default_album_art)
            self.album_art_label.image = default_album_art

    def play_pause(self):
        if self.is_playing:
            mixer.music.pause()
            self.play_button.config(image=self.play_image)
            self.is_playing = False
        else:
            if not mixer.music.get_busy():
                if self.playlist:
                    mixer.music.load(self.playlist[self.current_song_index])
                    mixer.music.play()
                    self.song_length = int(MP3(self.playlist[self.current_song_index]).info.length)
                    self.time_slider.config(to=self.song_length)
                    mins, secs = divmod(self.song_length, 60)
                    self.total_time_label.config(text=f"{mins}:{secs:02}")
            else:
                mixer.music.unpause()
            self.play_button.config(image=self.pause_image)
            self.is_playing = True

    def stop(self):
        mixer.music.stop()
        self.play_button.config(image=self.play_image)
        self.is_playing = False

    def next_track(self):
        if self.playlist:
            # Check if shuffle mode is on to choose the next song randomly
            if self.is_shuffling:
                self.current_song_index = random.randint(0, len(self.playlist) - 1)
            else:
                self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            
            self.play_selected_track()
        
    def prev_track(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.play_selected_track()

    def play_selected_track(self, event=None):
        if event:
            self.current_song_index = self.playlist_box.curselection()[0]
        self.stop()
        mixer.music.load(self.playlist[self.current_song_index])
        mixer.music.play()
        self.song_length = int(MP3(self.playlist[self.current_song_index]).info.length)
        self.time_slider.config(to=self.song_length)
        mins, secs = divmod(self.song_length, 60)
        self.total_time_label.config(text=f"{mins}:{secs:02}")
        self.update_track_label()
        self.play_button.config(image=self.pause_image)
        self.is_playing = True

    def toggle_shuffle(self):
        # Toggle shuffle state and update button appearance
        self.is_shuffling = not self.is_shuffling
        self.shuffle_button.config(relief="sunken" if self.is_shuffling else "raised")

    def toggle_repeat(self):
        self.is_repeating = not self.is_repeating
        self.repeat_button.config(relief="sunken" if self.is_repeating else "raised")

    def seek(self, value):
        if mixer.music.get_busy():
            mixer.music.set_pos(float(value))
            mins, secs = divmod(int(float(value)), 60)
            self.current_time_label.config(text=f"{mins}:{secs:02}")

    def set_volume(self, value):
        volume = int(value) / 100
        mixer.music.set_volume(volume)

    def update_slider(self):
        if mixer.music.get_busy():
            current_time = mixer.music.get_pos() / 1000
            self.time_slider.set(current_time)
            mins, secs = divmod(int(current_time), 60)
            self.current_time_label.config(text=f"{mins}:{secs:02}")
            
            if self.is_repeating and current_time >= self.song_length:
                self.play_selected_track()
        elif not self.is_repeating and self.is_playing:
            if self.current_song_index < len(self.playlist) - 1:
                self.next_track()
        self.root.after(1000, self.update_slider)


if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()
