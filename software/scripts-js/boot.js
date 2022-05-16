rename("boot_prog");
load("../config/config.js");
createTask("../scripts-js/tracking.js");
IO.fwritestr("../GNU_Radio/decoder_config.ini", "[main]\nlink=" + sids_server + "\nlatitude=" + gs_latitude + "\nlongitude=" + gs_longitude + "\ncallsign=" + receiver_callsign);