namespace Atoms {

    public class RegistryPrimaryProvider : RegistryTestProviderBase {
        protected override string provider_id { owned get { return "test"; } }
    }
}

[CCode (cname = "peas_register_types")]
public void register_types (Peas.ObjectModule module) {
    module.register_extension_type (
        typeof (Atoms.Provider),
        typeof (Atoms.RegistryPrimaryProvider)
    );
}
