#define STARTUPDELAY 10000    // Change to wanted startup delay, ~10ms min or 10000 micros
#define MAJORDELAY 2000       // Change to adjust delay to best fit use
#define BAUDRATE 115200
  /*
    Acceptable rates are as follows, but might be able to push up to 1,000,000
    if proper equipment is used. This will allow for faster log time and command
    time

      300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200
   */

#define TESTVOLUME 25

#define READPIN A0            // Pin to read voltage from must be on an analog capable pin
#define CONTROLPIN 12         // Pin to control output, assumed to be a digitally controlled item with hig/low control
