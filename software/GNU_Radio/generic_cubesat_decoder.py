#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Generic cubesat decoder
# Author: Enzo BECAMEL F4IAI
# Description: Cubesat decoder with telemtry parse & forward for automatic ground station.
# GNU Radio version: 3.8.5.0

from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import relative_path  # embedded python module
import satellites
import satellites.components.datasinks
import satellites.core
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class generic_cubesat_decoder(gr.top_block):

    def __init__(self, sat_norad=1):
        gr.top_block.__init__(self, "Generic cubesat decoder")

        ##################################################
        # Parameters
        ##################################################
        self.sat_norad = sat_norad

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.result_folder_path = result_folder_path = "../results/"
        self._link_forwarder_config = configparser.ConfigParser()
        self._link_forwarder_config.read('gs_config.ini')
        try: link_forwarder = self._link_forwarder_config.get('main', 'link')
        except: link_forwarder = "no"
        self.link_forwarder = link_forwarder
        self._kiss_server_port_config = configparser.ConfigParser()
        self._kiss_server_port_config.read('gs_config.ini')
        try: kiss_server_port = self._kiss_server_port_config.get('main', 'kiss_port')
        except: kiss_server_port = "no"
        self.kiss_server_port = kiss_server_port
        self._gs_longitude_config = configparser.ConfigParser()
        self._gs_longitude_config.read('gs_config.ini')
        try: gs_longitude = self._gs_longitude_config.getfloat('main', 'longitude')
        except: gs_longitude = 0.0000
        self.gs_longitude = gs_longitude
        self._gs_latitude_config = configparser.ConfigParser()
        self._gs_latitude_config.read('gs_config.ini')
        try: gs_latitude = self._gs_latitude_config.getfloat('main', 'latitude')
        except: gs_latitude = 0.0000
        self.gs_latitude = gs_latitude
        self._gs_callsign_config = configparser.ConfigParser()
        self._gs_callsign_config.read('gs_config.ini')
        try: gs_callsign = self._gs_callsign_config.get('main', 'callsign')
        except: gs_callsign = "no"
        self.gs_callsign = gs_callsign

        ##################################################
        # Blocks
        ##################################################
        self.satellites_telemetry_parser_0 = satellites.components.datasinks.telemetry_parser('ax25', file = result_folder_path + "decoder_output.txt", options="")
        self.satellites_submit_0 = satellites.submit(link_forwarder, int(sat_norad), gs_callsign, gs_longitude, gs_latitude, '')
        self.satellites_satellite_decoder_0 = satellites.core.gr_satellites_flowgraph(norad = sat_norad, samp_rate = samp_rate, grc_block = True, iq = True, options = "")
        self.satellites_kiss_server_sink_0 = satellites.components.datasinks.kiss_server_sink("", 8100, options="")
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(False, False)
        self.blocks_file_source_0_0_0 = blocks.file_source(gr.sizeof_short*1, '/opt/GS_ramdisk/rx.cs16', False, 0, 0)
        self.blocks_file_source_0_0_0.set_begin_tag(pmt.PMT_NIL)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.satellites_kiss_server_sink_0, 'in'))
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.satellites_submit_0, 'in'))
        self.msg_connect((self.satellites_satellite_decoder_0, 'out'), (self.satellites_telemetry_parser_0, 'in'))
        self.connect((self.blocks_file_source_0_0_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.satellites_satellite_decoder_0, 0))


    def get_sat_norad(self):
        return self.sat_norad

    def set_sat_norad(self, sat_norad):
        self.sat_norad = sat_norad

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_result_folder_path(self):
        return self.result_folder_path

    def set_result_folder_path(self, result_folder_path):
        self.result_folder_path = result_folder_path

    def get_link_forwarder(self):
        return self.link_forwarder

    def set_link_forwarder(self, link_forwarder):
        self.link_forwarder = link_forwarder

    def get_kiss_server_port(self):
        return self.kiss_server_port

    def set_kiss_server_port(self, kiss_server_port):
        self.kiss_server_port = kiss_server_port

    def get_gs_longitude(self):
        return self.gs_longitude

    def set_gs_longitude(self, gs_longitude):
        self.gs_longitude = gs_longitude

    def get_gs_latitude(self):
        return self.gs_latitude

    def set_gs_latitude(self, gs_latitude):
        self.gs_latitude = gs_latitude

    def get_gs_callsign(self):
        return self.gs_callsign

    def set_gs_callsign(self, gs_callsign):
        self.gs_callsign = gs_callsign




def argument_parser():
    description = 'Cubesat decoder with telemtry parse & forward for automatic ground station.'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--sat-norad", dest="sat_norad", type=intx, default=1,
        help="Set sat_norad [default=%(default)r]")
    return parser


def main(top_block_cls=generic_cubesat_decoder, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(sat_norad=options.sat_norad)

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
