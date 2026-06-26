#include "ADCFunctions.h"
#include "ClockHelper.h"
#include <stdint.h>

#define PRR (*(volatile uint8_t*)0x64)
#define ADCSRA (*(volatile uint8_t*)0x7A)
#define ADMUX (*(volatile uint8_t*)0x7C)
#define ADCSRB (*(volatile uint8_t*)0x7B)

#pragma region NON_HEADER
void SetPrescalerTo128()//conversion speed ~9.26kHz
{
    ADCSRA |= (1 << 0);
    ADCSRA |= (1 << 1);
    ADCSRA |= (1 << 2);
}

void SetPrescalerTo64()//changes conversion speed to ~18.518kHz
{
    ADCSRA &= ~(1 << 0);
    ADCSRA |= (1 << 1);
    ADCSRA |= (1 << 2);
}

void Setup_Set_Timer1TriggerSource()
{
    ADCSRB |= (1 << 0);//enable ADTS0
    ADCSRB &= ~(1 << 1);//disable ADTS1
    ADCSRB |= (1 << 2);//enable ADTS2

    EnableTimer1();
    SetTimer1CompareBTo16kHz();//already sets prescaler
    EnableTimer1CompareBInterrupt();
}

void EnableADCInterrupts()
{
    ADCSRA |= (1 << 3);//enable bit 3 (ADIE)
}

void EnableADCPower()
{
    ADCSRA |= (1 << 7);//enable bit 7 (ADEN)
    PRR &= ~(1 << 0);//disable sleep mode
}

void DisableADCPower()
{
    ADCSRA &= ~(1 << 7);//disable bit 7 (ADEN)
    PRR |= (1 << 0);//enable sleep mode
}

#pragma endregion

#pragma region HEADER
void StartADC()
{
    ChangeChannel(0);//channel in which microphone is plugged in
    EnableADCPower();
    EnableADCInterrupts();
    SetPrescalerTo64();
    Setup_Set_Timer1TriggerSource();//sets timer 1 and sets it as trigger source
    EnableAutoTrigger();
}

void DisableADC()
{
    DisableADCPower();
    DisableTimer1CompareBInterrupt();
    DisableTimer1();
}

void ChangeChannel(int channel)
{
    ADCSRA &= ~(1 << 5);//disable ADATE

    switch (channel)//omds so much boilerplate hell nah
    {
        case 0:
            ADMUX &= ~(1 << 0);
            ADMUX &= ~(1 << 1);
            ADMUX &= ~(1 << 2);
            ADMUX &= ~(1 << 3);
        case 1:
            ADMUX |= (1 << 0);
            ADMUX &= ~(1 << 1);
            ADMUX &= ~(1 << 2);
            ADMUX &= ~(1 << 3);
        case 2:
            ADMUX &= ~(1 << 0);
            ADMUX |= (1 << 1);
            ADMUX &= ~(1 << 2);
            ADMUX &= ~(1 << 3);
        case 3:
            ADMUX |= (1 << 0);
            ADMUX |= (1 << 1);
            ADMUX &= ~(1 << 2);
            ADMUX &= ~(1 << 3);
        case 4:
            ADMUX &= ~(1 << 0);
            ADMUX &= ~(1 << 1);
            ADMUX |= (1 << 2);
            ADMUX &= ~(1 << 3);
        case 5:
            ADMUX |= (1 << 0);
            ADMUX &= ~(1 << 1);
            ADMUX |= (1 << 2);
            ADMUX &= ~(1 << 3);
    }

    ADCSRA |= (1 << 5);//re-enable ADATE
}

void EnableAutoTrigger()
{
    ADCSRA |= (1 << 5);//enable bit 5 (ADATE)
}

void DisableAutoTrigger()
{
    ADCSRA &= ~(1 << 5);//disable bit 5 (ADATE)
}

#pragma endregion