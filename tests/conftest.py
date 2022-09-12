import os
import sys
from glob import glob
from pathlib import Path

import django  # noqa: E402
from django.apps import apps
from django.conf import settings  # noqa

CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
APPS_DIR = os.path.abspath(CURRENT_DIR / ".." / "app")
RUNTESTS_DIR = str(CURRENT_DIR / "app")
TESTS_RELATIVE_PATH = "tests.app"

sys.path.insert(0, APPS_DIR)
sys.path.insert(0, RUNTESTS_DIR)
SUBDIRS_TO_SKIP = []  # skip searching this directories for tests


def get_test_modules():
    modules = []
    discovery_paths = [(None, RUNTESTS_DIR)]
    for modpath, dirpath in discovery_paths:
        for f in os.scandir(dirpath):
            if (
                "." not in f.name
                and os.path.basename(f.name) not in SUBDIRS_TO_SKIP
                and not f.is_file()
                and os.path.exists(os.path.join(f.path, "__init__.py"))
            ):
                modules.append((modpath, f.name))
    return modules


def _module_match_label(module_label, label):
    # Exact or ancestor match.
    return module_label == label or module_label.startswith(label + ".")


def get_installed():
    return [app_config.name for app_config in apps.get_app_configs()]


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.app.settings")

    # Load all the ALWAYS_INSTALLED_APPS.
    django.setup()

    # Load all the test model apps.
    test_modules = get_test_modules()
    installed_app_names = set(get_installed())
    for modpath, module_name in test_modules:
        if modpath:
            module_label = modpath + "." + module_name
        else:
            module_label = TESTS_RELATIVE_PATH + "." + module_name
        if module_label not in installed_app_names:
            settings.INSTALLED_APPS.append(module_label)
    apps.set_installed_apps(settings.INSTALLED_APPS)


def dotted_path(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [
    dotted_path(fixture)
    for fixture in glob("tests/app/fixtures/*.py")
    if "__" not in fixture
]

pytest_configure()
