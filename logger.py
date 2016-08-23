import logging.handlers

LOG_FILENAME = 'logs/full_log.out'
REC_FILENAME = 'logs/dm_log.out'

formatter = logging.Formatter('%(asctime)s - %(name)s - %(uid)s - %(levelname)s - %(message)s')


# Set up a specific logger with our desired output level
main_logger = logging.getLogger('Main logger')
main_logger.setLevel(logging.DEBUG)
state_logger = logging.getLogger('State info')
state_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
db_handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=10240*5, backupCount=5)

nfo_handler = logging.handlers.RotatingFileHandler(
              REC_FILENAME, maxBytes=10240*5, backupCount=5)

db_handler.setLevel(logging.DEBUG)
nfo_handler.setLevel(logging.INFO)

db_handler.setFormatter(formatter)
nfo_handler.setFormatter(formatter)

main_logger.addHandler(db_handler)
main_logger.addHandler(nfo_handler)
state_logger.addHandler(db_handler)

