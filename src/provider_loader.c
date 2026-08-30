#include "provider_loader.h"

GObject *
atoms_provider_registry_create_extension (PeasEngine *engine,
                                          PeasPluginInfo *info,
                                          GType extension_type)
{
    return peas_engine_create_extension_with_properties (
        engine,
        info,
        extension_type,
        0,
        NULL,
        NULL
    );
}
