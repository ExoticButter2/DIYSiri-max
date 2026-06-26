#include "ADCFunctions.h"
#include "ClockHelper.h"
#include <avr/interrupt.h>
#include <stdint.h>

#define ADCH (*(volatile uint8_t*)0x79)
#define ADCL (*(volatile uint8_t*)0x78)

void setup() {
    StartADC();//boots up adc
    
}

void loop() {
    
}

ISR(_VECTOR(21)){
    OnConversionComplete();
}

void OnConversionComplete()
{
    uint16_t adcData = ADCL;//get 8 lower bits
    adcData |= (ADCH << 8);//get the other 2 high bits
    adcData >> 1;//9-bit precision
    //past here im preeeeeeeeeetty sure adcdata is set properly, now usart comms :(
}