import os.path
from pathlib import Path

from split_settings.tools import include, optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

ENVVAR_SETTINGS_PREFIX = "VENDORSETTINGS_"

LOCAL_SETTINGS_PATH = os.getenv(f'{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH')

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = 'local/settings.dev.py'

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    'base.py', 'logging.py', 'custom.py', 'rest_framework.py', optional(LOCAL_SETTINGS_PATH), 'envvars.py', 'docker.py'
)

# The following settings are included together, which makes it easy to seggregate what file deals with what settings.
# The settings are included in the following order:
# - base.py -> This file contains the base settings for the Django project.
# - logging.py -> This file contains the logging settings for the Django project.
# - custom.py -> This file contains the custom settings for the Django project.
# (settings related to the project, not any 3rd party packages)
# - rest_framework.py -> This file contains the settings for the Django Rest Framework.
# - optional(LOCAL_SETTINGS_PATH) -> This file contains the local settings for the Django project.
# (settings that are specific to the local environment)
# - envvars.py -> This file contains the settings that are loaded from the environment variables.
# - docker.py -> This file contains the settings that are specific to the Docker environment.
