import os
import psutil
import time
import tkinter as tk
from tkinter import filedialog
import random

# Dictionary that stores game exe as key and list of files to not delete as value
games_n_files = {}

# Function that prompts user to select game exe
def add_game_exe_to_dict():
    print("Select game exe")
    root = tk.Tk()
    root.withdraw()  # hide the Tkinter window
    exe_path = filedialog.askopenfilename()
    exe_name = os.path.basename(exe_path)
    print(f"Selected: {exe_path}")
    return exe_name

# Function that prompts user to select where saves are stored
def get_save_path():
    print("Select save folder")
    root = tk.Tk()
    root.withdraw()  # hide the Tkinter window
    folder_path = filedialog.askdirectory()
    return folder_path

# Function that prompts user to select any files to keep safe
def add_keep_files_to_dict():
    print("Select any files to keep safe")
    root = tk.Tk()
    root.withdraw()  # hide the Tkinter window
    file_paths = filedialog.askopenfilenames()
    for file in file_paths:
        file = os.path.basename(file)
    return file_paths

# Add both game exe and list of files to not delete to dictionary
def add_to_dict():
    game_exe = add_game_exe_to_dict()
    save_path = get_save_path()
    keep_files = add_keep_files_to_dict()
    games_n_files[game_exe] = [save_path, keep_files]
    print(games_n_files)

# Function that deletes saves
def delete_stuff_rev2(game):
    save_path = games_n_files[game][0]
    keep_files = [os.path.basename(file) for file in games_n_files[game][1]]
    for file in os.listdir(save_path):
        if file not in keep_files:
            file_path = os.path.join(save_path, file)
            os.remove(file_path)

# Check every second to see if game is running, game is a string, taken from dictionary key
def is_running():
    running = False
    while running == False:
        print("Game is not running, checking again in 1 second")
        time.sleep(1)
        progs = psutil.process_iter()
        for prog in progs:
            try:
                if prog.name() in games_n_files:
                    running = True
                    game = prog.name()
            except psutil.NoSuchProcess:
                pass  # skip terminated processes
    print(f"{game} detected, have fun!")
    return game

# Check every second to see if game is not running
def is_not_running(game):
    running = True
    while running == True:
        print("Game is still running, checking again every second")
        time.sleep(1)
        progs = psutil.process_iter()
        for prog in progs:
            try:
                if prog.name() == game:
                    running = True
                    break
            except psutil.NoSuchProcess:
                pass
        else:
            running = False
            print("Game is not running, deleting saves, get back in it!")

# Main function
def main():
    if games_n_files == {}:
        add_to_dict()
    while True:
        game = is_running()
        is_not_running(game)
        delete_stuff_rev2(game)

main()
