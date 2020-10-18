import sys
import importlib
import pkgutil

_prefix = "vortex_"

discovered_plugins = {
    name[len(_prefix) :]: importlib.import_module(name, ".")
    for finder, name, ispkg in pkgutil.iter_modules()
    if name.startswith(_prefix)
}

update_modules = {}
for import_name, module in sys.modules.items():
    if not import_name.startswith(_prefix):
        continue
    update_modules["vortex.plugins." + import_name[len(_prefix) :]] = module

sys.modules.update(update_modules)
