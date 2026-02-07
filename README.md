# Introduction
This configuration follows some of https://trash-guides.info/ to create a composition of containers for torrenting media. This README will show you what to do once you've cloned this repository to get started using ProtonVPN with a Wireguard configuration instead of OpenVPN.

# Getting started
## Creating .env
Your .env file is where docker-compose will look for secrets, such as your private key used to authenticate with ProtonVPN servers. Create this plain-text file in the root directory next to your docker-compose.yaml file. Secure it with `sudo chmod 600 .env`, and **do not ever commit this file**.

## Directory permissions
Run `mkdir data; sudo chmod -R +w:ugo data`.

### ProtonVPN authentication key/value pair
In your .env file, create a new line starting with `PRIVATEKEY=`. Then, go to https://account.proton.me/u/0/vpn/WireGuard, and
1. Give a name to the config to be generated (like protonvpn-cert.conf)
2. Select GLU/Linux
3. Select only the "VPN Accelerator" option
4. Select a specific VPN server to start with (we'll add more servers later to account for server lifespan)

## Logging into qBitTorrent (localhost:8080) for the first time

## Testing your connection
Go to https://torguard.net/check-my-torrent-ip-address/, right-click the green download button, and copy the magnet link. Paste this into your qBitTorrent web UI, and wait for it to download.