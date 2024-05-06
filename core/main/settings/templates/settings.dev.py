# Templates to handle the development environment settings
# You can add more templates and then take them over to '/local' folder to load them into Django

DEBUG = True
SECRET_KEY = 'django-insecure-3)txa&tof+)9#hc9d^x$=y)qgve1hto=2#tfva!($w5+c4dlk#'

LOGGING['formatters']['colored'] = {  # type: ignore # noqa: F821
    '()': 'colorlog.ColoredFormatter',
    'format': '%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s',
}
LOGGING['loggers']['core']['level'] = 'DEBUG'  # type: ignore # noqa: F821
LOGGING['handlers']['console']['level'] = 'DEBUG'  # type: ignore # noqa: F821
LOGGING['handlers']['console']['formatter'] = 'colored'  # type: ignore # noqa: F821
