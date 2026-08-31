using Atoms;

private void test_policy_clamp () {
    var policy = new EnvironmentPolicy () {
        network = true,
        home = true,
        display = true,
        usb = true,
        input = true,
        audio = true,
        host_commands = true,
        can_network = true,
        can_home = false,
        can_display = true,
        can_usb = false,
        can_input = true,
        can_audio = false,
        can_host_commands = false
    };

    policy.clamp ();
    assert (policy.network);
    assert (!policy.home);
    assert (policy.display);
    assert (!policy.usb);
    assert (policy.input);
    assert (!policy.audio);
    assert (!policy.host_commands);
}

private void test_models () {
    var distribution = new Distribution (
        "test",
        "example",
        "Example",
        "1",
        "Example distribution",
        "example.test/org/distribution"
    );
    assert (distribution.display_name () == "Example 1");

    var process = new ProcessInfo (12, "/bin/sh", 1.25, 2 * 1024 * 1024);
    assert (process.cpu_label () == "1.2%");
    assert (process.memory_label () == "2.0 MiB");

    var application = new DesktopApplication (
        "test",
        "/usr/share/applications/example.desktop",
        "Example",
        "Example application",
        "example",
        "/usr/bin/example %U",
        true
    );
    assert (application.exported);
}

private void test_empty_registry () {
    string[] paths = { "/path/that/does/not/exist" };
    var registry = new ProviderRegistry (paths);
    registry.load ();
    assert (registry.providers.size == 0);
}

private void test_registry_rejects_invalid_plugins () {
    string path = GLib.Environment.get_variable ("ATOMS_REGISTRY_TEST_PATH");
    string[] paths = { path };
    var registry = new ProviderRegistry (paths);
    registry.load ();
    assert (registry.providers.size == 1);
    assert (registry.providers[0].id == "test");
    assert (registry.diagnostics.size == 3);

    string diagnostics = string.joinv ("\n", registry.diagnostics.to_array ());
    assert (diagnostics.index_of ("invalid provider metadata") >= 0);
    assert (diagnostics.index_of ("identity does not match") >= 0);
    assert (diagnostics.index_of ("duplicate provider id") >= 0);
}

int main (string[] args) {
    Test.init (ref args);
    Test.add_func ("/atoms/policy/clamp", test_policy_clamp);
    Test.add_func ("/atoms/models", test_models);
    Test.add_func ("/atoms/registry/empty", test_empty_registry);
    Test.add_func ("/atoms/registry/invalid-plugins", test_registry_rejects_invalid_plugins);
    return Test.run ();
}
