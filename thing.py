import os
import psutil
import time
import tkinter as tk
from tkinter import filedialog
import random # For random messages to not be boring about the console spam every second
import configparser
import shutil
from halo import Halo
from quotes_library import *

# Dictionary that stores game exe as key and list of files to not delete as value
games_n_files = {}
floor_it = False

# Floor it? (automatically confirm everything for this session)
import tkinter as tk

root = tk.Tk()
root.withdraw()  # Hide the main window

def floor_it(title, message, yes_label="Yes", no_label="No"):
    result = [None]
    dialog = tk.Toplevel()
    dialog.title(title)

    def yes():
        result[0] = True
        dialog.destroy()
    def no():
        result[0] = False
        dialog.destroy()

     # Add some padding around the edges of the dialog
    frame = tk.Frame(dialog, padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    # Create a label with the message, and add some padding around it
    label = tk.Label(frame, text=message, wraplength=400)
    label.pack(pady=10)

    # Create a frame to hold the buttons, and add some padding around it
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=10)

    yes_button = tk.Button(dialog, text=yes_label, command=yes)
    yes_button.pack(side=tk.LEFT, padx=10)

    no_button = tk.Button(dialog, text=no_label, command=no)
    no_button.pack(side=tk.LEFT, padx=10)

    dialog.update_idletasks()
    dialog.geometry("+%d+%d" % ((dialog.winfo_screenwidth() - dialog.winfo_reqwidth()) / 2,
                                (dialog.winfo_screenheight() - dialog.winfo_reqheight()) / 2))

    dialog.wait_window()
    return result[0]

def delete_stuff_floored(game):
    save_path = games_n_files[game][0]
    keep_files = [os.path.basename(file) for file in games_n_files[game][1]]
    for file in os.listdir(save_path):
        if file not in keep_files and not os.path.isdir(os.path.join(save_path, file)):
            file_path = os.path.join(save_path, file)
            os.remove(file_path)
    print(f"GET BACK AT IT! {game.strip('.exe').upper()} COMING RIGHT BACK UP! {random.choice(floor_it_quotes).upper()}")
    os.startfile(game)
    

# Function that prompts user to select game exe
def add_game_exe_to_dict():
    print("Select game exe")
    exe_path = filedialog.askopenfilename()
    if exe_path == "":
        print("No exe selected, exiting")
        exit()
    exe_name = os.path.basename(exe_path)
    print(f"Selected: {exe_path}")
    return [exe_name, exe_path]

# Function to check folder permissions
def check_perms(folder_path):
    if not os.access(folder_path, os.W_OK):
        #Make a tkinter dialogue to tell the user to fix permissions of that folder
        tk.messagebox.showwarning("Heads up!", "Before going any further, make sure the folder you selected has write permissions. If you don't know how to fix this, please YouTube a tutorial. Also maybe don't run random things you find on GitHub? Run this again once you've done that. Closing for now.")
        exit()
    else:
        print("Sick. No permissions issues.")
        return True

# Function that prompts user to select where saves are stored
def get_save_path():
    print("Select save folder")
    folder_path = filedialog.askdirectory()
    if folder_path == "":
        print("No folder selected. Closing. Run again when you're ready.")
        exit()
    check_perms(folder_path)
    return folder_path

# Function that prompts user to select any files to keep safe
def add_keep_files_to_dict():
    print("Select any files to keep safe")
    file_paths = filedialog.askopenfilenames()
    if file_paths == "":
        print("All is fair game in there, I guess. Your funeral.")
        return []
    for file in file_paths:
        file = os.path.basename(file)
    return file_paths

# Add both game exe and list of files to not delete to dictionary
def add_to_config():
    config = configparser.ConfigParser()
    config.read('games.cfg')  # read existing config file

    game_info_base = add_game_exe_to_dict()
    game_exe = game_info_base[0]
    game_path = game_info_base[1]
    save_path = get_save_path()
    keep_files = add_keep_files_to_dict()

    # create a new section in the config file for the game
    if not config.has_section(game_exe):
        config.add_section(game_exe)

    # set the values in the config file
    config.set(game_exe, 'save_path', save_path)
    config.set(game_exe, 'game_path', game_path)
    config.set(game_exe, 'keep_files', ','.join(keep_files))  # store as comma-separated list

    # write the changes to the config file
    with open('games.cfg', 'w') as configfile:
        config.write(configfile)

    # Zip the current contents of the save folder and save it in this script's directory
    zip_name = game_exe.strip(".exe") + "_backup"
    #copy contents of save folder to current directory
    shutil.copytree(save_path, zip_name)
    print("Just in case, I backed up your existing saves to a folder in this script's directory. If you want to restore them, they're in here now.")
    

    print("Config saved to games.cfg")

def core_deletion(game):
    save_path = games_n_files[game][0]
    keep_files = [os.path.basename(file) for file in games_n_files[game][1]]
    for file in os.listdir(save_path):
        if file not in keep_files and not os.path.isdir(os.path.join(save_path, file)):
            file_path = os.path.join(save_path, file)
            os.remove(file_path)

# Function that deletes saves
def delete_stuff_rev2(game):
    # Ask user if they want to do another run
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.focus_set()
    answer = tk.messagebox.askyesno("Another run?", "Doing another run?")
    if answer == True:
        core_deletion(game)
        # relaunch the game
        print(f"Relaunching {game.strip('.exe')}. GLHF!")
        os.startfile(game)
        root.destroy()
    else:
        # ask if they want to restore the original saves
        answer = tk.messagebox.askyesno("Restore saves?", "Do you want to restore your original saves?")
        if answer == True:
            core_deletion(game)
            restore_saves(game)
            print("Saves restored! Peace! Go check out nam.rip")
            exit()
        else:
            print("Later. Hey, maybe donate to me if this is useful to you? Go to nam.rip")
            exit()

# Function to put the original saves back in the save folder
def restore_saves(game):
    save_path = games_n_files[game][0]
    backup_path = game.strip(".exe") + "_backup"
    shutil.copytree(backup_path, save_path, dirs_exist_ok=True)

# Check every second to see if game is running, game is a string, pulled from config file
def is_running():
    with Halo(text="Checking every second for games you've set up", spinner = "shark", text_color='magenta') as spinner:
        running = False
        while running == False:
            time.sleep(1)
            progs = psutil.process_iter()
            for prog in progs:
                try:
                    if prog.name() in games_n_files:
                        running = True
                        game = prog.name()
                except psutil.NoSuchProcess:
                    pass  # skip terminated processes
        spinner.succeed(f"{game.strip(".exe")} detected, have fun!")
        return game

# Get games that are already set up in games.cfg
def get_games():
    config = configparser.ConfigParser()
    config.read('games.cfg')
    for game in config.sections():
        save_path = config.get(game, 'save_path')
        game_path = config.get(game, 'game_path')
        keep_files = config.get(game, 'keep_files').split(',')
        #ut = config.get(game, 'ut_mode')
        #emu = config.get(game, 'emu')
        games_n_files[game] = [save_path, keep_files, game_path]
    check_perms(save_path)


# Check every second to see if game stopped running
def is_not_running(game):
    with Halo(text=f"Checking every second to see if {game.strip('.exe')} is still running", spinner = "shark", text_color='magenta') as spinner:
        running = True
        while running == True:
            time.sleep(1)
            progs = psutil.process_iter()
            for prog in progs:
                try:
                    if prog.name() == game:
                        break
                except psutil.NoSuchProcess:
                    pass
            else:
                running = False
                spinner.fail(f"{game.strip('.exe')} no longer running. Deleting saves. Get back in it!")
# Main function
def main():
    config = configparser.ConfigParser()
    config.read('games.cfg')
    # Check if games.cfg exists, or if it's empty
    if not os.path.exists('games.cfg') or os.stat('games.cfg').st_size == 0:
        print("First time? Let's create a config file")
        add_to_config()
        get_games()
    
    if not floor_it("Floor it?", "FLOOR IT???", yes_label="FLOOR IT!", no_label="NO, DON'T FLOOR IT!"):
        answer = tk.messagebox.askyesno("New game?","Do you want to run a game that you've already set up?")
        if answer == True:
            get_games()
        else:
            add_to_config()
            get_games()
    while True:
        game = is_running()
        os.chdir(games_n_files[game][2].strip(f"{game}"))
        is_not_running(game)
        if floor_it:
            delete_stuff_floored(game)
        else:
            delete_stuff_rev2(game)

main()
