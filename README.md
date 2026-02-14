Yeehargee, matey!

![Patchy](https://media1.tenor.com/m/phAx6aXjh0AAAAAd/patchy-the-pirate-spongebob.gif)

# 0. Introduction
This configuration follows some of [Trash Guides](https://trash-guides.info/) to create a composition of containers for torrenting media. This README will show you what to do once you've cloned this repository to get started using ProtonVPN with a Wireguard configuration instead of OpenVPN.

# 1. Getting started

## Creating wireguard_private_key
Your `wireguard_private_key` plaintext file is where docker-compose will look for authenticaton credientials to use with ProtonVPN servers. Create this plaintext file in the repository's root directory next to your `docker-compose.yaml` file. Secure it with `sudo chmod 600 wireguard_private_key`, and **do not ever commit or otherwise share this file**.

### ProtonVPN authentication
Go to [ProtonVPN account settings](https://account.proton.me/u/0/vpn/WireGuard), and
1. Give a name to the config to be generated (like protonvpn-cert.conf)
2. Select GNU/Linux
3. Select only the "VPN Accelerator" option
4. Click "Create" on any VPN server/location (the private key you are generating can be used for _any_ ProtonVPN server, not just the one you select)
5. Copy the text in the pop-up window into your `wireguard_private_key` file

## Data directory and permissions
Run `mkdir data`. Then use `mkdir` to create a `media` and `torrents` subdirectory in `data`, each with a `tv` and `movies` subdirectory. Last, run `sudo chmod a+w data/media/* data/torrents/*`. These commands will create your data directory storing your torrents and set the necessary permissions for services like Sonarr to write data. 

# 2. Running
Spin up your docker containers and detach them from stdout with `sudo docker-compose up -d`. Once your containers have finished starting and your command prompt returns, run `sudo docker-compose logs | grep qbit`. Find the temporary password that has been created, and copy it to your clipboard.

Your services at this point are available via your web browser. But, there are a few things to finish setting up.

# 3. Finish setting up

## Logging into qBitTorrent (localhost:8080) for the first time
In your browser, navigate to localhost:8080. Use "admin" for the username, and the password is the temporary password you copied to your clipboard.

### Change your qBitTorrent password
Once you've logged in, open the settings wheel through the web UI, tab over to "WebUI," and set up your username and password. Also, in the same tab, under Authentication, click the boxes to bypass authenticating for clients on the localhost and whitelisted IP subnets to allow Sonarr, Radarr, and other services to find qBitTorrent automatically.

## Connecting your services together
I recommend keeping your username "admin" for all the services when they prompt you to create your account.

### Prowlarr -> qBitTorrent
Open your indexer manager, Prowlarr, by navigating to localhost:9696 in your web browser. Go to Settings > Download Clients and click the button to connect a new download client. Select qBitTorrent, and for the username input "admin" and for the password, enter the password you already set up in the qBitTorrent UI. The host should be changed to "gluetun" since that is the service managing traffic for qBitTorrent and its webserver UI; the port is still 8080 as that is forwarded by gluetun in the `docker-compose.yaml` file.

### Prowlarr -> Sonarr & Radarr
In Prowlarr's web UI, go to Settings > Apps and click the button to connect a new application. Select Sonarr, change the Prowlarr server to prowlarr:9696 since Prowlarr and Sonarr are only able to access each other by service name due to docker-compose using the default network for services other than gluetun and qBitTorrent.

Now, keeping this tab open, open a new tab in your browser and navigate to localhost:8989. It should ask you what method you wish to set up for authenticating in the web browser, and you should choose the basic form (not pop-up), and if it asks you if you'd like to disable authentication for connections from local addresses, do so. Create your new credentials and log in, and then navigate to Settings > General to make sure Authentication Required is set to "Disabled for Local Addresses" (save this settings update with the button at the top left of the page) and to copy the API Key from under Security settings. Paste this in the Prowlarr web UI, and test the connection. If it tests the connection to Sonarr successfully, then do these same steps to connect Prowlarr to your Radarr app.

While you still have Sonarr and Radarr open, go to Settings > Media Management > Root Folders and add /data/media/tv as the root folder for Sonarr and /data/media/movies as the root folder for Radarr.

### Jellyfin
Navigate to localhost:8096 in your web browser. Add two libraries, Movies and Shows using their respective content types. Make sure Shows has one folder, /data/media/tv and make sure Movies has one folder, /data/media/movies.

Make your username "admin" instead of "root" to stay consistent with the other services' accounts. Also make sure you enable remote access to this server if/when it asks at the end of setup.

### Jellyseerr -> Jellyfin, Radarr, Sonarr
Navigate to localhost:5055 in your web browser, and choose "Jellyfin" as your server type. Make the Jellyfin URL "jellyfin" on port 8096, and use the same account credentials as all your other services. Sync your Jellyfin libraries, enable Movies and Shows, and save your changes. Continue to setting up your Radarr connection. Open Radarr (localhost:7878) in another tab, go to Settings > General > Security and copy your API key to Jellyseerr, and set the hostname/IP address to radarr. Do the same for Sonarr (localhost:8989).

### Add your indexer to Prowlarr
Navigate to localhost:9696 in your web browser to get to the Prowlarr web UI, and then navigate to Indexers. Add any indexers you'd like to use. The cookie is how you authenticate with torrentday after you've received your invite link and set up your account; follow the instructions under cookie's "More Info" hyperlink for help getting this cookie data.

### Integrate service settings homogeneously
First read "File and Folder Structure" and then follow the instructions for Sonarr and Radarr at [Trash Guides](https://trash-guides.info/). For Prowlarr, you should understand that this configuration uses gluetun instead of privoxy, and you may not need to set up a proxy in Prowlarr at all if your indexer (like TorrentDay) does not require it. Last, follow the instructions for qBitTorrent under "Downloaders."

# 4. Troubleshooting

## Elevated privileges
You should be aware that most docker commands require elevated privileges and for the command to be preceeded with `sudo`.

## Check your IP as it appears to servers
Go to [torguard](https://torguard.net/check-my-torrent-ip-address/), right-click the green download button, and copy the magnet link. Paste this into your qBitTorrent web UI, and it will hang on "Downloading metadata." Go back to the torguard webpage, and check the newly listed connection attempt. Compare this to your public IP (you can see this in your ProtonVPN app).

## Troubleshooting gluetun's startup health check
Sometimes, gluetun fails to start due to a failed connection to ProtonVPN. To fix this you can go back to ProtonVPN account settings and delete the certificate you created earlier, and follow the steps under "ProtonVPN authentication" again to create a new private key. I still don't know why this needs to be done so often, especially because I added a script to this repo for verifying your credentials work, `test-wg.sh`. To run it, enter `sudo test-wg.sh <your configuration file>`.

## Firewall limitations
If you use ufw or firewalld to manage firewall settings, be aware that when you expose container ports using Docker, these ports bypass your firewall rules. For more information, refer to Docker and ufw.
Docker is only compatible with iptables-nft and iptables-legacy. Firewall rules created with nft are not supported on a system with Docker installed. Make sure that any firewall rulesets you use are created with iptables or ip6tables, and that you add them to the DOCKER-USER chain, see Packet filtering and firewalls.
