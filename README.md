# funi max

This repo contains the code and dependencies in two separate folders for the server and client respectively.
Current wake word model only contains 2000 samples so it might not hear it all the time.

but its funi

# HOW TO USE

SETUP
Install all packages from requirements.txt (Server and Client folder)

START
1. Run WakeWordServer.py (MaxPiServerLogic folder)
2. Run main.py (MaxPiClientLogic folder)


After that main.py should take about 20 seconds to connect and then it'll output loudness from microphone
Say mahcks (see aladeen saying it for reference ayo lol max what)
You'll know it detected it when it outputs "max what" (imumoccupancy 120) through the speakers. (And on server it'll print "Wake word detected!")

After that prompt it something and dont say anything or make loud noise for 2.5 seconds (changeable in AudioRecording.py -> maxQuietTime)
You can also change up the noise gate values in AudioRecording.py (start/end threshold variable)

After prompting it, in a couple seconds it should: 
1. Convert the audio to text using faster-whisper
2. Generate a text response using Gemini API (or Ollama changeable in Prompting Helper module) and
3. Turn it to audio using KokoroTTS and finally to the speakers.

Then it goes back to wake word detection and you can repeat the process.
