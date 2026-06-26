#include "ADCFunctions.h"
#include "ClockHelper.h"
#include <avr/interrupt.h>
#include <stdint.h>

#define ADCH (*(volatile uint8_t*)0x79)
#define ADCL (*(volatile uint8_t*)0x78)
#define DDRD (*(volatile uint8_t*)0x0A)

bool sampling = false;
bool talking = false;
int timer0InterruptCount = 0;

void setup() {
    Serial.begin(230400);//sending audio at 16khz, no more than 16000*11 (so 176000)b/s needed (11 because of start + stop bit)
    DDRD |= (1 << 2);//set pin 2 to input mode
    attachInterrupt(0, StartedTalking, RISING);//when d0 from microphone on
    attachInterrupt(0, StoppedTalking, FALLING);//when off
}

void loop() {
    
}

ISR(ADC_vect){
    OnConversionComplete();
}

ISR(TIMER0_OVF_vect){//activates every 16.32ms @ 1024 prescaler
    timer0InterruptCount++;
}
//!!!START OF TRANSMISSION IS 0xFF, END OF TRANSMISSION IS 0xEE
void StartedTalking()
{
    if (!sampling)//cant sample twice
    {
        StartSampling();//start recording sound directly
    }

    talking = true;
}

void StartSampling()
{
    StartADC();
    sampling = true;
}

void OnConversionComplete()
{
    uint16_t adcData = (ADCL | (ADCH << 8)) >> 1;
    //past here im preeeeeeeeeetty sure adcdata is set properly, now usart comms :(
    Serial.write(0xFF);
    Serial.write(adcData & 0xFF);
    Serial.write((adcData >> 8) & 0xFF);
}

void StoppedTalking()
{
    talking = false;

    EnableTimer0();
    SetTimer0PrescalerTo1024();

    while (!timer0InterruptCount >= 184)//wait time (~3 seconds for 16.32ms steps)
    {
        if (talking)//if started talking again
        {
            DisableTimer0();//go back to normal sampling
            return;
        }
    }
    //if past waiting time
    StopSampling();
    timer0InterruptCount = 0;
}

void StopSampling()
{
    DisableTimer0();//no longer needed
    DisableADC();
    Serial.write(0xEE);//end of sampling flag

    sampling = false;
}