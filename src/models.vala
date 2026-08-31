using Gee;

namespace Atoms {

    public errordomain CoreError {
        NOT_AVAILABLE,
        INVALID_DATA,
        NOT_FOUND,
        NOT_SUPPORTED,
        PROVIDER_FAILED
    }

    public class EnvironmentPolicy : Object {
        public bool network { get; set; default = true; }
        public bool home { get; set; default = false; }
        public bool display { get; set; default = true; }
        public bool usb { get; set; default = false; }
        public bool input { get; set; default = false; }
        public bool audio { get; set; default = false; }
        public bool host_commands { get; set; default = false; }

        public bool can_network { get; set; default = false; }
        public bool can_home { get; set; default = false; }
        public bool can_display { get; set; default = false; }
        public bool can_usb { get; set; default = false; }
        public bool can_input { get; set; default = false; }
        public bool can_audio { get; set; default = false; }
        public bool can_host_commands { get; set; default = false; }

        public EnvironmentPolicy copy () {
            return new EnvironmentPolicy () {
                network = network,
                home = home,
                display = display,
                usb = usb,
                input = input,
                audio = audio,
                host_commands = host_commands,
                can_network = can_network,
                can_home = can_home,
                can_display = can_display,
                can_usb = can_usb,
                can_input = can_input,
                can_audio = can_audio,
                can_host_commands = can_host_commands
            };
        }

        public void clamp () {
            network = network && can_network;
            home = home && can_home;
            display = display && can_display;
            usb = usb && can_usb;
            input = input && can_input;
            audio = audio && can_audio;
            host_commands = host_commands && can_host_commands;
        }
    }

    public class Distribution : Object {
        public string provider_id { get; construct; }
        public string id { get; construct; }
        public string name { get; construct; }
        public string version { get; construct; }
        public string description { get; construct; }
        public string origin { get; construct; }
        public string icon_path { get; construct; }

        public Distribution (string provider_id,
                             string id,
                             string name,
                             string version,
                             string description,
                             string origin,
                             string icon_path = "") {
            Object (
                provider_id: provider_id,
                id: id,
                name: name,
                version: version,
                description: description,
                origin: origin,
                icon_path: icon_path
            );
        }

        public string display_name () {
            return version == "" ? name : "%s %s".printf (name, version);
        }
    }

    public class Environment : Object {
        public string provider_id { get; construct; }
        public string id { get; construct; }
        public string name { get; construct; }
        public string version { get; construct; }
        public string origin { get; construct; }
        public string icon_path { get; construct; }
        public string provider_data { get; construct; }
        public EnvironmentPolicy policy { get; set; }

        public Environment (string provider_id,
                            string id,
                            string name,
                            string version,
                            string origin,
                            string icon_path = "",
                            string provider_data = "",
                            EnvironmentPolicy? policy = null) {
            Object (
                provider_id: provider_id,
                id: id,
                name: name,
                version: version,
                origin: origin,
                icon_path: icon_path,
                provider_data: provider_data,
                policy: policy ?? new EnvironmentPolicy ()
            );
        }

        public string display_name () {
            return version == "" ? name : "%s %s".printf (name, version);
        }
    }

    public class ProcessInfo : Object {
        public int pid { get; construct; }
        public string command { get; construct; }
        public double cpu_percent { get; construct; }
        public uint64 memory_bytes { get; construct; }
        public bool can_signal { get; construct; }

        public ProcessInfo (int pid,
                            string command,
                            double cpu_percent,
                            uint64 memory_bytes,
                            bool can_signal = true) {
            Object (
                pid: pid,
                command: command,
                cpu_percent: cpu_percent,
                memory_bytes: memory_bytes,
                can_signal: can_signal
            );
        }

        public string cpu_label () {
            return "%.1f%%".printf (cpu_percent);
        }

        public string memory_label () {
            const uint64 KIB = 1024;
            const uint64 MIB = 1024 * KIB;
            if (memory_bytes < MIB)
                return "%.0f KiB".printf ((double) memory_bytes / KIB);
            return "%.1f MiB".printf ((double) memory_bytes / MIB);
        }
    }

    public class DesktopApplication : Object {
        public string provider_id { get; construct; }
        public string id { get; construct; }
        public string name { get; construct; }
        public string description { get; construct; }
        public string icon { get; construct; }
        public string command { get; construct; }
        public bool exported { get; set; }

        public DesktopApplication (string provider_id,
                                   string id,
                                   string name,
                                   string description,
                                   string icon,
                                   string command,
                                   bool exported = false) {
            Object (
                provider_id: provider_id,
                id: id,
                name: name,
                description: description,
                icon: icon,
                command: command,
                exported: exported
            );
        }
    }
}
