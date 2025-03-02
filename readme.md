# How to run:

0. Have Python installed such that you can do "python --version" in your terminal/command line interface of choice, and actually get a version returned to you. My machine uses Python 3.13, and so does my only QA tester so far. It works on both of our machines.

1. Go up top, hit that green code dropdown, hit download zip, and extract that zip to its own folder somewhere you won't forget.  
2. Run init.bat and it should grab everything it needs automatically.  
3. See next section, as it should then run the main script. You can just run init.bat every time, if you don't feel like running it from the command line.  

### Note: I've only tested this on Windows 10/11, so if you're on Linux/Mac, I'd be amazed if it works at all, let alone correctly. I will not be supporting either one, myself. Someone(s) else can feel free to fork this for those if they want to. If you do, I'd appreciate it if you linked back here for credit.

# What is this for?

For now, it's just a python script for speedrunners that run games which need their saves deleted between runs, to save on menuing, that asks the following:  
1. What game are you running? (Locate the exe)  
2. Where are the saves located? (Navigate to, and select their folder)  
3. Are there any files in that folder that need to be ignored? (Things like config files or any practice saves that you don't want it to delete when you reset/close the game)  
4. Does your run include any intentional crashes/exits?  
 * If yes, how many?  
5. Locate your splits file for this game. (It currently only supports one category for each game.)

Make sure you have that game's cloud saves turned off in Steam (or whatever other launcher it uses, if it does at all) if you didn't already, otherwise this thing is just gonna make it so Steam has to redownload your most recent cloud save every time, and effectively do nothing.

After all 5 of those steps are complete, it will check every second for whether one of your speedgames is running, and do nothing ~~but spam up the terminal~~ until it is. Hey, no more terminal spam, I use Halo spinners instead now!

* If you only have one game set up, it'll launch that game immediately, as well as open your splits, then start the rest of the loop.

Once the game is running, if you did it manually, having set up more than one game, it'll launch your splits file directly, then the main loop: it'll recheck every second to see that it's still running, and continue to do nothing but ~~spam "game is still running"~~ show a Halo spinner in the console.

Once the game is no longer detected, it will immediately delete every file in the given save folder, except any files submitted in step 3. 
* If it's an "Undertale Mode" game, it will just relaunch the game and increment an internal counter, and will not delete the files until you've exited the game enough times that your run should be over. I plan to add a confirmation box that your run is still ongoing, that won't necessarily need any actual input if the run is still in progress. It'll default to yes for that.

Finally, it will ask if you're doing another run. If yes, it'll immediately re-launch the exe you chose in step 1. If no, it'll ask if you want to restore the saves it quietly backed up when you first set up the config for that game. If yes, it does that, and if no, it'll just exit.

# Floor it?  
If you have at least one game set up, it'll ask you on launch whether you wanna floor it. If you say yes, it's a confirmation that you just wanna mindlessly mash out run after run, so it'll skip asking you, for that entire session, whether you want to relaunch the game, and whether you're gonna do another run. If you want your game to stop launching, you'll have to just kill the script, either by closing your terminal, or hitting Ctrl+C (Keyboard interrupt) in the terminal window.

If you say no, it'll be a lot less aggressive.  

TLDR: "FLOOR IT" TURNS ALT+F4 INTO A RESET BUTTON!

# Undertale mode
During setup of a new game, you're asked if your run has any intentional crashes/exits.  
If you say yes, it'll ask how many times it should expect the game to have closed within 1 run.  
It will not delete the save files until you've closed the game one more time than that number, at which point, it'll either ask if you wanna do another run, resetting that internal crash/exit counter, or it will just autodelete everything and relaunch the game if you enabled "FLOOR IT" when you launched the program.

## TO DO for now: 

1. ~~Make it check that it actually can delete the files, and if not, tell the user to change the folder permissions.~~  
1a. ~~Make it so empty selections in the first step do not add to config, and do not cause crashes.~~  
1b. ~~Instead of ONLY deleting the files, make it so it first copies the entire contents of the save folder,~~  
1c. ~~Add functionality to then re-deploy those files if needed.~~  
2. ~~Make it ask if we're doing another run (y/n), kill itself if not.~~  
2a. Option not to delete saves if not.  
2b. ~~If yes, relaunch the game immediately.~~  
2c. ~~It does that, but it's really ugly.~~ It's no longer ugly!  
3. ~~Actually save the submitted info between sittings.~~  
3a. ~~Add initial check to see if user wants to create a new game profile.~~  
3b. ~~Fix initial run after adding a profile, currently does not detect the new game until the script starts over.~~  
3c. ~~Make it ignore subfolders in the save directory~~  
3d. Make it check for additional files repeatedly until none are selected, run the same permissions check on each folder/files. (really low priority, might not even do this unless someone shows me a specific game that'd need it)  
4. ~~Make an "Undertale mode" for any games that involve an intentional crash/quit during a run.~~  
4a. ~~Ask when setting up a game if there are any intentional crashes/exits in a normal run.  ~~
4b. ~~If yes, ask how many, assign that to a variable, increment counter per-exit, auto-relaunch like "floor it", stop when counter >= exits.~~  
4c. ~~Add confirmation on each exit as to whether the run is still going.~~
5. "Emulator mode" to allow a single program to be set up for multiple games' saves.  
6. ~~"Floor it!" mode. (Only initial interaction needed, then automate everything to yes cause we're grinding runs like crazy.)~~  
7. Make a video showing what it should look like in practice.  
8. ~~Add check on first run to see if the user uses LiveSplit.~~  
8a. ~~Insult them if not (but disable any LiveSplit functionality)~~  
8 and 8a got rolled into a single check during initial setup of a game that asks for the splits file, and it just launches that file directly.
8b. If yes, have them locate and assign their splits file for that game, so that can also be launched by this script.  
8c. MAYBE either figure out how to do the clean websocket interaction, or do an ungabunga pyautogui thing for timer resets.  
8d. Support multiple categories for single games?
9. Prevent users from putting system32 as the save path. (Because ["BITCH ARE YOU FOR REAL???"](https://www.youtube.com/watch?v=PB3EmjYFQUo))  
10. Support switching games from one run to another without having to re-launch the script.  (low priority, relaunching the script is not that hard.)
11. ~~If the user has only one game set up, and they choose to floor it, or run a game they've already set up, just launch that one.~~  
11a. If 8d gets implemented, have them pick their category for the session.  

## TO DO for later when I actually know how to do it at all:  
1. Make it able to trigger OBS overlays based on timer conditions.  
2. Make it control LiveSplit via websocket.  

## Dependencies not included with Python
Again, init.bat should grab these for you, but in case you wanna look further into what I used for this, here you go:

[psutil](https://github.com/giampaolo/psutil)  
[Halo](https://github.com/manrajgrover/halo)  

### Weird known fringe cases:  
* SM64EX, at least specifically the [Archipelago](https://archipelago.gg/) version, doesn't seem to close itself properly, so instead of selecting the exe for your existing build, set it up with the SM64AP launcher's exe instead.

#### Donate?  
I'm not gonna give you anything special if you do, but I'm not a fan of paywalling things if you can't, so only donate if you actually want to just give me money.

[Ko-fi link here](https://ko-fi.com/nam_137)