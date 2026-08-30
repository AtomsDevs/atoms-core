models_test = executable(
  'atoms-core-models-test',
  'models_test.vala',
  dependencies: atoms_core_dep
)

registry_test_provider_base = shared_library(
  'atoms-registry-test-provider-base',
  'registry_test_provider_base.vala',
  dependencies: atoms_core_dep
)

registry_test_provider_base_dep = declare_dependency(
  link_with: registry_test_provider_base,
  dependencies: atoms_core_dep
)

registry_modules = []
foreach provider : ['primary', 'duplicate', 'mismatch']
  registry_modules += shared_module(
    'registry-' + provider,
    'registry_' + provider + '_provider.vala',
    dependencies: registry_test_provider_base_dep
  )
endforeach

foreach metadata : [
  'registry-primary.plugin',
  'registry-duplicate.plugin',
  'registry-mismatch.plugin',
  'registry-invalid.plugin'
]
  configure_file(
    input: metadata,
    output: metadata,
    copy: true
  )
endforeach

models_test_env = environment()
models_test_env.set('ATOMS_REGISTRY_TEST_PATH', meson.current_build_dir())

test(
  'atoms-core-models',
  models_test,
  env: models_test_env,
  depends: registry_modules
)
