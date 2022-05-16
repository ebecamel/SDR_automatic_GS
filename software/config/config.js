/*
    STATION CONFIGURATION FILE
*/

// Ground station configuration
var gs_latitude = 0.00000; // latitude
var gs_longitude = 150.00000; // longitude
var gs_asl = 200; // Altitude above sea level

// file path
var tle_path = "https://www.celestrak.com/NORAD/elements/gp.php?GROUP=satnogs&FORMAT=tle"; // path to .txt file or link to TLE file. Default link is satellites available on SatNOGS
var path_cmd_file = "../launch_decode.sh"; // path to the bash file
var ramdisk_path = "/opt/GS_ramdisk/rx.cs16"; // Path to ramdish and FIFO

// RTLSDR
var rtl_gain = -1; // rtlsdr gain

// Print in terminal
var print_passes = true; // print list of future passes true or false
var print_debug = true; //Print debug in terminal true or false

// Upload config
    //FTP
var send_by_ftp = false; // Send data by ftp or no (True or False);
var ftp_server = "ftp://server"; // FTP server address
var ftp_username = "username"; // FTP username
var ftp_password = "password"; // FTP password
var ftp_destination_folder = "path/to/directory"; // Path to detsination folder on the FTP server
    //SIDS
var send_to_satnogs = false; // Send data by SIDS (SatnOGS for example)  or no (True or False)
var sids_server = "sids-server.com"; // SIDS server address (https://db.satnogs.org/api/telemetry/ for SatnOGS server)
var receiver_callsign = "FXXXX"; // Receiver callsign for SIDS send
