import importlib
import pkgutil
from pathlib import Path

# Auto-import every module in the models package so all DeclarativeBase models are registered
package_dir = Path(__file__).resolve().parent

for _, module_name, is_pkg in pkgutil.iter_modules([str(package_dir)]):
    if not is_pkg and module_name != "__init__":
        imported_module = importlib.import_module(f".{module_name}", package=__name__)
        # Expose public symbols in this module's namespace
        for attr in getattr(imported_module, "__all__", dir(imported_module)):
            if not attr.startswith("_"):
                globals()[attr] = getattr(imported_module, attr)
