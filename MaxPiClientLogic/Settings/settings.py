from pyaudio import PyAudio

state = 0
playingAudio = False
playedAudioBefore = False
pyAudioInstance:PyAudio = PyAudio()