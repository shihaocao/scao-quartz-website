---
title: Radio
date: 2025-03-18
tags:
  - something...
---

Objectives

- Understand how we as a society got here... how did wireless communication come to be?
- Pick apart one of these channels and understand how it works, what it looks like, and how does it do its job

Areas of interest
- FM
- LTE
- WiFi
- BT
- 915 mhz

FM
- What is decimation, and why does a low pass filter do anything interesting?
- Yay I have a FM radio!
- Links
  - https://en.wikipedia.org/wiki/FM_broadcasting
  - ![FM](http://upload.wikimedia.org/wikipedia/commons/a/ac/ElectromagneticSpectrum-Radio-VHF-FM.png)

<div style="flex: 1; display: flex; justify-content: center; max-width: 100%; margin: 0 5px;">
    <img src="notes/radio/images/fm_rx.jpg" style="height: auto; max-width: 80%;">
</div>
<div style="flex: 1; display: flex; text-align: center; justify-content: center; font-style: italic;">Getting a FM reciever to work in HackRF + GRC.</div>

What are the stages in FM Demodulation?
- Radio Demodulation
  - Extract the baseband signal from the carrier signal

LTE:
- https://www.blackhillsinfosec.com/intro-to-software-defined-radio-and-gsm-lte/
- https://github.com/JiaoXianjun/LTE-Cell-Scanner
- https://www.sharetechnote.com/html/FrameStructure_DL.html

```
shihao@shihao-T490V2:~/Code/radio/kalibrate-hackrf$ kal -s GSM900 -g 40
kal: Scanning for GSM-900 base stations.
GSM-900:
	chan:  121 (959.2MHz + 33.246kHz)	power: 1495086.29
	chan:  122 (959.4MHz + 33.356kHz)	power: 1545344.57
	chan:  123 (959.6MHz + 8.301kHz)	power: 1575789.55
	chan:  124 (959.8MHz - 16.792kHz)	power: 1616360.63
```

```
/src/CellSearch   -s 1931000000   -e 1990000000   -g 40   -v
```

```
Examining center frequency 1942.3 MHz ... try 0
Capturing live data
PSS XCORR  cost 2.21364s
  Calculating PSS correlations
  Searching for and examining correlation peaks...
Hit  num peaks 1
try peak 0 tdd_flag 0
try peak 0 tdd_flag 1
```

This works
```
./src/CellSearch   -s 1950000000   -e 1950300000   -g 40   -v  --correction 1.00004
```

```
 ./src/LTE-Tracker -f 1950100000 -g 40
```

<div style="flex: 1; display: flex; justify-content: center; max-width: 100%; margin: 0 5px;">
    <img src="notes/radio/images/LTE-cell.jpg" style="height: auto; max-width: 80%;">
</div>
<div style="flex: 1; display: flex; text-align: center; justify-content: center; font-style: italic;">I can see the PSS and RBs and subframes?</div>
