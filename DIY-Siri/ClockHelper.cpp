#include "ClockHelper.h"
#include <stdint.h>

#define TCCR1B (*(volatile uint8_t*)0x81)
#define TCCR0B (*(volatile uint8_t*)0x25)
#define OCR1BH (*(volatile uint8_t*)0x8B)
#define OCR1BL (*(volatile uint8_t*)0x8A)
#define TIMSK1 (*(volatile uint8_t*)0x6F)
#define TIMSK0 (*(volatile uint8_t*)0x6E)
#define TIFR0 (*(volatile uint8_t*)0x15)
#define PRR (*(volatile uint8_t*)0x64)

#pragma region NON_HEADER

#pragma endregion

#pragma region HEADER
void EnableTimer1()//default prescaler 1
{
    PRR &= ~(1 << 3);//disable PRTIM1
    SetTimer1PrescalerTo1();
}

void DisableTimer1()
{
    ResetTimer1Prescaler();
    PRR |= (1 << 3);
}

void EnableTimer1CompareBInterrupt()
{
    TIMSK1 |= (1 << 2);//enable OCIE1B
}

void DisableTimer1CompareBInterrupt()
{
    TIMSK1 &= ~(1 << 2);//disable OCIE1B
}

void SetTimer1PrescalerTo1()
{
    TCCR1B |= (1 << 0);
    TCCR1B &= ~(1 << 1);
    TCCR1B &= ~(1 << 2);
}

void SetTimer1PrescalerTo8()
{
    TCCR1B &= ~(1 << 0);//disable cs10
    TCCR1B |= (1 << 1);//yeah like ayo fr cs11 11212 12313143423940
    TCCR1B &= ~(1 << 2);//banana
}

void ResetTimer1Prescaler()
{
    TCCR1B &= ~(1 << 0);
    TCCR1B &= ~(1 << 1);
    TCCR1B &= ~(1 << 2);
}

void SetTimer1CompareBTo16kHz()
{
    SetTimer1PrescalerTo8();
    //set to 125 for 16khz timing wait actually?? omg
    OCR1BL;//read low byte before high
    OCR1BH = 0;//fr 1 bih worth 0 sigma
    OCR1BL = 125;
}

void EnableTimer0()//default prescaler 1
{
    PRR &= ~(1 << 5);
    SetTimer0PrescalerTo1();
    EnableTimer0OverflowInterrupts();
}

void EnableTimer0OverflowInterrupts()
{
    TIFR0 &= ~(1 << 0);//interrupt flag
    TIMSK0 |= (1 << 0);//interrupt toggle
}

void DisableTimer0OverflowInterrupts()
{
    TIFR0 &= ~(1 << 0);
    TIMSK0 &= ~(1 << 0);
}

void DisableTimer0()
{
    DisableTimer0OverflowInterrupts();
    ResetTimer0Prescaler();
    PRR |= (1 << 5);
}

void SetTimer0PrescalerTo1()
{
    TCCR0B |= (1 << 0);
    TCCR0B &= ~(1 << 1);
    TCCR0B &= ~(1 << 2);
}

void SetTimer0PrescalerTo1024()
{
    TCCR0B |= (1 << 0);
    TCCR0B |= (1 << 1);
    TCCR0B |= (1 << 2);
}

void ResetTimer0Prescaler()
{
    TCCR0B &= ~(1 << 0);
    TCCR0B &= ~(1 << 1);
    TCCR0B &= ~(1 << 2);
}

void SetTimer0CompareADelay()//goal: 3 seconds
{

}

// void EnableTimer0CompareAInterrupt()
// {

// }

// void DisableTimer0CompareAInterrupt()
// {

// }
#pragma endregion