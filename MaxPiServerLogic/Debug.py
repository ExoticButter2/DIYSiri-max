# import torch
# from kokoro import KPipeline
# import numpy
# import openwakeword.utils

# pipeline = KPipeline(lang_code='a')

# print(torch.cuda.is_available())

# def ConvertTextResponseToAudio():
#     ttsAudioArray = []
#     generator = pipeline("hi", voice='am_eric')
    
#     for _, _, audio in generator:
#         ttsAudioArray.append(audio)
        
#     concatArray = numpy.concatenate(ttsAudioArray)
#     convertedArray = concatArray
    
#     print("Generated tts response")
#     print(concatArray.dtype)
#     return concatArray

# ConvertTextResponseToAudio()