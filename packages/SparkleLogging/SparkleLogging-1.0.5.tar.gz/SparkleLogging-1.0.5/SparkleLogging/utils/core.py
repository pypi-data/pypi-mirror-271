from SparkleLogging.utils.getLog import LogManager ,FOMATTER
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL,FATAL

DEFAULT_LOGGER = LogManager().GetLogger(
    log_name='main',
    setConsoleLevel=DEBUG,
    setFileLevel=INFO,
    setWebsocketLevel=INFO,
    setHTTPLevel=INFO,
    out_to_console=True,
    web_log_mode=False,
    WSpost_url="",
    HTTPpost_url="",
    http_mode=False,
    custom_formatter=FOMATTER
)