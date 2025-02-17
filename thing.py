import os
import psutil
import time
import tkinter as tk
from tkinter import filedialog
import random
import configparser


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

# Function to check folder permissions
def check_perms(folder_path):
    if not os.access(folder_path, os.W_OK):
        #Make a tkinter dialogue to tell the user to fix permissions of that folder
        root = tk.Tk()
        root.withdraw()  # hide the Tkinter window
        tk.messagebox.showwarning("Error", "Before going any further, make sure the folder you selected has write permissions. If you don't know how to fix this, please check out the readme.")
    else:
        print("Sick. No permissions issues.")
        return True

# Function that prompts user to select where saves are stored
def get_save_path():
    print("Select save folder")
    root = tk.Tk()
    root.withdraw()  # hide the Tkinter window
    folder_path = filedialog.askdirectory()
    check_perms(folder_path)
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
def add_to_config():
    config = configparser.ConfigParser()
    config.read('games.cfg')  # read existing config file

    game_exe = add_game_exe_to_dict()
    save_path = get_save_path()
    keep_files = add_keep_files_to_dict()

    # create a new section in the config file for the game
    if not config.has_section(game_exe):
        config.add_section(game_exe)

    # set the values in the config file
    config.set(game_exe, 'save_path', save_path)
    config.set(game_exe, 'keep_files', ','.join(keep_files))  # store as comma-separated list

    # write the changes to the config file
    with open('games.cfg', 'w') as configfile:
        config.write(configfile)

    print("Config saved to games.cfg")

# Function that deletes saves
def delete_stuff_rev2(game):
    save_path = games_n_files[game][0]
    keep_files = [os.path.basename(file) for file in games_n_files[game][1]]
    for file in os.listdir(save_path):
        if file not in keep_files and not os.path.isdir(os.path.join(save_path, file)):
            file_path = os.path.join(save_path, file)
            os.remove(file_path)

# Check every second to see if game is running, game is a string, pulled from config file
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

# Get games that are already set up in games.cfg
def get_games():
    config = configparser.ConfigParser()
    config.read('games.cfg')
    for game in config.sections():
        save_path = config.get(game, 'save_path')
        keep_files = config.get(game, 'keep_files').split(',')
        games_n_files[game] = [save_path, keep_files]
    check_perms(save_path)


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
    config = configparser.ConfigParser()
    config.read('games.cfg')
    # Check if games.cfg exists, or if it's empty
    if not os.path.exists('games.cfg') or os.stat('games.cfg').st_size == 0:
        print("First time? Let's create a config file")
        add_to_config()
        get_games()
    else:
        # Ask player if they're running a game they've already set up, y/n
        # Ask using a tkinter dialog yes/no box
        root = tk.Tk()
        root.withdraw()  # hide the Tkinter window
        answer = tk.messagebox.askyesno("Do you want to run a game that you've already set up?")
        if answer == True:
            get_games()
        else:
            add_to_config()
            get_games()
    while True:
        game = is_running()
        is_not_running(game)
        delete_stuff_rev2(game)

main()
