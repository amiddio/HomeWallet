import logging

_LOG_INFO = './log/info.log'


def log() -> logging:
    format_str = "%(asctime)s,%(msecs)d %(name)s %(levelname)s " \
                 "[%(pathname)s:%(lineno)d in function %(funcName)s] %(message)s "
    logging.basicConfig(filename=_LOG_INFO,
                        format=format_str,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        encoding='utf-8',
                        level=logging.INFO)
    return logging

