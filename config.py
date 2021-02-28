import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Configuration:
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get(
        'SECRET_KEY',
        'you-will-never-guess'
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    SERVER_NAME = 'localhost:5000'
    STATIC_FOLDER = os.path.join(basedir, 'static')


# ---------------- <logger settings> ---------------- #
LOG_NAME = 'server.log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-26s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-26s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': LOG_NAME
        }
    },
    'loggers': {
        '': {
            'level': 'ERROR',
            'handlers': [
                'console',
                # 'file'
            ]
        },
        'dispatcher.server': {
            'level': 'DEBUG',
            'handlers': [
                'console',
                'file'
            ]
        },
        'dispatcher.app.writer': {
            'level': 'DEBUG',
            'handlers': [
                # 'console',
                'file'
            ]
        },

        'dispatcher.app.listener': {
            'level': 'DEBUG',
            'handlers': [
                # 'console',
                'file'
            ]
        },

        'dispatcher.app.ext': {
            'level': 'DEBUG',
            'handlers': [
                'console',
                'file'
            ]
        },

    }
}

# ---------------- </logger settings> ---------------- #
