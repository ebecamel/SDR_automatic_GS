#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM narrow band recorder
# Author: Enzo BECAMEL F4IAI
# Description: FM narrow band receiver & recorder for automatic ground station
# GNU Radio version: 3.8.5.0

from gnuradio import analog
from gnuradio import audio
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


class fm_narrow_recorder(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "FM narrow band recorder")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.result_folder_path = result_folder_path = "../results/"
        self.audio_samp_rate = audio_samp_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                12e3,
                1e3,
                firdes.WIN_HAMMING,
                6.76))
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(result_folder_path + "audio_record.wav", 1, audio_samp_rate, 8)
        self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(False, False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, '/opt/GS_ramdisk/rx.cs16', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0.set_min_output_buffer(1024)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=audio_samp_rate,
        	quad_rate=samp_rate,
        	tau=75e-6,
        	max_dev=5e3,
          )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_nbfm_rx_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 12e3, 1e3, firdes.WIN_HAMMING, 6.76))

    def get_result_folder_path(self):
        return self.result_folder_path

    def set_result_folder_path(self, result_folder_path):
        self.result_folder_path = result_folder_path
        self.blocks_wavfile_sink_0.open(self.result_folder_path + "audio_record.wav")

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate





def main(top_block_cls=fm_narrow_recorder, options=None):
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
