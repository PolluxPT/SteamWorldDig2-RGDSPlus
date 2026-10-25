# SteamWorld Dig 2 RGDS+ — public compatibility kit

- Based on the working private 1.2 port configuration.
- Commercial game files, artwork, saves, logs and GNU runtime binaries excluded.
- Prepare_Game.sh builds a private installation from the owner's Linux game.
- Pinned runtime downloads, notices, SHA-256 checks and supported-build validation.
- Standard `game/` directory for all three ports; standalone Applications launcher.
- MIT port code plus preserved Box64/GL4ES/SDL notices.

Preparation: `sh Prepare_Game.sh "/path/to/installed/Linux/game"`.
Copy the resulting folder and launch `.sh` from `build/APPS/` to `TF2/Roms/APPS/`.
Linux GOG edition tested previously; see README for build restrictions.

The public packaging revision needs a new RGDS+ smoke test before claiming it is
identical in behavior to the private build. No commercial game download included.
