#ifndef CLOCKHELPER_H
#define CLOCKHELPER_H

void EnableTimer1();
void DisableTimer1();
void SetTimer1PrescalerTo1();
void SetTimer1PrescalerTo8();
void ResetTimer1Prescaler();
void SetTimer1CompareBTo16kHz();
void SetTimer1CompareBInterrupt();
void SetTimer1CompareADelay();
void EnableTimer1CTC();
void DisableTimer1CTC();

void EnableTimer2();
void DisableTimer2();
void SetTimer2PrescalerTo1();
void SetTimer2PrescalerTo1024();
void ResetTimer2Prescaler();
void EnableTimer2OverflowInterrupt();
void DisableTimer2OverflowInterrupt();

#endif