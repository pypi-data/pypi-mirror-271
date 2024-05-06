import logging
import random


def get_logger(name: str) -> logging.Logger:
    """
    Internally calls the logging.getLogger function with the `name` argument to create or
    retrieve a logger object. It is recommended to pass __name__ as argument when calling
    get_logger. The returned logger object logs to the standard error stream and formats
    the messages appropriately.
    Parameters
    ----------
    name
        The name that gets passed to the logger.getLogger function.
    Returns
    -------
    A logger instance with the given name.
    """

    logger = logging.getLogger(name)
    # numbaのloggerをWARNINGに変更することで、numbaのdebugログが出ることを防ぐ
    numba_logger = logging.getLogger("numba")
    numba_logger.setLevel(logging.WARNING)

    return logger


def root_logger(level="WARNING") -> logging.Logger:
    if level == "INFO":
        log_level = logging.INFO
    elif level == "DEBUG":
        log_level = logging.DEBUG
    elif level == "WARNING":
        log_level = logging.WARNING
    elif level == "ERROR":
        log_level = logging.ERROR
    elif level == "CRITICAL":
        log_level = logging.CRITICAL
    else:
        raise ValueError(f"level: {level} is wrong.")

    # root loggerを取得
    logger = logging.getLogger()

    # formatterを作成
    formatter = logging.Formatter(
        "time:%(asctime)s.%(msecs)03d\tthread:%(threadName)s\tlogger:%(name)s\t"
        "level:%(levelname)s\tmessage:%(message)s"
    )

    # handlerを作成しフォーマッターを設定
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # loggerにhandlerを設定、イベント捕捉のためのレベルを設定
    logger.addHandler(handler)
    # log levelを設定
    logger.setLevel(log_level)
    return logger
