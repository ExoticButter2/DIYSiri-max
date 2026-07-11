from Settings import settings

def FindWMDeviceIndex(mode):
    print(f"Searching for wm {mode} device index")
    
    pyAudioInstance = settings.pyAudioInstance
    
    for i in range(pyAudioInstance.get_device_count()):
        dev = pyAudioInstance.get_device_info_by_index(i)
        
        if 'wm8960' in dev['name'].lower():
            if mode == 'output' and dev['maxOutputChannels'] > 0:
                print("Found output device!")
                return i
            elif mode == 'input' and dev['maxInputChannels'] > 0:
                print("Found input device!")
                return i
            
    return None