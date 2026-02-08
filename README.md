# Introduction
This configuration follows some of [Trash Guides](https://trash-guides.info/) to create a composition of containers for torrenting media. This README will show you what to do once you've cloned this repository to get started using ProtonVPN with a Wireguard configuration instead of OpenVPN.

# Getting started

## Creating wireguard_private_key
Your `wireguard_private_key` plaintext file is where docker-compose will look for authenticaton credientials to use with ProtonVPN servers. Create this plaintext file in the repository's root directory next to your `docker-compose.yaml` file. Secure it with `sudo chmod 600 wireguard_private_key`, and **do not ever commit this file**.

### ProtonVPN authentication
Go to [ProtonVPN account settings](https://account.proton.me/u/0/vpn/WireGuard), and
1. Give a name to the config to be generated (like protonvpn-cert.conf)
2. Select GLU/Linux
3. Select only the "VPN Accelerator" option
4. Click "Create" on any VPN server/location (the private key you are generating can be used for _any_ ProtonVPN server, not just the one you select)
5. Copy the text in the pop-up window into your `wireguard_private_key` file

## Data directory and permissions
Run `mkdir data; sudo chmod -R +w:ugo data`. This will create your data directory storing your torrents and set the necessary permissions for services like Sonarr to write data. Use `mkdir` to create a media and torrents subdirectory in `data`.

# Running
Spin up your docker containers and detach them from stdout with `docker-compose up -d`. Once your containers have finished starting and your command prompt returns, run `docker-compose logs | grep qbit`. Find the temporary password that has been created, and copy it to your clipboard.

Your services at this point are available via your web browser.

## Logging into qBitTorrent (localhost:8080) for the first time
In your browser, navigate to localhost:8080. Use "admin" for the username, and the password is the temporary password you copied to your clipboard.

### Change your password
Once you've logged in, open the settings wheel through the web UI, tab over to "WebUI," and set up your username and password. Also, in the same tab, under Authentication, click the boxes to bypass authenticating for clients on the localhost and whitelisted IP subnets to allow Sonarr, Radarr, and other services to find qBitTorrent automatically.

### Change your torrent location
In the web UI settings, under the Downloads tab, change "Default save path" to `/data/torrents`.

# Testing your connection

## Check your IP as it appears to servers
Go to [torguard](https://torguard.net/check-my-torrent-ip-address/), right-click the green download button, and copy the magnet link. Paste this into your qBitTorrent web UI, and it will hang on "Downloading metadata." Go back to the torguard webpage, and check the newly listed connection attempt. Compare this to your public IP (you can see this in your ProtonVPN app).

## Troubleshooting gluetun's startup health check
Sometimes, gluetun fails to start due to a failed connection to ProtonVPN. To fix this you can go back to ProtonVPN account settings and delete the certificate you created earlier, and follow the steps under "ProtonVPN authentication" again to create a new private key. I still don't know why this needs to be done so often, especially because I added a script to this repo for verifying your credentials work, `test-wg.sh`. To run it, enter `sudo test-wg.sh <your configuration file>`.
