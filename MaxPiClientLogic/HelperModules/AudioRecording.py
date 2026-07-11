import pyaudio
import numpy
from HelperModules import PyAudioHelper
import time
from Settings import settings
import queue

FORMAT = pyaudio.paInt16
CHANNELS = 1
CHUNK = 1280
RATE = 16000

speaking = False

loudnessThreshold = -60

maxQuietTime = 3#in seconds

audio_queue = queue.Queue()

def Callback(in_data, frame_count, time_info, status):
    audio_queue.put(in_data)
    return (None, pyaudio.paContinue)

mic_stream = settings.pyAudioInstance.open(format=FORMAT, 
                                           channels=CHANNELS, 
                                           rate=RATE, 
                                           input=True, 
                                           frames_per_buffer=CHUNK,
                                           input_device_index=PyAudioHelper.FindWMDeviceIndex('input'), 
                                           stream_callback=Callback)
    
def OpenStreamBuffer():
    mic_stream.start_stream()
    
def CloseStreamBuffer():
    ClearStreamBuffer()
    mic_stream.stop_stream()
    
def ClearStreamBuffer():
    mic_stream.read(mic_stream.get_read_available())
    
def GetWMRecordingBuffer():
    try:
        audioBytes = audio_queue.get_nowait()
        return numpy.frombuffer(audioBytes, dtype=numpy.int16)
    except queue.Empty:
        return numpy.zeros(CHUNK, dtype=numpy.int16)

def GetBufferLoudness(buffer):
    rms = numpy.sqrt(numpy.mean(numpy.square(numpy.astype(buffer, numpy.float64))))
    db = 20 * numpy.log10(rms/ 32767.0)
    
    return rms, db

def LoudnessOverThreshold(buffer):
    rms, db = GetBufferLoudness(buffer)
    
    if db >= loudnessThreshold:
        return True
    
    return False

#PROMPTING
def RecordPrompt():#returns an array of the prompt audio
    print("Recording prompt")
    
    speaking = True
    promptArray = []
    
    quiet = False
    
    startTime = 0
    
    while speaking:
        recordingBuffer = GetWMRecordingBuffer()
        
        if quiet:
            if LoudnessOverThreshold(recordingBuffer):#if loud enough
                quiet = False#continue recording
            else:
                currentTime = time.perf_counter()
                deltaTime = currentTime - startTime
                
                if deltaTime > maxQuietTime:
                    speaking = False
                continue
                
        promptArray.append(recordingBuffer)
        
        if not LoudnessOverThreshold(recordingBuffer):
            quiet = True
            startTime = time.perf_counter()
        
        
    concatPromptArray = numpy.concatenate(promptArray)
    return concatPromptArray