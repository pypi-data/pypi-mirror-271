import logging
import logging.config

class ColorFormatter(logging.Formatter):
    color_formats = {
        'DEBUG': '\033[0;36m[DEBUG]\033[0m - \033[0;36m[%(asctime)s]\033[0m - \033[0;36m[%(filename)s:%(lineno)d]\033[0m - %(message)s',
        'INFO': '\033[0;32m[INFO]\033[0m - \033[0;32m[%(asctime)s]\033[0m - \033[0;32m[%(filename)s:%(lineno)d]\033[0m - %(message)s',
        'WARNING': '\033[0;33m[WARNING]\033[0m - \033[0;33m[%(asctime)s]\033[0m - \033[0;33m[%(filename)s:%(lineno)d]\033[0m - %(message)s',
        'ERROR': '\033[0;31m[ERROR]\033[0m - \033[0;31m[%(asctime)s]\033[0m - \033[0;31m[%(filename)s:%(lineno)d]\033[0m - %(message)s',
        'CRITICAL': '\033[1;31m[CRITICAL]\033[0m - \033[1;31m[%(asctime)s]\033[0m - \033[1;31m[%(filename)s:%(lineno)d]\033[0m - %(message)s'
    }

    def format(self, record):
        log_format = self.color_formats.get(record.levelname, '%(asctime)s - %(message)s')
        formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

def setup_logging():
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'colorFormatter': {
                '()': ColorFormatter,
            },
            'fileFormatter': {
                'format': '[%(levelname)s] - [%(asctime)s] - [%(filename)s:%(lineno)d] - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'colorFormatter',
                'stream': 'ext://sys.stdout',
            },
            'fileHandler': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'fileFormatter',
                'filename': 'app.log',
            },
        },
        'loggers': {
            'ruleopt': {
                'level': 'DEBUG',
                'handlers': ['consoleHandler', 'fileHandler'],
                'propagate':True,
            },
        },
    })
