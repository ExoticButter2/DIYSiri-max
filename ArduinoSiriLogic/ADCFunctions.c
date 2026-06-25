#include "ADCFunctions.h"
#include "ClockHelper.h"
#include <stdint.h>

#define PRR (*(volatile uint8_t*)0x64)
#define ADCSRA (*(volatile uint8_t*)0x7A)
#define ADMUX (*(volatile uint8_t*)0x7C)
#define ADCSRB (*(volatile uint8_t*)0x7B)

#pragma region NON_HEADER
void SetPrescalerTo128()
{
    ADCSRA |= (1 << 0);
    ADCSRA |= (1 << 1);
    ADCSRA |= (1 << 2);
}

void SetPrescalerTo64()
{
    ADCSRA &= ~(1 << 0);
    ADCSRA |= (1 << 1);
    ADCSRA |= (1 << 2);
}

void SetTriggerSourceToTimer1()
{
    ADCSRB |= (1 << 0);//enable ADTS0
    ADCSRB &= ~(1 << 1);//disable ADTS1
    ADCSRB |= (1 << 2);//enable ADTS2
}

void EnableADCInterrupts()
{
    ADCSRA |= (1 << 3);//enable bit 3 (ADIE)
}

void EnableADCPower()
{
    ADCSRA |= (1 << 7);//enable bit 7 (ADEN)
}

#pragma endregion

#pragma region HEADER
void StartADC()
{
    EnableADCPower();
    EnableADCInterrupts();
    SetPrescalerTo128();
    SetTriggerSourceToTimer0();
    EnableAutoTrigger();
}

void DisableADC()
{
    ADCSRA &= ~(1 << 7);//disable bit 7 (ADEN)
}

void ChangeChannel(int channel)
{

}

void EnableAutoTrigger()
{
    ADCSRA |= (1 << 5);//enable bit 5 (ADATE)
}

void DisableAutoTrigger()
{
    ADCSRA &= ~(1 << 5);//disable bit 5 (ADATE)
}

void StartConversion()
{
    PRR &= ~(1 << 0);//clear bit 0 (PRADC)
    ADCSRA |= (1 << 6);//enable bit 6 (ADSC)


}

#pragma endregion