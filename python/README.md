### Install Python dependencies


Run the following command from the python folder:

`sudo pip install -r requirements.txt`


### Forward NatNet data through OSC

Run the following command from the python folder:

`bin/forward_natnet [natnet_host_address] [natnet_multicast_address] [natnet_port]`

It will forward through OSC to localhost ("127.0.0.1") at port 8080


### Record NatNet JSON data

TOFIX


### Playback recorded JSON data

Run the following command from the python folder:

`bin/play_recording [<path/to/file.json>]`
