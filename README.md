# minitower_oled kit
The files here are an [update](https://github.com/geeekpi/absminitowerkit) for the absminitowerkit `sysinfo.py` script.

## File locations
all the `.py` files should be located here;
```
/usr/local/luma.examples/examples/
```
the other files should be placed here (these files **will** require execute permission);
```
/usr/local/bin/
```

## Info Displayed
The updated `sysinfo.py` script, as currently configured, will displayed the following information on the OLED display;
```
   IP: <Pi IP address>
  CPU: 43.8°C
   SD: <used space on M.2>
etho0: <Tx and Rx data>
Up: <system up time>
```
The colour of the LEDs within the case will change based on the temperature of the CPU.

CPU temp:
```
             < 45.0: LEDs are Blue
 >= 45.0 and < 49.9: LEDs are Green
 >= 50.0 and < 59.9: LEDs are Orange
            >= 60.0: LEDs are Red
```

## Setting up a Service
Information on how to setup a service, to update the information displayed on the OLED periodically, see [this](https://wiki.52pi.com/index.php?title=ZP-0130-4wire#How_to_Install_All_Drivers_Automatically) section of the Wiki.

## Notes
1. You'll need to alter line 122, in 'sysinfo.py`, and use the mount point you created for your M.2 SSD.

2. The script, `sysinfo.py`, is setup to report the IP address of the `eth0` LAN port if you wish to use the Wireless interface then change line 126.

3. You'll also need to set the required file permissions so the files in `/usr/local/bin` can be executed.
