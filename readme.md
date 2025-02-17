# What it do?

For now, just a simple python script for speedrunners playing games that need their saves deleted between runs, that asks the following:
1. What game are you running? (Locate the exe)
2. Where are the saves located? (Navigate to the folder)
3. Are there any files in that folder that need to be ignored (Things like config files or any practice saves that you don't want it to delete when you reset/close the game)

After all 3 of those steps are complete, it will check every second for whether the game is running, and do nothing else until it is.

Once the game is running, it'll recheck every second to see that it's still running, and continue to do nothing but spam "game is still running" in the console.

Once the game is no longer detected, it will delete every file in the given folder, except any files submitted in step 3.

## TODO: 

1. Make it check that it actually can delete the files, and if not, tell the user to change the folder permissions.  
2. Make it ask if we're doing another run (y/n), kill itself if not.  
2a. Option not to delete saves if not.  
2b. If yes, relaunch the game immediately.  
3. ~~Actually save the submitted info between sittings.~~
3a. ~~Add initial check to see if user wants to create a new game profile.~~  
3b. ~~Fix initial run after adding a profile, currently does not detect the new game until the script starts over.~~  
3c. ~~Make it ignore subfolders in the save directory~~

## Dependencies not included with Python
[psutil](https://github.com/giampaolo/psutil)