#include "ClockHelper.h"
#include <stdint.h>

#define TCCR1B (*(volatile uint32_t*)0x81)
#define OCR1BH (*(volatile uint32_t*)0x8B)
#define OCR1BL (*(volatile uint32_t*)0x8A)
#define TIMSK1 (*(volatile uint32_t*)0x6F)
#define PRR (*(volatile uint8_t*)0x64)

#pragma region NON_HEADER

#pragma endregion

#pragma region HEADER
void EnableTimer1()
{
    PRR &= ~(1 << 3);//disable PRTIM1
}

void EnableTimer1CompareBInterrupt()
{
    TIMSK1 |= (1 << 2);//enable OCIE1B
}

void DisableTimer1CompareBInterrupt()
{
    TIMSK1 &= ~(1 << 2);//disable OCIE1B
}

void SetTimer1PrescalerTo8()
{
    TCCR1B &= ~(1 << 0);//disable cs10
    TCCR1B |= (1 << 1);//yeah like ayo fr cs11 11212 12313143423940
    TCCR1B &= ~(1 << 2);//banana
}

void EnableTimer1CompareBTo16kHz()
{
    EnableTimer1CompareBInterrupt();
    SetTimer1PrescalerTo8();
    //set to 125 for 16khz timing wait actually?? omg
    OCR1BL;//read low byte before high
    OCR1BH = 0;//fr 1 bih worth 0 sigma
    OCR1BL = 125;//ayo 0xddddddd
}
#pragma endregion