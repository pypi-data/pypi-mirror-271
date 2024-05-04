# Lumberstack

### Global init in \_\_main\_\_
#### Example to determine log file name
```
if helpers.am_debugging:
  log_file_name = f'{config.log_file.rstrip(".log")}_debug.log'
  if os.path.exists(log_file_name):
    os.remove(log_file_name)
else:
  log_file_name = (f'{config.log_file.rstrip(".log")}_'
                   f'{str(datetime.now() if helpers.am_debugging else datetime.utcnow()).split(".", 1)[0].replace(":", ".").replace(" ", "_")}'
                    '.log')
```

#### Only run global_init once in \_\_main\_\_
```
Lumberstack.global_init(timezone=time.localtime if helpers.am_debugging else time.gmtime, log_filename=log_file_name, log_level=config.log_level, console_output=True)
```

#### Add a custom handler during global init
```
fh = logging.FileHandler(filename='new.log')
Lumberstack.global_init(log_level=config.log_level, custom_handlers=[fh])
```

#### Update log levels of imported libraries using the logging package
```
Lumberstack.update_library_levels(libraries=['requests', 'urllib3'], log_level=config.lib_log_level)
Lumberstack.update_library_levels(libraries=['cli.azure.cli.core', 'cli.knack.cli', 'msal.authority', 'msal.application', 'msal.telemetry'], log_level=config.az_log_level)
```


### Local init for each file/module
```
logger = Lumberstack()
logger.info(f'{APP_NAME} - {APP_DESCRIPTION}')
```


### Log levels use the logging package values

* CRITICAL = 50
* FATAL = CRITICAL
* ERROR = 40
* WARNING = 30
* WARN = WARNING
* INFO = 20
* DEBUG = 10
* NOTSET = 0
