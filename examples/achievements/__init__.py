"""
Basic example on how to grant an achievement. 
"""

import os
import sys
import time

if sys.version_info >= (3, 8):
  os.add_dll_directory(os.getcwd()) # Required since Python 3.8

from steamworks import STEAMWORKS # Import main STEAMWORKS class

"""
In this example, we'll set up a basic achievement. We'll assume your game is Spacewar. 
Initialise Steamworks as seen in the basic example first. 
"""
steamworks = STEAMWORKS()


steamworks.initialize() 

"""
The Interstellar achievement needs stats. Get those as seen in the stats example first. 
"""
if (steamworks.UserStats.RequestCurrentStats() == True):
  print('Stats successfully retrieved!')
else:
  print('Failed to get stats. Shutting down.')
  exit(0)

"""
Now that that's done, we can get the stats we want. 
"""

distance_travelled = steamworks.UserStats.GetStatFloat('FeetTravelled')
won_games = steamworks.UserStats.GetStatInt('NumWins')

"""
The Interstellar achievement requires you to travel a total of one mile. One mile is 5,280 feet. 
The Champion achievement needs you to win 100 games. 
"""

interstellar_requirement = 5280.0 #This is a float value in the stats, so we force this to be a float here
champion_requirement = 100

""" 
Now we have those, lets also see if we have the achievement already...
The GetAchievement method returns true or false, depending on whether
the player has it already. 
"""

champion_achieved = steamworks.UserStats.GetAchievement('ACH_WIN_100_GAMES')
interstellar_achieved = steamworks.UserStats.GetAchievement('ACH_TRAVEL_FAR_ACCUM')

""" 
Now we have the status, we should do some sanity checks. Sometimes, if the user is
playing offline, the stats may tick over into a state where they should have the 
achievement, but didn't get it because the servers were unreachable. Checking
and awarding here would be useful. 
"""

if champion_achieved is False and (won_games >= champion_requirement):
  steamworks.UserStats.SetAchievement('ACH_WIN_100_GAMES')
  champion_achieved = True 
if interstellar_achieved is False and (distance_travelled >= interstellar_requirement):
  steamworks.UserStats.SetAchievement('ACH_TRAVEL_FAR_ACCUM')
  interstellar_achieved = True 

"""
Caveat of the above: Python's float handling and making sure it's valid are
an exercise left to the reader. 

Now that that's done, you can use the same methods as above to set the achievements
when whatever conditions required for them are met. 
"""
