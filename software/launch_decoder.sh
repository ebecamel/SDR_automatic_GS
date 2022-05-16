#!/bin/sh
CWD=$(pwd)
cd $CWD
cd ../GNU_Radio/


case $2 in
    TM)
        /usr/bin/python3 generic_cubesat_decoder.py --sat-norad $1
        ;;

    PD120)
        /usr/bin/python3 sstv_pd120_decoder.py
        ;;

    NFM)
        /usr/bin/python3 fm_narrow_recorder.py
        ;;

    APT)
        /usr/bin/python3 noaa_apt_decoder.py
        ;;
    
    *)
        echo "Unknow decoder selection $2"
        ;;
esac