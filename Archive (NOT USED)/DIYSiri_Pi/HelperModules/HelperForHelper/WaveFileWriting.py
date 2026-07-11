import struct
import wave

def WriteWaveFile(filename, data, sample_rate):
    bytesData = struct.pack(f"{len(data)}h", *data)
    
    with wave.open(filename, 'wb') as waveFile:
        waveFile.setchannels(1)
        waveFile.setsampwidth(2)
        waveFile.setframerate(sample_rate)
        waveFile.writeframes(bytesData)
        return waveFile