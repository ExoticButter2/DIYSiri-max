#include "ClockHelper.h"
#include <stdint.h>
#include <avr/io.h>


#pragma region NON_HEADER

#pragma endregion

#pragma region HEADER
void EnableTimer1()//default prescaler 1
{
    PRR &= ~(1 << PRTIM1);//disable PRTIM1
    SetTimer1PrescalerTo1();
}

void DisableTimer1()
{
    ResetTimer1Prescaler();
    DisableTimer1CTC();
    PRR |= (1 << PRTIM1);
}

void SetTimer1PrescalerTo1()
{
    ResetTimer1Prescaler();

    TCCR1B |= (1 << CS10);
}

void SetTimer1PrescalerTo8()
{
    ResetTimer1Prescaler();

    TCCR1B |= 2;//second bit (010)
}

void ResetTimer1Prescaler()
{
    TCCR1B &= 0xF8;
}

void SetTimer1CompareBTo16kHz()
{
    EnableTimer1CTC();
    SetTimer1PrescalerTo8();
    //set to 124 (125 - 1) for 16khz timing wait actually?? omg
    OCR1B = 124;//fr 1 bih worth 0 sigma
    OCR1A = 124;
}

void EnableTimer1CTC()
{
    TCCR1B |= (1 << WGM12);
}

void DisableTimer1CTC()
{
    TCCR1B &= ~(1 << WGM12);
}


void EnableTimer2()//default prescaler 1
{
    PRR &= ~(1 << PRTIM2);
    SetTimer2PrescalerTo1();
    EnableTimer2OverflowInterrupt();
}

void DisableTimer2()
{
    DisableTimer2OverflowInterrupt();
    ResetTimer2Prescaler();
    PRR |= (1 << PRTIM2);
}

void EnableTimer2OverflowInterrupt()
{
    TIFR2 = (1 << TOV2);//interrupt flag
    TIMSK2 |= (1 << TOIE2);//interrupt toggle
}

void DisableTimer2OverflowInterrupt()
{
    TIFR2 = (1 << TOV2);
    TIMSK2 &= ~(1 << TOIE2);
}

void SetTimer2PrescalerTo1()
{
    ResetTimer2Prescaler();

    TCCR2B |= (1 << CS20);
}

void SetTimer2PrescalerTo1024()
{
    ResetTimer2Prescaler();

    TCCR2B |= 7;//first 3 bits (111)
}

void ResetTimer2Prescaler()
{
    TCCR2B &= 0xF8;
}

#pragma endregion