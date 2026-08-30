using Gee;

namespace Atoms {

    public abstract class RegistryTestProviderBase : Object, Provider {
        protected abstract string provider_id { owned get; }

        public string id { owned get { return provider_id; } }
        public string name { owned get { return "Registry test"; } }
        public uint abi_version { get { return PROVIDER_ABI; } }
        public bool available { get { return true; } }
        public string unavailable_reason { owned get { return ""; } }

        public async ArrayList<Distribution> list_distributions (
            Cancellable? cancellable = null
        ) throws Error {
            return new ArrayList<Distribution> ();
        }

        public async ArrayList<Environment> list_environments (
            Cancellable? cancellable = null
        ) throws Error {
            return new ArrayList<Environment> ();
        }

        public async Environment create_environment (
            Distribution distribution,
            string name,
            Cancellable? cancellable = null
        ) throws Error {
            throw new CoreError.NOT_SUPPORTED ("not supported by registry test provider");
        }

        public string[] shell_argv (Environment environment,
                                    string command,
                                    string[] arguments) throws Error {
            throw new CoreError.NOT_SUPPORTED ("not supported by registry test provider");
        }

        public async Environment update_policy (
            Environment environment,
            Cancellable? cancellable = null
        ) throws Error {
            throw new CoreError.NOT_SUPPORTED ("not supported by registry test provider");
        }

        public async ArrayList<ProcessInfo> list_processes (
            Environment environment,
            Cancellable? cancellable = null
        ) throws Error {
            return new ArrayList<ProcessInfo> ();
        }

        public async string[] list_signals (
            Cancellable? cancellable = null
        ) throws Error {
            return new string[0];
        }

        public async void signal_process (
            Environment environment,
            int pid,
            string signal_name,
            Cancellable? cancellable = null
        ) throws Error {
            throw new CoreError.NOT_SUPPORTED ("not supported by registry test provider");
        }

        public async void stop_environment (
            Environment environment,
            Cancellable? cancellable = null
        ) throws Error {
            throw new CoreError.NOT_SUPPORTED ("not supported by registry test provider");
        }

        public async void delete_environment (
            Environment environment,
            Cancellable? cancellable = null
        ) throws Error {
            throw new CoreError.NOT_SUPPORTED ("not supported by registry test provider");
        }
    }
}
