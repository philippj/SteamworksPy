# 2.0.0
- Reworked into python module, legacy source is located in the github legacy branch

# 1.6.1
- Added: all Apps functions from Experimental branch
- Added: all Screenshot functions from Experimental branch
- Added: all User functions from Experimental branch
- Added: all Controller functions from Experimental branch
- Changed: steamInit to give correct feedback, now returns INT instead of BOOL
	- Note: if you used version 1.5 or lower, you need to update how your steamInit() works in your project or it may crash
- Changed: some commenting formats
- Removed: HasOtherApp() which is now IsSubscribedApp()
