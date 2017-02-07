# AndroidForensics
LiME, Volatility and custom Python wrapper script for android forensic analysis

# Description
This project contains files and custom scripts to extract processes from Android devices using LiME and Volatility.
The main file androidforensics.py can be run using the command python androidforensics.py

# Details
The script has options to
* start an emulator with a custom built kernel that has custom modules enabled
* upload custom apps to emulator
* functions to upload and install a custom module for LiME that has been cross compiled for this kernel
* dump the contents of the running machine via netcat as emulators virtual sdcards are rarely large enough
* use volatility to intergate the memory dump
* use volatility to dump out the running processes from the memory dump

Video's demosing how to use this script are available on YouTube at:
https://www.youtube.com/playlist?list=PLIHEc6VrhPadSg6Gvts1e224INVROKfRR
