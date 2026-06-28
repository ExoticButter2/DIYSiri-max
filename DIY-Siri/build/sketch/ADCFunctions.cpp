#line 1 "C:\\Users\\maksi\\OneDrive\\Documents\\GitHub\\DIYSiri Ayo\\DIY-Siri\\ADCFunctions.cpp"
#include "ADCFunctions.h"
#include "ClockHelper.h"
#include <stdint.h>
#include <avr/io.h>

#pragma region NON_HEADER
void ResetADCTimerPrescaler()
{
    ADCSRA &= 0xF8;
}

void SetPrescalerTo128()//conversion speed ~9.26kHz
{
    ResetADCTimerPrescaler();

    ADCSRA |= 7;//111
}

void SetPrescalerTo64()//changes conversion speed to ~18.518kHz
{
    ResetADCTimerPrescaler();

    ADCSRA |= 6;
}

void Setup_Set_Timer1TriggerSource()
{
    ADCSRB = (ADCSRB & 0xF8) | 5;

    EnableTimer1();
    SetTimer1CompareBTo16kHz();//already sets prescaler
}

void DefaultTimer1TriggerSource()
{
    ADCSRB &= ~((1 << ADTS0) | (1 << ADTS1) | (1 << ADTS2));
}

void EnableADCInterrupts()
{
    ADCSRA |= (1 << ADIE);//enable bit 3 (ADIE)
}

void EnableADCPower()
{
    PRR &= ~(1 << PRADC);//disable sleep mode
    ADCSRA |= (1 << ADEN);//enable bit 7 (ADEN)
}

void DisableADCPower()
{
    ADCSRA &= ~(1 << ADEN);//disable bit 7 (ADEN)
    PRR |= (1 << PRADC);//enable sleep mode
}

#pragma endregion

#pragma region HEADER
void StartADC()
{
    ChangeChannel(0);//channel in which microphone is plugged in
    EnableADCPower();
    EnableADCInterrupts();
    SetPrescalerTo64();
    EnableAutoTrigger();
    Setup_Set_Timer1TriggerSource();//sets timer 1 and sets it as trigger source
}

void DisableADC()
{
    ResetADCTimerPrescaler();
    DisableADCPower();
    DefaultTimer1TriggerSource();
    DisableTimer1();
}

void ChangeChannel(int channel)
{
    if (channel < 0 || channel > 5)
    {
        return;
    }

    ADCSRA &= ~(1 << ADATE);//disable ADATE

    ADMUX &= ~((1 << REFS0) | (1 << REFS1) | 0xF);

    ADMUX |= (channel & 0xF) | (1 << REFS0);//vref (AREF) and multiplexer selection

    ADCSRA |= (1 << ADATE);//re-enable ADATE
}

void EnableAutoTrigger()
{
    ADCSRA |= (1 << ADATE);//enable bit 5 (ADATE)
}

void DisableAutoTrigger()
{
    ADCSRA &= ~(1 << ADATE);//disable bit 5 (ADATE)
}

#pragma endregion