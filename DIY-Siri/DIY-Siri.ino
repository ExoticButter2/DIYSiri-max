#include "ADCFunctions.h"
#include "ClockHelper.h"
#include "UARTHelper.h"
#include <avr/interrupt.h>
#include <avr/io.h>
#include <stdint.h>

#define WAKE_WORD_MODE 0
#define PROMPTING_MODE 1

//WAKE WORD FLAG

bool samplingEnabled = true;

bool mode = WAKE_WORD_MODE;

bool sampling = false;
bool talking = false;
int timer0InterruptCount = 0;

int samplesInsideBuffer = 0;

uint8_t sampleBuffer80ms[2560];

void setup() {
    Serial.begin(500000);//sending audio at 16khz, no more than 16*20 (so 320)kb/s needed (11 because of start + stop bit)
    DDRD |= (1 << DDD2);//set pin 2 to input mode
    attachInterrupt(0, StartedTalking, RISING);//when d0 from microphone on
    attachInterrupt(0, StoppedTalking, FALLING);//when off
}

void loop() {
    if ((talking && !sampling) && samplingEnabled)
    {
        StartSampling();
    }

    if (Serial.available())
    {
        uint8_t flag = Serial.read();

        switch(flag)
        {
            case 0x0://wake word sampling mode
            mode = WAKE_WORD_MODE;
            break;

            case 0x1://prompt sampling mode
            mode = PROMPTING_MODE;
            break;

            case 0x2://enable sampling
            samplingEnabled = true;
            break;

            case 0x3://disable sampling
            samplingEnabled = false;
            break;
        }
    }
}

ISR(ADC_vect){
    OnConversionComplete();
}

ISR(TIMER2_OVF_vect){//activates every 16.32ms @ 1024 prescaler
    timer0InterruptCount++;
}
//!!!START OF (PACKET) IS 0xAA FOLLOWED BY 0x55, END OF SAMPLE IS 0xEE FOLLOWED BY 
void StartedTalking()
{
    if (!sampling && samplingEnabled)//cant sample twice
    {
        StartSampling();//start recording sound directly
    }

    talking = true;
}

void StoppedTalking()
{
    talking = false;

    EnableTimer2();
    SetTimer2PrescalerTo1024();

    while (!timer0InterruptCount >= 184)//wait time (~3 seconds for 16.32ms steps)
    {
        if (talking)//if started talking again
        {
            DisableTimer2();//go back to normal sampling
            return;
        }
    }
    //if past waiting time
    StopSampling();
    timer0InterruptCount = 0;
}

void StartSampling()
{
    if (mode == PROMPTING_MODE)
    {
        SendPromptSamplingStart();
    }

    sampling = true;
    StartADC();//turn on conversions
}

void StopSampling()
{
    if (mode == PROMPTING_MODE)
    {
        SendPromptSamplingEnd();
    }

    DisableTimer2();//no longer needed
    DisableADC();//turn off conversions

    sampling = false;
}

void OnConversionComplete()
{
    uint16_t adcData = (ADCL | (ADCH << 8)) >> 1;//first put data in one pack, then shift to 9-bit
    //past here im preeeeeeeeeetty sure adcdata is set properly, now usart comms :(

    uint8_t length = sizeof(sampleBuffer80ms) / sizeof(sampleBuffer80ms[0]);

    if (sizeof(sampleBuffer80ms) == length)//if buffer filled up
    {
        SendSampleBuffer(sampleBuffer80ms);
    }

    sampleBuffer80ms[samplesInsideBuffer++] = adcData & 0xFF;//send low byte
    sampleBuffer80ms[samplesInsideBuffer++] = ((adcData >> 8) & 0x1);//send high byte
}