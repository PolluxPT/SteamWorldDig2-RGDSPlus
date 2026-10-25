#!/bin/sh
pid=$1; lower=$2; volume=$3
case "$pid" in ''|*[!0-9]*) exit 1;; esac
trap 'exit 0' TERM INT
while kill -0 "$pid" 2>/dev/null; do sleep 1; done
[ -z "$lower" ] || printf '%s
' "$lower" > /sys/class/backlight/backlight/brightness 2>/dev/null || :
[ -z "$volume" ] || printf '%s
' "$volume" > /sys/class/anbernic_misc/openbor_volume 2>/dev/null || :
