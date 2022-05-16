#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: NOAA APT decoder
# Author: Enzo BECAMEL F4IAI
# Description: APT NOAA decoder for automatic ground station.
# GNU Radio version: 3.8.5.0

from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import relative_path  # embedded python module
import satnogs


class noaa_apt_decoder(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "NOAA APT decoder")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.result_folder_path = result_folder_path = "../results/"
        self.audio_samp_rate = audio_samp_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self.satnogs_noaa_apt_sink_0 = satnogs.noaa_apt_sink(result_folder_path + "picture.png", 2080, 1800, True, True)
        self.rational_resampler_xxx_2 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=4,
                taps=None,
                fractional_bw=0.000000000000000001)
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=16640,
                decimation=31250,
                taps=None,
                fractional_bw=0.000000000000000001)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=62500,
                decimation=48000,
                taps=None,
                fractional_bw=0.000000000000000001)
        self.hilbert_fc_0 = filter.hilbert_fc(65, firdes.WIN_HAMMING, 6.76)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(2, [0.5])
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/enzo/Documents/GNURadio/decodeur_NOAA/record.cf32', False, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.band_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                6,
                62500,
                500,
                4200,
                200,
                firdes.WIN_HAMMING,
                6.76))
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=audio_samp_rate,
        	audio_decimation=1,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.rational_resampler_xxx_2, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.hilbert_fc_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.hilbert_fc_0, 0))
        self.connect((self.rational_resampler_xxx_2, 0), (self.satnogs_noaa_apt_sink_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_result_folder_path(self):
        return self.result_folder_path

    def set_result_folder_path(self, result_folder_path):
        self.result_folder_path = result_folder_path

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate





def main(top_block_cls=noaa_apt_decoder, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
