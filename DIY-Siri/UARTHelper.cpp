#include "UARTHelper.h"
#include <stdint.h>

//start header always 0xAA followed by 0x55
void SendSampleBuffer(uint8_t* dataBuffer)
{
    Serial.write(0xAA);
    Serial.write(0x55);

    uint8_t length = sizeof(dataBuffer) / sizeof(dataBuffer[0]);

    for (int i = 0; i < length; i++)
    {
        Serial.write(dataBuffer[i]);//send all data through serial port
        dataBuffer[i] = 0;//clear after
    }
}

//prompt buffer has a start header (0x0 followed by 0xFF)
void SendPromptSamplingStart()
{
    Serial.write(0x0);
    Serial.write(0xFF);
}

//prompt buffer has an end header (0xF0 followed by 0x0F)
void SendPromptSamplingEnd()
{
    Serial.write(0xF0);
    Serial.write(0x0F);
}

void SendSinglePromptSample(uint16_t sample)
{
    uint8_t lowByte = sample & 0xFF;
    uint8_t highByte = (sample >> 8) & 0x1;//make sure only one bit is there

    Serial.write(lowByte);
    Serial.write(highByte);
}