#!/bin/sh
BASE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
GAME="$BASE/SteamWorldDig2"
LOG="$GAME/Arranque_SteamWorldDig2.txt"
mkdir -p "$GAME/logs" "$GAME/savedata/SteamWorld Dig 2"
exec >"$LOG" 2>&1
printf 'SteamWorld Dig 2 RGDS+ RELEASE 1.2 - 2026-10-24\n'
date; uname -a
cd "$GAME" || exit 1
for f in game/Dig2 runtime/box64 runtime/gl4es/libGL.so.1 runtime/glx-compat/libglx_compat_v8_x64.so runtime/libs.x64/libstdc++.so.6 runtime/libs.x64/libgcc_s.so.1 runtime/rgds-settings.xml runtime/rgds-controller.txt; do
 [ -s "$f" ] || { echo "Falta ficheiro: $f"; exit 2; }
done
# Settings: preserve saves and other user options; force known-working graphics and screen values.
SETTINGS="$GAME/savedata/SteamWorld Dig 2/settings.xml"
if [ ! -s "$SETTINGS" ]; then cp "$GAME/runtime/rgds-settings.xml" "$SETTINGS" || exit 3; fi
cp "$SETTINGS" "$SETTINGS.bak-release1" 2>/dev/null || :
for entry in 'Visualizer.Bloom:0' 'Visualizer.EnableAO:0' 'Visualizer.HiQualityLight:0' 'Visualizer.ResolutionScale:1' 'Screen.Fullscreen:1' 'Screen.FullscreenSize:desktop' 'Screen.WindowSize:640;480' 'Screen.WindowResizable:0' 'Screen.VSync:1' 'MusicVolume:0.80' 'SoundVolume:0.90'; do
 key=${entry%%:*}; val=${entry#*:}
 if grep -Fq "Key=\"$key\"" "$SETTINGS"; then
  sed -i "s/\(Key=\"$key\" Value=\"\)[^\"]*/\1$val/" "$SETTINGS" || :
 else
  sed -i "/<\/Settings>/i\\ <Setting Key=\"$key\" Value=\"$val\" />" "$SETTINGS" || :
 fi
done
# Do not replace saved user gamepad config, but make the Anbernic mapping available to SDL.
export SDL_GAMECONTROLLERCONFIG="$(cat "$GAME/runtime/rgds-controller.txt")"
export SDL_GAMECONTROLLER_IGNORE_DEVICES_EXCEPT=''
echo "Comandos SDL: $SDL_GAMECONTROLLERCONFIG"
export XDG_DATA_HOME="$GAME/savedata"
unset SDL_DYNAMIC_API BOX64_BOX32 BOX64_EMULATED_LIBS BOX64_PREFER_EMULATED
export BOX64_DYNAREC=1 BOX64_LOG=1 BOX64_SHOWSEGV=1
export BOX64_LD_LIBRARY_PATH="$GAME/runtime/libs.x64:$GAME/game:$GAME"
export LD_LIBRARY_PATH="$GAME/runtime/gl4es:$GAME/runtime/libs.aarch64:${LD_LIBRARY_PATH:-}"
export SDL_VIDEO_GL_DRIVER="$GAME/runtime/gl4es/libGL.so.1"
export LIBGL_ES=2 LIBGL_GL=21 LIBGL_FB=0
export SDL_AUDIODRIVER=alsa
if [ -n "${WAYLAND_DISPLAY:-}" ]; then export SDL_VIDEODRIVER=wayland;
elif [ -n "${DISPLAY:-}" ]; then export SDL_VIDEODRIVER=x11;
else echo 'Sem ambiente grafico'; exit 4; fi
export BOX64_LD_PRELOAD="$GAME/runtime/glx-compat/libglx_compat_v8_x64.so"
LOWER=/sys/class/backlight/backlight/brightness
VOLUME=/sys/class/anbernic_misc/openbor_volume
lower_saved='' volume_saved='' guard_pid='' audio_pid=''
if [ -r "$LOWER" ] && [ -w "$LOWER" ]; then
 lower_saved=$(cat "$LOWER" 2>/dev/null)
 case "$lower_saved" in ''|*[!0-9]*) lower_saved='';; esac
fi
if [ -r "$VOLUME" ] && [ -w "$VOLUME" ]; then
 volume_saved=$(cat "$VOLUME" 2>/dev/null)
 case "$volume_saved" in ''|*[!0-9]*) volume_saved='';; *) [ "$volume_saved" -le 10 ] || volume_saved='';; esac
fi
restore() {
 trap - EXIT INT TERM HUP
 [ -z "$audio_pid" ] || { kill "$audio_pid" 2>/dev/null || :; wait "$audio_pid" 2>/dev/null || :; }
 [ -z "$guard_pid" ] || { kill "$guard_pid" 2>/dev/null || :; wait "$guard_pid" 2>/dev/null || :; }
 [ -z "$lower_saved" ] || printf '%s\n' "$lower_saved" > "$LOWER" 2>/dev/null || :
 [ -z "$volume_saved" ] || printf '%s\n' "$volume_saved" > "$VOLUME" 2>/dev/null || :
}
trap 'restore' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM HUP
[ -z "$lower_saved" ] || { printf '0\n' > "$LOWER" 2>/dev/null || :; echo 'Ecra inferior desligado'; }
# System hardware volume remains adjustable via its physical buttons.
# Start at moderate level, restore the original system level when leaving.
[ -z "$volume_saved" ] || { printf '6\n' > "$VOLUME" 2>/dev/null || :; echo 'Volume inicial: 6/10'; }
# Audio keys require active monitoring; the sysfs level alone does not control OpenAL.
if command -v python3 >/dev/null 2>&1; then
 python3 -u "$GAME/runtime/rgds-audio-keys.py" "$VOLUME" >>"$LOG" 2>&1 &
 audio_pid=$!
else
 echo 'AVISO: python3 indisponivel; teclas de volume sem monitorizacao'
fi
cd "$GAME/game" || exit 5
"$GAME/runtime/box64" "$GAME/game/Dig2" &
game_pid=$!
# Independent guard restores hardware state if launcher is interrupted.
if [ -n "$lower_saved$volume_saved" ]; then
 /bin/sh "$GAME/runtime/rgds-guard.sh" "$game_pid" "$lower_saved" "$volume_saved" &
 guard_pid=$!
fi
wait "$game_pid"; rc=$?
echo "Dig2 exit code: $rc"
exit "$rc"
