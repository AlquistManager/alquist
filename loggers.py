import logging.handlers
import os

loggers = {}


# create loggers for each bot
def create_loggers():
    folders = get_immediate_subdirectories("bots")
    for folder in folders:
        if not os.path.exists('bots/' + folder + '/logs/'):
            os.makedirs('bots/' + folder + '/logs/')
        LOG_FILENAME = 'bots/' + folder + '/logs/full_log.out'
        REC_FILENAME = 'bots/' + folder + '/logs/dm_log.out'
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(uid)s - %(levelname)s - %(message)s')
        # Set up a specific logger with our desired output level
        main_logger = logging.getLogger('Main logger')
        main_logger.setLevel(logging.DEBUG)
        state_logger = logging.getLogger('State info')
        state_logger.setLevel(logging.DEBUG)

        # Add the log message handler to the logger
        db_handler = logging.handlers.RotatingFileHandler(
            LOG_FILENAME, maxBytes=10240 * 5, backupCount=5, encoding="UTF-8")

        nfo_handler = logging.handlers.RotatingFileHandler(
            REC_FILENAME, maxBytes=10240 * 5, backupCount=5, encoding="UTF-8")

        db_handler.setLevel(logging.DEBUG)
        nfo_handler.setLevel(logging.INFO)

        db_handler.setFormatter(formatter)
        nfo_handler.setFormatter(formatter)

        main_logger.addHandler(nfo_handler)
        state_logger.addHandler(db_handler)
        loggers.update({folder.lower(): {"main_logger": main_logger, "state_logger": state_logger}})


# return all subdirectories directly in directory
def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
