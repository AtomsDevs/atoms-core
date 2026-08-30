#pragma once

#include <glib-object.h>
#include <libpeas-2/libpeas.h>

GObject *atoms_provider_registry_create_extension (
    PeasEngine *engine,
    PeasPluginInfo *info,
    GType extension_type
);
