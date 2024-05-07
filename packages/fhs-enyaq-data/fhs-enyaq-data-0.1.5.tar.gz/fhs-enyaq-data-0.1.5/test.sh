#!/bin/bash

docker run --rm -ti -v "$HOME/.config/fhs_enyaq_data":/config fhs-iptv-tools send-data --config-full-path=/config/config.yaml
