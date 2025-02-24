import os
import psutil
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import simpledialog
import random # For random messages to not be boring about the console spam
import configparser
import shutil
from halo import Halo
from quotes_library import *
import webbrowser

# Dictionary that everything uses, floor it var, and undertale var

games_n_files = {}
floor_it = False
ut_counter = 0

# Floor it? (automatically confirm everything for this session)
import tkinter as tk

root = tk.Tk()
root.withdraw()  # Hide the main window

# Ask user if their run contains any intentional crashes/quits
def get_undertale_mode():
    answer = floor_it(
        "Undertale mode?", 
        "Do your runs of this game involve any intentional crashes or exits?",
        yes_label="Yes",
        no_label="No"
    )
    if answer == True:
        #open tkinter dialogue with a number input field
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        undertale = simpledialog.askinteger("Input", "Enter a number")
        return str(undertale)
    return "False"
        
        

def floor_it(title, message, yes_label="Yes", no_label="No"):
    global floor_it
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
    floor_it = result[0]
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
        print(f"Sick. No permissions issues for {folder_path}.")
        return True

# Function that prompts user to select where saves are stored
def get_save_path():
    print("Select save folder")
    folder_path = filedialog.askdirectory()
    if folder_path == "":
        print("No folder selected. Closing. Run again when you're ready.")
        exit()
    if "system32" in folder_path.lower():
        #open url in default browser
        webbrowser.open("https://www.youtube.com/watch?v=52tHsOk-Gy0")
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
    undertale = get_undertale_mode()

    # create a new section in the config file for the game
    if not config.has_section(game_exe):
        config.add_section(game_exe)

    # set the values in the config file
    config.set(game_exe, 'save_path', save_path)
    config.set(game_exe, 'game_path', game_path)
    config.set(game_exe, 'keep_files', ','.join(keep_files))  # store as comma-separated list
    config.set(game_exe, 'ut_mode', undertale)

    # write the changes to the config file
    with open('games.cfg', 'w') as configfile:
        config.write(configfile)

    # Zip the current contents of the save folder and save it in this script's directory
    zip_name = game_exe.strip(".exe") + "_backup"
    #copy contents of save folder to current directory
    shutil.copytree(save_path, zip_name, dirs_exist_ok=True)
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
        undertale = config.get(game, 'ut_mode') #undertale mode var
        games_n_files[game] = [
            save_path,
            keep_files,
            game_path,
            undertale
            ]
        check_perms(save_path)


# Check every second to see if game stopped running
def is_not_running(game):
    global ut_counter
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
                if games_n_files[game][3] != "False" and ut_counter < int(games_n_files[game][3]):
                    spinner.fail(f"{game.strip('.exe')} no longer running. {int(games_n_files[game][3]) - ut_counter} exits remaining in the run. Relaunching {game.strip('.exe')}. You're doing great!")
                else:
                    spinner.fail(f"{game.strip('.exe')} no longer running. Deleting saves. Get back in it!")
# Main function
def main():
    global ut_counter
    config = configparser.ConfigParser()
    config.read('games.cfg')
    # Check if games.cfg exists, or if it's empty
    if not os.path.exists('games.cfg') or os.stat('games.cfg').st_size == 0:
        print("First time? Let's create a config file")
        add_to_config()

    if not floor_it("Floor it?", "FLOOR IT???", yes_label="FLOOR IT!", no_label="NO, DON'T FLOOR IT!"):
        answer = tk.messagebox.askyesno("New game?","Have you already set up the game you'll be running?")
        if answer == False:
            add_to_config()
    get_games()
    game = is_running()
    os.chdir(games_n_files[game][2].strip(f"{game}"))
    print(f"Now working in {games_n_files[game][2].strip(f"{game}")}")
    while True:
        is_not_running(game)
        if floor_it:
            if games_n_files[game][3] == "False" or ut_counter < int(games_n_files[game][3]):
                delete_stuff_floored(game)
            elif ut_counter >= int(games_n_files[game][3]):
                delete_stuff_floored(game)
                ut_counter = 0
        
            
        else:
            if games_n_files[game][3] == "False" or ut_counter < int(games_n_files[game][3]):
                os.startfile(game)
            elif ut_counter >= int(games_n_files[game][3]):
                delete_stuff_rev2(game)
                ut_counter = 0
        if games_n_files[game][3] != "False":
            ut_counter += 1
            

main()
