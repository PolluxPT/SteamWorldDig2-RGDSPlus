# SteamWorld Dig 2 — Anbernic RGDS+ compatibility port

Unofficial standalone launcher maintained by [PolluxPT](https://github.com/PolluxPT).
Based on the previously working private 1.2 configuration. The public
package contains compatibility code and permitted runtime components, **not the game**.

## Prepare your own game

Use a Linux PC (or WSL2 with the source files accessible), Python **3.10+**, and
an internet connection for the small Debian runtime downloads. No root or system
package installation is required. The console does not need internet afterward.

1. Obtain **your own lawfully acquired Linux copy** of SteamWorld Dig 2. The tested
   edition was GOG Linux. Install/extract it on your PC using the store's normal
   instructions. For a GOG `.sh` installer, run it locally and select an installation
   directory; then locate the installed `game` folder. Windows `.exe` files will not work.
2. Locate the folder containing **`Dig2` and its `Bundle/` (or `BundlePC/`) resources together**.
   Pass that folder, or its parent containing `game/`, to the preparation script.
3. Extract this port ZIP and run from its directory:

```sh
sh ./Prepare_Game.sh "/path/to/your/Linux/SteamWorld Dig 2/game"
```

You can also pass your own **GOG Linux `.sh` installer directly**:

```sh
sh ./Prepare_Game.sh "/path/to/gog_linux_installer.sh"
```

For supported GOG appended-ZIP installers, the script reads only
`data/noarch/game/` locally without executing the installer. If that layout is
unavailable, install it normally on Linux and pass the resulting game folder.
No installer is downloaded or uploaded by this tool.

For a different output location:

```sh
sh ./Prepare_Game.sh "/path/to/your/Linux/game" "/path/to/private-output/APPS"
```

4. The default output is `build/APPS/`. Copy **`SteamWorldDig2.sh`** and the
   **`SteamWorldDig2/` folder** from there into **`TF2/Roms/APPS/`**.
5. Open **Applications** on the RGDS+ and launch `SteamWorldDig2`.

The generated layout is:

```text
TF2/Roms/APPS/
  SteamWorldDig2.sh
  SteamWorldDig2/
    game/
      Dig2
      Bundle/
      [other files from your own Linux copy]
    runtime/
    savedata/                 # created on the device
```

The `.sh` preparation script copies your files locally, verifies the executable,
and downloads pinned GNU runtime packages directly from Debian with SHA-256
checks. It never patches the executable on disk. It refuses existing destinations
to protect saves. Keep the entire generated `build/` directory private.

## Supported build and limitations

Requires an x86_64 Linux ELF executable. The prior tested edition was GOG Linux; no exact executable fingerprint was retained for Dig 2. Architecture checks do not prove compatibility with every edition.

640×480 configuration; RGDS+ controller mapping; hardware volume helper; lower
screen switched off during play and restored on normal exit. D-pad and left
analog direction mappings are included. L2/R2 input indices were not verified.
Do not assume compatibility with other handhelds or firmware.

The original private configurations were reported working on one RGDS+.
This publication revision standardizes the `game/` folder, removes proprietary
payloads, and obtains GNU libraries from Debian instead of redistributing the
old copies. These packaging changes have host-side checks, **not a fresh console
playthrough**. See [validation](docs/VALIDATION.md) and [troubleshooting](docs/TROUBLESHOOTING.md).

## What may be published

This repository/ZIP can be shared as the compatibility package. **Do not upload
the generated installation**, commercial executables, resource folders, game
installers, game artwork/music, Steam libraries, DLC, saves or private logs.
Each player supplies their own files. No DRM bypass or game download is provided.

Port-owned scripts/shims: MIT, [LICENSE](LICENSE). Third-party components keep
their own terms: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Game names identify
compatibility only. Not affiliated with or endorsed by the games' rights holders,
GOG, Valve or Anbernic. This license grants no rights over the commercial games.

See [publishing instructions](PUBLISHING.md) for the GitHub repository and Release.
