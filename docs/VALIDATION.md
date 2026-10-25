# Validation scope

Previously reported working on the owner's RGDS+: original private port gameplay,
controller, graphics/audio and hardware volume behavior. This is not a claim of
new hardware testing of the public kit.

This publication revision is checked on the preparation host for shell/Python
syntax, exact file inventory, exclusion of game payloads, pinned runtime package
hashes, ELF architecture and importer destination/build validation. The game
executable is not altered. Dig 2's launcher now runs from game/ instead of the port
root; save data remains outside game/. GNU runtime libraries are newly sourced
from Debian bookworm; console compatibility must be rechecked after this change.

Before marking a public release hardware-verified, complete a fresh RGDS+ test:
start a new game, load a scene, verify D-pad/analog/buttons, adjust volume, exit,
relaunch and confirm save data and lower-screen restoration. Do not upload the
private test installation to GitHub. No Quest files are included.

Host verification completed for all three kits: live pinned Debian downloads and
SHA-256 checks, library extraction/ELF checks, sparse payload copies with genuine
supported Dig/Heist executables (Dig 2 used a synthetic ELF fixture), spaces in
paths, no source executable modification, wrong-architecture rejection and
existing-destination/save protection. GOG appended-ZIP handling and path-traversal
rejection passed synthetic fixtures. All included bridge sources compiled.
These checks are not console gameplay tests.
