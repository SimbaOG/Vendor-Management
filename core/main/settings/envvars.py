from core.core.utils.collections import update_vals
from core.core.utils.settings import get_settings_from_environment

update_vals(globals(), get_settings_from_environment(ENVVAR_SETTINGS_PREFIX))  # type: ignore # noqa: F821
