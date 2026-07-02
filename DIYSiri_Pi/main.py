import HelperModules.Prompting.PromptFunctions as PromptFunctions
import HelperModules.WakeWord.WakeWordFunctions as WakeWordFunctions
import settings
 
def HeaderProcess(headers):#check if headers are valid depending on mode
    if settings.state == 0:
        if headers[0] == 0xAA and headers[1] == 0x55:#wake word sampling start
            WakeWordFunctions.WakeWordProcessStart()
    else:
        if headers[0] == 0x0 and headers[1] == 0xFF:#prompt sampling start
            PromptFunctions.PromptSampleStart()
        elif headers[0] == 0xF0 and headers[1] == 0x0F:#prompt sampling end
            PromptFunctions.PromptSampleEnd()
    return False  

while True:
    headers = settings.serialComm.read(2)
    
    if headers:
        HeaderProcess(headers)