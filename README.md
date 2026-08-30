# Atoms Core
Atoms Core is the Vala library used to create and manage Atoms environments.

It provides the shared models and provider ABI used by [Atoms](https://github.com/AtomsDevs/Atoms) and [Atoms CLI](https://github.com/AtomsDevs/atoms-cli).

Providers are native libpeas modules and keep backend-specific code outside the clients.

## Dependencies
Atoms Core requires GLib, libgee, and libpeas 2.

## Install
```sh
meson setup build
meson compile -C build
meson install -C build
```
