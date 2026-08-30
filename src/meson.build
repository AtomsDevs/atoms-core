pkg = import('pkgconfig')

glib_dep = dependency('glib-2.0', version: '>= 2.74')
gio_dep = dependency('gio-2.0')
gee_dep = dependency('gee-0.8')
libpeas_dep = dependency('libpeas-2', version: '>= 2.0')

provider_dir = get_option('prefix') / get_option('libdir') / 'atoms' / 'providers'
build_config = configure_file(
  input: 'build_config.vala.in',
  output: 'build_config.vala',
  configuration: {
    'SYSTEM_PROVIDER_DIR': provider_dir,
  }
)

atoms_core_sources = files(
  'models.vala',
  'provider.vala',
  'provider_registry.vala'
) + [build_config]

atoms_core_lib = library(
  'atoms-core-2',
  atoms_core_sources,
  dependencies: [glib_dep, gio_dep, gee_dep, libpeas_dep],
  vala_header: 'atoms-core-2.h',
  vala_vapi: 'atoms-core-2.vapi',
  version: meson.project_version(),
  soversion: '2',
  install: true,
  install_dir: [
    true,
    get_option('includedir') / 'atoms-core-2',
    get_option('datadir') / 'vala/vapi'
  ]
)

atoms_core_inc = include_directories('.')
atoms_core_dep = declare_dependency(
  link_with: atoms_core_lib,
  include_directories: atoms_core_inc,
  dependencies: [glib_dep, gio_dep, gee_dep, libpeas_dep]
)

pkg.generate(
  atoms_core_lib,
  name: 'Atoms Core',
  description: 'Provider-neutral environment management library for Atoms',
  filebase: 'atoms-core-2',
  subdirs: 'atoms-core-2',
  requires: [glib_dep, gio_dep, gee_dep, libpeas_dep]
)
