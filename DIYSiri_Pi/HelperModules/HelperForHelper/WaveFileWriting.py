import struct
import wave

def WriteWaveFile(filename, data):
    bytesData = struct.pack(f"{len(data)}h", *data)
    
    with wave.open(filename, 'wb') as waveFile:
        waveFile.setchannels(1)
        waveFile.setsampwidth(2)
        waveFile.setframerate(16000)
        waveFile.writeframes(bytesData)