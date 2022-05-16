# SDR based autotmatic Ground Station
Automatic SDR based ground station for VHF and UHF satellite reception. Working on Linux computer and Jetson Nano 2GB / 4GB.

## Description
The objective is to build a automatic ground station. The software download the TLE, predict passses, track satellites, receive the signal, demodule the signal and upload the datas.
The ground station can receive :
- Telemetry (do a txt output file with HEX datas),
- SSTV PD120 mode (produce a .png picture),
- APT from NOAA 15, 18 and 19 (produce .png picture),
- Narrow band FM (produce a .wav audio file).

## Requirements
To build this ground station you need to install :
- sdr4space.light (tested with all versions),
- GNU Radio Companion (tested with version 3.8),
- gr-satellites library,
- gr-satnogs library.

#### sdr4space.light
sdr4space.light is a freeware software. To use the software, you just need to download the .appImage file for your system from this link : [https://github.com/SDR4space/FreeVersion/releases](https://github.com/SDR4space/FreeVersion/releases).
Maybe you will have to install some dependencies :
- SoapySDR 0.8
- fftw3-3
- libliquid1d
- mosquitto
- mosquitto-clients

#### GNU Radio Companion
GNU Radio Companion is an Open-Source software to develop Sofwware Defined Radio based applications.
To install GNU Radio on a computer you can read the [dedicated page on my website](https://f4iai.fr/logiciels/gnu-radio/installation-du-logiciel-gnu-radio-companion-sous-linux/).

For Jetson Nano, I recommand to use a Linux distribution with GNU Radio already installed. You can download the [NanoSDR distribution available on this link](https://github.com/SDR-Technologies/NanoSDR).

#### gr-satellites
With GNU Radio you need to install the gr-satellites library to add satellites functions to GNU Radio. You can read how to install [on the dediacted Git](https://github.com/daniestevez/gr-satellites) and [on the online documentation](https://gr-satellites.readthedocs.io/en/latest/installation_intro.html).

#### gr-satnogs
With GNU Radio you need to install the gr-satellites library to add some decoders to GNU Radio. You can read how to install [on the dediacted Git](https://gitlab.com/librespacefoundation/satnogs/gr-satnogs). 

#### The ramdisk
You need to create a ramdisk for the fifo file. For this, add the following line in /etc/fstab :
~~~
tmpfs /opt/GS_ramdisk tmpfs   defaults,size=128M   0 0
~~~
If you want you can replace /opt/GS_ramdisk by an other path.

## How to use ?
First you need to download the files from this git. You can copy the software folder where you want. In this folder you can find all Javascripts files and Python scripts you need. All scripts are working, you just need to configure some variables. For this, the only files you have to edit is the general configuration file and the satellite list in **software/config/config.js** and **software/config/sat_list.txt**.

#### config.js file
This file contain all the variables needed by the ground station to work :
- Ground station configuration (ground station coordinates and altitude),
- File path (path to important files : TLE, bash command file and fifo in ramdisk),
- RTLSDR (RX gain for the rtlsdr receiver),
- Print in terminal (allow or no the debug in terminal and print all the passes),
- Upload config :
-- FTP : allow or no the ftp upload of datas and define the server configuration,
-- SIDS : allow or no the SIDS upload of decoded telemetry (for SatNOGS for example) and define the SIDS server

#### sat_list.txt
This file contain the list of the satellites you want receive. Be aware about the satellites available with your TLE (with the default TLE link you can receive all satellites availables on SatNOGS).
You have to fill the file with this struture (one satellite by line) :
***NORAD_ID;FREQUENCY_HZ;MODE***

You can read the file from the git who allow the reception of 4 satellites :
- Satellite 40967 (FO-29) on 145.980 MHz in Narrow band FM,
- Satellite 47438 (UVSQ-SAT) on 437.020 MHz, telemetry decode,
- Satellite 42792 (ROBUSTA-1B) on 437.325 MHz, telemetry decode,
- Satellite 25338 (NOAA-15) on 137.620 MHz, APT decode.

A this time, 4 types of reception are availaibles :
- NFM for Narrow band FM (audio record),
- TM for telemetry decode (txt file),
- APT for NOAA APT decode (picture),
- PD120 for SSTV PD120 decode (picture).

## Launch the ground station
You can launch the ground station with the following command in your terminal :
~~~
path/to/sdr4space/sdr4space_lite_version.AppImage -d path/to/software/scripts-js/
~~~

You can find all the results of the passes in the results folder (and / or on the FTP and / or SIDS if you configure them)
