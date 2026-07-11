#ifndef UARTHELPER_H
#define UARTHELPER_H

#include <stdint.h>

#pragma region NON_HEADER



#pragma endregion


#pragma region HEADER

void SendSampleBuffer(uint8_t* dataBuffer);
void SendSinglePromptSample(uint16_t sample);
void SendPromptSamplingEnd();
void SendPromptSamplingStart();

#pragma endregion

#endif