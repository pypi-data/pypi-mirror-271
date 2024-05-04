import logging, requests
from .custom_handler import CustomHandler


class DiscordHandler(CustomHandler):
    def __init__(self, webhook_url, level: int = 0, name: str = None, 
                 mention_id: str = None, 
                 mention_id_threshold: int = 30, mention_everyone_threshold: int = 0, mention_here_threshold: int = 0, 
                 error_logger: logging.Logger = None, 
                 remove_timestamp: bool = True, custom_formatting: str = None):
        """
        Generates log output to the supplied Discord webhook
        """
        self.webhook_url = webhook_url
        self.mention_id = mention_id
        self.mention_id_threshold = mention_id_threshold
        self.mention_everyone_threshold = mention_everyone_threshold
        self.mention_here_threshold = mention_here_threshold
        self.handling_mentions = (mention_id or mention_everyone_threshold or mention_here_threshold)
        self.error_logger = error_logger

        CustomHandler.__init__(self, level=level, name=name, custom_formatting=custom_formatting, remove_timestamp=remove_timestamp)
            
        
    def _disable_timestamps_(self):
        pass


    def emit(self, record: logging.LogRecord):
        
        # can't log urllib3 or requests debug events due to recursion issues (i.e. these discord webhook calls
        # will fire events that generate logs to be handled which fire events)
        if record.levelno < 20 and (record.name.startswith('urllib3') or record.name.startswith('requests')):
            return

        msg_prepend = []

        if self.handling_mentions:
            if self.mention_id and record.levelno >= self.mention_id_threshold:
                msg_prepend.append(f'<@{self.mention_id}>')
            if self.mention_everyone_threshold and record.levelno >= self.mention_everyone_threshold:
                msg_prepend.append(f'@everyone')
            if self.mention_here_threshold and record.levelno >= self.mention_here_threshold:
                msg_prepend.append(f'@here')


        # params: https://discordapp.com/developers/docs/resources/webhook#execute-webhook
        data = {
            "content" : f'{" ".join(msg_prepend)}{" " if len(msg_prepend) > 0 else ""}`{self.format(record=record)}`',
            "username" : self.name
        }

        # #leave this out if you dont want an embed
        # #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
        # data["embeds"] = [
        #     {
        #         "description" : "text in embed",
        #         "title" : "embed title"
        #     }
        # ]

        try:
            result = requests.post(self.webhook_url, json = data)

            result.raise_for_status()
        except Exception as error:
            if self.error_logger:
                self.error_logger.error(f'discord logging failed to post message: {self.format(record=record)}')
                self.error_logger.error(str(error))        
