rename("end_of_pass_task");
load("../config/config.js");

var norad_number = parseInt(argv(0));
var mode = argv(1);
var final_output = "";


if(send_by_ftp)
{
    if(print_debug)
    {
        print("Send the result by FTP to " + ftp_server);
    }

    var ftp_params = {
        host: ftp_server,
        user: ftp_username,
        password: ftp_password,
        passive: true,
        destination_folder: ftp_destination_folder
   };

   if(mode == "NFM")
   {
        final_output = '../results/' + norad_number + '_' + mode + '_audio_record.wav';
        IO.frename('../results/audio_record.wav', final_output);
   }
   else if(mode == "TM")
   {
        final_output = '../results/' + norad_number + '_' + mode + '_decoder_output.txt';
        IO.frename('../results/decoder_output.txt', final_output);
   }
   else if(mode == "APT" || mode == "PD120")
   {
        final_output = '../results/' + norad_number + '_' + mode + '_picture.png';
        IO.frename('../results/picture.png', final_output);
   }

   var ftp_connect_result = IO.FTPSend( ftp_params, final_output);
}