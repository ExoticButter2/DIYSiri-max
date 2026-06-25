#ifndef CLOCKHELPER_H
#define CLOCKHELPER_H

void EnableTimer1();
void SetTimer1PrescalerTo8();
void SetTimer1CompareBTo9kHz();
void EnableTimer1CompareBInterrupt();
void DisableTimer1CompareBInterrupt();

#endif