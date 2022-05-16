rename("stream_task");
load("../config/config.js");
var tracker = new SharedMap('tracking');


var fifo_from_rx = Queues.create( 'input');
var fifo_to_file = Queues.create( 'outut');
var IQBlock = new IQData('iq');
var samples = 0 ;



var rx = Soapy.makeDevice( {'query' : 'driver=rtlsdr' });
if( typeof rx != 'object' ) {
	print('no radio ?');
	exit();
}

if( !rx.isValid()) {
	print('no radio ?');
	exit();
}

if( rx.isAvailable() ) {
   // set sample rate
   if( rx.setRxSampleRate( 1e6 )) {
      if(print_debug)
      {
         print('Sample rate changed');
      }  
   }
} else {
   print('device is already used, we do not change Sampling Rate');
}

var current_frequency = tracker.load("frequency");


rx.setGain( rtl_gain, 0 );
rx.setRxCenterFreq( (current_frequency/1e6) - 0.2);

// create output file
if(print_debug)
{
   print('create out queue');
}

fifo_to_file.writeToFile(ramdisk_path);

if(print_debug)
{
   print('connect queue to receiver');
}

// engage streaming
if( !fifo_from_rx.ReadFromRx( rx ) ) {
	print('Cannot stream from rx');
	exit();
}



var slice = new DDC('one');
slice.setOutBandwidth(48e3); // 48 kHz output
slice.setCenter( 200e3) ;

if(print_debug)
{
   print('starting rx process');
}

var doppler_value = tracker.load("doppler");

var sat_view = tracker.load("status");

while( fifo_from_rx.isFromRx() && sat_view) { // if we have something in the input
    sat_view = tracker.load("status");
    if( IQBlock.readFromQueue( fifo_from_rx ) ) {     // load samples from input queue into IQBlock object
        slice.write( IQBlock );               // write the samples in the DDC object
        var ifdata = slice.read();            // read down converted samples
        if(!sat_view)
        {
           if(print_debug)
           {
               print("end of pass");
           }
           exit();
        }

        while( ifdata.getLength() > 0) {         // if we have something
         if(print_debug)
         {
            print('Writing ...');
         }
         
         fifo_to_file.enqueue( ifdata );         // write the samples in the output queue
         doppler_value = tracker.load("doppler");  // Read doppler value
         slice.setCenter( 200e3 + parseInt(doppler_value)) ; // Correct doppler deviation
         ifdata = slice.read();              // read more
        }        
    }
 }
 
exit();
