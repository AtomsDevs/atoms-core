using Gee;

namespace Atoms {

    public const uint PROVIDER_ABI = 1;

    public interface Provider : Object {
        public abstract string id { owned get; }
        public abstract string name { owned get; }
        public abstract uint abi_version { get; }
        public abstract bool available { get; }
        public abstract string unavailable_reason { owned get; }

        public abstract async ArrayList<Distribution> list_distributions (
            Cancellable? cancellable = null
        ) throws Error;

        public abstract async ArrayList<Environment> list_environments (
            Cancellable? cancellable = null
        ) throws Error;

        public abstract async Environment create_environment (
            Distribution distribution,
            string name,
            Cancellable? cancellable = null
        ) throws Error;

        public abstract string[] shell_argv (
            Environment environment,
            string command,
            string[] arguments
        ) throws Error;

        public abstract async Environment update_policy (
            Environment environment,
            Cancellable? cancellable = null
        ) throws Error;

        public abstract async ArrayList<ProcessInfo> list_processes (
            Environment environment,
            Cancellable? cancellable = null
        ) throws Error;

        public abstract async string[] list_signals (
            Cancellable? cancellable = null
        ) throws Error;

        public abstract async void signal_process (
            Environment environment,
            int pid,
            string signal_name,
            Cancellable? cancellable = null
        ) throws Error;

        public abstract async void stop_environment (
            Environment environment,
            Cancellable? cancellable = null
        ) throws Error;

        public abstract async void delete_environment (
            Environment environment,
            Cancellable? cancellable = null
        ) throws Error;
    }
}
