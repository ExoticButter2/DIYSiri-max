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

loudnessStartThreshold = -24
loudnessStopThreshold = -40

maxQuietTime = 3#in seconds

audio_queue = queue.Queue(maxsize=3)

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
    readAvailable = mic_stream.get_read_available()
    
    if readAvailable <= 0:
        print("Stream empty when clearing!")
        return
    
    mic_stream.read(readAvailable)
    
def GetWMRecordingBuffer():
    while True:
        try:
            audioBytes = audio_queue.get()
            return numpy.frombuffer(audioBytes, dtype=numpy.int16)
        except queue.Empty:
            continue

def GetBufferLoudness(buffer):
    if numpy.all(buffer == 0):
        return 0, -200.0
    
    rms = numpy.sqrt(numpy.mean(numpy.square(numpy.astype(buffer, numpy.float64))))
    db = 20 * numpy.log10(numpy.maximum(rms/ 32767.0, 1e-10))
    print(f"Loudness in dB: {db}")
    
    return rms, db

def LoudnessOverThreshold(buffer, mode):
    rms, db = GetBufferLoudness(buffer)
    
    if mode == 'start':
        if db >= loudnessStartThreshold:
            return True
    elif mode == 'stop':
        if db >= loudnessStopThreshold:
            return True
    
    return False

#PROMPTING
def RecordPrompt():#returns an array of the prompt audio
    ClearStreamBuffer()
    print("Recording prompt")
    
    speaking = True
    promptArray = []
    
    quiet = False
    
    startTime = 0
    
    while speaking:
        print(f"Quiet: {quiet}")
        recordingBuffer = GetWMRecordingBuffer()
        promptArray.append(recordingBuffer)
        
        if quiet:
            if LoudnessOverThreshold(recordingBuffer, 'start'):#if loud enough
                quiet = False#continue recording
            else:
                currentTime = time.perf_counter()
                deltaTime = currentTime - startTime
                
                if deltaTime > maxQuietTime:
                    speaking = False
                continue
        
        if not LoudnessOverThreshold(recordingBuffer, 'stop'):
            quiet = True
            startTime = time.perf_counter()
        
        
    concatPromptArray = numpy.concatenate(promptArray)
    return concatPromptArray