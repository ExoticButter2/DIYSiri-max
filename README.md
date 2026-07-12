# funi max

This repo contains the code and dependencies in two separate folders for the server and client respectively.
Current wake word model only contains 2000 samples so it makes mistakes frequently.

but its funi

# HOW TO USE

SETUP
For server: Install openwakeword (pip install openwakeword) and run Debug.py (to install resources for openwakeword)
For client: Install all packages from requirements.txt

START
1. Run WakeWordServer.py (MaxPiServerLogic folder)
2. Run main.py


After that main.py should take about 20 seconds to connect and then it'll output loudness from microphone
Say mahcks (see aladeen saying it for reference ayo lol max what)
You'll know it detected it when it outputs "max what" (imumoccupancy 120) through the speakers. (And on server it'll print "Wake word detected!")

After that prompt it something and dont say anything or make loud noise for 3 seconds (changeable in AudioRecording.py -> maxQuietTime)
You can also change up the noise gate values in AudioRecording.py (start/end threshold variable)

After prompting it, in a couple seconds it should generate a text response using Gemini API and then turn it to audio using edge tts and finally to the speakers.
Then it goes back to wake word detection and you can repeat the process.
