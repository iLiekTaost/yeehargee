#!/bin/env bash

if [[ `whoami` != "root" ]]; then
    echo "Run this script with \`sudo test-wg.sh <configuration file>\`."
    exit 2
elif [[ "$#" -ne 1 ]]; then
    echo "Run this script with \`sudo test-wg.sh <configuration file>\`."
    exit 3
fi

wg-quick -h &>/dev/null
if [[ $? != 0 ]]; then
    echo "You need to install the wg-quick command to test wireguard using your configuration file."
    echo "Run \`dnf install wireguard-tools\`."
    exit 1
fi

wg-quick up $1
wg
wg-quick down $1

