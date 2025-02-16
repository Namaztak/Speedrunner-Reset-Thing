What it do?

For now, just a simple python script for speedrunners playing games that need their saves deleted between runs, that asks the following:
1. What game are you running? (Locate the exe)
2. Where are the saves located? (Navigate to the folder)
3. Are there any files in that folder that need to be ignored (Things like config files or any practice saves that you don't want it to delete when you reset/close the game)

After all 3 of those steps are complete, it will check every second for whether the game is running, and do nothing else until it is.

Once the game is running, it'll recheck every second to see that it's still running, and continue to do nothing but spam "game is still running" in the console.

Once the game is no longer detected, it will delete every file in the given folder, except any files submitted in step 3.