import logging


class Logger:
    """
    This class allows setting of a logger using a common format.
    """
    def __init__(self, name):
        """
        To instantiate the Logger you must pass a name to be used during logging.
        :param name: - name to be used as a prefix when logging (e.g. your tool name or Id)
        """
        self.__name = name

    def set_logger(self, logging_level='INFO'):
        """
        Set the logger.
        :param logging_level
        :return: logger instance
        """
        logger = logging.getLogger(self.__name)

        log_level = Logger.__log_level(logging_level)
        logger.setLevel(log_level)

        formatter = logging.Formatter('[%(name)s] %(asctime)s.%(msecs)03d %(levelname)s - %(message)s', '%Y-%m-%d %I:%M:%S')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger

    @staticmethod
    def __log_level(log_level):
        return {
            'CRITICAL': logging.CRITICAL,
            'DEBUG': logging.DEBUG,
            'ERROR': logging.ERROR,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
        }.get(log_level, logging.INFO)
