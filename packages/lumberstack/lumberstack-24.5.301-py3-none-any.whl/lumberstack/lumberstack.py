import datetime, inspect, logging, os, sys, time, typing
from logging import Logger, Handler
from .constants import *
from .custom_handler import CustomHandler

# Documentation from logging library
# CRITICAL = 50
# FATAL = CRITICAL
# ERROR = 40
# WARNING = 30
# WARN = WARNING
# INFO = 20
# DEBUG = 10
# NOTSET = 0

class _Dummy_Logger_:
  def __init__(self, name: str = 'dummy') -> None:
    self.base = logging.getLogger(name=name)
    self.base.debug = _Dummy_Logger_._dummy_log_
    self.base.info = _Dummy_Logger_._dummy_log_
    self.base.warn = _Dummy_Logger_._dummy_log_
    self.base.warning = _Dummy_Logger_._dummy_log_
    self.base.error = _Dummy_Logger_._dummy_log_
    self.base.critical = _Dummy_Logger_._dummy_log_

  @staticmethod
  def _dummy_log_(arg0: 'typing.any' = None, arg1: 'typing.any' = None, 
                  arg2: 'typing.any' = None, arg3: 'typing.any' = None, 
                  arg4: 'typing.any' = None, arg5: 'typing.any' = None):
    pass

root_formatting: logging.Formatter = DEFAULT_FORMAT_STRING
mute_errors: bool

class Lumberstack:
  last_msg: str = None
  history: list[str] = []

  def __init__(self, name: str = os.path.basename(inspect.stack()[1].filename), log_level_override: int = None, retain_history: bool = False, capitalize_messages: bool = True) -> None:
    
    self.name = name if 'lumberstack' not in name else os.path.basename(inspect.stack()[1].filename)
    self.retain_history = retain_history
    self.capitalize_messages = capitalize_messages

    self.base = logging.getLogger(name=self.name)

    if log_level_override:
      self.base.setLevel(level=log_level_override)

  # run once from __main__
  @staticmethod
  def global_init(timezone: time.struct_time = time.localtime, log_filename: str = None, log_level: int = logging.INFO, format_str: str = DEFAULT_FORMAT_STRING, console_output: bool = True, custom_handlers: list[logging.Handler] | list[CustomHandler] = None, mute_errors_from_lumberstack: bool = False):

    # initialize global instance of logger module
    logging.Formatter.converter = timezone
    logging.basicConfig(filename=log_filename, level=log_level, format=format_str)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    global root_formatting
    root_formatting = logging.Formatter(fmt=format_str)
    global mute_errors
    mute_errors = mute_errors_from_lumberstack

    # remove default handlers
    for h in root_logger.handlers:
      root_logger.removeHandler(hdlr=h)

    # set file handler
    if log_filename:
      fh = logging.FileHandler(filename=log_filename)
      fh.setFormatter(root_formatting)
      root_logger.addHandler(hdlr=fh)
      if not mute_errors and log_level < logging.INFO:
        Lumberstack(name='lumberstack').debug(f'File Handler Added: {log_filename}')

    # set console handler
    if console_output:
      ch = logging.StreamHandler(stream=sys.stdout)
      ch.setFormatter(root_formatting)
      root_logger.addHandler(hdlr=ch)
      if not mute_errors and log_level < logging.INFO:
        Lumberstack(name='lumberstack').debug(f'Console Handler Added: STDOUT')
    
    # add custom handlers
    if custom_handlers:
      Lumberstack.add_handlers(handlers=custom_handlers)

    # mute me if you desire
    if mute_errors:
      Lumberstack.mute_library_logging(libraries='lumberstack')

  # add a handler
  @staticmethod
  def add_handlers(handlers: Handler | list[Handler] | CustomHandler | list[CustomHandler]) -> None:
    if isinstance(handlers, Handler):
      handlers = [handlers]
    elif isinstance(handlers, CustomHandler):
      handlers = [handlers]

    global root_formatting
    for h in handlers:

      # use our root_formatting if one has not been set
      if not h.formatter:
        h.setFormatter(root_formatting)

      # remove timestamp if set to do so by CustomHandler
      if isinstance(h, CustomHandler):
        if h.remove_timestamp and h.formatter._fmt:
          if isinstance(h.formatter._style, logging.PercentStyle):
            h.setFormatter(logging.Formatter(h.formatter._fmt.replace('%(asctime)s', '').strip()))
          elif isinstance(h.formatter._style, logging.StrFormatStyle):
            h.setFormatter(logging.Formatter(h.formatter._fmt.replace('{asctime}', '').strip()))
          elif isinstance(h.formatter._style, logging.StrFormatStyle):
            h.setFormatter(logging.Formatter(h.formatter._fmt.replace('${asctime}', '').strip()))
      
      logging.getLogger().addHandler(hdlr=h)
      Lumberstack(name='lumberstack').debug(f'Handler Added: {type(h).__name__}{" - " + h.name if h.name else ""}')


  # retrieve logger by name
  @staticmethod
  def get_logger(name: str) -> Logger:
    return logging.getLogger(name)

  # update log level of a list of libraries (i.e. requests)
  @staticmethod
  def update_library_levels(libraries: list[str] = [], log_level: int = logging.root.level):
    for l in libraries:
      Lumberstack.get_logger(name=l).setLevel(log_level)

  # forcibly override a logger's output level
  @staticmethod
  def force_update_library_levels(libraries: list[str] = [], log_level: int = logging.root.level):
    if log_level == 0:
      log_level = 100
    
    for l in libraries:
      logger = Lumberstack.get_logger(name=l)
      if log_level > logging.DEBUG:
        logger.debug = _Dummy_Logger_._dummy_log_
      if log_level > logging.INFO:
        logger.info = _Dummy_Logger_._dummy_log_
      if log_level > logging.WARN:
        logger.warn = _Dummy_Logger_._dummy_log_
        logger.warning = _Dummy_Logger_._dummy_log_
      if log_level > logging.ERROR:
        logger.error = _Dummy_Logger_._dummy_log_
      if log_level > logging.FATAL:
        logger.fatal = _Dummy_Logger_._dummy_log_
        logger.critical = _Dummy_Logger_._dummy_log_

  # forcibly mute a logger
  @staticmethod
  def mute_library_logging(libraries: str | list[str]):
    Lumberstack.force_update_library_levels(libraries=[libraries] if isinstance(libraries, str) else libraries, log_level=100)

  @property
  def _my_logger_(self):
    return Lumberstack(name='lumberstack')

  def critical(self, msg):
    self._log_(msg=msg, level=logging.CRITICAL)

  def error(self, msg):
    self._log_(msg=msg, level=logging.ERROR)

  def warning(self, msg):
    self._log_(msg=msg, level=logging.WARNING)

  def info(self, msg):
    self._log_(msg=msg, level=logging.INFO)

  def debug(self, msg):
    self._log_(msg=msg, level=logging.DEBUG)

  def _log_(self, msg: str, level: int):
    if logging.root.level <= 0 or logging.root.level > 50:
      return

    try:
      msg = str(msg)
    except Exception as error:
      level_name = logging.getLevelName(level=level)
      self._my_logger_.error(f'failed to log {level_name} message, could not cast to string value... see following error for details')
      self._my_logger_.error(str(error))
      return

    if self.capitalize_messages:
      msg = f'{msg[0].upper()}{msg[1:]}'

    # set last message and append message history
    if logging.root.level <= level:

      timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f"))[:-3]
      formatted_msg = f'{timestamp} {self.name} {logging.getLevelName(level)}: {msg}'
      self.last_msg = formatted_msg

      if self.retain_history:
        self.history.append(formatted_msg)

    # run core logger
    {
        logging.CRITICAL: self.base.critical,
        logging.ERROR: self.base.error,
        logging.WARNING: self.base.warning,
        logging.INFO: self.base.info,
        logging.DEBUG: self.base.debug
    }[level](msg)
