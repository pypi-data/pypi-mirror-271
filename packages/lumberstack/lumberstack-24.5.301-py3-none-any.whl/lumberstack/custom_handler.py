import logging

class CustomHandler(logging.Handler):
    def __init__(self, level: int = 0, name: str = None, custom_formatting: str | logging.Formatter = None, remove_timestamp: bool = False) -> None:
        
        self.custom_formatting = custom_formatting
        self.remove_timestamp = remove_timestamp

        logging.Handler.__init__(self, level=level)
        self.set_name(name)
        self.setFormatter(self.custom_formatting)

    
    @property
    def custom_formatting(self) -> logging.Formatter:
        return self._custom_formatting_
    
    @custom_formatting.setter
    def custom_formatting(self, value: str | logging.Formatter):
        if isinstance(value, str):
            self._custom_formatting_ = logging.Formatter(value)
        elif isinstance(value, logging.Formatter):
            self._custom_formatting_ = value
        elif value is None:
            self._custom_formatting_ = None