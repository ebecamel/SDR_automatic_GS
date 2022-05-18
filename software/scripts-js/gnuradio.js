rename("gnuradio_task")
load("../config/config.js");

var command_end_pass = {
    'command' : "/bin/bash",
    'args' : ['../launch_decoder.sh', argv(0), argv(1)]
    };
 
var msg_python = System.exec( command_end_pass );

if(print_debug)
{
    print(JSON.stringify(msg_python));
}