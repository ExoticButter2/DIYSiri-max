from HelperModules import AudioRecording
from HelperModules import AudioPlaying
from HelperModules import PromptHelper
from Settings import settings
import socket
import os

PC_IP = "192.168.178.162"
PORT = 4000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((PC_IP, PORT))
client_socket.setblocking(False)

settings.state = 0#0 for wake word, 1 for prompt
lastState = 0

receiveBuffer = b""#create empty buffer for TRIGGERED message

while True:
    print(settings.state)
    if settings.state == 0:#if wake word mode
        if lastState == 1:
            AudioRecording.ClearStreamBuffer()
        
        audioBuffer = AudioRecording.GetWMRecordingBuffer()
        rms, db = AudioRecording.GetBufferLoudness(audioBuffer)
        
        print(f"Loudness: {db}")
        
        try:
            if rms != 0:
                client_socket.send(audioBuffer)
        except BlockingIOError:
            pass
        
        try:
            response = client_socket.recv(1024)
            
            if response:
                receiveBuffer += response
                
            if b"\n" in receiveBuffer:
                message, receiveBuffer = receiveBuffer.split(b"\n", 1)
                
                if message == b"TRIGGERED":
                    AudioRecording.ClearStreamBuffer()
                    settings.state = 1
                    receiveBuffer = b""
                    print("Wake word found")
                    
                    AudioPlaying.PlayAudio(os.path.join(os.getcwd(), "maxwhat.wav"))
                    settings.playedAudioBefore = False
        except BlockingIOError:
            pass
        
        lastState = 0
    elif settings.state == 1:#if prompt mode
        if not settings.playingAudio and settings.playedAudioBefore:
            settings.playedAudioBefore = False
            settings.state = 0#set back to wake word mode after audio playing
            continue
        elif settings.playingAudio:
            continue
        
        promptArray = AudioRecording.RecordPrompt()
        
        if promptArray.size == 0:
            continue
        
        textResponse = PromptHelper.ProcessPrompt(promptArray)
        
        if not textResponse:
            continue
        print(textResponse)
        audioResponsePath = PromptHelper.ConvertPromptTextToAudio(textResponse)
        
        if not audioResponsePath:
            continue
        
        
        AudioPlaying.PlayAudio(audioResponsePath)
        lastState = 1