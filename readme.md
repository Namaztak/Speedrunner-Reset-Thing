# What it do?

For now, just a simple python script for speedrunners playing games that need their saves deleted between runs, that asks the following:
1. What game are you running? (Locate the exe)
2. Where are the saves located? (Navigate to the folder)
3. Are there any files in that folder that need to be ignored (Things like config files or any practice saves that you don't want it to delete when you reset/close the game)

Make sure you have that game's cloud saves turned off in Steam (or whatever other launcher it uses, if it does at all) if you didn't already, otherwise this thing is just gonna make it so Steam has to redownload your most recent cloud save every time, and effectively do nothing.

After all 3 of those steps are complete, it will check every second for whether the game is running, and do nothing but ~~spam up the terminal~~ until it is. Hey, no more terminal spam, I use Halo spinners instead now!

Once the game is running, it'll recheck every second to see that it's still running, and continue to do nothing but ~~spam "game is still running"~~ show a Halo spinner in the console.

Once the game is no longer detected, it will delete every file in the given folder, except any files submitted in step 3.

## TODO: 

1. ~~Make it check that it actually can delete the files, and if not, tell the user to change the folder permissions.~~  
1a. ~~Make it so empty selections in the first step do not add to config, and do not cause crashes.~~  
1b. ~~Instead of ONLY deleting the files, make it so it first copies the entire contents of the save folder,~~  
1c. ~~Add functionality to then re-deploy those files if needed.~~  
2. ~~Make it ask if we're doing another run (y/n), kill itself if not.~~  
2a. Option not to delete saves if not.  
2b. If yes, relaunch the game immediately.  
2c. It does that, but it's really ugly. 
3. ~~Actually save the submitted info between sittings.~~  
3a. ~~Add initial check to see if user wants to create a new game profile.~~  
3b. ~~Fix initial run after adding a profile, currently does not detect the new game until the script starts over.~~  
3c. ~~Make it ignore subfolders in the save directory~~  
3d. Make it check for additional files repeatedly until none are selected, run the same permissions check on each folder/files.  
4. Make an "Undertale mode" for any games that involve an intentional crash/quit during a run.  
5. "Emulator mode" for to allow a single program to be set up for multiple games' saves.  

## Dependencies not included with Python
[psutil](https://github.com/giampaolo/psutil)
[pyautogui](https://github.com/asweigart/pyautogui)
[Halo](https://github.com/manrajgrover/halo)