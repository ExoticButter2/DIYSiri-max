#ifndef CLOCKHELPER_H
#define CLOCKHELPER_H

void EnableTimer1();
void DisableTimer1();
void SetTimer1PrescalerTo8();
void SetTimer1CompareBTo16kHz();
void SetTimer1CompareBInterrupt();
void EnableTimer1CompareBInterrupt();
void DisableTimer1CompareBInterrupt();
void SetTimer1CompareADelay();
void EnableTimer0();
void DisableTimer0();
void SetTimer0PrescalerTo1();
void SetTimer0PrescalerTo1024();
// void EnableTimer0CompareAInterrupt();
// void DisableTimer0CompareAInterrupt();

#endif