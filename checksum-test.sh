#!/usr/bin/env bash

check_dir_checksums() {
    local dir="$1"
    local checksum_file="${dir}/checksum.txt"

    # checksum not present
    if [ ! -f "$checksum_file" ]; then
        return
    fi

    # single letter secret files
    local secret_file
    secret_file=$(find "$dir" -maxdepth 1 -type f -name "[a-z].txt" | head -n 1)

    echo ""
    echo "testing ${secret_file}..."

    # read checksum file
    local expected_md5
    local expected_sha256

    expected_md5=$(sed -n '2p' "$checksum_file" | tr -d '\r\n')
    expected_sha256=$(sed -n '4p' "$checksum_file" | tr -d '\r\n')

    # compute hashes
    local actual_md5
    local actual_sha256

    actual_md5=$(md5sum "$secret_file" | awk '{print $1}')
    actual_sha256=$(sha256sum "$secret_file" | awk '{print $1}')

    local color_green="\033[0;32m"
    local color_red="\033[0;31m"
    local color_reset="\033[0m"

    # Validate MD5
    if [ "$actual_md5" = "$expected_md5" ]; then
        echo -e "  md5    ${color_green}match${color_reset}"
    else
        echo -e "  md5    ${color_red}mismatch${color_reset}"
    fi

    # Validate SHA256
    if [ "$actual_sha256" = "$expected_sha256" ]; then
        echo -e "  sha256 ${color_green}match${color_reset}"
    else
        echo -e "  sha256 ${color_red}mismatch${color_reset}"
    fi
}

# Iterate over all top-level directories
for dir in */; do
    # Strip trailing slash
    dir="${dir%/}"

    if [ -d "$dir" ]; then
        check_dir_checksums "$dir"
    fi
done