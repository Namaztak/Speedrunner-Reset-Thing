import os
import psutil
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
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
ut_counter = 1

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
        undertale = simpledialog.askinteger("Input", "Enter the expected number of exits/crashes in one run:")
        root.destroy()
        return str(undertale)
    return "-1"

# Use for timed yes/no confirmations
def timed_yes_no(title, message, timeout=10, default_yes=True):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.focus_set()  # Set focus to the dialog box
    dialog.attributes("-topmost", True)  # Set dialog box to be topmost
    dialog.lift()

    label = tk.Label(dialog, text=message)
    label.pack(pady=10)

    var = tk.BooleanVar()
    var.set(default_yes)

    yes_button = tk.Button(dialog, text="Yes", command=lambda: [var.set(True), dialog.destroy()])
    yes_button.pack(side=tk.LEFT, padx=10)

    no_button = tk.Button(dialog, text="No", command=lambda: [var.set(False), dialog.destroy()])
    no_button.pack(side=tk.LEFT, padx=10)

    def close_dialog():
        dialog.destroy()
        root.destroy()
    def timeout_callback():
        close_dialog()
        return var.get()

    dialog.after(timeout * 1000, timeout_callback)
    dialog.update_idletasks()
    dialog.geometry("+%d+%d" % ((dialog.winfo_screenwidth() - dialog.winfo_reqwidth()) / 2,
                                (dialog.winfo_screenheight() - dialog.winfo_reqheight()) / 2))
    dialog.protocol("WM_DELETE_WINDOW", close_dialog)
    dialog.wait_window()
    return var.get()

        
#function to check if an undertale mode run is still going after an exit is detected
def undertale_confirm_ongoing(time):
    return timed_yes_no(
        "Run still going?",
        f"That was an intentional exit, yeah? Run still going? (This'll default to yes if you ignore it for {time} seconds)",
        timeout=time,
        default_yes=True
        )
    
# Emulator mode functions
def get_emu():
    answer = tk.messagebox.askyesno("Emulator mode?", "Is the exe you just selected an emulator?")
    if answer == True:
        return "True"
    return "False"

def multi_cat_setup():
    if ask_mult_cats():
        all_cats = []
        more = True
        while more:
            all_cats.append(get_split_file())
            more = simpledialog.askyesno("More categories?", "Do you want to add another category?")
        return all_cats
    return False

def ask_mult_cats():
    answer = simpledialog.askyesno("Multiple categories?", "Do you wanna set this up to run multiple categories?")
    return answer

def get_split_file():
    print("Select your splits file for this category")
    location = filedialog.askopenfilename()
    actual_file = os.path.basename(location)
    #ask for the user to input a string using tkinter dialogue
    category = simpledialog.askstring("Input", "Enter the category name:")
    return [location, actual_file, category]



def floor_it(title, message, yes_label="Yes", no_label="No"):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    result = [None]
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.focus_set()
    dialog.attributes("-topmost", True)
    dialog.lift()

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
    result = result[0]
    root.destroy()
    return result

def delete_stuff_floored(game):
    save_path = games_n_files[game][0]
    keep_files = [os.path.basename(file) for file in games_n_files[game][1]]
    for file in os.listdir(save_path):
        if file not in keep_files and not os.path.isdir(os.path.join(save_path, file)):
            file_path = os.path.join(save_path, file)
            os.remove(file_path)
    print(f"GET BACK AT IT! {game[:-4].upper()} COMING RIGHT BACK UP! {random.choice(floor_it_quotes).upper()}")
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
    emu = get_emu()
    #emu_rom = get_emu_rom()
    #categories = str(get_categories())

    # create a new section in the config file for the game
    if not config.has_section(game_exe):
        config.add_section(game_exe)

    # set the values in the config file
    config.set(game_exe, 'save_path', save_path)
    config.set(game_exe, 'game_path', game_path)
    config.set(game_exe, 'keep_files', ','.join(keep_files))  # store as comma-separated list
    config.set(game_exe, 'ut_mode', undertale)
    config.set(game_exe, 'emu', emu)
    #config.set(game_exe, 'emu_rom', emu_rom) # store a list for a dropdown of games when emu detected
    #config.set(game_exe, 'categories', categories) #store list of speedrun categories, if more than one
    #config.set(game_exe, 'splits', splits) # store list of splits files, assigned to categories
    # write the changes to the config file
    with open('games.cfg', 'w') as configfile:
        config.write(configfile)

    # Copy the save folder's contents to a backup folder
    zip_name = game_exe[:-4] + "_backup"
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
        print(f"Relaunching {game[:-4]}. GLHF!")
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
    backup_path = game[:-4] + "_backup"
    shutil.copytree(backup_path, save_path, dirs_exist_ok=True)

# Check every second to see if game is running, game is a string, pulled from config file
def is_running():
    with Halo(text="Checking every second for games you've set up", spinner = "shark", text_color='magenta') as spinner:
        running = False
        if len(games_n_files.keys()) == 1:
            game = list(games_n_files.keys())[0]
            return game
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
        spinner.succeed(f"{game[:-4]} detected, have fun!")
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
                if games_n_files[game][3] != "-1" and ut_counter < int(games_n_files[game][3]):
                    spinner.fail(f"{game.strip('.exe')} no longer running. {'Full reset, pitter patter.' if ut_counter == 0 or int(games_n_files[game][3] == -1) else f'{int(games_n_files[game][3]) - ut_counter} exits remaining in the run'}. Relaunching {game.strip('.exe')}. You're doing great!")
                else:
                    spinner.fail(f"{game.strip('.exe')} no longer running. Deleting saves. Get back in it!")
# Main function
def main():
    global ut_counter, floor_it
    config = configparser.ConfigParser()
    config.read('games.cfg')
    # Check if games.cfg exists, or if it's empty
    if not os.path.exists('games.cfg') or os.stat('games.cfg').st_size == 0:
        print("First time? Let's create a config file")
        add_to_config()

    floor_it = floor_it("Floor it?", "FLOOR IT???", yes_label="FLOOR IT!", no_label="NO, DON'T FLOOR IT!")
    if not floor_it:
        answer = tk.messagebox.askyesno("New game?","Have you already set up the game you'll be running?")
        if answer == False:
            add_to_config()
    get_games()
    if len(games_n_files.keys()) == 1:
        game = list(games_n_files.keys())[0]
        os.chdir(games_n_files[game][2].strip(f"{game}"))
        os.startfile(game)
    else:
        game = is_running()
    os.chdir(games_n_files[game][2].strip(f"{game}"))
    print(f"Now working in {games_n_files[game][2].strip(f"{game}")}")
    while True:
        is_not_running(game)
        if floor_it:
            if games_n_files[game][3] == "-1" or ut_counter >= int(games_n_files[game][3]):
                ut_still_going = False
            else:
                ut_still_going = undertale_confirm_ongoing(3)
            if ut_still_going == False:
                if ut_counter >= int(games_n_files[game][3]):
                    if games_n_files[game][3] != "-1":
                        print("Your did it! Gold star. And hopefully some gold splits. Saves deleted, go next.".upper())
                    delete_stuff_floored(game)
                    ut_counter = 0
                else:
                    if games_n_files[game][3] != "-1":
                        print("Mission failed. We'll get 'em next time. Saves deleted, go next.".upper())
                    delete_stuff_floored(game)
                    ut_counter = 0
            elif ut_still_going == True or ut_counter == 0:
                os.startfile(game)
                ut_counter += 1
                        
        else:
            if games_n_files[game][3] == "-1" or ut_counter >= int(games_n_files[game][3]):
                ut_still_going = False
            elif ut_counter < int(games_n_files[game][3]):
                ut_still_going = undertale_confirm_ongoing(10)
            if ut_still_going == False:               
                if games_n_files[game][3] != "-1" and ut_counter >= int(games_n_files[game][3]):
                    print("Your did it! Gold star. And hopefully some gold splits.")
                elif games_n_files[game][3] != "-1":
                    print("Mission failed. We'll get 'em next time. Saves deleted, go next.")
                delete_stuff_rev2(game)
                ut_counter = 0
            else:
                print("Ayy, nice. You made it past whatever that exit marks. Keep at it!")
                os.startfile(game)
                ut_counter += 1
            
if __name__ == "__main__":
    main()
