# Rights and third-party notices

Only the compatibility package is distributed. The commercial games, their
executables, data, artwork, music, store installers and Steam API library are
**not included**. Their rights remain with their respective owners. Players must
obtain their own lawfully acquired Linux edition. Nothing here authorizes sharing
those files, and MIT does not apply to them.

## Box64 / Box32 — MIT

Copyright (c) 2020 ptitSeb and contributors. Upstream:
https://github.com/ptitSeb/box64 . Full notice in licenses/box64.txt.
The shipped ARM64 executable is preserved from the prior private working port.
For Dig/Heist it includes Box32 (reports development version 0.4.5); Dig 2 uses
its earlier x86_64-capable runtime. Exact original upstream build commits were
not retained. This is a binary-identification limitation, not a claim of a
reproducible upstream build. No upstream endorsement is implied.

## GL4ES — MIT

Copyright (c) 2016–2018 Sebastien Chevalier; Copyright (c) 2013–2016 Ryan Hileman,
and contributors. Upstream: https://github.com/ptitSeb/gl4es . Full notice in
licenses/gl4es.txt. ARM64 libGL.so.1 is preserved from the working port. The
Dig/Heist build reports 1.1.7; exact upstream build commit was not retained.
No ARM Mali driver, native firmware library or native SDL binary is included.

## SDL2 ABI declarations and compatibility metadata — zlib

SDL copyright Sam Lantinga and contributors. Upstream:
https://github.com/libsdl-org/SDL/tree/SDL2 . Full terms in licenses/sdl2.txt.
The Heist dynapi declaration files derive from SDL2. The Linux subset is an
altered version; original notices are retained. Dig redirect signatures and
Heist dispatch addresses identify the user's embedded SDL implementation and
are functional compatibility metadata. They do not include the game executable.
SDL-related third-party material retains SDL's terms, not this project's MIT.

## Port-owned code — MIT

Launchers, hardware helpers, gamepad bindings, preparation/audit tools and custom
GLX/SDL bridge implementation are covered by LICENSE, to the extent of the port
maintainer's rights. They grant no license to third-party code or game content.
Dig/Heist bridge source is included. Dig 2's original v8 binary is retained;
source/glx_v8_maintenance.c is a maintenance reconstruction, **not a byte-identical
source claim**. Rebuilt replacements require fresh hardware testing.

## GNU runtime and zlib packages — not redistributed

No libstdc++.so.6, libgcc_s.so.1, libz.so.1 or Debian .deb archive is bundled.
Prepare_Game.sh downloads pinned Debian bookworm packages directly for each
user's private installation, verifies SHA-256 and extracts the needed libraries
and their Debian copyright notices locally. Those generated files must not be
committed or attached to the public release.

libstdc++ and libgcc: GPL with the applicable GCC Runtime Library Exception.
The exception does not remove the obligations when distributing the libraries
as independent libraries. See:
https://www.gnu.org/licenses/gcc-exception-3.1-faq.html
https://gcc.gnu.org/onlinedocs/libstdc++/manual/license.html
https://sources.debian.org/src/gcc-12/

zlib: zlib license; https://sources.debian.org/src/zlib/ . Package versions and
hashes are recorded in runtime-lock.json. Firmware SDL2, OpenAL, ALSA and glibc
are not distributed by this repository. Users retain their own game's notices.

## Publication boundary

The prepared build/APPS output is private. Public release construction uses an
explicit, hashed file allowlist; .gitignore also excludes game payloads, runtime
downloads, saves and logs. Do not publish old full-game ZIPs. This package avoids
redistributing commercial content and keeps the listed open-source notices;
it is not a legal warranty for a user's game license or local jurisdiction.

## Acknowledgments

The initial Dig 2 runtime was supplied through the PortMaster SteamWorld Dig 2
package, credited there to porter **Rehex**. Thank you to Rehex, PortMaster,
ptitSeb, GL4ES contributors and SDL contributors. This standalone RGDS+ kit does
not copy PortMaster launcher scripts, covers, game descriptions or screenshots,
and does not require PortMaster or its Weston runtime.
