using Gee;

namespace Atoms {

    [CCode (
        cname = "atoms_provider_registry_create_extension",
        cheader_filename = "provider_loader.h"
    )]
    private static extern GLib.Object create_provider_extension (
        Peas.Engine engine,
        Peas.PluginInfo info,
        GLib.Type extension_type
    );

    public class ProviderRegistry : Object {
        private Peas.Engine engine;
        private ArrayList<Provider> loaded_providers;
        private ArrayList<string> load_diagnostics;
        private string[] search_paths;

        public Gee.List<Provider> providers {
            owned get { return loaded_providers.read_only_view; }
        }

        public Gee.List<string> diagnostics {
            owned get { return load_diagnostics.read_only_view; }
        }

        public ProviderRegistry (string[]? search_paths = null) {
            this.search_paths = search_paths ?? default_search_paths ();
            loaded_providers = new ArrayList<Provider> ();
            load_diagnostics = new ArrayList<string> ();
            engine = new Peas.Engine.with_nonglobal_loaders ();
            foreach (var path in this.search_paths)
                engine.add_search_path (path, path);
        }

        public void load () {
            loaded_providers.clear ();
            load_diagnostics.clear ();
            engine.rescan_plugins ();

            var ids = new HashSet<string> ();
            for (uint i = 0; i < engine.get_n_items (); i++) {
                var info = engine.get_item (i) as Peas.PluginInfo;
                if (info == null)
                    continue;
                load_provider (info, ids);
            }
        }

        public Provider? find (string id) {
            foreach (var provider in loaded_providers) {
                if (provider.id == id)
                    return provider;
            }
            return null;
        }

        public Provider require (string id) throws Error {
            var provider = find (id);
            if (provider == null)
                throw new CoreError.NOT_FOUND ("provider is not installed: %s".printf (id));
            if (!provider.available)
                throw new CoreError.NOT_AVAILABLE (
                    provider.unavailable_reason == ""
                        ? "provider is not available: %s".printf (id)
                        : provider.unavailable_reason
                );
            return provider;
        }

        private void load_provider (Peas.PluginInfo info,
                                    HashSet<string> ids) {
            string? metadata_abi = info.get_external_data ("X-Atoms-Provider-ABI");
            string? metadata_id = info.get_external_data ("X-Atoms-Provider-Id");
            if (metadata_abi != PROVIDER_ABI.to_string () ||
                metadata_id == null || metadata_id == "") {
                load_diagnostics.add (
                    "%s: invalid provider metadata".printf (info.get_module_name ())
                );
                return;
            }

            try {
                if (!info.is_available ()) {
                    load_diagnostics.add (
                        "%s: plugin is unavailable".printf (metadata_id)
                    );
                    return;
                }
            } catch (Error error) {
                load_diagnostics.add ("%s: %s".printf (metadata_id, error.message));
                return;
            }

            engine.load_plugin (info);
            if (!info.is_loaded () ||
                !engine.provides_extension (info, typeof (Provider))) {
                load_diagnostics.add (
                    "%s: provider extension was not registered".printf (metadata_id)
                );
                return;
            }

            var extension = create_provider_extension (
                engine,
                info,
                typeof (Provider)
            ) as Provider;
            if (extension == null ||
                extension.abi_version != PROVIDER_ABI ||
                extension.id != metadata_id) {
                load_diagnostics.add (
                    "%s: provider identity does not match its metadata".printf (metadata_id)
                );
                return;
            }
            if (ids.contains (extension.id)) {
                load_diagnostics.add (
                    "%s: duplicate provider id".printf (extension.id)
                );
                return;
            }

            ids.add (extension.id);
            loaded_providers.add (extension);
        }

        private static string[] default_search_paths () {
            var paths = new ArrayList<string> ();
            string? configured = GLib.Environment.get_variable ("ATOMS_PROVIDER_PATH");
            if (configured != null && configured != "") {
                foreach (var path in configured.split (Path.SEARCHPATH_SEPARATOR_S)) {
                    if (path != "")
                        paths.add (path);
                }
            }
            paths.add (Path.build_filename (
                GLib.Environment.get_user_data_dir (),
                "atoms",
                "providers"
            ));
            paths.add (SYSTEM_PROVIDER_DIR);

            var result = new string[paths.size];
            for (int i = 0; i < paths.size; i++)
                result[i] = paths[i];
            return result;
        }
    }
}
