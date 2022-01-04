# pi-multiroom-radio-ansible

This is a (personal) playbook to configure my multi-room radio/Spotify HiFi system. Running on 
MPD, Snapcast, librespot (raspotify) and lirc. Built over frustration of missing features or configurability
in the existing pre-built systems such as RuneAudio, Volumio, Pi MusicBox or Moode.

At some point I realised, it was quicker to just build the system myself. Using Ansible I can easily 
reproduce such a configuration and keep it manageable. 

Hopefully these playbooks can also offer some inspiration to you.

## Rationale 

I like to play internet radio and Spotify (Connect) in a multi-room setup. 
The radio part I'm mostly controlling via a traditional remote control, connected via
a simple infrared eye on one of the Pi's.

* For spotify [librespot](https://github.com/librespot-org/librespot) is the obvious choice.
  * Using the nice wrapper [raspotify](https://github.com/dtcooper/raspotify) to daemonize librespot
  * [Spotifyd](https://github.com/Spotifyd/spotifyd) was tempting, because it would allow control of playback via MPRIS
    * But named pipe output is currently broken. Making Snapcast setup difficult
* For internet radio classic [MPD](https://www.musicpd.org/) is being used
  * I started with Mopidy, but run into issues with a very slow startup (10 s) to start an internet stream.
    * Also `mpc` commands were relatively slow (2 s) to execute. 
    * For my usecase I didn't need the Mopidy features, so I switched to the simpler MPD.
    * I kept the playbook tasks file, in case I want to switch back
  * Using [mpdbear](https://play.google.com/store/apps/details?id=net.clacks.mpdbear&hl=nl&gl=US) for Android to control MPD from my phone.
  * Volume control is entirely in Snapcast. I don't touch the MPD (or librespot) volume.
* Multi-room is achieved using [Snapcast](https://github.com/badaix/snapcast)
  * Using the software mixer on all systems, and then finetuning the hardware (ALSA) mixers to a nice level gave me
    the best equal response in volume.
  * The `snap_default.py` is being run to reset the Snapcast volume on every (nightly) reboot for all clients (no surprises in the morning)
    * Added as `ExecStartPost` to the Systemd service file
  * Both MPD and librespot pipe their output into the same named pipe. This makes the setup easier to understand.
    * This does mean that MPD and librespot should not play at the same time. 
    * Librespot executes the `mpc_stop.sh` script using the `--onevent` handler
    * The other way around, I've not found a good way to stop librespot when MPD starts.
      * I did include a simple `sudo service raspotify restart` to execute on the remote control power button
  * Using [Snapdroid](https://github.com/badaix/snapdroid) for Android to control Snapcast
* Using [lirc](https://www.lirc.org/) to have my simple remote control working
  * The infrared eye has been connected on 3 GPIO pins
  * Getting the remote to work using `irrecord` can be a bit of a pain 
  * I looked at using `uevent` for passing events, but in the end defaulted to the simpler `irexec` for sending commands
  * Most of the magic is in `irexec.lircrc`. 
    * Using `python-snapcast` to control the Snapcast volume
    * Created simple scripts `snap_mute.py` and `snap_volume.py` to control the muting and volume of the Snapcast clients

## Base configuration pi

Running on Raspberry Pi OS Lite (Raspbian 11 (bullseye)).  

### Enable SSH and WiFi
```
touch /boot/ssh
```

`/boot/wpa_supplicant.conf`
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=NL

network={
     ssid="<SSID>"
     psk="<PASSWORD>"
     scan_ssid=1
}
```

### raspi-config
Run `sudo raspi-config`. Enable:

* Wait for network to boot
* Install nl_NL.UTF8 locale
* Expand SD card

### Set options in /boot/config.txt
Disable most of the HMDI options.

For kitchen (a Raspberry Pi Zero 2 W with HifiBerry Zero AMP)
```
dtparam=act_led_trigger=actpwr
hdmi_blanking=2
dtoverlay=hifiberry-dac
```

For living (a Raspberry Pi 3 with HifiBerry MiniAMP)
```
dtoverlay=hifiberry-amp
dtoverlay=gpio-ir,gpio_pin=17
dtoverlay=disable-wifi
dtoverlay=disable-bt
```

### Setup authentication

* Change default password. 
* Add personal SSH key


## TODO
* Maybe include PiHole to set persistent hostnames, and not having to use IPs. 
  * Why-o-why is zeroconf/avahi still so unreliable, and not enabled on Android??
  