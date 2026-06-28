#include <Arduino.h>
#line 1 "C:\\Users\\maksi\\OneDrive\\Documents\\GitHub\\DIYSiri Ayo\\DIY-Siri\\DIY-Siri.ino"
#include "ADCFunctions.h"
#include "ClockHelper.h"
#include <avr/interrupt.h>
#include <avr/io.h>
#include <stdint.h>

bool sampling = false;
bool talking = false;
int timer0InterruptCount = 0;

#line 11 "C:\\Users\\maksi\\OneDrive\\Documents\\GitHub\\DIYSiri Ayo\\DIY-Siri\\DIY-Siri.ino"
void setup();
#line 18 "C:\\Users\\maksi\\OneDrive\\Documents\\GitHub\\DIYSiri Ayo\\DIY-Siri\\DIY-Siri.ino"
void loop();
#line 30 "C:\\Users\\maksi\\OneDrive\\Documents\\GitHub\\DIYSiri Ayo\\DIY-Siri\\DIY-Siri.ino"
void StartedTalking();
#line 40 "C:\\Users\\maksi\\OneDrive\\Documents\\GitHub\\DIYSiri Ayo\\DIY-Siri\\DIY-Siri.ino"
void StartSampling();
#line 46 "C:\\Users\\maksi\\OneDrive\\Documents\\GitHub\\DIYSiri Ayo\\DIY-Siri\\DIY-Siri.ino"
void OnConversionComplete();
#line 56 "C:\\Users\\maksi\\OneDrive\\Documents\\GitHub\\DIYSiri Ayo\\DIY-Siri\\DIY-Siri.ino"
void StoppedTalking();
#line 76 "C:\\Users\\maksi\\OneDrive\\Documents\\GitHub\\DIYSiri Ayo\\DIY-Siri\\DIY-Siri.ino"
void StopSampling();
#line 11 "C:\\Users\\maksi\\OneDrive\\Documents\\GitHub\\DIYSiri Ayo\\DIY-Siri\\DIY-Siri.ino"
void setup() {
    Serial.begin(230400);//sending audio at 16khz, no more than 16000*11 (so 176000)b/s needed (11 because of start + stop bit)
    DDRD |= (1 << DDD2);//set pin 2 to input mode
    attachInterrupt(0, StartedTalking, RISING);//when d0 from microphone on
    attachInterrupt(0, StoppedTalking, FALLING);//when off
}

void loop() {
    
}

ISR(ADC_vect){
    OnConversionComplete();
}

ISR(TIMER2_OVF_vect){//activates every 16.32ms @ 1024 prescaler
    timer0InterruptCount++;
}
//!!!START OF (PACKET) IS 0xAA FOLLOWED BY 0x55, END OF SAMPLE IS 0xEE
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
    sampling = true;
    StartADC();
}

void OnConversionComplete()
{
    uint16_t adcData = (ADCL | (ADCH << 8)) >> 1;//first put data in one pack, then shift to 9-bit
    //past here im preeeeeeeeeetty sure adcdata is set properly, now usart comms :(
    Serial.write(0xAA);//conversion transmit start
    Serial.write(0xDA);//second part
    Serial.write(adcData & 0xFF);
    Serial.write((adcData >> 8) & 0x55);
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

void StopSampling()
{
    DisableTimer2();//no longer needed
    DisableADC();
    Serial.write(0xEE);//end of sampling flag

    sampling = false;
}
