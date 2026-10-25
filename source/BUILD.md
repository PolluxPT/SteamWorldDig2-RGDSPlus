# Compatibility source and binary provenance

The release preserves the existing known-good compatibility binaries. Exact
hashes, ELF class and architecture are in docs/BINARY_INVENTORY.json. Existing
source for Dig/Heist is included; Dig 2's maintenance reconstruction is explicitly
labeled. Rebuilding is optional and is not part of normal game preparation.

On an x86_64 Linux development machine with GCC:

```sh
# Dig / Heist: run the matching two commands for the source files present.
gcc -m32 -shared -fPIC -O2 -fno-builtin -nostdlib -Wl,-soname,libdig_sdl_bridge.so dig_sdl_bridge.c -o libdig_sdl_bridge.so
gcc -m32 -shared -fPIC -O2 -fno-builtin -nostdlib -Wl,-soname,libdig_glx_compat.so dig_glx_compat.c -o libdig_glx_compat.so
gcc -m32 -shared -fPIC -O2 -fno-builtin -nostdlib -Wl,-soname,libheist_sdl_bridge.so heist_sdl_bridge.c -o libheist_sdl_bridge.so
gcc -m32 -shared -fPIC -O2 -fno-builtin -nostdlib -Wl,-soname,libheist_glx_compat.so heist_glx_compat.c -o libheist_glx_compat.so
# Dig 2 maintenance alternative; not a byte-identical rebuild of the shipped v8:
gcc -shared -fPIC -O2 glx_v8_maintenance.c -ldl -o libglx_compat_v8_x64.so
```

Run commands from source/. Files for the other games are intentionally absent.
A missing 32-bit toolchain is a development requirement, not an end-user issue.
Use a separate test copy; never overwrite the user's working installation.

To rebuild Box64/Box32 or GL4ES, use the official upstream repositories and their
current build documentation. Original commit IDs were not preserved, so no
byte-reproducible upstream build recipe is claimed here. Preserve their licenses
and retest replacement builds on the console. Do not call a replacement a tested
stable binary merely because the source compiled successfully.
