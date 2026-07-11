from HelperModules import AudioRecording
from HelperModules import AudioPlaying
from HelperModules import PromptHelper
from Settings import settings
import socket

PC_IP = "192.168.178.162"
PORT = 4000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(PC_IP, PORT)
client_socket.setblocking(False)

settings.state = 0#0 for wake word, 1 for prompt
lastState = 0

while True:
    if settings.state == 0:#if wake word mode
        if lastState == 1:
            AudioRecording.ClearStreamBuffer()
        
        audioBuffer = AudioRecording.GetWMRecordingBuffer()
        client_socket.sendall(audioBuffer)
        
        try:
            response = client_socket.recv(1024)
            if response == b"TRIGGERED":
                AudioRecording.ClearStreamBuffer()
                settings.state = 1
        except BlockingIOError:
            continue
        
        # if WakeWordAnalyzing.AnalyzeAudioBuffer():#if wake word detected
        AudioRecording.ClearStreamBuffer()
        settings.state = 1#go to prompt mode
        
        lastState = 0
    elif settings.state == 1:#if prompt mode
        if not settings.playingAudio and settings.playedAudioBefore:
            settings.playedAudioBefore = False
            settings.state = 0#set back to wake word mode after audio playing
            continue
        elif settings.playingAudio:
            continue
        
        lastState = 1
        promptArray = AudioRecording.RecordPrompt()
        
        if not promptArray:
            continue
        
        textResponse = PromptHelper.ProcessPrompt(promptArray)
        
        if not textResponse:
            continue
        print(textResponse)
        audioResponsePath = PromptHelper.ConvertPromptTextToAudio(textResponse)
        
        if not audioResponsePath:
            continue
        
        
        # AudioPlaying.PlayAudio(audioResponsePath)