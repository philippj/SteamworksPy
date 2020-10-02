"""
Basic example on how to request stat values from Steamworks. 
"""

import os
import sys

if sys.version_info >= (3, 8):
  os.add_dll_directory(os.getcwd()) # Required since Python 3.8

from steamworks import STEAMWORKS # Import main STEAMWORKS class

"""
Initialise Steamworks as shown in the basic example. We'll assume your game is Spacewar. 
"""

steamworks = STEAMWORKS()


steamworks.initialize() # This method has to be called in order for the wrapper to become functional!

"""
Returning stats relies on them being set up in Steamworks first. Once you're sure that's done, first, request the stats. 
Ordinarily this is done during initialisation, but it's included here for completeness.
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


print(f'You\'ve travelled {distance_travelled}, and won {won_games} games!')
