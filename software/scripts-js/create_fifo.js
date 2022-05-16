rename("fifo_creation_task")
load("../config/config.js");

var command_create_fifo = {
    'command' : "/bin/mkfifo",
    'args' : [ramdisk_path]
    };
 
var msg = System.exec( command_create_fifo );

if(print_debug)
{
    print(JSON.stringify(msg));
}
