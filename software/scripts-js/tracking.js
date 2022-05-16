rename("tracking_task");
var tracker = new SharedMap('tracking');

var station1 = new Observer('station_1');

load("../config/config.js");

station1.setPosition( {'latitude' : gs_latitude, 'longitude' : gs_longitude, 'asl' : gs_asl} ); // Création de l'emplacement de la station

var TLE_first; // create TLE
var sat_track = [];

var sat_freq_list = IO.fread("../config/sat_list.txt").split(/\n/);
var nb_target_satellites = sat_freq_list.length;
print(nb_target_satellites + " satellites in the list.");

var freq_list = [];
var target_sat_list = [];
var sat_name_list = [];
var sat_mode_list = [];

for(var i = 0; i < nb_target_satellites; i++)
{
	var sat_infos = sat_freq_list[i].split(/;/);
	target_sat_list[i] = parseInt(sat_infos[0]);
	freq_list[i] = parseFloat(sat_infos[1]); 
	sat_mode_list[i] = sat_infos[2];
}

if(print_debug)
{
	print("SAT LIST : " + target_sat_list);
	print("FREQ LIST : " + freq_list);
	print("MODES LIST : " + sat_mode_list);
}

while(1)
{
	var satlist = TLE.loadTLE(tle_path); // Download TLE

	if(print_debug)
	{
		print(satlist.length + ' satellites loaded.');
	}

	for(var i=0; i < nb_target_satellites; i++)
	{
		for(var j=0; j < satlist.length; j++) // Read downloaded TLE
		{
			TLE_first = satlist[j];
			sat_name_list[i] = satlist[j].name;

				if(TLE_first.norad_number == target_sat_list[i]) // Search the NORAD number in the TLE
				{
					sat_track[i] = new Satellite(satlist[j].name);
					sat_track[i].setTLE(TLE_first.L1, TLE_first.L2);
					break;
				}
			
		}
	}

	if(print_debug)
	{
		print("SAT NAME LIST : " + sat_name_list);
	}

	var passes = [];

	for(var i = 0; i < nb_target_satellites; i++)
	{
		passes[i] = sat_track[i].predictPasses(station1, 36); // calcul des passages sur les prochaines 24h sur la station sol

		if(passes[i].length > 0)
		{
			for(n=0; n < 5; n++)
			{
				var next = passes[i][n]; // On sélectionne le prochain passage
				var dopev = sat_track[i].getPassDetails(station1, next.aos_secs, next.pass_duration); // Stocke les infos du prochains passage
				if(print_passes)
				{
					print(sat_name_list[i] + " : " + "AOS : " + dopev.pass_start_time + " -- LOS : " + dopev.pass_end_time + " -- max elev : " + passes[i][n].max_elevation);
				}
				
			}

		}
	}

	var n = 0;
	var sat_id_in_view;
	var satellite_in_view = false;

	while(satellite_in_view == false)
	{
		for(var i = 0; i < nb_target_satellites; i++)
		{
			if(sat_track[i].waitInView(station1) == true)
			{
				satellite_in_view = true;
				sat_id_in_view = i;
				print(sat_name_list[sat_id_in_view] + " in view !");
				break;
			}
			else
			{
				satellite_in_view = false;
				if(print_debug)
				{
					passes = sat_track[i].predictPasses(station1, 15);
					print("Waiting " + sat_name_list[i] + ", AOS in " + new Date(passes[0].aos_secs * 1000).toISOString().substr(11, 8) );
				}
			}
		}
		sleep(2000);
	}

	var n = 0;
	while(sat_track[sat_id_in_view].waitInView(station1) == true)
	{
		var doppler = sat_track[sat_id_in_view].getDopplerEstimation( station1, freq_list[i] );
		tracker.store('doppler', doppler.doppler_avg);
		tracker.store('frequency',freq_list[i]);
		
		if(print_debug)
		{
			print("Doppler: " + doppler.doppler_avg);
		}
		tracker.store('status', true);
		if(!n)
		{
			createTask("../scripts-js/create_fifo.js");
			sleep(100);
			
			createTask("../scripts-js/gnuradio.js", target_sat_list[sat_id_in_view].toString(), sat_mode_list[sat_id_in_view]);

			sleep(3000);
			createTask("../scripts-js/stream.js");

			n = 1;
		}
		sleep(1000);
	}

	tracker.store('status', false);
	if(print_debug)
	{
		print("End of pass, starting end of pass task...");
	}

	createTask("../scripts-js/end_pass.js", target_sat_list[sat_id_in_view].toString(), sat_mode_list[sat_id_in_view]);
}