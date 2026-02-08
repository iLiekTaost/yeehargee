#!/bin/env bash
if [[ `whoami` != "root" ]]; then
    echo "Run this script with \`sudo ts-up.sh\`."
    exit 2
fi
curl --version &>/dev/null
if [[ $? -ne 0 ]]; then
    echo "Install curl"
    exit 1
fi
tailscale --version &>/dev/null
if [[ $? -ne 0 ]]; then
    echo "Installing tailscale..."
    curl -fsSL https://tailscale.com/install.sh | sh
fi
set -e
tailscale up

