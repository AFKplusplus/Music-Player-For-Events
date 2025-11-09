########## IMPORTS ##########

# Tkinter imports
import tkinter as tk # Basic
import tkinter.font # Fonts
from tkinter import ttk # Scrollbar
from tkinter.filedialog import askopenfilename # Add songs popup

# Other imports
from os import listdir # Get songs
import random # Shuffle songs
import pygame # Play songs
import shutil # Add songs

########## INITIALIZATIONS ##########
win = tk.Tk()
pygame.init()

########## FRONTEND VARIABLES #####
dark_blue = "#01161e"
blue = "#124559"
light_blue = "#598392"
white = "#aec3b0"
consolas = tkinter.font.Font(family="Consolas", size=15)
small_consolas = tkinter.font.Font(family="Consolas", size=11)
add_s = ""

########## BACKEND VARIABLES ##########
song_dictionary = {}
current_song_name = ""
current_song_idx = 0
song_folder_path = "songs\\"
end_music_check = pygame.USEREVENT + 1

########## WINDOW INFORMATION ##########
win.title("AFK's Music Player")
win.geometry("1280x720")
win.iconbitmap("icon.ico")
win.configure(bg=dark_blue)

# Maximum and minimum size window can be resized to
win.minsize(960, 540)
win.maxsize(1280, 720)

########## WIDGETS ##########
title = tk.Label(win, text="AFK's Music Player", fg = blue, bg = dark_blue, font = ("Consolas", 50, "bold"))
title.pack()

# Label for checking if paused
paused = tk.Label(win, text = "Song player for projects", fg = blue, bg = dark_blue, font = consolas)
paused.pack()

# Label for song amount
song_length = tk.Label(win, text = f"{len(song_dictionary)} song{add_s} loaded", fg = blue, bg = dark_blue, font = consolas)
song_length.pack()

# Frame to store all song file buttons
song_button_frame = tk.Frame(win, bg=dark_blue)
song_button_frame.pack()

# Freame to store all song buttons
button_frame = tk.Frame(win, bg=dark_blue)
button_frame.pack()

# Frame to store all songs and the canvas with scroll bar and totally not AI generated what who would say that
parent_song_frame = tk.Frame(win, bg=dark_blue)
parent_song_frame.pack(fill=tk.BOTH, expand=True)

parent_song_canvas = tk.Canvas(parent_song_frame, bg=dark_blue, highlightthickness=0)
parent_song_canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

scrollbar = ttk.Scrollbar(parent_song_frame, orient="vertical", command=parent_song_canvas.yview)
scrollbar.pack(side="right", fill="y")

song_frame = tk.Frame(parent_song_canvas, bg=dark_blue)
song_frame.bind("<Configure>", lambda event: parent_song_canvas.configure(yscrollcommand=scrollbar.set, scrollregion=parent_song_canvas.bbox("all")))

center_x = song_frame.winfo_screenwidth() / 2
center_y = song_frame.winfo_screenheight() / 2
parent_song_canvas.create_window((center_x, center_y), window=song_frame, anchor="n")

def on_mouse_wheel(event):
    parent_song_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

parent_song_canvas.bind_all("<MouseWheel>", on_mouse_wheel)

def load_songs(event):
    global song_dictionary, current_song_idx, current_song_name

    # Clear all labels and destroy them from song_dict
    for label in song_dictionary.values():
        label.destroy()
    song_dictionary.clear()

    # Reset the current song index and name
    current_song_name = ""
    current_song_idx = 0

    # Get every song in the songs folder
    song_name_list = listdir(song_folder_path)

    for name in song_name_list:
        song_name = name[:len(name)-4] # Remove the .mp3 at the end of the filename
        song_dictionary[song_name] = tk.Label(song_frame, text=song_name, fg = light_blue, bg = dark_blue, font = small_consolas)
        song_dictionary[song_name].pack(side=tk.TOP)
    
    # Turn off event so that the song stops
    pygame.mixer.music.set_endevent()
    pygame.mixer.music.stop()

def shuffle_songs(event):
    global song_dictionary, current_song_idx

    # Return if the song dictionary is empty
    if song_dictionary == {}: return

    # Destroy all labels from song_dict
    for label in song_dictionary.values():
        label.destroy()

    # Shuffle the keys
    items = list(song_dictionary.keys())
    random.shuffle(items)
    song_dictionary.clear()

    # Recreate the labels
    for idx, song in enumerate(items):
        if song == current_song_name:
            # Highlight the name
            song_dictionary[song] = tk.Label(song_frame, text=song, fg = blue, bg = light_blue, font = small_consolas)

            # Set the current song index to this song's index
            #current_song_idx = len(items) - idx - 1
            current_song_idx = idx
        else:
            song_dictionary[song] = tk.Label(song_frame, text=song, fg = light_blue, bg = dark_blue, font = small_consolas)
        song_dictionary[song].pack(side=tk.TOP)
    
def clear_songs(event):
    global song_dictionary

    # Destroy all labels from song_dict and clear it
    for label in song_dictionary.values():
        label.destroy()
    song_dictionary.clear()

    # Turn off event so that the song stops
    pygame.mixer.music.set_endevent()
    pygame.mixer.music.stop()

def play_songs(event):
    global current_song_name, current_song_idx, song_dictionary

    # Return if the song dictionary is empty
    if song_dictionary == {}: return

    if song_dictionary != {}:
        # List of song names
        song_list = list(song_dictionary.keys())

        # The song name of the current song index
        #current_song_name = song_list[len(song_list) - current_song_idx - 1]
        current_song_name = song_list[current_song_idx]

        # The song to play
        current_song_file = song_folder_path + current_song_name + ".mp3"
        song_dictionary[current_song_name].config(fg = blue, bg = light_blue)

        # Mixer initialize and loading, aswell as playing and adding a check at the end of the song
        pygame.mixer.init()
        pygame.mixer.music.load(current_song_file)
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(end_music_check)

def stop_songs(event):
    global song_dictionary

    # Return if the song dictionary is empty
    if song_dictionary == {}: return

    # List of song names
    song_list = list(song_dictionary.keys())
    for song in song_list:
        # Highlight the label
        song_dictionary[song].config(fg = light_blue, bg = dark_blue)
    
    # Turn off event so that the song doesn't continue and stop
    pygame.mixer.music.set_endevent()
    pygame.mixer.music.stop()

def skip_songs(event):
    global song_dictionary

    # Return if the song dictionary is empty
    if song_dictionary == {}: return

    # Set the label back to normal
    song_dictionary[current_song_name].config(fg = light_blue, bg = dark_blue)

    # Stop the current song and skip to the next
    pygame.mixer.music.stop()

def previous_songs(event):
    global song_dictionary, current_song_idx

    # Return if the song dictionary is empty
    if song_dictionary == {}: return

    # Set the label back to normal
    song_dictionary[current_song_name].config(fg = light_blue, bg = dark_blue)

    # Stop the current song and skip to the previous
    current_song_idx -= 2
    if current_song_idx < -1:
        current_song_idx = len(song_dictionary) - 2
    pygame.mixer.music.stop()

def pause_songs(event):

    # Return if the song dictionary is empty
    if song_dictionary == {}: return

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

        # Set paused label to "paused"
        paused.config(text = "Song Paused")
    else:
        pygame.mixer.music.unpause()

        # Set paused label to original
        paused.config(text = "Song player for projects")

def restart_songs(event):
    global current_song_idx

    # Return if the song dictionary is empty
    if song_dictionary == {}: return

    # Set the label back to normal
    song_dictionary[current_song_name].config(fg = light_blue, bg = dark_blue)

    current_song_idx = 0
    play_songs("not need bruh")

load_song = tk.Button(song_button_frame, text="Load Songs", width=15, height=2, bg=dark_blue, fg=light_blue, activebackground=light_blue, activeforeground=white, font=consolas)
load_song.pack(side=tk.LEFT, padx=10)
load_song.bind("<Button-1>", load_songs)

shuffle_song = tk.Button(song_button_frame, text="Shuffle Songs", width=15, height=2, bg=dark_blue, fg=light_blue, activebackground=light_blue, activeforeground=white, font=consolas)
shuffle_song.pack(side=tk.LEFT, padx=10)
shuffle_song.bind("<Button-1>", shuffle_songs)

clear_song = tk.Button(song_button_frame, text="Clear Songs", width=15, height=2, bg=dark_blue, fg=light_blue, activebackground=light_blue, activeforeground=white, font=consolas)
clear_song.pack(side=tk.LEFT, padx=10)
clear_song.bind("<Button-1>", clear_songs)

play_song = tk.Button(button_frame, text="Play Song", width=15, height=2, bg=dark_blue, fg=light_blue, activebackground=light_blue, activeforeground=white, font=consolas)
play_song.pack(side=tk.LEFT, padx=10)
play_song.bind("<Button-1>", play_songs)

pause_song = tk.Button(button_frame, text="Pause/Resume Song", width=20, height=2, bg=dark_blue, fg=light_blue, activebackground=light_blue, activeforeground=white, font=consolas)
pause_song.pack(side=tk.LEFT, padx=10)
pause_song.bind("<Button-1>", pause_songs)

stop_song = tk.Button(button_frame, text="Stop Song", width=15, height=2, bg=dark_blue, fg=light_blue, activebackground=light_blue, activeforeground=white, font=consolas)
stop_song.pack(side=tk.LEFT, padx=10)
stop_song.bind("<Button-1>", stop_songs)

previous_song = tk.Button(button_frame, text="Previous Song", width=15, height=2, bg=dark_blue, fg=light_blue, activebackground=light_blue, activeforeground=white, font=consolas)
previous_song.pack(side=tk.LEFT, padx=10)
previous_song.bind("<Button-1>", previous_songs)

skip_song = tk.Button(button_frame, text="Skip Song", width=15, height=2, bg=dark_blue, fg=light_blue, activebackground=light_blue, activeforeground=white, font=consolas)
skip_song.pack(side=tk.LEFT, padx=10)
skip_song.bind("<Button-1>", skip_songs)

restart_song = tk.Button(button_frame, text="Restart", width=15, height=2, bg=dark_blue, fg=light_blue, activebackground=light_blue, activeforeground=white, font=consolas)
restart_song.pack(side=tk.LEFT, padx=10)
restart_song.bind("<Button-1>", restart_songs)

def check_pygame_events():
    global current_song_idx, song_dictionary

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Destroy the application
            win.destroy()
        elif event.type == end_music_check:
            # Increment the current song index
            current_song_idx += 1
            
            # If the current song index is overflowing
            if current_song_idx >= len(song_dictionary):
                # Reset the counter (loop back to the start)
                current_song_idx = 0
            
            # Set the label back to normal
            song_dictionary[current_song_name].config(fg = light_blue, bg = dark_blue)

            play_songs("not need smh")
    
    add_s = ""
    if len(song_dictionary) != 1: 
        add_s = "s"
    song_length.configure(text = f"{len(song_dictionary)} song{add_s} loaded")

    win.after(100, check_pygame_events)

check_pygame_events()

win.mainloop()
pygame.quit()
