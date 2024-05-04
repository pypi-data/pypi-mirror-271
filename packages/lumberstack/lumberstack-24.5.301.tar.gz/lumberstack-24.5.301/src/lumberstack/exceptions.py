# custom exception types for this project
class LumberstackError(Exception):
  # base class
  pass

class LoggingError(LumberstackError):
  def __init__(self, message, code: int = 569) -> None:
    self.message = message
    self.code = code
    super().__init__(f'{code}: {message}')
